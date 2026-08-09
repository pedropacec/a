"""Testes unitários dos analisadores, usando fontes sintéticas (sem câmera real)."""
from datetime import datetime

from app.analytics.motion import MotionAnalyzer
from app.analytics.schedule import AfterHoursAnalyzer
from app.analytics.tamper import TamperAnalyzer
from app.analytics.zones import ZoneIntrusionAnalyzer
from app.analytics.base import FrameContext
from app.core.sources import SyntheticSource

CAMERA = {"id": 1, "name": "teste", "url": "synthetic://motion"}


def run_frames(source, analyzers, n, shared_chain=True):
    """Roda n quadros pelo pipeline e devolve todos os achados."""
    findings = []
    for _ in range(n):
        _, frame = source.read()
        ctx = FrameContext(frame=frame, ts=datetime.now(), camera=CAMERA)
        for analyzer in analyzers:
            findings.extend(analyzer.process(ctx))
    return findings


def test_motion_detects_moving_object():
    analyzer = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    findings = run_frames(SyntheticSource("motion"), [analyzer], 30)
    assert any(f.type == "movimento" for f in findings)


def test_motion_quiet_on_static_scene():
    analyzer = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    findings = run_frames(SyntheticSource("static"), [analyzer], 30)
    assert not findings


def test_tamper_detects_blackout():
    analyzer = TamperAnalyzer({"warmup": 2, "cooldown": 0})
    findings = run_frames(SyntheticSource("black"), [analyzer], 10)
    blackouts = [f for f in findings if f.type == "sabotagem_camera"]
    assert blackouts and blackouts[0].details["modo"] == "blackout"


def test_tamper_quiet_on_normal_scene():
    analyzer = TamperAnalyzer({"warmup": 2, "cooldown": 0})
    findings = run_frames(SyntheticSource("motion"), [analyzer], 20)
    assert not findings


def test_zone_intrusion_fires_when_motion_crosses_zone():
    motion = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    # zona cobrindo o quadro inteiro (320x240) — o retângulo em movimento cruza
    zones = ZoneIntrusionAnalyzer(
        {"cooldown": 0, "zones": [{"name": "área restrita", "polygon": [[0, 0], [320, 0], [320, 240], [0, 240]]}]}
    )
    findings = run_frames(SyntheticSource("motion"), [motion, zones], 30)
    assert any(f.type == "intrusao_zona" for f in findings)


def test_zone_quiet_outside_polygon():
    motion = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    # zona minúscula no canto — o movimento passa pelo centro, longe dela
    zones = ZoneIntrusionAnalyzer(
        {"cooldown": 0, "zones": [{"name": "canto", "polygon": [[0, 0], [5, 0], [5, 5], [0, 5]]}]}
    )
    findings = run_frames(SyntheticSource("motion"), [motion, zones], 30)
    assert not any(f.type == "intrusao_zona" for f in findings)


def test_after_hours_fires_when_closed():
    motion = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    schedule = AfterHoursAnalyzer({"cooldown": 0, "days": []})  # nunca aberto
    findings = run_frames(SyntheticSource("motion"), [motion, schedule], 30)
    assert any(f.type == "fora_de_horario" for f in findings)


def test_after_hours_quiet_when_open():
    motion = MotionAnalyzer({"warmup": 5, "cooldown": 0, "min_area_ratio": 0.001})
    schedule = AfterHoursAnalyzer(
        {"cooldown": 0, "open": "00:00", "close": "23:59", "days": [0, 1, 2, 3, 4, 5, 6]}
    )
    findings = run_frames(SyntheticSource("motion"), [motion, schedule], 30)
    assert not any(f.type == "fora_de_horario" for f in findings)


def test_overnight_schedule():
    analyzer = AfterHoursAnalyzer({"open": "22:00", "close": "06:00", "days": [0, 1, 2, 3, 4, 5, 6]})
    assert analyzer.is_open(datetime(2026, 8, 3, 23, 30))
    assert analyzer.is_open(datetime(2026, 8, 3, 5, 0))
    assert not analyzer.is_open(datetime(2026, 8, 3, 12, 0))
