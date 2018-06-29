from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        'SECRET_KEY': os.environ['SECRET_KEY'],
        'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    from forum_app.models.db import db
    db.init_app(app)
    with app.test_request_context():
        db.drop_all()  # drops all tables in database
        db.create_all()  # creates all the tables from db models

        from forum_app import forum
        app.register_blueprint(forum.bp)
        app.add_url_rule('/', endpoint='forum.index')

        from forum_app import register
        app.register_blueprint(register.bp)

        return app
