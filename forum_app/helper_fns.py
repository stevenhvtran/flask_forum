from flask import url_for, request
from forum_app.models.auth import auth
from forum_app.models.db import db, Post, User


def post_to_dict(post_obj):
    """Converts Post object to a dictionary of values"""
    if isinstance(post_obj, Post):
        author = Find.user(User.id, post_obj.author_id)
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


def get_post_response():
    response = request.get_json()
    if response:
        if 'title' in response.keys():
            if 'body' in response.keys():
                return response['title'], response['body']
            return response['title'], ''
    return None


class Find:
    @staticmethod
    def user(column, value):
        user = User.query.filter(column == value).first()
        return user

    @staticmethod
    def post(column, value):
        post = Post.query.filter(column == value).first()
        return post


class PostTable:
    @staticmethod
    def add():
        title, body = get_post_response()
        author_id = Find.user(User.username, auth.username()).id
        post = Post(title=title, body=body, author_id=author_id)
        db.session.add(post)
        db.session.commit()

    @staticmethod
    def update(post_id):
        post = Find.post(Post.id, post_id)
        title, body = get_post_response()
        post.title, post.body = title, body
        db.session.commit()

    @staticmethod
    def delete(post_id):
        post = Find.post(Post.id, post_id)
        db.session.delete(post)
        db.session.commit()


class ValidPost:
    @staticmethod
    def title(title):
        if isinstance(title, str):
            if 3 < len(title) < 25:
                return True
        return False

    @staticmethod
    def body(body):
        if isinstance(body, str):
            if len(body) <= 1000:
                return True
        return False
