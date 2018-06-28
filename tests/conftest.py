import pytest
from forum_app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    yield test_client


@pytest.fixture
def client_with_user():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    # TODO: Fix the way this fixture set-up so this post command doesn't have to be checked
    test_client.post('/api/submit',
                     json={
                         'username': 'test123',
                         'password': 'test123'
                     })

    yield test_client
