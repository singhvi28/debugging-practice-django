import pytest
from django.test import Client
from api import store
@pytest.fixture()
def client(): store.reset(); return Client()
AUTH={"Authorization":"Bearer secret-token"}
