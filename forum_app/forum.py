from flask import Blueprint, url_for, abort, request
from flask.json import jsonify
from forum_app.models.auth import auth
from forum_app.models.db import db, Post, User

bp = Blueprint(name='forum', import_name=__name__, url_prefix='/api')


@bp.route('/')
@auth.login_required
def index():
    return jsonify({'message': f'Hello {auth.username()}'})


def post_to_dict(post_obj):
    if isinstance(post_obj, Post):
        post_dict = {
            'id': post_obj.id,
            'title': post_obj.title,
            'body': post_obj.body,
            'author': post_obj.author_id,
            'url': url_for('forum.get_post', post_id=post_obj.id)
        }
        return post_dict
    return None


@bp.route('/posts')
def get_all_posts():
    posts = db.session.query(Post).all()
    post_list = [post_to_dict(post) for post in posts]
    return jsonify({'posts': post_list})


@bp.route('/post/<int:post_id>')
def get_post(post_id):
    post_query = Post.query.filter(Post.id == post_id).first()
    if post_query:
        return jsonify(post_to_dict(post_query))
    return abort(404)


def valid_title(title):
    if isinstance(title, str):
        if 3 < len(title) < 25:
            return True
    return False


def valid_body(body):
    if isinstance(body, str):
        if len(body) <= 1000:
            return True
    return False


def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return user.id
    return None


def commit_post_to_db(title, body, username):
    author_id = get_user_id(username)
    post = Post(title=title, body=body, author_id=author_id)
    db.session.add(post)
    db.session.commit()


@bp.route('/submit', methods=('POST',))
@auth.login_required
def submit_post():
    response = request.get_json()
    title, body, username = response['title'], response['body'], auth.username()
    if not valid_title(title):
        return jsonify({'error': 'Invalid title'})
    if not valid_body(body):
        return jsonify({'error': 'Invalid body'})
    commit_post_to_db(title, body, username)
    return jsonify({'message': 'Post created successfully'})
