from flask import Blueprint, request, redirect, url_for
from flask.json import jsonify
from forum_app.db import db, User

bp = Blueprint(name='forum', import_name=__name__)


@bp.route('/')
def index():
    return jsonify({'message': 'Hello World'})


@bp.route('/users')
def show_users():
    usernames = db.session.query(User.username).all()
    return jsonify({'users': usernames})


@bp.route('/create', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        request_data = request.get_json()
        if db.session.query(User.query.filter(User.username == request_data['Username']).exists()).scalar():
            return jsonify({'Error': f"User {request_data['Username']} already exists"})
        user = User(username=request_data['Username'])
        db.session.add(user)
        db.session.commit()
        return jsonify(f"New user {request_data['Username']} added")
    return redirect(url_for('forum.index'))
