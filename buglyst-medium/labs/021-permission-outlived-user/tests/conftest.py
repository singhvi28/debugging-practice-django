import pytest
from django.test import Client

from permissions import reset


@pytest.fixture()
def client():
    reset()
    return Client()
