import pytest
import json


@pytest.fixture()
def sku_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client
    client = Client()
    # client.login(username=admin_user.username, password='password')
    response = client.post(
        path='/api/token/',
        data=json.dumps({'username': admin_user.username, 'password': 'password'}),
        content_type='application/json',
        follow=True
    )
    assert response.status_code == 200
    data = json.loads(response.content)
    client = Client(HTTP_AUTHORIZATION=f"Bearer {data['access']}")
    return client
