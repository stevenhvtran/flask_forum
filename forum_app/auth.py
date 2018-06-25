from flask import Blueprint, request
from flask.json import jsonify
from forum_app.db import db, User
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint(name='auth', import_name=__name__)


def get_users():
    return db.session.query(User.username).all()


@bp.route('/users', methods=('GET',))
def users():
    if request.method == 'GET':
        return jsonify({'users': get_users()})


def exists_in_db(table_obj, table_value, value):
    if db.session.query(table_obj.query.filter(table_value == value).exists()).scalar():
        return True
    return False


def create_user(username, password):
    user = User(username=username, password=generate_password_hash(password=password))
    db.session.add(user)
    db.session.commit()


def valid_username(username):
    if not username.isalnum() or len(username) < 5 or exists_in_db(User, User.username, username):
        return False
    return True


def valid_password(password):
    if len(password) < 5:
        return False
    return True


@bp.route('/signup', methods=('POST',))
def signup():
    request_data = request.get_json()

    if not valid_username(request_data['username']):
        return jsonify({'Error': 'Invalid Username'})
    elif not valid_password(request_data['password']):
        return jsonify({'Error': 'Invalid Password'})
    else:
        create_user(request_data['username'], request_data['password'])
        return jsonify(f"New user {request_data['username']} added")


def get_pwhash(username):
    return db.session.query(User.password.query.filter(User.username == username))


@bp.route('/signin', methods=('POST',))
def signin():
    request_data = request.get_json()
    if not valid_password(request_data['username']):
        return jsonify({'Error': 'Invalid Username'})
    if check_password_hash(get_pwhash(request['username']), request['password']):
        return jsonify('Login Successful')
