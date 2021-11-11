from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask, jsonify, json
import json
import requests

app = Flask(__name__)
api = Api(app)

result = ""


@app.route('/info/<id>', methods=['GET'])
def getBookById(id):
    r = requests.get('http://10.0.2.14:5050/books/{}'.format(id))  # catalog

    if r.status_code == 404:
        return "invalid book number"

    if r.status_code == 200:
        response = r.json()
        result = ""
        result += "id      : "+str(response["id"]) + "\n"
        result += "title   : "+response["title"] + "\n"
        result += "price   : "+str(response["price"]) + "\n"
        result += "quantity: "+str(response["quantity"])

        return result

    else:
        return "ERROR try again later"


@app.route('/search/<topic>', methods=['GET'])
def getBooksByTopic(topic):
    r = requests.get(
        'http://10.0.2.14:5050/books?topic={}'.format(topic))  # catalog
    if r.status_code == 404:  # not found
        return "  no books found with this topic"
    if r.status_code == 200:  # ok found
        response = r.json()
        print(r.text)

        for d in response:
            result = ""
            result += "id    : "+str(d["id"]) + "\n"
            result += "title : "+d["title"]

        return result

    else:
        return "ERROR"


@app.route('/purchase/<id>', methods=['POST'])
def updateBookQuantity(id):
    body = request.get_json()
    name = body["name"]

    r = requests.post('http://10..0.2.15:4040/orders',
                      json={"id": int(id), "name": name})
    if r.status_code == 404:
        return "Invalid"
    if r.status_code == 400:
        return "Out of stock"
    if r.status_code == 200:
        response = r.json()
        return "Bought Book '" + response["title"]+"'"
    else:
        return "ERROR try again later"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
