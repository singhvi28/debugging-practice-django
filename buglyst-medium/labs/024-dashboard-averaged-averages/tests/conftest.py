import pytest
from django.test import Client

from metrics import reset


@pytest.fixture()
def client():
    reset()
    return Client()
