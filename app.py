import os

import yaml
from flask import Flask

config = yaml.load(file(os.path.dirname(os.path.abspath(__file__)) + '/config.yml'), Loader=yaml.Loader)


def get_app(new_config_dict):
    app = Flask(__name__)
    app.config.from_object(__name__)

    config_dict = dict(
        MONGO_HOST=config['mongo_host'],
        MONGO_PORT=config['mongo_port'],
        MONGO_DBNAME='coffee_advisor')
    config_dict.update(new_config_dict)

    app.config.update(config_dict)
    return app
