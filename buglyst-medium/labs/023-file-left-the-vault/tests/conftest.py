import os

import pytest
from django.test import Client

from vault import reset


@pytest.fixture()
def client():
    reset()
    c = Client()
    secret_path = os.path.join(os.path.dirname(__file__), "..", "secret.txt")
    secret_path = os.path.abspath(secret_path)
    with open(secret_path, "w", encoding="utf-8") as fh:
        fh.write("top-secret")
    yield c
    if os.path.exists(secret_path):
        os.remove(secret_path)
