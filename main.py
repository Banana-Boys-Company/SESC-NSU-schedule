from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import parser.parser as parser
import urllib.request
import json
import os.path
# import eventlet
import shutil

app = Flask(__name__)

app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'
socketio = SocketIO(app)
URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"
clients = []


# Server data initialization
if os.path.exists("data.json"):
    with open('data.json', "r", encoding="cp1251") as f:
        cashed_data = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        with open("data.json", "w") as f:
            cashed_data = parser.parse_schedule(
                'data.xlsx', 'Расписание_1 сем', fp=f)
    else:
        try:
            urllib.request.urlretrieve(URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            with open("data.json", "w") as f:
                cashed_data = parser.parse_schedule(
                    'data.xlsx', 'Расписание_1 сем', fp=f)
BANNER_DATA = {"new_data": [f"images/banner/{element}" for element in os.listdir(
    "\\\\WHITEEVILBRO-LA\Share")], "old_data": [], "filenames": os.listdir(
    "\\\\WHITEEVILBRO-LA\Share")}


for item in BANNER_DATA["new_data"]:
    filename = item.split("/")[-1]
    if filename not in os.listdir(f"{os.getcwd()}\\static\\images\\banner"):
        shutil.copyfile(
            f"//WHITEEVILBRO-LA/Share/{filename}", "{}\\static\\{}".format(os.getcwd(), item.replace("/", "\\")))


def update_banner_data():
    files = os.listdir("\\\\WHITEEVILBRO-LA\Share")
    files = [f"images/banner/{element}" for element in files]
    for file in BANNER_DATA["new_data"]:
        if file not in files:
            if file not in BANNER_DATA["old_data"]:
                BANNER_DATA["old_data"].append(files)
            os.remove("{}\\static\\{}".format(
                os.getcwd(), file.replace("/", "\\")))
    for file in files:
        if file not in BANNER_DATA["new_data"]:
            filename = file.split("/")[-1]
            if filename not in os.listdir(f"{os.getcwd()}\\static\\images\\banner"):
                a = shutil.copyfile(
                    f"//WHITEEVILBRO-LA/Share/{filename}", "{}\\static\\{}".format(os.getcwd(), file.replace("/", "\\")))
    BANNER_DATA["new_data"] = files
    # BANNER_DATA_old = set(BANNER_DATA["new_data"])
    # for i in range(len(files)):
    #     if files[i] not in BANNER_DATA["new_data"]:
    #         BANNER_DATA["new_data"].append(files[i])
    #     continue
    # for item in BANNER_DATA["new_data"]:
    #     if item not in files:
    #         BANNER_DATA["new_data"].remove(item)
    # if files != list(BANNER_DATA_old):
    #     new_files = list(set(files).difference(set(BANNER_DATA_old)))
    #     old_files = []
    #     for item in BANNER_DATA_old:
    #         if item.replace("images/banner/", '') not in files:
    #             old_files.append(item)
    #     print("THIIIIIIIS", files)
    #     print("OOOOOOOOOOOLDS", old_files)
    #     links = []
    #     for item in new_files:
    #         a = shutil.copyfile(
    #             f"//WHITEEVILBRO-LA/Share/{item}", f"{os.getcwd()}\\static\\images\\banner\\{item}")
    #         links.append(f"images/banner/{item}")
    #     for item in old_files:
    #         os.remove(f"{os.getcwd()}\\static\\images\\banner\\{item}")
    #     BANNER_DATA = {"new_data": links, "old_data": old_files}
    # else:
    #     print("DATA NOT UPDATED")


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
job_banner = scheduler.add_job(update_banner_data, 'interval', minutes=0.08)
job_parser = scheduler.add_job(
    update_schedule_json_data, 'interval', minutes=30)


@socketio.on("request-banner")
def sendBanner():
    emit('response-banner', BANNER_DATA)


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
    print(data)
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
