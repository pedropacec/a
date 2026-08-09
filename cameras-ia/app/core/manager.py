"""Gerencia o ciclo de vida dos workers de câmera."""
from __future__ import annotations

import logging

from app.analytics import create_analyzers
from app.core.bus import EventBus
from app.core.worker import CameraWorker

log = logging.getLogger(__name__)


class CameraManager:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.workers: dict[int, CameraWorker] = {}

    def start_camera(self, camera: dict) -> None:
        self.stop_camera(camera["id"])
        analyzers, missing = create_analyzers(camera.get("analyzers", []), camera.get("config", {}))
        if missing:
            log.warning(
                "Câmera %s: analisadores indisponíveis ignorados: %s",
                camera["name"],
                ", ".join(missing),
            )
        worker = CameraWorker(camera, analyzers, self.bus.publish)
        self.workers[camera["id"]] = worker
        worker.start()

    def stop_camera(self, camera_id: int) -> None:
        worker = self.workers.pop(camera_id, None)
        if worker is not None:
            worker.stop()
            worker.join(timeout=5)

    def stop_all(self) -> None:
        for camera_id in list(self.workers):
            self.stop_camera(camera_id)

    def is_running(self, camera_id: int) -> bool:
        worker = self.workers.get(camera_id)
        return worker is not None and worker.is_alive()

    def snapshot(self, camera_id: int) -> bytes | None:
        worker = self.workers.get(camera_id)
        return worker.snapshot_jpeg() if worker is not None else None

    def start_enabled(self, cameras: list[dict]) -> None:
        for camera in cameras:
            if camera.get("enabled"):
                self.start_camera(camera)
