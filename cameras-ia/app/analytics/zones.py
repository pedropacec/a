"""Intrusão em zonas restritas.

Opções (config["zones"]):
  zones: [{"name": "corredor A", "polygon": [[x, y], ...]}, ...]

Usa as caixas de movimento publicadas pelo analisador "motion" (que deve vir
antes na lista de analisadores da câmera).
"""
from __future__ import annotations

import cv2
import numpy as np

from app.analytics.base import Analyzer, Finding, FrameContext, register


@register
class ZoneIntrusionAnalyzer(Analyzer):
    name = "zones"
    DEFAULT_COOLDOWN = 15.0

    def __init__(self, options: dict | None = None):
        super().__init__(options)
        self.zones = []
        for zone in self.options.get("zones", []):
            polygon = np.array(zone.get("polygon", []), dtype=np.int32)
            if len(polygon) >= 3:
                self.zones.append({"name": zone.get("name", "zona"), "polygon": polygon})

    def process(self, ctx: FrameContext) -> list[Finding]:
        if not self.zones or not ctx.shared.get("motion_active"):
            return []

        findings: list[Finding] = []
        boxes = ctx.shared.get("motion_boxes", [])
        for zone in self.zones:
            hit = None
            for x, y, w, h in boxes:
                center = (float(x + w / 2), float(y + h / 2))
                if cv2.pointPolygonTest(zone["polygon"], center, False) >= 0:
                    hit = [x, y, w, h]
                    break
            if hit and self.cooldown_ok(ctx.ts, zone["name"]):
                findings.append(
                    Finding(
                        type="intrusao_zona",
                        severity="critico",
                        message=f'Movimento na zona restrita "{zone["name"]}"',
                        details={"zona": zone["name"], "box": hit},
                    )
                )
        return findings
