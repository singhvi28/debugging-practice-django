import pytest
from django.test import Client

from config import load_config, reset


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    reset()
    load_config()
    return Client()
