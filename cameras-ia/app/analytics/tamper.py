"""Detecção de sabotagem da câmera.

Dois sinais:
  - blackout: imagem quase toda escura (lente coberta, cabo cortado, luz apagada)
  - defocus:  nitidez muito abaixo da linha de base (lente borrada/spray)
"""
from __future__ import annotations

import cv2

from app.analytics.base import Analyzer, Finding, FrameContext, register


@register
class TamperAnalyzer(Analyzer):
    name = "tamper"
    DEFAULT_COOLDOWN = 30.0

    def __init__(self, options: dict | None = None):
        super().__init__(options)
        self.warmup = int(self.options.get("warmup", 3))
        self.dark_threshold = float(self.options.get("dark_threshold", 12.0))
        self.blur_ratio = float(self.options.get("blur_ratio", 0.1))
        self.frames = 0
        self.baseline_sharpness: float | None = None

    def process(self, ctx: FrameContext) -> list[Finding]:
        self.frames += 1
        if self.frames <= self.warmup:
            return []

        gray = cv2.cvtColor(ctx.frame, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        findings: list[Finding] = []

        if brightness < self.dark_threshold:
            if self.cooldown_ok(ctx.ts, "blackout"):
                findings.append(
                    Finding(
                        type="sabotagem_camera",
                        severity="critico",
                        message="Imagem escura demais — possível lente coberta ou falha de iluminação",
                        details={"modo": "blackout", "brilho": round(brightness, 1)},
                    )
                )
            return findings

        if self.baseline_sharpness is None:
            self.baseline_sharpness = sharpness
        else:
            # média móvel lenta para acompanhar variações normais de cena
            self.baseline_sharpness = 0.98 * self.baseline_sharpness + 0.02 * sharpness

        if (
            self.baseline_sharpness > 30.0
            and sharpness < self.baseline_sharpness * self.blur_ratio
            and self.cooldown_ok(ctx.ts, "defocus")
        ):
            findings.append(
                Finding(
                    type="sabotagem_camera",
                    severity="critico",
                    message="Nitidez caiu bruscamente — possível lente borrada ou desfocada",
                    details={
                        "modo": "defocus",
                        "nitidez": round(sharpness, 1),
                        "linha_base": round(self.baseline_sharpness, 1),
                    },
                )
            )
        return findings
