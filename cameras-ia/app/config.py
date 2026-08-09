"""Configuração do sistema, lida de variáveis de ambiente.

Variáveis suportadas (todas opcionais):
  CAMIA_DB    — URL do banco (padrão: sqlite em ./data/sentinela.db)
  CAMIA_HOST  — host do servidor (padrão 0.0.0.0)
  CAMIA_PORT  — porta do servidor (padrão 8000)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    db_url: str
    host: str
    port: int

    @classmethod
    def from_env(cls) -> "Settings":
        default_db = f"sqlite:///{BASE_DIR / 'data' / 'sentinela.db'}"
        db_url = os.environ.get("CAMIA_DB", default_db)
        if db_url.startswith("sqlite:///"):
            Path(db_url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
        return cls(
            db_url=db_url,
            host=os.environ.get("CAMIA_HOST", "0.0.0.0"),
            port=int(os.environ.get("CAMIA_PORT", "8000")),
        )
