from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CameraCreate(BaseModel):
    name: str
    url: str
    location: str | None = None
    enabled: bool = True
    fps: float = Field(default=5.0, gt=0, le=60)
    analyzers: list[str] = Field(default_factory=lambda: ["motion", "tamper"])
    config: dict = Field(default_factory=dict)


class CameraUpdate(BaseModel):
    name: str | None = None
    url: str | None = None
    location: str | None = None
    enabled: bool | None = None
    fps: float | None = Field(default=None, gt=0, le=60)
    analyzers: list[str] | None = None
    config: dict | None = None


class CameraOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    location: str | None
    enabled: bool
    fps: float
    analyzers: list[str]
    config: dict
    created_at: datetime
    online: bool = False


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    camera_id: int | None
    camera_name: str
    type: str
    severity: str
    message: str
    details: dict
    acknowledged: bool
    created_at: datetime


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    severity: str
    title: str
    body: str
    camera_id: int | None
    camera_name: str
    details: dict
    count: int
    read: bool
    resolved: bool
    created_at: datetime
    updated_at: datetime


class NotificationSummary(BaseModel):
    unread: int
    open: int  # não resolvidas
    by_severity: dict


class StatusOut(BaseModel):
    cameras_total: int
    cameras_online: int
    events_24h: dict
    notifications_unread: int
    analyzers_available: list[str]
