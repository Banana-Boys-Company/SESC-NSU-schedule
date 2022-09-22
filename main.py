from flask import Flask, render_template, url_for
import datetime

app = Flask(__name__)


class Table:
    def __init__(self, class_number, group_number):
        self.class_number = class_number
        self.group_number = group_number


class_data = Table("10-4", "207")

class_nums = []


@app.route("/")
def index():
    return render_template("table.html", table_data=class_nums)


if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0", debug=True)