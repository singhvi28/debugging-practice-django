import pytest
from django.test import Client

from budget_helper import reset_budget


@pytest.fixture()
def client():
    reset_budget()
    return Client()
