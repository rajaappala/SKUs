import pytest


@pytest.fixture()
def sku_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client
    client = Client()
    client.login(username=admin_user.username, password='password')
    return client
