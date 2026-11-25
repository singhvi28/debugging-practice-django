import json

import pytest
from django.test import Client

from jobs import reset


@pytest.fixture()
def client():
    reset()
    return Client()
