from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = '&85e8hE1%J2&eH(D*E8i2v)5DoquH*)D'

socketio = SocketIO(app)


class Classes_data:
    def __init__(self, class_ids: list = None):
        self.class_ids = class_ids


class Class_info(Classes_data):
    def __init__(self, class_number: str = None, group_number=None):
        self.class_number = class_number
        self.group_number = group_number
        if class_number is not None:
            self.status = 200


global_data = Classes_data(["9-1", "9-2", "10-1", "10-2", "10-3", "10-4", "10-5", "10-6", "10-7", "10-8", "11-1", "11-2", "11-3", "11-4", "11-5", "11-6", "11-7", "11-8", "11-9", "11-10", "11-11", "11-12"])


def get_class_info(item_id: str):
    data = Class_info(item_id.split(":")[0], item_id.split(":")[-1])
    return {"class_number": data.class_number, "status": data.status}


@socketio.on("connect")
def getConnection(data):
    print("Connected")


@socketio.on("getClassData")
def responseData(data):
    print("response-data")

    if (isinstance(data, dict)) and ('item_id' in data.keys()):
        print(data)
        if data['item_id'].split(":")[0] in global_data.class_ids:
            print(get_class_info(data['item_id']))
            emit('schedule', get_class_info(data['item_id']))
            return
    return url_for("index")


@app.route("/")
def index():
    return render_template("table.html")


if __name__ == '__main__':
    socketio.run(app, port=80, host="127.0.0.1", debug=True)
