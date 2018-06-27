from flask_httpauth import HTTPBasicAuth, make_response
from forum_app.models.db import db, User
from flask.json import jsonify
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()


def username_exists(username):
    user_query = User.query.filter(User.username == username).first()
    if user_query:
        return True
    return False


def get_pw_from_db(username):
    user_query = User.query.filter_by(username=username).first()
    password = user_query.password
    return password


@auth.verify_password
def verify_password(username, password):
    if username_exists(username):
        return check_password_hash(get_pw_from_db(username), password)
    return False


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
