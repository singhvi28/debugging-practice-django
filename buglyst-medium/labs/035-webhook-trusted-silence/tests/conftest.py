import pytest
from django.test import Client

from views import _reset_processed


@pytest.fixture()
def client():
    _reset_processed()
    return Client()
