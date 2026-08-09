"""Motor de pontos de atenção.

Roda periodicamente sobre os eventos brutos e o estado das câmeras e mantém
a área de notificação do cliente: em vez de 200 eventos de movimento, um
ponto de atenção legível ("3 intrusões na zona restrita nas últimas 24h").

Regras:
  camera_sem_sinal       — último camera_offline sem camera_online depois (auto-resolve)
  monitoramento_parado   — câmera habilitada mas sem worker vivo (auto-resolve)
  sabotagem              — eventos sabotagem_camera na janela (rollup)
  intrusao_recorrente    — eventos intrusao_zona na janela (rollup)
  atividade_fora_horario — eventos fora_de_horario na janela (rollup)
  pico_criticos          — muitos eventos críticos na última hora (global)
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from app.models import Camera, Event, Notification

log = logging.getLogger(__name__)

# (kind, tipo de evento, severidade, título por câmera)
ROLLUP_RULES = [
    ("sabotagem", "sabotagem_camera", "critico", "Possível sabotagem na câmera {name}"),
    ("intrusao_recorrente", "intrusao_zona", "critico", "Intrusão em zona restrita — {name}"),
    ("atividade_fora_horario", "fora_de_horario", "critico", "Atividade fora do horário — {name}"),
]


class Notifier:
    def __init__(self, session_factory, manager, window_hours: float = 24.0,
                 burst_threshold: int = 10):
        self.session_factory = session_factory
        self.manager = manager
        self.window_hours = window_hours
        self.burst_threshold = burst_threshold
        self._stop: asyncio.Event | None = None
        self._task: asyncio.Task | None = None

    # ------------------------------------------------------------ ciclo de vida
    async def start(self, interval: float = 30.0) -> None:
        self._stop = asyncio.Event()
        self._task = asyncio.create_task(self._loop(interval))

    async def stop(self) -> None:
        if self._stop is not None:
            self._stop.set()
        if self._task is not None:
            await self._task
            self._task = None

    async def _loop(self, interval: float) -> None:
        while not self._stop.is_set():
            try:
                await asyncio.to_thread(self.run_once)
            except Exception:
                log.exception("Falha ao avaliar pontos de atenção")
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

    # ------------------------------------------------------------------ regras
    def run_once(self) -> int:
        """Avalia todas as regras; devolve quantas notificações mudaram."""
        now = datetime.now()
        window_start = now - timedelta(hours=self.window_hours)
        changed = 0

        with self.session_factory() as session:
            cameras = session.query(Camera).all()

            for camera in cameras:
                changed += self._check_signal(session, camera, now)
                changed += self._check_worker(session, camera, now)
                for kind, event_type, severity, title in ROLLUP_RULES:
                    count = (
                        session.query(Event)
                        .filter(
                            Event.camera_id == camera.id,
                            Event.type == event_type,
                            Event.created_at >= window_start,
                        )
                        .count()
                    )
                    if count:
                        changed += self._upsert(
                            session,
                            kind=kind,
                            camera=camera,
                            severity=severity,
                            title=title.format(name=camera.name),
                            body=f"{count} ocorrência(s) nas últimas {self.window_hours:.0f}h. "
                                 "Revise os eventos da câmera.",
                            count=count,
                            now=now,
                        )

            burst = (
                session.query(Event)
                .filter(Event.severity == "critico", Event.created_at >= now - timedelta(hours=1))
                .count()
            )
            if burst >= self.burst_threshold:
                changed += self._upsert(
                    session,
                    kind="pico_criticos",
                    camera=None,
                    severity="critico",
                    title="Pico de eventos críticos na última hora",
                    body=f"{burst} eventos críticos na última hora — algo fora do comum "
                         "está acontecendo. Verifique o painel.",
                    count=burst,
                    now=now,
                )

            session.commit()
        return changed

    def _check_signal(self, session, camera: Camera, now: datetime) -> int:
        def last_of(event_type: str):
            return (
                session.query(Event)
                .filter(Event.camera_id == camera.id, Event.type == event_type)
                .order_by(Event.created_at.desc())
                .first()
            )

        last_off = last_of("camera_offline")
        last_on = last_of("camera_online")
        offline = last_off is not None and (
            last_on is None or last_on.created_at < last_off.created_at
        )
        if offline:
            return self._upsert(
                session,
                kind="camera_sem_sinal",
                camera=camera,
                severity="critico",
                title=f"Câmera {camera.name} sem sinal",
                body=f"Sem sinal desde {last_off.created_at:%d/%m %H:%M}. "
                     "Verifique conexão, alimentação e o cabo da câmera.",
                count=1,
                now=now,
            )
        return self._auto_resolve(session, "camera_sem_sinal", camera.id, now)

    def _check_worker(self, session, camera: Camera, now: datetime) -> int:
        if camera.enabled and not self.manager.is_running(camera.id):
            return self._upsert(
                session,
                kind="monitoramento_parado",
                camera=camera,
                severity="alerta",
                title=f"Monitoramento parado — {camera.name}",
                body="A câmera está habilitada mas o monitoramento não está rodando. "
                     "Reinicie a câmera no painel.",
                count=1,
                now=now,
            )
        return self._auto_resolve(session, "monitoramento_parado", camera.id, now)

    # -------------------------------------------------------------- persistência
    def _find_open(self, session, kind: str, camera_id: int | None) -> Notification | None:
        return (
            session.query(Notification)
            .filter(
                Notification.kind == kind,
                Notification.camera_id == camera_id,
                Notification.resolved == False,  # noqa: E712
            )
            .first()
        )

    def _upsert(self, session, *, kind: str, camera: Camera | None, severity: str,
                title: str, body: str, count: int, now: datetime) -> int:
        camera_id = camera.id if camera is not None else None
        existing = self._find_open(session, kind, camera_id)
        if existing is None:
            session.add(
                Notification(
                    kind=kind,
                    severity=severity,
                    title=title,
                    body=body,
                    camera_id=camera_id,
                    camera_name=camera.name if camera is not None else "sistema",
                    count=count,
                    created_at=now,
                    updated_at=now,
                )
            )
            return 1
        if existing.count != count or existing.body != body:
            if count > existing.count:
                existing.read = False  # novas ocorrências reacendem a notificação
            existing.count = count
            existing.body = body
            existing.title = title
            existing.updated_at = now
            return 1
        return 0

    def _auto_resolve(self, session, kind: str, camera_id: int | None, now: datetime) -> int:
        existing = self._find_open(session, kind, camera_id)
        if existing is None:
            return 0
        existing.resolved = True
        existing.updated_at = now
        existing.body += " (Resolvido automaticamente — situação normalizada.)"
        return 1
