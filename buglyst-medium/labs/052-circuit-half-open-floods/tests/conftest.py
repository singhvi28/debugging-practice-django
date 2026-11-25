import pytest
from django.test import Client

from views import reset


@pytest.fixture()
def client():
    reset()
    return Client()
