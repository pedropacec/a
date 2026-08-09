"""Testes da área de notificação (pontos de atenção)."""
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.models import Event


@pytest.fixture()
def app_and_client(tmp_path):
    settings = Settings(db_url=f"sqlite:///{tmp_path}/test.db", host="127.0.0.1", port=8000)
    app = create_app(settings)
    with TestClient(app) as client:
        yield app, client


def seed_event(app, type_, severity="critico", camera_id=None, camera_name="Portaria",
               minutes_ago=5):
    with app.state.session_factory() as session:
        session.add(
            Event(
                camera_id=camera_id,
                camera_name=camera_name,
                type=type_,
                severity=severity,
                message="teste",
                created_at=datetime.now() - timedelta(minutes=minutes_ago),
            )
        )
        session.commit()


def create_camera(client, **overrides):
    payload = {
        "name": "Portaria",
        "url": "synthetic://static",
        "analyzers": [],
        **overrides,
    }
    res = client.post("/api/cameras", json=payload)
    assert res.status_code == 201
    return res.json()


def open_notices(client, **params):
    res = client.get("/api/notifications", params=params)
    assert res.status_code == 200
    return res.json()


def test_offline_creates_and_autoresolves(app_and_client):
    app, client = app_and_client
    cam = create_camera(client)

    seed_event(app, "camera_offline", camera_id=cam["id"])
    app.state.notifier.run_once()
    notices = open_notices(client)
    kinds = [n["kind"] for n in notices]
    assert "camera_sem_sinal" in kinds

    # rodar de novo não duplica
    app.state.notifier.run_once()
    assert len([n for n in open_notices(client) if n["kind"] == "camera_sem_sinal"]) == 1

    # câmera volta → auto-resolve
    seed_event(app, "camera_online", severity="info", camera_id=cam["id"], minutes_ago=1)
    app.state.notifier.run_once()
    assert not [n for n in open_notices(client) if n["kind"] == "camera_sem_sinal"]


def test_worker_stopped_notice(app_and_client):
    app, client = app_and_client
    cam = create_camera(client)
    app.state.manager.stop_camera(cam["id"])  # habilitada no banco, worker morto

    app.state.notifier.run_once()
    assert [n for n in open_notices(client) if n["kind"] == "monitoramento_parado"]

    # religa → auto-resolve
    client.post(f"/api/cameras/{cam['id']}/start")
    app.state.notifier.run_once()
    assert not [n for n in open_notices(client) if n["kind"] == "monitoramento_parado"]


def test_rollup_updates_count_and_reawakens(app_and_client):
    app, client = app_and_client
    cam = create_camera(client)

    seed_event(app, "intrusao_zona", camera_id=cam["id"])
    app.state.notifier.run_once()
    notice = [n for n in open_notices(client) if n["kind"] == "intrusao_recorrente"][0]
    assert notice["count"] == 1

    client.post(f"/api/notifications/{notice['id']}/read")

    seed_event(app, "intrusao_zona", camera_id=cam["id"])
    seed_event(app, "intrusao_zona", camera_id=cam["id"])
    app.state.notifier.run_once()
    updated = [n for n in open_notices(client) if n["kind"] == "intrusao_recorrente"][0]
    assert updated["id"] == notice["id"]  # mesmo registro (rollup)
    assert updated["count"] == 3
    assert updated["read"] is False  # novas ocorrências reacendem


def test_burst_rule(app_and_client):
    app, client = app_and_client
    for _ in range(10):
        seed_event(app, "movimento", severity="critico")
    app.state.notifier.run_once()
    assert [n for n in open_notices(client) if n["kind"] == "pico_criticos"]


def test_resolve_read_summary_and_status(app_and_client):
    app, client = app_and_client
    cam = create_camera(client)
    seed_event(app, "sabotagem_camera", camera_id=cam["id"])
    app.state.notifier.run_once()

    summary = client.get("/api/notifications/summary").json()
    assert summary["unread"] >= 1 and summary["open"] >= 1
    assert summary["by_severity"].get("critico", 0) >= 1

    status = client.get("/api/status").json()
    assert status["notifications_unread"] == summary["unread"]

    client.post("/api/notifications/read-all")
    assert client.get("/api/notifications/summary").json()["unread"] == 0

    notice = [n for n in open_notices(client) if n["kind"] == "sabotagem"][0]
    res = client.post(f"/api/notifications/{notice['id']}/resolve")
    assert res.json()["resolved"] is True
    assert not [n for n in open_notices(client) if n["kind"] == "sabotagem"]


def test_refresh_endpoint(app_and_client):
    app, client = app_and_client
    cam = create_camera(client)
    seed_event(app, "fora_de_horario", camera_id=cam["id"])
    res = client.post("/api/notifications/refresh")
    assert res.status_code == 200
    assert [n for n in open_notices(client) if n["kind"] == "atividade_fora_horario"]
