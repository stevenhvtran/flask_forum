import pytest
from forum_app.models.db import User


@pytest.mark.usefixtures('client')
def test_valid_registration(client):
    response = client.post('/api/submit', json={'username': 'test123', 'password': 'test123'})
    assert response.status_code == 200
    assert dict(response.json()) == {'message': 'Registration successful'}
    created_user = User.query.filter(User.username == 'test123').first()
    assert created_user is not None


@pytest.mark.usefixtures('client')
@pytest.mark.parametrize('username', ['a', 'supersupersuperlongusername', '', 'test!'])
def test_username_length_errors(client, username):
    response = client.post('/api/submit', json={'username': username, 'password': 'test123'})
    assert response.status_code == 400
    assert dict(response.json()) == {'error': 'Invalid username or password'}


@pytest.mark.usefixtures('client_with_user')
def test_username_already_exists_errors(client_with_user):
    response = client_with_user.post('/api/submit', json={'username': 'test123', 'password': 'test123'})
    assert response.status_code == 400
    assert dict(response.json()) == {'error': 'Invalid username or password'}


@pytest.mark.usefixtures('client')
@pytest.mark.parametrize('password', ['a', 'testtest', '123123'])
def test_password_errors(client, password):
    response = client.post('/api/submit', json={'username': 'test123', 'password': password})
    assert response.status_code == 400
    assert dict(response.json()) == {'error': 'Invalid username or password'}
