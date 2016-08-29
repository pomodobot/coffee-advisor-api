# coding=utf-8
import json
import os

import math
import yaml
from bson.objectid import ObjectId
from flask import Flask, request
from flask.ext.cors import CORS
from flask_pymongo import PyMongo

from app import get_app

config = yaml.load(file(os.path.dirname(os.path.abspath(__file__)) + '/config.yml'), Loader=yaml.Loader)

app = get_app({})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mongo = PyMongo(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/api/places', methods=['GET', 'POST'])
def places():
    if request.method == 'GET':
        return get_places(), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'POST':
        return post_places()


def get_places():
    lat = float(request.args.get('latitude'))
    lon = float(request.args.get('longitude'))
    radius = request.args.get('radius') or 5000.0

    if not lat or not lon:
        return 'Bad Request', 400

    # Earth’s radius, sphere
    earth_radius = 6378137.0

    # offsets in meters
    dn = radius
    de = radius

    # Coordinate offsets in radians
    d_lat = dn / earth_radius
    d_lon = de / (earth_radius * math.cos(math.pi * lat / 180))

    # OffsetPosition, decimal degrees
    lat0 = lat + d_lat * 180 / math.pi
    lon0 = lon + d_lon * 180 / math.pi

    lat1 = lat - d_lat * 180 / math.pi
    lon1 = lon - d_lon * 180 / math.pi

    print lat0, lon0, lat1, lon1

    places = list(mongo.db.places.find(
        {
            "location.latitude": {"$lt": lat0, "$gt": lon0},
            "location.longitude": {"$lt": lat1, "$gt": lon1}
        }))
    return JSONEncoder().encode(places)


@app.route('/api/places', methods=['POST'])
def post_places():
    if request.json:
        mongo.db.places.save(request.json)
        return '', 201
    return '', 400


if __name__ == '__main__':
    app.run(host=config['site_host'], port=config['site_port'])
