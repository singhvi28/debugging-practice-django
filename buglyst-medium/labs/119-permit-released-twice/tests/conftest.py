import pytest
from django.test import Client

from semaphore import reset


@pytest.fixture()
def client():
    reset()
    return Client()
