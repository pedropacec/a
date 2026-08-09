"""Atividade fora do horário de funcionamento.

Opções (config["schedule"]):
  open:  "08:00"  — abertura
  close: "18:00"  — fechamento (se menor que open, o expediente vira a noite)
  days:  [0..6]   — dias em que o local funciona (0 = segunda)

Qualquer movimento fora desse período gera um evento crítico.
"""
from __future__ import annotations

from datetime import datetime, time

from app.analytics.base import Analyzer, Finding, FrameContext, register


def _parse(value: str, fallback: time) -> time:
    try:
        hour, minute = value.split(":")
        return time(int(hour), int(minute))
    except (ValueError, AttributeError):
        return fallback


@register
class AfterHoursAnalyzer(Analyzer):
    name = "schedule"
    DEFAULT_COOLDOWN = 30.0

    def __init__(self, options: dict | None = None):
        super().__init__(options)
        self.open = _parse(self.options.get("open", "08:00"), time(8, 0))
        self.close = _parse(self.options.get("close", "18:00"), time(18, 0))
        self.days = list(self.options.get("days", [0, 1, 2, 3, 4, 5]))

    def is_open(self, now: datetime) -> bool:
        if now.weekday() not in self.days:
            return False
        current = now.time()
        if self.open <= self.close:
            return self.open <= current < self.close
        return current >= self.open or current < self.close  # expediente noturno

    def process(self, ctx: FrameContext) -> list[Finding]:
        if not ctx.shared.get("motion_active") or self.is_open(ctx.ts):
            return []
        if not self.cooldown_ok(ctx.ts):
            return []
        return [
            Finding(
                type="fora_de_horario",
                severity="critico",
                message="Atividade detectada fora do horário de funcionamento",
                details={
                    "horario": ctx.ts.strftime("%H:%M"),
                    "expediente": f"{self.open:%H:%M}–{self.close:%H:%M}",
                },
            )
        ]
