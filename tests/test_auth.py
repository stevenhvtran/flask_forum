import pytest
from tests.fixtures import client


@pytest.mark.usefixtures('client')
def test_get_users(client):
    response = client.get('/users')
    json_data = response.get_json()
    assert response.status_code == 200
    assert dict(json_data) == {'users': []}


@pytest.mark.usefixtures('client')
def test_signup_valid_credentials(client):
    response = client.post('/signup', json={
        'username': 'testtest',
        'password': 'secret',
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == 'New user testtest added'


@pytest.mark.usefixtures('client')
@pytest.mark.parametrize('username,password,expected', [
    ('a', 'secret', {'Error': 'Invalid Username'}),
    ('test!', 'secret', {'Error': 'Invalid Username'}),
    ('testtest', 'a', {'Error': 'Invalid Password'})
])
def test_signup_invalid(username, password, expected, client):
    response = client.post('/signup', json={
        'username': username,
        'password': password,
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert dict(json_data) == expected