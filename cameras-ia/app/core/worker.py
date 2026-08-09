"""Worker de câmera: uma thread por câmera.

Captura quadros na taxa configurada, roda o pipeline de analisadores e publica
os achados no barramento de eventos. Reconecta sozinho em caso de queda e
sinaliza camera_offline / camera_online.
"""
from __future__ import annotations

import logging
import threading
import time
from datetime import datetime

import cv2
import numpy as np

from app.analytics import Analyzer, FrameContext
from app.core.sources import open_source

log = logging.getLogger(__name__)

MAX_FAILURES = 30  # leituras falhas consecutivas antes de marcar offline
RECONNECT_DELAY = 5.0


class CameraWorker(threading.Thread):
    def __init__(self, camera: dict, analyzers: list[Analyzer], publish):
        super().__init__(daemon=True, name=f"camera-{camera['id']}")
        self.camera = camera
        self.analyzers = analyzers
        self.publish = publish
        self._stop_event = threading.Event()
        self._frame_lock = threading.Lock()
        self._latest_frame: np.ndarray | None = None
        self._latest_ts: datetime | None = None

    # ------------------------------------------------------------- controle
    def stop(self) -> None:
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def snapshot_jpeg(self) -> bytes | None:
        with self._frame_lock:
            frame = None if self._latest_frame is None else self._latest_frame.copy()
        if frame is None:
            return None
        ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return buffer.tobytes() if ok else None

    # ---------------------------------------------------------------- loop
    def _emit(self, type_: str, severity: str, message: str, details: dict | None = None) -> None:
        self.publish(
            {
                "camera_id": self.camera["id"],
                "camera_name": self.camera["name"],
                "type": type_,
                "severity": severity,
                "message": message,
                "details": details or {},
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

    def run(self) -> None:
        interval = 1.0 / float(self.camera.get("fps") or 5.0)
        source = open_source(self.camera["url"])
        failures = 0
        offline = False

        try:
            while not self._stop_event.is_set():
                started = time.monotonic()
                ok, frame = source.read()

                if not ok or frame is None:
                    failures += 1
                    if failures >= MAX_FAILURES and not offline:
                        offline = True
                        self._emit(
                            "camera_offline",
                            "critico",
                            "Câmera sem sinal — verifique conexão e alimentação",
                        )
                    if failures >= MAX_FAILURES:
                        source.release()
                        if self._stop_event.wait(RECONNECT_DELAY):
                            break
                        source = open_source(self.camera["url"])
                        failures = 0
                    continue

                if offline:
                    offline = False
                    self._emit("camera_online", "info", "Câmera voltou a transmitir")
                failures = 0

                now = datetime.now()
                with self._frame_lock:
                    self._latest_frame = frame
                    self._latest_ts = now

                ctx = FrameContext(frame=frame, ts=now, camera=self.camera)
                for analyzer in self.analyzers:
                    try:
                        for finding in analyzer.process(ctx):
                            self._emit(
                                finding.type, finding.severity, finding.message, finding.details
                            )
                    except Exception:
                        log.exception(
                            "Analisador %s falhou na câmera %s",
                            analyzer.name,
                            self.camera["name"],
                        )

                elapsed = time.monotonic() - started
                if elapsed < interval:
                    self._stop_event.wait(interval - elapsed)
        finally:
            source.release()
