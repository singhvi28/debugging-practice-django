import pytest
from django.test import Client

from backend import reset as reset_backend
from cache import reset as reset_cache


@pytest.fixture()
def client():
    reset_backend()
    reset_cache()
    return Client()
