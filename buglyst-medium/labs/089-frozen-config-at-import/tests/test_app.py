from django.test import Client

from helper import feature_beta_enabled


def test_feature_disabled_by_default(monkeypatch):
    monkeypatch.delenv("FEATURE_BETA", raising=False)
    assert feature_beta_enabled() is False


def test_feature_enabled_when_env_set(monkeypatch):
    monkeypatch.setenv("FEATURE_BETA", "on")
    assert feature_beta_enabled() is True


def test_features_endpoint_reflects_runtime_env(monkeypatch):
    monkeypatch.setenv("FEATURE_BETA", "on")
    client = Client()
    assert client.get("/features").json()["feature_beta"] is True


def test_beta_endpoint_available_when_enabled(monkeypatch):
    monkeypatch.setenv("FEATURE_BETA", "on")
    client = Client()
    response = client.get("/beta")
    assert response.status_code == 200
    assert response.json()["enabled"] is True
