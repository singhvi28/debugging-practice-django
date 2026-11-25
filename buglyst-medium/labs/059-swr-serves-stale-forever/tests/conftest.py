import pytest
from django.test import Client

from swr_helper import reset


@pytest.fixture()
def client():
    reset()
    return Client()
