from flask import Flask
from flask.json import jsonify


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar('FLASK_CONFIG')

    from forum_app.model import db
    db.init_app(app)

    @app.route('/')
    def hello():
        return jsonify('Hello World')

    return app
