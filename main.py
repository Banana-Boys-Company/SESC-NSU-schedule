from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import parser.parser as parser
import urllib.request
import json
import os.path

app = Flask(__name__)

app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'
socketio = SocketIO(app)
URL = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pub?output=xlsx"


if os.path.exists("data.json"):
    with open('data.json') as f:
        cashed_data = json.load(f)
else:
    if os.path.exists("data.xlsx"):
        cashed_data = parser.parse_schedule(
            'data.xlsx', 'Расписание_1 сем')
    else:
        try:
            urllib.request.urlretrieve(URL, "data.xlsx")
        except Exception:
            print(Exception)
        else:
            cashed_data = parser.parse_schedule(
                'data.xlsx', 'Расписание_1 сем')


def update_schedule_json_data():
    print("Start updating data...")
    global cashed_data
    try:
        urllib.request.urlretrieve(URL, "data.xlsx")
    except Exception:
        print("Downloading error, trying to open json data...")
        with open('data.json') as f:
            cashed_data = json.load(f)
        print("JSON data was loaded!")
    else:
        cashed_data = parser.parse_schedule(
            'data.xlsx', 'Расписание_1 сем')
    print("Data updated!")


scheduler = BackgroundScheduler()
job = scheduler.add_job(update_schedule_json_data, 'interval', minutes=30)


@socketio.on("connect")
def getConnection(data):
    print("Connected")


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
    return render_template("table.html")


if __name__ == '__main__':
    scheduler.start()
    socketio.run(app, port=80, host="127.0.0.1", debug=True)
