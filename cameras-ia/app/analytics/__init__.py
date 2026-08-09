"""Pipeline de análise de vídeo.

Cada analisador é uma classe registrada no REGISTRY. O worker da câmera roda
os analisadores em sequência sobre cada quadro; eles compartilham resultados
intermediários via ctx.shared (ex.: o detector de movimento publica as caixas
de movimento, que os analisadores de zona e horário reutilizam).
"""
from app.analytics.base import REGISTRY, Analyzer, Finding, FrameContext, create_analyzers
from app.analytics import motion, tamper, zones, schedule, objects  # noqa: F401 — registram-se

__all__ = ["REGISTRY", "Analyzer", "Finding", "FrameContext", "create_analyzers"]
