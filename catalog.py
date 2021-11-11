from flask import Flask
import flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask import request
from flask import Flask,jsonify,json
import json


app = Flask(__name__)
api = Api(app)

 
@app.route('/books/<id>', methods=['GET'])
def getBookById(id):

    file = open('books.json',) #opens json file
    data = json.load(file)#load json file in a var 

    for b in data['books']: #loop to find the book in catalog
        if b['id'] == int(id) :
            return jsonify(b)
    file.close()#close file
    abort(404)#if not found return 404

@app.route('/books', methods=['GET'])
def getBooksByTopic():
    topic = request.args.get('topic')#to know which topic we are searching for
    file = open('books.json',) # open json file
    data = json.load(file) #load json in data var
    booksList = []
    for book in data['books']: 
        if book['topic'] == topic :
            bookDict = {#struct for the book found 
            'id': book['id'],
            'title': book['title']}
            booksList.append(bookDict)#add the struct for the array of books
            
    file.close()

    if len(booksList) == 0 : #if the array of books is empty then return 404 (not found)
        abort(404)

    return jsonify(booksList) #else return the list of books

@app.route('/books/<id>', methods=['PUT'])
def updateBookQuantity(id):

    body = request.json
    newNoOfBooks = body["quantity"]

    file = open('books.json','r+') #open file for read
    data = json.load(file) 
    for book in data['books']: #to search for the certin book 
        if book['id'] == int(id) :
            if (book['quantity'] < 1) or (newNoOfBooks < 0) : #if the there are no books return 403 (forbidden)
                return abort(403) 
            book['title'] = body["title"] 
            book['topic'] = body["topic"]
            book['quantity'] = newNoOfBooks#else we will update the no of books
            book['price'] = body["price"]
    file.close()

    with open("books.json", "w") as jsonFile:#then we will write to the json file to update the book info (no of books)
        json.dump(data, jsonFile)

    return flask.Response(status=204)#no content
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')#run and to be able to transe from device to another
