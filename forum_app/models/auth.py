from flask_httpauth import HTTPBasicAuth, md5, make_response
from forum_app.models.db import db, User
from flask.json import jsonify

auth = HTTPBasicAuth()


def username_exists(username):
    user_query = User.query.filter(User.username == username)
    db_query = db.session.query(user_query)
    return db_query.exists().scalar()


def get_pw_from_db(username):
    user_query = User.query.filter_by(username=username).first()
    password = user_query.password
    return password


@auth.get_password
def get_pw(username):
    if username_exists(username):
        return get_pw_from_db(username)
    return None


@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
