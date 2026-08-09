from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.api.deps import get_session_factory
from app.models import Notification
from app.schemas import NotificationOut, NotificationSummary

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationOut])
def list_notifications(
    resolved: bool | None = False,
    read: bool | None = None,
    severity: str | None = None,
    limit: int = Query(default=50, le=500),
    session_factory=Depends(get_session_factory),
):
    with session_factory() as session:
        query = session.query(Notification).order_by(
            Notification.updated_at.desc(), Notification.id.desc()
        )
        if resolved is not None:
            query = query.filter(Notification.resolved == resolved)
        if read is not None:
            query = query.filter(Notification.read == read)
        if severity is not None:
            query = query.filter(Notification.severity == severity)
        return query.limit(limit).all()


@router.get("/summary", response_model=NotificationSummary)
def summary(session_factory=Depends(get_session_factory)):
    with session_factory() as session:
        open_items = session.query(Notification).filter(Notification.resolved == False).all()  # noqa: E712
    by_severity: dict[str, int] = {}
    for item in open_items:
        by_severity[item.severity] = by_severity.get(item.severity, 0) + 1
    return NotificationSummary(
        unread=sum(1 for n in open_items if not n.read),
        open=len(open_items),
        by_severity=by_severity,
    )


@router.post("/refresh", response_model=NotificationSummary)
def refresh(request: Request, session_factory=Depends(get_session_factory)):
    """Reavalia as regras agora (o motor também roda sozinho periodicamente)."""
    request.app.state.notifier.run_once()
    return summary(session_factory)


def _get_or_404(session, notification_id: int) -> Notification:
    notification = session.get(Notification, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
    return notification


@router.post("/read-all", response_model=NotificationSummary)
def read_all(session_factory=Depends(get_session_factory)):
    with session_factory() as session:
        session.query(Notification).filter(Notification.read == False).update(  # noqa: E712
            {Notification.read: True}
        )
        session.commit()
    return summary(session_factory)


@router.post("/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, session_factory=Depends(get_session_factory)):
    with session_factory() as session:
        notification = _get_or_404(session, notification_id)
        notification.read = True
        session.commit()
        session.refresh(notification)
        return notification


@router.post("/{notification_id}/resolve", response_model=NotificationOut)
def resolve(notification_id: int, session_factory=Depends(get_session_factory)):
    with session_factory() as session:
        notification = _get_or_404(session, notification_id)
        notification.resolved = True
        notification.read = True
        session.commit()
        session.refresh(notification)
        return notification
