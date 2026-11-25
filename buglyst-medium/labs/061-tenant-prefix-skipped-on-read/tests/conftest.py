import pytest
from django.test import Client

from tenant_helper import reset


@pytest.fixture()
def client():
    reset()
    return Client()
