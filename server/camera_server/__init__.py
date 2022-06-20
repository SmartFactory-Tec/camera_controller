import toml
from flask import Flask
from os.path import abspath
from os import makedirs
from camera_server.utilities import dict_merge

def create_app():
    app = Flask("server", instance_relative_config=True)

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

    import camera_server.cameras

    app.register_blueprint(cameras.bp)

    return app



