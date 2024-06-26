# -*- coding: utf-8 -*-
# -----------------------------------
# Dictonary Part
stritzel_outside_sorts = {
    "0": "Vanille Zucker",
    "1": "Zimt Zucker",
    "2": "Oreo",
    "3": "Raffaello",
    "4": "Mandel",
    "5": "Walnuss",
    "6": "Haselnuss",
    "7": "Buntestreusel",
    "8": "Schokostreusel",
    "9": "Kakao",
    "10": "Cocos",
    "11": "Lotus",
}

stritzel_inside_sorts = {
    "0": "Ohne",
    "1": "Nutella",
    "2": "Weiße Schokoloade",
    "3": "Apfelmus",
}

# -----------------------------------
# Function Part
from flask import Flask, render_template, url_for, request, redirect, Response, json
from flask_socketio import SocketIO, send, join_room, leave_room
import sys
import re
import csv
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


order_list = []


def convert_to_name(outside, inside):
    outside_name = stritzel_outside_sorts[outside]
    inside_name = stritzel_inside_sorts[inside]

    return {
        "outside": outside_name,
        "inside": inside_name,
    }


def add_order(order_list, order):
    order_list.append(order)

    return order_list


def remove_order(order_list, order_number=0):
    try:
        removed_order = order_list.pop(order_number)
    except:
        return None
        print("failed")

    return {"list": order_list, "order": removed_order}


def add_history(order, file_name="order_history.csv"):
    fieldnames = ["order_outside", "order_inside", "order_time"]

    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(
            {
                "order_outside": order["outside_sort"],
                "order_inside": order["inside_sort"],
                "order_time": datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"),
            }
        )


def print_orders(orders, mode):
    print()
    print(orders)
    if mode == "production":
        for order in orders:
            print(f'{order["name"]["outside"]}')
    elif mode == "service":
        for order in orders:
            print(f'{order["name"]["outside"]} mit {order["name"]["inside"]}')


def is_valid_code(code):
    # old regex ((0[0-9])|[1-9]{2})[0-3]
    if re.match(r"^((0[0-9])|[1-9]{2}|[1-9]0)[0-3]$", code) or code == "rm":
        return True
    return False


def convert_code_to_order(code):
    outside_sort = "0" if code[:2] == "00" else code[:2].lstrip("0")
    inside_sort = code[2:]
    name = convert_to_name(outside_sort, inside_sort)

    return {
        "outside_sort": outside_sort,
        "inside_sort": inside_sort,
        "name": name,
    }


# -----------------------------------
# Flask Part
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/history")
def history():
    return render_template("history.html,")


@app.route("/production")
def production():
    return render_template("production.html")


@app.route("/service")
def service():
    return render_template(
        "service.html",
        stritzel_outside_sorts=stritzel_outside_sorts,
        stritzel_inside_sorts=stritzel_inside_sorts,
    )


#------------------
#Socketio

common_room = "common_room"

@socketio.on("connect")
def handel_connect():
    join_room(common_room)

@socketio.on("disconnect")
def handle_disconnect():
    leave_room(common_room)



@socketio.on("message")
def handel_message(message):
    #print("Recived message: " + message)

    data = json.loads(message)

    match data["code"]:
        case "rm":
            add_history(remove_order(order_list)["order"])
        case "connected":
            pass
        case _:
            add_order(order_list, convert_code_to_order(data["code"]))

    #print(f"Answering message: {order_list}")
    send(message=json.dumps(order_list), room=common_room)


if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
    )