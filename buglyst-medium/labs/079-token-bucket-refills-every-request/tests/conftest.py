import pytest
from django.test import Client

from helper import reset


@pytest.fixture()
def client():
    reset()
    return Client()
