from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    # rtsp://…, http://…, índice de webcam ("0") ou synthetic://motion|static|black
    url: Mapped[str] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    fps: Mapped[float] = mapped_column(Float, default=5.0)
    # nomes dos analisadores ativos, ex.: ["motion", "tamper", "zones", "schedule"]
    analyzers: Mapped[list] = mapped_column(JSON, default=list)
    # opções por analisador, ex.: {"motion": {"min_area_ratio": 0.02}, "zones": {...}}
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "location": self.location,
            "enabled": self.enabled,
            "fps": self.fps,
            "analyzers": list(self.analyzers or []),
            "config": dict(self.config or {}),
        }


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    camera_id: Mapped[int | None] = mapped_column(ForeignKey("cameras.id"), nullable=True)
    camera_name: Mapped[str] = mapped_column(String(120), default="")
    # movimento | intrusao_zona | fora_de_horario | sabotagem_camera |
    # camera_offline | camera_online | pessoa_detectada | objeto_detectado
    type: Mapped[str] = mapped_column(String(50), index=True)
    severity: Mapped[str] = mapped_column(String(20), default="info")  # info | alerta | critico
    message: Mapped[str] = mapped_column(Text, default="")
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
