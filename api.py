# coding=utf-8
import math
import os

import yaml
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo

from app import get_app
from utils import JSONEncoder

config = yaml.load(file(os.path.dirname(os.path.abspath(__file__)) + '/config.yml'), Loader=yaml.Loader)

app = get_app({})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = PyMongo(app)


@app.route('/api/places', methods=['GET', 'POST'])
def places():
    if request.method == 'GET':
        return get_places(), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == 'POST':
        return post_places()


def get_places():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lng'))
    radius = request.args.get('radius') or 5000.0

    if not lat or not lon:
        return 'Bad Request', 400

    radius /= 1.40

    # Earth’s radius, sphere
    earth_radius = 6378137.0

    # Coordinate offsets in radians
    d_lat = radius / earth_radius
    d_lon = radius / (earth_radius * math.cos(math.pi * lat / 180))

    # OffsetPosition, decimal degrees
    lat0 = lat + d_lat * 180 / math.pi
    lon0 = lon + d_lon * 180 / math.pi

    lat1 = lat - d_lat * 180 / math.pi
    lon1 = lon - d_lon * 180 / math.pi

    places = list(mongo.db.places.find(
        {
            "location.lat": {"$lt": lat0, "$gt": lon0},
            "location.lng": {"$lt": lat1, "$gt": lon1}
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
