import pytest
from django.test import Client

from store import reset


@pytest.fixture()
def client():
    reset()
    return Client()
