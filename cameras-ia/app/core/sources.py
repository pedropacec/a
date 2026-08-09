"""Fontes de vídeo.

Suporta:
  - rtsp:// e http(s)://  — câmeras IP/DVR/NVR via OpenCV
  - "0", "1", …           — webcams locais
  - caminho de arquivo    — vídeo gravado
  - synthetic://motion|static|black — fontes sintéticas para testes e demonstração
"""
from __future__ import annotations

import cv2
import numpy as np


class SyntheticSource:
    """Gera quadros artificiais — permite rodar e testar sem câmera real."""

    def __init__(self, mode: str = "motion", width: int = 320, height: int = 240):
        self.mode = mode
        self.width = width
        self.height = height
        self.i = 0
        gradient = np.linspace(40, 120, width, dtype=np.uint8)
        self._background = np.dstack([np.tile(gradient, (height, 1))] * 3)

    def isOpened(self) -> bool:  # noqa: N802 — espelha a interface do OpenCV
        return True

    def read(self):
        if self.mode == "black":
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        else:
            frame = self._background.copy()
            if self.mode == "motion":
                size = 40
                x = (self.i * 9) % (self.width - size)
                y = (self.height - size) // 2
                cv2.rectangle(frame, (x, y), (x + size, y + size), (255, 255, 255), -1)
        self.i += 1
        return True, frame

    def release(self) -> None:
        pass


def open_source(url: str):
    if url.startswith("synthetic://"):
        return SyntheticSource(mode=url.removeprefix("synthetic://") or "static")
    if url.isdigit():
        return cv2.VideoCapture(int(url))
    return cv2.VideoCapture(url)
