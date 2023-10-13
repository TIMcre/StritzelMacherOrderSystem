import sys
import re
import time

strizel_sorts = {
    0: "Vanille Zucker",
    1: "Zimt und Zucker",
    2: "Oreo",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
    12: "",
}

stritzel_insert_sorts = {
    0: "h",
    1: "Nutella",
    2: "Weiße Schokoloade",
    3: "Apfelmus",
}


def get_input():
    while True:
        code = input("Button Code: ")
        # if re.match(code, r""):
        return code


def convert_to_stritzel(number):
    stritzel = stritzel_sorts[number]

    return stritzel


def add_order(order_list, order):
    order_list.append(order)
    return order_list


def remove_order(order_list, order_number=0):
    removed_order = order_list.pop(order_number)
    return {"list": order_list, "order": removed_order}


def add_history(order, file="order_history.csv"):
    with open(file, "a"):
        file.write([order["number"], order["insert"]])


def main():
    order_list = []
    input_code = get_input()
    if input_code == "rm":
        remove_order(order_list)
    strizel = convert_to_strizel(input)
    add_order(strizel)
    # if 2nd input true remove_order and add to history


if __name__ == "__main__":
    main()
