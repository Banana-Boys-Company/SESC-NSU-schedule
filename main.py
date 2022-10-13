from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import parser.parser as pars
from parser.common import first_table_properties, second_table_properties, merge_dicts
import urllib.request
import json
import os.path
import urllib.parse
# import eventlet
import shutil

app = Flask(__name__)

app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'
socketio = SocketIO(app)
URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"
clients = []
parser = pars.ScheduleParser('data.xlsx')


def parse_both_tables(bar_is_on=False):
    dict1 = parser.parse('Расписание_1 сем', first_table_properties, bar_is_on=bar_is_on)
    dict2 = parser.parse('Расписание_1сем_2пол.дня', second_table_properties, bar_is_on=bar_is_on)
    full_dict = merge_dicts(dict1, dict2)
    del dict1, dict2
    return full_dict


# Server data initialization
if os.path.exists("data.json"):
    with open('data.json', "r", encoding="cp1251") as f:
        cashed_data = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("data.json", "w") as f:
            cashed_data = parse_both_tables(bar_is_on=True)
            json.dump(cashed_data, fp=f)
    else:
        try:
            urllib.request.urlretrieve(URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("data.json", "w") as f:
                cashed_data = parse_both_tables(bar_is_on=True)
                json.dump(cashed_data, fp=f)

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


def update_schedule_json_data():
    print("Start updating data...")
    global cashed_data
    try:
        urllib.request.urlretrieve(URL, "data.xlsx")
    except Exception:
        print("Downloading error, trying to open json data...")
        with open('data.json', "r", encoding="cp1251") as f:
            cashed_data = json.load(f)
        print("JSON data was loaded!")
    else:
        with open("data.json", "w") as f:
            cashed_data = parser.parse_schedule(
                'data.xlsx', 'Расписание_1 сем', fp=f)
    print("Data updated!")


scheduler = BackgroundScheduler()
job_banner = scheduler.add_job(update_banner_data, 'interval', minutes=0.1)
job_parser = scheduler.add_job(
    update_schedule_json_data, 'interval', minutes=30)


@socketio.on("request-banner")
def sendBanner():
    new_data = BANNER_DATA.copy()
    new_data["new_data"] = [urllib.parse.quote_plus(item).replace(r"%2F", "/")
                            for item in BANNER_DATA.copy()["new_data"]]
    emit('response-banner', new_data)


@socketio.on("connect")
def getConnection(data):
    print('Client connected')
    clients.append(request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)


@socketio.on("getClassData")
def responseData(data):
    print("response-data")
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


if __name__ == '__main__':
    scheduler.start()
    socketio.run(app, port=80, host="127.0.0.1", debug=True)
