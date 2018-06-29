import pytest
from forum_app import create_app
from forum_app.models.db import db
import base64


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

        test_client.post('/api/register', json={'username': 'test123', 'password': 'test123'})

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

        test_client.post('/api/register', json={'username': 'test123', 'password': 'test123'})

        valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
        test_client.post('/api/submit',
                         json={'title': 'test title', 'body': 'test body'},
                         headers={'Authorization': 'Basic ' + valid_credentials})

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

        test_client.post('/api/register', json={'username': 'testuser1', 'password': 'test123'})
        test_client.post('/api/register', json={'username': 'testuser2', 'password': 'test123'})

        valid_credentials = base64.b64encode(b'testuser1:test123').decode('utf-8')
        test_client.post('/api/submit',
                         json={'title': 'test title', 'body': 'test body'},
                         headers={'Authorization': 'Basic ' + valid_credentials})

        yield test_client