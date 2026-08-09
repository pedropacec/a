from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import numpy as np

SEVERITIES = ("info", "alerta", "critico")


@dataclass
class Finding:
    """Um achado de um analisador em um quadro — vira um evento no sistema."""

    type: str
    severity: str
    message: str
    details: dict = field(default_factory=dict)


@dataclass
class FrameContext:
    """Contexto de um quadro passando pelo pipeline."""

    frame: np.ndarray
    ts: datetime
    camera: dict
    shared: dict = field(default_factory=dict)


class Analyzer:
    name = "base"

    def __init__(self, options: dict | None = None):
        self.options = options or {}
        self._last_emit: dict[str, datetime] = {}

    @classmethod
    def is_available(cls) -> bool:
        return True

    def cooldown_ok(self, now: datetime, key: str = "default") -> bool:
        """Evita rajadas de eventos idênticos: um por período de cooldown."""
        cooldown = float(self.options.get("cooldown", self.DEFAULT_COOLDOWN))
        last = self._last_emit.get(key)
        if last is not None and (now - last).total_seconds() < cooldown:
            return False
        self._last_emit[key] = now
        return True

    DEFAULT_COOLDOWN = 10.0

    def process(self, ctx: FrameContext) -> list[Finding]:
        raise NotImplementedError


REGISTRY: dict[str, type[Analyzer]] = {}


def register(cls: type[Analyzer]) -> type[Analyzer]:
    REGISTRY[cls.name] = cls
    return cls


def create_analyzers(names: list[str], config: dict) -> tuple[list[Analyzer], list[str]]:
    """Instancia os analisadores pedidos; devolve (instâncias, indisponíveis)."""
    instances: list[Analyzer] = []
    missing: list[str] = []
    for name in names:
        cls = REGISTRY.get(name)
        if cls is None or not cls.is_available():
            missing.append(name)
            continue
        instances.append(cls(config.get(name, {})))
    return instances, missing
