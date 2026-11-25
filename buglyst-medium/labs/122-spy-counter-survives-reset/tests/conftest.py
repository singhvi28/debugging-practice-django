import pytest
from django.test import Client

from spy import reset_spy


@pytest.fixture()
def client():
    reset_spy()
    return Client()
