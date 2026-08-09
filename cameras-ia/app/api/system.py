from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from app.analytics import REGISTRY
from app.api.deps import get_manager, get_session_factory
from app.models import Camera, Event, Notification
from app.schemas import StatusOut

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/status", response_model=StatusOut)
def status(session_factory=Depends(get_session_factory), manager=Depends(get_manager)):
    with session_factory() as session:
        cameras = session.query(Camera).all()
        cutoff = datetime.now() - timedelta(hours=24)
        recent = session.query(Event).filter(Event.created_at >= cutoff).all()
        unread = (
            session.query(Notification)
            .filter(Notification.resolved == False, Notification.read == False)  # noqa: E712
            .count()
        )

    by_severity: dict[str, int] = {}
    for event in recent:
        by_severity[event.severity] = by_severity.get(event.severity, 0) + 1

    return StatusOut(
        cameras_total=len(cameras),
        cameras_online=sum(1 for c in cameras if manager.is_running(c.id)),
        events_24h={"total": len(recent), **by_severity},
        notifications_unread=unread,
        analyzers_available=[name for name, cls in REGISTRY.items() if cls.is_available()],
    )
