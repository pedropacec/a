from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_session_factory
from app.models import Event
from app.schemas import EventOut

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[EventOut])
def list_events(
    camera_id: int | None = None,
    type: str | None = None,
    severity: str | None = None,
    since: datetime | None = None,
    acknowledged: bool | None = None,
    limit: int = Query(default=100, le=1000),
    session_factory=Depends(get_session_factory),
):
    with session_factory() as session:
        query = session.query(Event).order_by(Event.created_at.desc(), Event.id.desc())
        if camera_id is not None:
            query = query.filter(Event.camera_id == camera_id)
        if type is not None:
            query = query.filter(Event.type == type)
        if severity is not None:
            query = query.filter(Event.severity == severity)
        if since is not None:
            query = query.filter(Event.created_at >= since)
        if acknowledged is not None:
            query = query.filter(Event.acknowledged == acknowledged)
        return query.limit(limit).all()


@router.post("/{event_id}/ack", response_model=EventOut)
def acknowledge(event_id: int, session_factory=Depends(get_session_factory)):
    with session_factory() as session:
        event = session.get(Event, event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        event.acknowledged = True
        session.commit()
        session.refresh(event)
        return event
