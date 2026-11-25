import pytest
from django.test import Client

from orders import reset


@pytest.fixture()
def client():
    reset()
    return Client()
