from flask import Blueprint, request
from flask.json import jsonify
from flask_httpauth import make_response
from forum_app.models.db import db, User
from forum_app.models.auth import username_exists
from werkzeug.security import generate_password_hash


bp = Blueprint(name='register', import_name=__name__, url_prefix='/api')


def valid_username(username):
    if isinstance(username, str):
        valid_conditions = (
            not username_exists(username)
            and username.isalnum()
            and 3 < len(username) < 24
        )
        if valid_conditions:
            return True
    return False


def valid_password(password):
    if isinstance(password, str):
        valid_conditions = (
            len(password) > 5
            and not password.isalpha()
            and not password.isdigit()
        )
        if valid_conditions:
            return True
    return False


def create_user(username, password):
    user = User(username=username, password=generate_password_hash(password=password))
    db.session.add(user)
    db.session.commit()


@bp.route('/register', methods=('POST',))
def register():
    response = request.get_json()
    username, password = response['username'], response['password']
    if valid_username(username) and valid_password(password):
        create_user(username, password)
        return jsonify({'message': 'Registration successful'})
    return make_response(jsonify({'error': 'Invalid username or password'}), 400)
