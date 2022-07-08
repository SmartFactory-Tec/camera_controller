import toml
from flask import Flask
from os.path import abspath
from os import makedirs
from camera_server.utilities import dict_merge

from datetime import datetime
import yappi
import atexit

def create_app():
    app = Flask("server", instance_relative_config=True,static_url_path='',
            static_folder='../client/build/')

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    # Default settings
    settings = toml.load(abspath("./camera_server/config.toml"))

    try:
        instance_settings = toml.load(app.instance_path + "/config.toml")
        settings = dict_merge(settings, instance_settings)
    except FileNotFoundError:
        pass

    app.config.update(settings)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    import camera_server.api

    app.register_blueprint(api.bp)

    return app



