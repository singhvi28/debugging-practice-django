import json

import pytest
from django.test import Client

from helper import reset


@pytest.fixture()
def client():
    reset()
    return Client()


@pytest.fixture(autouse=True)
def _reset_memo_cache():
    reset()
    yield
    reset()
