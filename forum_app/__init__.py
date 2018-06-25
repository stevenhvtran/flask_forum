from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar('FLASK_CONFIG')

    from forum_app.db import db
    db.init_app(app)

    with app.test_request_context():
        db.drop_all()  # resets the database when server is first run
        db.create_all()  # creates all the tables from db.py

    from forum_app import forum
    app.register_blueprint(forum.bp)
    app.add_url_rule('/', endpoint='index')

    return app
