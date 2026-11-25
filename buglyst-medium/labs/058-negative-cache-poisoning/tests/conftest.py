import pytest
from django.test import Client

from views import reset_all


@pytest.fixture()
def client():
    reset_all()
    return Client()
