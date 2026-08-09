"""Barramento de eventos.

Os workers (threads) publicam eventos com publish(); uma tarefa assíncrona os
drena, persiste no banco e repassa aos assinantes (conexões WebSocket).
"""
from __future__ import annotations

import asyncio
import logging
import queue
from typing import Callable

log = logging.getLogger(__name__)

_SENTINEL = object()


class EventBus:
    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue()
        self._subscribers: set[asyncio.Queue] = set()
        self._task: asyncio.Task | None = None

    def publish(self, event: dict) -> None:
        """Seguro para chamar de qualquer thread."""
        self._queue.put(event)

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=200)
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._subscribers.discard(q)

    async def start(self, persist: Callable[[dict], dict]) -> None:
        self._task = asyncio.create_task(self._run(persist))

    async def stop(self) -> None:
        self._queue.put(_SENTINEL)
        if self._task is not None:
            await self._task
            self._task = None

    async def _run(self, persist: Callable[[dict], dict]) -> None:
        while True:
            event = await asyncio.to_thread(self._queue.get)
            if event is _SENTINEL:
                break
            try:
                event = persist(event) or event
            except Exception:
                log.exception("Falha ao persistir evento: %s", event.get("type"))
            for q in list(self._subscribers):
                try:
                    q.put_nowait(event)
                except asyncio.QueueFull:
                    pass
