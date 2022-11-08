from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import parser.parser as pars
from parser.common import department_to_id
from parser.common import first_table_properties, second_table_properties, merge_dicts
import urllib.request
import json
import os.path
import urllib.parse
import eventlet
eventlet.monkey_patch()
import shutil

app = Flask(__name__)

app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'
socketio = SocketIO(app)
URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"
clients = []
parser = pars.ScheduleParser('data.xlsx')

courses_dict = {}

def parse_both_tables(bar_is_on=False, only_courses=False):
    if only_courses is True:
        dict3 = parser.parse_cources("СПЕЦКУРСЫ")
        return dict3
    dict1 = parser.parse('Расписание_1 сем', first_table_properties, bar_is_on=bar_is_on)
    dict2 = parser.parse('Расписание_1сем_2пол.дня', second_table_properties, bar_is_on=bar_is_on)
    full_dict = merge_dicts(dict1, dict2)
    dict3 = parser.parse_cources("СПЕЦКУРСЫ")
    del dict1, dict2
    return full_dict, dict3


# Server data initialization
if os.path.exists("data.json"):
    with open('data.json', "r", encoding="cp1251") as f:
        cashed_data = json.load(f)
    if os.path.exists("courses.json"):
        with open('courses.json', "r", encoding="cp1251") as f:
            courses_dict = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("data.json", "w") as f:
            cashed_data, courses_dict = parse_both_tables(bar_is_on=True)
            json.dump(cashed_data, fp=f)
        if os.path.exists("courses.json"):
            with open('courses.json', "r", encoding="cp1251") as f:
                json.dump(courses_dict, fp=f)
    else:
        try:
            urllib.request.urlretrieve(URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("data.json", "w") as f:
                cashed_data, courses_dict = parse_both_tables(bar_is_on=True)
                json.dump(cashed_data, fp=f)
            if os.path.exists("courses.json"):
                with open('courses.json', "r", encoding="cp1251") as f:
                    json.dump(courses_dict, fp=f)

if os.path.exists("courses.json") and (courses_dict == {}):
    with open('courses.json', "r", encoding="cp1251") as f:
        courses_dict = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("courses.json", "w") as f:
            courses_dict = parse_both_tables(only_courses=True)
            json.dump(courses_dict, fp=f)
    else:
        try:
            urllib.request.urlretrieve(URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("courses.json", "w") as f:
                courses_dict = parse_both_tables(only_courses=True)
                json.dump(courses_dict, fp=f)


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
    global courses_dict
    try:
        urllib.request.urlretrieve(URL, "data.xlsx")
    except Exception:
        print("Downloading error, trying to open json data...")
        with open('data.json', "r", encoding="cp1251") as f:
            cashed_data = json.load(f)
            courses_dict = parse_both_tables(only_courses=True)
        print("JSON data was loaded!")
    else:
        cashed_data, courses_dict = parse_both_tables(bar_is_on=True)
    print("Data updated!")


scheduler = BackgroundScheduler()
job_parser = scheduler.add_job(
    update_schedule_json_data, 'interval', minutes=30)

courses_prefix = [el[-1] for el in list(department_to_id.items())]
@socketio.on("getСoursesData")
def responseData_(data):
    print("if")
    if (isinstance(data, dict)) and ('item_id' in data.keys()) and (data["item_id"] in courses_prefix):
        emit('courses', courses_dict[data["item_id"]])
        return
    return url_for("index")


@socketio.on("connect")
def getConnection(data):
    clients.append(request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)


@socketio.on("getClassData")
def responseData(data):
    if (isinstance(data, dict)) and ('item_id' in data.keys()):
        requested_data = data["item_id"].split(":")
        cashed_data[requested_data[0]][requested_data[1]].update({
                                                                 "status": 200})
        emit('schedule', cashed_data[requested_data[0]][requested_data[1]])
        return
    return url_for("index")


@app.route("/")
def index():
    socketio.start_background_task(update_banner_data)
    return render_template("table.html", banner_links=BANNER_DATA["new_data"])

eventlet.spawn(update_banner_data)

if __name__ == '__main__':
    scheduler.start()
    socketio.run(app, port=80, host="127.0.0.1", debug=True)
