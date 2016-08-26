# coding=utf-8
import flask
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.coffee_advisor


@app.route('/api/places', methods=['GET', 'POST'])
def places():
    if request.method == 'GET':
        return get_places()
    elif request.method == 'POST':
        return post_places()


def get_places():
    return flask.jsonify(db.places.find())


@app.route('/api/places', methods=['POST'])
def post_places():
    if request.json:
        db.places.save(request.json)
        return '', 201
    return '', 400


if __name__ == '__main__':
    app.run(port=12346)
