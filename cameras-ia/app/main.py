from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api import cameras, events, notifications, system, ws
from app.config import Settings
from app.core.bus import EventBus
from app.core.manager import CameraManager
from app.core.notifier import Notifier
from app.database import init_db
from app.models import Camera, Event

log = logging.getLogger(__name__)

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    engine, session_factory = init_db(settings.db_url)
    bus = EventBus()
    manager = CameraManager(bus)
    notifier = Notifier(session_factory, manager)

    def persist_event(event: dict) -> dict:
        created_at = datetime.fromisoformat(event["created_at"])
        with session_factory() as session:
            row = Event(
                camera_id=event.get("camera_id"),
                camera_name=event.get("camera_name", ""),
                type=event["type"],
                severity=event.get("severity", "info"),
                message=event.get("message", ""),
                details=event.get("details", {}),
                created_at=created_at,
            )
            session.add(row)
            session.commit()
            return {**event, "id": row.id}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await bus.start(persist_event)
        with session_factory() as session:
            enabled = [c.as_dict() for c in session.query(Camera).filter(Camera.enabled).all()]
        manager.start_enabled(enabled)
        await notifier.start()
        log.info("Sentinela IA iniciado — %d câmera(s) ativa(s)", len(enabled))
        yield
        await notifier.stop()
        manager.stop_all()
        await bus.stop()

    app = FastAPI(
        title="Sentinela IA — Gestão de Câmeras",
        description="Gestão de câmeras com análise contínua por IA",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.session_factory = session_factory
    app.state.bus = bus
    app.state.manager = manager
    app.state.notifier = notifier

    app.include_router(cameras.router)
    app.include_router(events.router)
    app.include_router(notifications.router)
    app.include_router(system.router)
    app.include_router(ws.router)

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(WEB_DIR / "index.html")

    return app
