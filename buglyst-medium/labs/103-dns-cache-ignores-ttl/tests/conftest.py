import pytest
from django.test import Client

from helper import reset
from views import _reset_resolver_state


@pytest.fixture()
def client():
    _reset_resolver_state()
    return Client()


@pytest.fixture(autouse=True)
def _reset_dns_state():
    _reset_resolver_state()
    yield
    _reset_resolver_state()
