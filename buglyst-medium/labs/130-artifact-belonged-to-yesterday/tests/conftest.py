import pytest
from django.test import Client

from artifacts import reset


@pytest.fixture()
def client():
    reset()
    return Client()
