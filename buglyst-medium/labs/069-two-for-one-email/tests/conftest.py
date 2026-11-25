import pytest
from django.test import Client

from register_helper import reset


@pytest.fixture()
def client():
    reset()
    return Client()
