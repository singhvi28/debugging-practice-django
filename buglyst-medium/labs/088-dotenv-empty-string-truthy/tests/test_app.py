from django.test import Client

from helper import env_flag, maintenance_enabled


def test_unset_maintenance_flag_is_off(monkeypatch):
    monkeypatch.delenv("MAINTENANCE_MODE", raising=False)
    assert maintenance_enabled() is False
    assert env_flag("MAINTENANCE_MODE") is False


def test_explicit_false_is_off(monkeypatch):
    monkeypatch.setenv("MAINTENANCE_MODE", "false")
    assert maintenance_enabled() is False


def test_explicit_true_is_on(monkeypatch):
    monkeypatch.setenv("MAINTENANCE_MODE", "true")
    assert maintenance_enabled() is True


def test_status_endpoint_when_unset(monkeypatch):
    monkeypatch.delenv("MAINTENANCE_MODE", raising=False)
    client = Client()
    assert client.get("/status").json()["maintenance_mode"] is False


def test_work_endpoint_available_when_unset(monkeypatch):
    monkeypatch.delenv("MAINTENANCE_MODE", raising=False)
    client = Client()
    assert client.get("/work").status_code == 200
