import pytest
from forum_app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    test_client = app.test_client()

    yield test_client
