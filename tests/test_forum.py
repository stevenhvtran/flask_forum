import pytest


@pytest.mark.usefixtures('client')
def test_base_url(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert dict(json_data) == {'message': 'Hello World'}
