import pytest
from forum_app import create_app
from forum_app.models.db import db, User, Post
from werkzeug.security import generate_password_hash


def create_user(username, password):
    user = User(username=username, password=generate_password_hash(password=password))
    db.session.add(user)
    db.session.commit()


def create_post(title, body, author_id):
    post = Post(title=title, body=body, author_id=author_id)
    db.session.add(post)
    db.session.commit()



@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    db.init_app(app)
    with app.test_request_context():
        db.drop_all()  # drops all tables for fresh database
        db.create_all()  # creates all the tables from db models

        yield test_client


@pytest.fixture
def client_with_user():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    db.init_app(app)
    with app.test_request_context():
        db.drop_all()  # drops all tables for fresh database
        db.create_all()  # creates all the tables from db models

        create_user('test123', 'test123')

        yield test_client


@pytest.fixture
def client_with_post():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    db.init_app(app)
    with app.test_request_context():
        db.drop_all()  # drops all tables for fresh database
        db.create_all()  # creates all the tables from db models

        create_user('test123', 'test123')
        create_post('test title', 'test body', 1)

        yield test_client


@pytest.fixture
def client_with_post_and_two_users():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    db.init_app(app)
    with app.test_request_context():
        db.drop_all()  # drops all tables for fresh database
        db.create_all()  # creates all the tables from db models

        create_user('testuser1', 'test123')
        create_user('testuser2', 'test123')
        create_post('test title', 'test body', 1)

        yield test_client