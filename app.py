from modules.parser.common import first_table_properties, second_table_properties, merge_dicts
from werkzeug.security import check_password_hash
from flask import Flask, render_template, url_for, request, jsonify, g
from apscheduler.schedulers.background import BackgroundScheduler
from modules.parser.common import department_to_id
from flask_socketio import SocketIO, emit
import modules.parser.parser as pars
import urllib.request
import json
import os.path
import shutil
import urllib.parse
import eventlet
import sqlite3
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'data', 'database.db')
EXEL_TABLE_URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"
API_VERSION = ["1"]
CLIENTS = []
COURSES_DATA = {}
API_ADMIN_LOGIN = "admin"
API_ADMIN_PASS = "very_secret"
API_SESSION = {}
VALID_CLASSES = ["9_1", "9_2", "10_1", "11_12"]

parser = pars.ScheduleParser('data.xlsx')


def parse_both_tables(bar_is_on=False, only_courses=False):
    if only_courses is True:
        dict3 = parser.parse_cources("СПЕЦКУРСЫ")
        return dict3
    dict1 = parser.parse('Расписание_1 сем',
                         first_table_properties, bar_is_on=bar_is_on)
    dict2 = parser.parse('Расписание_1сем_2пол.дня',
                         second_table_properties, bar_is_on=bar_is_on)
    full_dict = merge_dicts(dict1, dict2)
    dict3 = parser.parse_cources("СПЕЦКУРСЫ")
    del dict1, dict2
    return full_dict, dict3


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


with app.app_context():
    API_OWNER = query_db(
        "SELECT token FROM api WHERE permission=100", one=True)["token"]

