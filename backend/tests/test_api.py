import os

import pytest

from backend.app import create_app


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    os.environ["SKIP_MODEL_LOAD"] = "true"
    app = create_app("testing")
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    payload = response.get_json()

    assert response.status_code in {200, 503}
    assert payload["success"] is True
    assert "data" in payload
    assert "timestamp" in payload


def test_ping_endpoint(client):
    response = client.get("/api/v1/ping")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["message"] == "pong"


def test_diagnosis_validation(client):
    response = client.post("/api/v1/diagnosis/predict", json={})
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["success"] is False
    assert payload["message"]
