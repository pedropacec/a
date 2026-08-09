"""Testes de integração da API com câmeras sintéticas."""
import time

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

MOTION_CONFIG = {"motion": {"warmup": 3, "cooldown": 0, "min_area_ratio": 0.001}}


@pytest.fixture()
def client(tmp_path):
    settings = Settings(db_url=f"sqlite:///{tmp_path}/test.db", host="127.0.0.1", port=8000)
    with TestClient(create_app(settings)) as client:
        yield client


def create_camera(client, **overrides):
    payload = {
        "name": "Câmera Teste",
        "url": "synthetic://motion",
        "fps": 30,
        "analyzers": ["motion"],
        "config": MOTION_CONFIG,
        **overrides,
    }
    res = client.post("/api/cameras", json=payload)
    assert res.status_code == 201, res.text
    return res.json()


def wait_for_event(client, event_type, timeout=10.0, **params):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        res = client.get("/api/events", params={"type": event_type, **params})
        assert res.status_code == 200
        events = res.json()
        if events:
            return events
        time.sleep(0.2)
    raise AssertionError(f"Nenhum evento '{event_type}' em {timeout}s")


def test_camera_crud_and_worker_lifecycle(client):
    cam = create_camera(client)
    assert cam["online"] is True

    res = client.get("/api/cameras")
    assert [c["id"] for c in res.json()] == [cam["id"]]

    res = client.patch(f"/api/cameras/{cam['id']}", json={"name": "Portaria"})
    assert res.json()["name"] == "Portaria"
    assert res.json()["online"] is True

    res = client.post(f"/api/cameras/{cam['id']}/stop")
    assert res.json()["online"] is False

    res = client.delete(f"/api/cameras/{cam['id']}")
    assert res.status_code == 204
    assert client.get(f"/api/cameras/{cam['id']}").status_code == 404


def test_motion_events_flow_from_worker_to_api(client):
    cam = create_camera(client)
    events = wait_for_event(client, "movimento", camera_id=cam["id"])
    event = events[0]
    assert event["camera_name"] == "Câmera Teste"
    assert event["severity"] == "alerta"
    assert "ratio" in event["details"]


def test_snapshot_returns_jpeg(client):
    cam = create_camera(client)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        res = client.get(f"/api/cameras/{cam['id']}/snapshot")
        if res.status_code == 200:
            assert res.headers["content-type"] == "image/jpeg"
            assert res.content[:2] == b"\xff\xd8"  # magic number de JPEG
            return
        time.sleep(0.1)
    raise AssertionError("Snapshot não ficou disponível")


def test_event_ack(client):
    cam = create_camera(client)
    events = wait_for_event(client, "movimento", camera_id=cam["id"])
    res = client.post(f"/api/events/{events[0]['id']}/ack")
    assert res.status_code == 200
    assert res.json()["acknowledged"] is True

    res = client.get("/api/events", params={"acknowledged": False})
    assert events[0]["id"] not in [e["id"] for e in res.json()]


def test_status_endpoint(client):
    create_camera(client)
    res = client.get("/api/status")
    assert res.status_code == 200
    body = res.json()
    assert body["cameras_total"] == 1
    assert body["cameras_online"] == 1
    assert "motion" in body["analyzers_available"]


def test_websocket_receives_live_events(client):
    with client.websocket_connect("/ws/events") as ws:
        create_camera(client)
        event = ws.receive_json()
        assert event["type"] in {"movimento"}
        assert event["camera_name"] == "Câmera Teste"