# Server data initialization
if os.path.exists("data.json"):
    with open('data.json', "r", encoding="cp1251") as f:
        cashed_data = json.load(f)
    if os.path.exists("courses.json"):
        with open('courses.json', "r", encoding="cp1251") as f:
            COURSES_DATA = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("data.json", "w") as f:
            cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
            json.dump(cashed_data, fp=f)
        if os.path.exists("courses.json"):
            with open('courses.json', "r", encoding="cp1251") as f:
                json.dump(COURSES_DATA, fp=f)
    else:
        try:
            urllib.request.urlretrieve(EXEL_TABLE_URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("data.json", "w") as f:
                cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
                json.dump(cashed_data, fp=f)
            if os.path.exists("courses.json"):
                with open('courses.json', "r", encoding="cp1251") as f:
                    json.dump(COURSES_DATA, fp=f)

if os.path.exists("courses.json") and (COURSES_DATA == {}):
    with open('courses.json', "r", encoding="cp1251") as f:
        COURSES_DATA = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("courses.json", "w") as f:
            COURSES_DATA = parse_both_tables(only_courses=True)
            json.dump(COURSES_DATA, fp=f)
    else:
        try:
            urllib.request.urlretrieve(EXEL_TABLE_URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("courses.json", "w") as f:
                COURSES_DATA = parse_both_tables(only_courses=True)
                json.dump(COURSES_DATA, fp=f)


# Banner initialization
try:
    BANNER_DATA = {"new_data": [f"images/banner/{element}" for element in os.listdir(
        "\\\\WHITEEVILBRO-LA\Share")], "old_data": [], "filenames": os.listdir(
        "\\\\WHITEEVILBRO-LA\Share")}
except FileNotFoundError:
    BANNER_DATA = {"new_data": [f"images/banner/{element}" for element in os.listdir(
        "static\\images\\banner\\")], "old_data": [], "filenames": os.listdir(
        "static\\images\\banner\\")}


for item in BANNER_DATA["new_data"]:
    filename = item.split("/")[-1]
    if filename not in os.listdir(f"{os.getcwd()}\\static\\images\\banner"):
        shutil.copyfile(
            f"//WHITEEVILBRO-LA/Share/{filename}", "{}\\static\\{}".format(os.getcwd(), item.replace("/", "\\")))


def update_banner_data():
    while True:
        is_online = None
        try:
            files = os.listdir("\\\\WHITEEVILBRO-LA\Share")
            is_online = True
        except FileNotFoundError:
            files = os.listdir(f"{os.getcwd()}\\static\\images\\banner")
            is_online = False
        files = [f"images/banner/{element}" for element in files]
        for file in BANNER_DATA["new_data"]:
            if file not in files:
                if file not in BANNER_DATA["old_data"]:
                    BANNER_DATA["old_data"].append(files)
                os.remove("{}\\static\\{}".format(
                    os.getcwd(), file.replace("/", "\\")))
        if is_online is True:
            for file in files:
                if file not in BANNER_DATA["new_data"]:
                    filename = file.split("/")[-1]
                    if filename not in os.listdir(f"{os.getcwd()}\\static\\images\\banner"):
                        a = shutil.copyfile(
                            f"//WHITEEVILBRO-LA/Share/{filename}", "{}\\static\\{}".format(os.getcwd(), file.replace("/", "\\")))
        BANNER_DATA["new_data"] = files
        new_data = BANNER_DATA.copy()
        new_data["new_data"] = [urllib.parse.quote_plus(item).replace(r"%2F", "/")
                                for item in BANNER_DATA.copy()["new_data"]]
        socketio.emit('response-banner', new_data)
        eventlet.sleep(10)


def update_schedule_json_data():
    print("Start updating data...")
    global cashed_data
    global COURSES_DATA
    try:
        urllib.request.urlretrieve(EXEL_TABLE_URL, "data.xlsx")
    except Exception:
        print("Downloading error, trying to open json data...")
        with open('data.json', "r", encoding="cp1251") as f:
            cashed_data = json.load(f)
            COURSES_DATA = parse_both_tables(only_courses=True)
        print("JSON data was loaded!")
    else:
        cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
    print("Data updated!")


scheduler = BackgroundScheduler()
job_parser = scheduler.add_job(
    update_schedule_json_data, 'interval', minutes=30)

courses_prefix = [el[-1] for el in list(department_to_id.items())]


@socketio.on("getСoursesData")
def responseData_(data):
    if (isinstance(data, dict)) and ('item_id' in data.keys()) and (data["item_id"] in courses_prefix):
        emit('courses', COURSES_DATA[data["item_id"]])
        return
    return url_for("index")


@socketio.on("connect")
def getConnection(data):
    CLIENTS.append(request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    CLIENTS.remove(request.sid)


@socketio.on("getClassData")
def responseData(data):
    if isinstance(data, dict):
        if 'get_all' in data.keys():
            if data["get_all"] is True:
                requested_data = data["item_id"].split(":")
                if requested_data[-1] in VALID_CLASSES:
                    response = cashed_data[requested_data[-1]].copy()
                    emit('schedule', {"data": list(response.values()), "get_all": True, "status": 200})
                    return
            return url_for("index")
        if 'item_id' in data.keys():
            requested_data = data["item_id"].split(":")
            cashed_data[requested_data[0]][requested_data[1]].update({
                                                                    "status": 200})
            emit('schedule', cashed_data[requested_data[0]][requested_data[1]])
            return
    return url_for("index")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    socketio.start_background_task(update_banner_data)
    return render_template("table.html", banner_links=BANNER_DATA["new_data"])

# admin token --> O4ymBcTmiAFVIop17RLc57sDf4lW3RBkWdyZpC-6MZ8


@app.route("/api/v<string:version>/get_owner", methods=["POST", "GET"])
def api_get_owner(version):
    if version not in API_VERSION:
        return jsonify({
            "version": None,
            "error_message": "API version does not exist",
            "code": 404
        })
    login = request.args.get("login")
    password = request.args.get("password")
    if (login != API_ADMIN_LOGIN) or (password != API_ADMIN_PASS):
        return jsonify({
            "version": version,
            "error_message": "Incorrect login or password",
            "code": 401
        })
    else:
        return jsonify({
            "version": version,
            "owner_token": "O4ymBcTmiAFVIop17RLc57sDf4lW3RBkWdyZpC-6MZ8",
            "error_message": None,
            "code": 200,
        })


@app.route("/api/v<string:version>/test", methods=["POST", "GET"])
def api_test(version):
    response = {}
    if version not in API_VERSION:
        return jsonify({
            "version": None,
            "error_message": "API version does not exist",
            "code": 401
        })
    token = request.args.get("token")
    if token is not None:
        if check_password_hash(API_OWNER, token):
            token = API_OWNER
            response["owner"] = True
        authorization = query_db(
            "SELECT token FROM api WHERE token = ?", (token,), one=True)
        if authorization is None:
            response["status"] = "unauthorized"
            response["role"] = {
                "permission": 0
            }
            response["version"] = version
            response["error_message"] = "Invalid API token"
            response["code"] = 401
            return jsonify(response)
    else:
        response["status"] = "unauthorized"
        response["role"] = {
            "permission": 0
        }
        response["version"] = version
        response["error_message"] = None
        response["code"] = 200
        return jsonify(response)

    response["status"] = "authorized"
    response["role"] = {
        "permission": query_db("SELECT permission FROM api WHERE token = ?", (token,), one=True)["permission"]
    }
    response["version"] = version
    response["error_message"] = None
    response["code"] = 200
    return jsonify(response)


eventlet.spawn(update_banner_data)

if __name__ == '__main__':
    scheduler.start()
    socketio.run(app, port=80, host="127.0.0.1", debug=True,
                 reloader_options={"reloader_type": 'stat'})