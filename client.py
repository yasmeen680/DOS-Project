import http
import argparse

import os
import sys
from typing import Type
from flask.json import jsonify
import requests
import json
from datetime import datetime
import urllib
import urllib3
urllib.request

divider = "\n-----------------------------------------------\n"
exit = "/exit"
# help = "/help"
search = "search"
info = "info"
purchase = "purchase"
admin = "/admin"
changePrice = "/change_price"


def searchBycatagory(topic):
    # request to front device to search by topic
    r = requests.get('http://10.0.2.14:6060/search/{}'.format(topic))
    return r.text


def infobyId(id):
    # request to front device to search by id
    r = requests.get('http://10.0.2.14:6060/info/{}'.format(id))

    return r.text


def purchasebyId(id, name):
    r = requests.post('http://10.0.2.14:6060/purchase/{}'.format(id),
                      json=({"name": name}))  # request to front to send name
    return r.text


commands = ["search {topic}", "info {item_num}",
            "purchase {item_num}"]  # the commands saved in a list

print("\n Welcome\n")

inputt = ""
while (True):  # here we will see which command the user intered
    inputt = input("> ")  # > is the char in the command
    command = inputt.split(" ", 1)  # split using space
    if inputt == exit:
        break
    elif inputt == help:  # to help user
        for x in commands:
            print("  # "+x+"\n")
    elif len(command) < 2:
        print("  invalid command")
    else:
        if command[0] == search:
            print(searchBycatagory(command[1]))

        elif (command[0] == info):
            print(infobyId(command[1]))

        elif (command[0] == purchase):
            print("Enter your name: ")
            clientName = input("< ")
            print("  " + purchasebyId(command[1], clientName))

        else:
            print("  invalid command")
