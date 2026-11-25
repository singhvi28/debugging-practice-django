import pytest
from django.test import Client

from items import reset


@pytest.fixture()
def client():
    reset()
    return Client()
