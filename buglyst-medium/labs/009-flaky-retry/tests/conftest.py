import pytest
from django.test import Client

from upstream import reset


@pytest.fixture()
def client():
    reset()
    return Client()
