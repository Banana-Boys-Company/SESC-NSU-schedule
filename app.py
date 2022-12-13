from modules.parser.common import first_table_properties, second_table_properties, merge_dicts
from werkzeug.security import check_password_hash
from flask import Flask, render_template, url_for, request, jsonify, g
from apscheduler.schedulers.background import BackgroundScheduler
from modules.parser.common import department_to_id
from flask_socketio import SocketIO, emit
from copy import deepcopy
import modules.parser.parser as pars
import logging
import urllib.request
import json
import os
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
logging.basicConfig(filename='output_log.log')


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
logging.info(msg=f"ROOT директория: {PROJECT_ROOT}")
DATABASE = os.path.join(PROJECT_ROOT, 'data', 'database.db')
EXEL_TABLE_URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"
API_VERSION = ["1"]
logging.info(msg="Версии API: {}".format(", ".join(API_VERSION)))
CLIENTS = []
COURSES_DATA = {}
API_ADMIN_LOGIN = "admin"
API_ADMIN_PASS = "very_secret"
API_SESSION = {}
VALID_CLASSES = ["9_1", "9_2", "10_1", "10_2", "10_3", "10_4", "10_5", "10_6", "10_7", "10_8",
                 "11_1", "11_2", "11_3", "11_4", "11_5", "11_6", "11_7", "11_8", "11_9", "11_10", "11_11" "11_12"]


def parse_both_tables(bar_is_on=False, only_courses=False):
    logging.info(msg="Начало парсинга обеих таблиц...")
    parser = pars.ScheduleParser('data.xlsx')
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
    logging.info(msg="Успешный парсинг!")
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
if os.path.exists(PROJECT_ROOT + "/data.json"):
    with open(PROJECT_ROOT + '/data.json', "r", encoding="cp1251") as f:
        cashed_data = json.load(f)
    if os.path.exists(PROJECT_ROOT + "/courses.json"):
        with open(PROJECT_ROOT + '/courses.json', "r", encoding="cp1251") as f:
            COURSES_DATA = json.load(f)
else:
    if os.path.exists(PROJECT_ROOT + "/data.xlsx"):
        with open(PROJECT_ROOT + "/data.json", "w", encoding="cp1251") as f:
            cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
            json.dump(cashed_data, fp=f, ensure_ascii=False)
        if os.path.exists(PROJECT_ROOT + "/courses.json"):
            with open(PROJECT_ROOT + '/courses.json', "r", encoding="cp1251") as f:
                json.dump(COURSES_DATA, fp=f, ensure_ascii=False)
    else:
        try:
            urllib.request.urlretrieve(
                EXEL_TABLE_URL, PROJECT_ROOT + "/data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open(PROJECT_ROOT + "/data.json", "w", encoding="cp1251") as f:
                cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
                json.dump(cashed_data, fp=f, ensure_ascii=False)
            if os.path.exists(PROJECT_ROOT + "/courses.json"):
                with open(PROJECT_ROOT + '/courses.json', "r", encoding="cp1251") as f:
                    json.dump(COURSES_DATA, fp=f, ensure_ascii=False)

if os.path.exists(PROJECT_ROOT + "/courses.json") and (COURSES_DATA == {}):
    with open(PROJECT_ROOT + '/courses.json', "r", encoding="cp1251") as f:
        COURSES_DATA = json.load(f)
else:
    if os.path.exists(PROJECT_ROOT + "/data.xlsx"):
        with open(PROJECT_ROOT + "/courses.json", "w", encoding="cp1251") as f:
            COURSES_DATA = parse_both_tables(only_courses=True)
            json.dump(COURSES_DATA, fp=f, ensure_ascii=False)
    else:
        try:
            urllib.request.urlretrieve(
                EXEL_TABLE_URL, PROJECT_ROOT + "/data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open(PROJECT_ROOT + "/courses.json", "w", encoding="cp1251") as f:
                COURSES_DATA = parse_both_tables(only_courses=True)
                json.dump(COURSES_DATA, fp=f, ensure_ascii=False)


# Banner initialization
try:
    BANNER_DATA = {"new_data": [f"images/banner/{element}" for element in os.listdir(
        "/mnt/sesc-share/background") if element.endswith((".png", ".jpeg", ".jpg", ".gif", ".webm"))], "old_data": [], "filenames": os.listdir(
        "/mnt/sesc-share/background")}
except FileNotFoundError:
    BANNER_DATA = {"new_data": [f"images/banner/{element}" for element in os.listdir(
        PROJECT_ROOT + "/static/images/banner")], "old_data": [], "filenames": os.listdir(
        "static/images/banner/")}


for item in BANNER_DATA["new_data"]:
    filename = item.split("/")[-1]
    if filename not in os.listdir(PROJECT_ROOT + "/static/images/banner"):
        shutil.copyfile(
            f"/mnt/sesc-share/background/{filename}", "/static/images/banner/{}".format(item))


def update_banner_data():
    while True:
        is_online = None
        try:
            files = os.listdir("/mnt/sesc-share/background")
        except FileNotFoundError:
            files = os.listdir(PROJECT_ROOT + "/static/images/banner")
            is_online = False
        else:
            is_online = True
        files = [PROJECT_ROOT + f"/images/banner/{element}" for element in files if element.endswith(
            (".png", ".jpeg", ".jpg", ".gif", ".webm"))]
        for file in BANNER_DATA["new_data"]:
            if file not in files:
                if file not in BANNER_DATA["old_data"]:
                    BANNER_DATA["old_data"].append(files)
                try:
                    os.remove(PROJECT_ROOT + f"/static/{file}")
                except Exception as exp:
                    logging.error(
                        f"Ошибка при обновлении списка изображений: {exp}")
        if is_online is True:
            for file in files:
                if file not in BANNER_DATA["new_data"]:
                    filename = file.split("/")[-1]
                    if filename not in os.listdir(PROJECT_ROOT + f"/static/images/banner"):
                        shutil.copyfile(
                            f"/mnt/sesc-share/background/{filename}", "/static/{file}")
        BANNER_DATA["new_data"] = deepcopy(files)
        new_data = deepcopy(BANNER_DATA)
        new_data["new_data"] = [urllib.parse.quote_plus(item).replace(r"%2F", "/")
                                for item in BANNER_DATA["new_data"]]
        socketio.emit('response-banner', new_data)
        eventlet.sleep(10)


def update_schedule_json_data():
    logging.info("Начало обновления exel данных...")
    global cashed_data
    global COURSES_DATA
    try:
        urllib.request.urlretrieve(EXEL_TABLE_URL, "data.xlsx")
    except Exception:
        logging.warn("Ошибка установки таблицы, использованы локальные данные")
        with open(PROJECT_ROOT + '/data.json', "r", encoding="cp1251") as f:
            cashed_data = json.load(f)
            COURSES_DATA = parse_both_tables(only_courses=True)
        logging.info("Локальные JSON загружены")
    else:
        cashed_data, COURSES_DATA = parse_both_tables(bar_is_on=True)
    logging.info("Exel данные обновлены!")


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
                    emit('schedule', {"data": list(
                        response.values()), "get_all": True, "status": 200})
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
    socketio.run(app, port=1735, host="0.0.0.0", debug=True,
                 reloader_options={"reloader_type": 'stat'})
