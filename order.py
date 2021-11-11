from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask, jsonify, json
import requests
import json
import time
from datetime import datetime

app = Flask(__name__)
api = Api(app)


@app.route('/orders', methods=['POST'])
def addNewOrder():
    body = request.get_json()  # returns json and put it in the body var
    id = body["id"]
    name = body["name"]

    # here we ask the cataloge server if it has a certin book
    requestt = requests.get(
        'http://10.0.2.13:5050/books/{}'.format(id))  # catalog
    if requestt.status_code == 404:
        return abort(404, description="we didn't find the book")

    req = requestt.json()  # to save the info as json in a var
    NoOfBooks = req["quantity"]  # to know the no of books
    if NoOfBooks == 0:
        # if there are no books then it well be ot of stock
        return abort(400, description="empty")

    newNoOfBooks = NoOfBooks - 1  # else the no of books will decrease by 1
    req["quantity"] = newNoOfBooks  # update
    # update to catalog
    r2 = requests.put(
        'http://10.0.2.13:5050/books/{}'.format(str(id)), json=(req))  # catalog
    if requestt.status_code == 403:
        return abort(403, description="failed")
    elif requestt.status_code == 204:

        array = {
            'id': int(id),
            'name': name,
        }

        with open("orders.json", "r") as file:  # read
            data = json.load(file)
        data.append(array)
        with open("orders.json", "w") as file:  # write
            json.dump(data, file)

    return jsonify({"title": req["title"]})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
