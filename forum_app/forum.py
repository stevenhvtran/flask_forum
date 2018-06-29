from flask import Blueprint
from flask.json import jsonify
from flask_httpauth import make_response
from forum_app.helper_fns import *

bp = Blueprint(name='forum', import_name=__name__, url_prefix='/api')


@bp.route('/')
@auth.login_required
def index():
    return jsonify({'message': f'Hello {auth.username()}'})


@bp.route('/posts')
def get_all_posts():
    posts = db.session.query(Post).all()
    post_list = [post_to_dict(post) for post in posts]
    return jsonify({'posts': post_list})


@bp.route('/post/<int:post_id>', methods=('GET',))
def get_post(post_id):
    post = get_post_from_post_id(post_id)
    if post:
        return jsonify(post_to_dict(post))
    return make_response(jsonify({'error': 'Post not found'}), 404)


@bp.route('/submit', methods=('POST',))
@auth.login_required
def submit_post():
    errors = get_post_errors()
    if errors:
        return jsonify(errors)
    commit_post_to_db()
    return jsonify({'message': 'Post created successfully'})


@bp.route('/post/<int:post_id>', methods=('PUT', 'DELETE'))
@auth.login_required
def modify_post(post_id):
    update_errors = get_post_update_errors(post_id)
    if update_errors:
        return make_response(update_errors['error_msg'], update_errors['status_code'])

    if request.method == 'PUT':
        errors = get_post_errors()
        if errors:
            return jsonify(errors)
        update_post_in_db(post_id)
        return jsonify({'message': 'Post updated successfully'})

    if request.method == 'DELETE':
        delete_post(post_id)
        return jsonify({'message': 'Post deleted successfully'})
