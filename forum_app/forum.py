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
    post = Find.post(Post.id, post_id)
    if post:
        return jsonify(post_to_dict(post))
    return make_response(jsonify({'error': 'Post not found'}), 404)


def get_post_errors():
    response = get_post_response()
    if response:
        title, body = response
        if not ValidPost.title(title):
            return jsonify({'error': 'Invalid title'})
        if not ValidPost.body(body):
            return jsonify({'error': 'Invalid body'})
        return None
    return make_response({'error': 'Malformed request'}, 400)


@bp.route('/submit', methods=('POST',))
@auth.login_required
def submit_post():
    errors = get_post_errors()
    if errors:
        return errors
    PostTable.add()
    return jsonify({'message': 'Post created successfully'})


@bp.route('/post/<int:post_id>', methods=('PUT', 'DELETE'))
@auth.login_required
def modify_post(post_id):
    post = Find.post(Post.id, post_id)
    if not post:
        return make_response(jsonify({'error': 'Post not found'}), 404)
    if post.author_id != Find.user(User.username, auth.username()).id:
        return make_response(jsonify({'error': 'You do not have permission to edit this post'}), 401)

    if request.method == 'PUT':
        errors = get_post_errors()
        if errors:
            return errors
        PostTable.update(post_id)
        return jsonify({'message': 'Post updated successfully'})

    if request.method == 'DELETE':
        PostTable.delete(post_id)
        return jsonify({'message': 'Post deleted successfully'})
