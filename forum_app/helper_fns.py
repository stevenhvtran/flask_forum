from flask import url_for, request
from forum_app.models.auth import auth
from forum_app.models.db import db, Post, User


def get_user_from_id(user_id):
    user = User.query.filter(User.id == user_id).first()
    return user


def get_post_from_post_id(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    return post


def post_to_dict(post_obj):
    if isinstance(post_obj, Post):
        author = get_user_from_id(post_obj.author_id)
        post_dict = {
            'post_id': post_obj.id,
            'title': post_obj.title,
            'body': post_obj.body,
            'author_id': post_obj.author_id,
            'author_name': author.username,
            'url': url_for('forum.get_post', post_id=post_obj.id)
        }
        return post_dict
    return None


def get_user_id(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return user.id
    return None


def get_post_response():
    response = request.get_json()
    return response['title'], response['body']


def commit_post_to_db():
    title, body = get_post_response()
    author_id = get_user_id(auth.username())
    post = Post(title=title, body=body, author_id=author_id)
    db.session.add(post)
    db.session.commit()


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


def get_post_errors():
    title, body = get_post_response()

    if not valid_title(title):
        return {'error': 'Invalid title'}
    if not valid_body(body):
        return {'error': 'Invalid body'}
    return None


def update_post_in_db(post_id):
    post = get_post_from_post_id(post_id)
    title, body = get_post_response()
    post.title, post.body = title, body
    db.session.commit()


def get_post_update_errors(post_id):
    post = get_post_from_post_id(post_id)
    if not post:
        return dict(error_msg={'error': 'Post not found'}, status_code=404)
    if post.username != auth.username():
        return dict(error_msg={'error': 'You do not have permission to edit this post'}, status_code=401)
    return None


def delete_post(post_id):
    post = get_post_from_post_id(post_id)
    post.delete()
    db.session.commit()
