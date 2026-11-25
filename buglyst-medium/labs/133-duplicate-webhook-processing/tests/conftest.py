import pytest
from django.test import Client

from webhooks import reset


@pytest.fixture()
def client():
    reset()
    return Client()
