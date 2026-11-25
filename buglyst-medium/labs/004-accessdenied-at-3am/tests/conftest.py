import pytest
from django.test import Client

from credentials import reset


@pytest.fixture()
def client():
    reset()
    return Client()
