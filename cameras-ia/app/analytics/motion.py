"""Detecção de movimento por subtração de fundo (MOG2).

Publica em ctx.shared:
  motion_ratio   — fração da imagem com movimento (0..1)
  motion_boxes   — caixas [x, y, w, h] das regiões em movimento
  motion_active  — True quando o movimento passa do limiar (pós-aquecimento)
"""
from __future__ import annotations

import cv2
import numpy as np

from app.analytics.base import Analyzer, Finding, FrameContext, register


@register
class MotionAnalyzer(Analyzer):
    name = "motion"

    def __init__(self, options: dict | None = None):
        super().__init__(options)
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=int(self.options.get("history", 120)),
            varThreshold=float(self.options.get("var_threshold", 25)),
            detectShadows=False,
        )
        self.warmup = int(self.options.get("warmup", 10))
        self.min_area_ratio = float(self.options.get("min_area_ratio", 0.01))
        self.frames = 0

    def process(self, ctx: FrameContext) -> list[Finding]:
        gray = cv2.cvtColor(ctx.frame, cv2.COLOR_BGR2GRAY)
        mask = self.subtractor.apply(gray)
        self.frames += 1

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)

        ratio = float(cv2.countNonZero(mask)) / mask.size
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_px = self.min_area_ratio * mask.size * 0.25
        boxes = [list(cv2.boundingRect(c)) for c in contours if cv2.contourArea(c) >= min_px]

        active = self.frames > self.warmup and ratio >= self.min_area_ratio
        ctx.shared["motion_ratio"] = ratio
        ctx.shared["motion_boxes"] = boxes
        ctx.shared["motion_active"] = active

        if active and self.cooldown_ok(ctx.ts):
            return [
                Finding(
                    type="movimento",
                    severity="alerta",
                    message=f"Movimento detectado ({ratio:.1%} da imagem)",
                    details={"ratio": round(ratio, 4), "boxes": boxes},
                )
            ]
        return []
