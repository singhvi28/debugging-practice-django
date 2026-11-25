import json

import pytest
from django.test import Client

from events import reset


@pytest.fixture()
def client():
    reset()
    return Client()
