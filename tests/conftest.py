import pytest
from forum_app import create_app
from forum_app.models.db import db


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

        # TODO: Fix the way this fixture set-up so this post command doesn't have to be checked
        test_client.post('/api/register',
                         json={
                             'username': 'test123',
                             'password': 'test123'
                         })

        yield test_client
