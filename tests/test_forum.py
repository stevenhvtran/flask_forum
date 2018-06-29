import pytest
import base64

expected_post_dict = {
        'post_id': 1,
        'title': 'test title',
        'body': 'test body',
        'author_id': 1,
        'author_name': 'test123',
        'url': '/api/post/1'
    }


@pytest.mark.usefixtures('client_with_user')
def test_index(client_with_user):
    valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
    response = client_with_user.get('/', headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'message': 'Hello test123'}


@pytest.mark.usefixtures('client')
def test_get_all_posts_unpopulated(client):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert dict(response.get_json()) == {'posts': []}


@pytest.mark.usefixtures('client_with_post')
def test_get_all_posts_populated(client_with_post):
    response = client_with_post.get('/api/posts')
    assert response.status_code == 200
    assert dict(response.get_json()) == {'posts': [expected_post_dict]}


@pytest.mark.usefixtures('client')
def test_get_post_non_existent(client):
    response = client.get('/api/post/1')
    assert response.status_code == 404
    assert dict(response.get_json()) == {'error': 'Post not found'}


@pytest.mark.usefixtures('client_with_post')
def test_get_post_exists(client_with_post):
    response = client_with_post.get('/api/post/1')
    assert response.status_code == 200
    assert dict(response.get_json()) == expected_post_dict


@pytest.mark.usefixtures('client_with_user')
def test_submit_post(client_with_user):
    valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
    response = client_with_user.post('/api/submit',
                                     json={'title': 'test title', 'body': 'test body'},
                                     headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'message': 'Post created successfully'}


@pytest.mark.usefixtures('client_with_user')
@pytest.mark.parametrize('title', [1, 'a', 'supersupersupersuperlongtitle', True])
def test_submit_post_title_error(client_with_user, title):
    valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
    response = client_with_user.post('/api/submit',
                                     json={'title': title, 'body': 'test body'},
                                     headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'error': 'Invalid title'}


@pytest.mark.usefixtures('client_with_user')
@pytest.mark.parametrize('body', [1, True, ['some list']])
def test_submit_post_body_error(client_with_user, body):
    valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
    response = client_with_user.post('/api/submit',
                                     json={'title': 'test title', 'body': body},
                                     headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'error': 'Invalid body'}


@pytest.mark.usefixtures('client_with_user')
def test_submit_post_success(client_with_user):
    valid_credentials = base64.b64encode(b'test123:test123').decode('utf-8')
    response = client_with_user.post('/api/submit',
                                     json={'title': 'test title', 'body': 'test body'},
                                     headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'message': 'Post created successfully'}

    response = client_with_user.get('/api/post/1')
    assert response.status_code == 200
    assert dict(response.get_json()) == expected_post_dict


@pytest.mark.usefixtures('client_with_post_and_two_users')
def test_update_post_auth_error(client_with_post_and_two_users):
    valid_credentials = base64.b64encode(b'testuser2:test123').decode('utf-8')
    client = client_with_post_and_two_users
    response = client.put('/api/post/1',
                          json={'title': 'test title', 'body': 'test body'},
                          headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 401
    assert dict(response.get_json()) == {'error': 'You do not have permission to edit this post'}


@pytest.mark.usefixtures('client_with_post_and_two_users')
def test_delete_post_auth_error(client_with_post_and_two_users):
    valid_credentials = base64.b64encode(b'testuser2:test123').decode('utf-8')
    client = client_with_post_and_two_users
    response = client.delete('/api/post/1',
                             headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 401
    assert dict(response.get_json()) == {'error': 'You do not have permission to edit this post'}


@pytest.mark.usefixtures('client_with_post_and_two_users')
def test_delete_post_success(client_with_post_and_two_users):
    valid_credentials = base64.b64encode(b'testuser1:test123').decode('utf-8')
    client = client_with_post_and_two_users
    response = client.delete('/api/post/1',
                             headers={'Authorization': 'Basic ' + valid_credentials})
    assert response.status_code == 200
    assert dict(response.get_json()) == {'message': 'Post deleted successfully'}

    response = client.get('/api/post/1')
    assert response.status_code == 404
