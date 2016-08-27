# coding=utf-8
import yaml
from bson import json_util
from flask import Flask, request
from pymongo import MongoClient

config = yaml.load(file('config.yml'), Loader=yaml.Loader)

app = Flask(__name__)
client = MongoClient(host=config['mongo_host'], port=config['mongo_port'])
db = client.coffee_advisor


@app.route('/api/places', methods=['GET', 'POST'])
def places():
    if request.method == 'GET':
        return get_places()
    elif request.method == 'POST':
        return post_places()


def get_places():
    places = list(db.places.find())
    return json_util.dumps(places)


@app.route('/api/places', methods=['POST'])
def post_places():
    if request.json:
        db.places.save(request.json)
        return '', 201
    return '', 400


if __name__ == '__main__':
    app.run(host=config['site_host'], port=config['site_port'])
