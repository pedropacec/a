"""Detecção de pessoas e objetos com YOLO (opcional).

Requer o pacote `ultralytics` (descomentar em requirements.txt). Sem ele, o
analisador fica indisponível e é ignorado com aviso — o resto do pipeline
continua funcionando normalmente.

Opções (config["objects"]):
  model:           caminho/nome do modelo (padrão "yolov8n.pt")
  every_n_frames:  roda a inferência a cada N quadros (padrão 10)
  confidence:      confiança mínima (padrão 0.5)
  classes:         classes de interesse (padrão ["person"])
"""
from __future__ import annotations

from app.analytics.base import Analyzer, Finding, FrameContext, register

try:
    from ultralytics import YOLO

    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False

_LABELS_PT = {"person": "pessoa", "car": "carro", "truck": "caminhão", "dog": "cachorro"}


@register
class ObjectDetectionAnalyzer(Analyzer):
    name = "objects"
    DEFAULT_COOLDOWN = 15.0

    @classmethod
    def is_available(cls) -> bool:
        return _AVAILABLE

    def __init__(self, options: dict | None = None):
        super().__init__(options)
        self.model = YOLO(self.options.get("model", "yolov8n.pt"))
        self.every = int(self.options.get("every_n_frames", 10))
        self.confidence = float(self.options.get("confidence", 0.5))
        self.classes = set(self.options.get("classes", ["person"]))
        self.frames = 0

    def process(self, ctx: FrameContext) -> list[Finding]:
        self.frames += 1
        if self.frames % self.every != 0:
            return []

        results = self.model.predict(ctx.frame, verbose=False)[0]
        names = results.names
        findings: list[Finding] = []
        for box in results.boxes:
            label = names[int(box.cls)]
            conf = float(box.conf)
            if label not in self.classes or conf < self.confidence:
                continue
            if not self.cooldown_ok(ctx.ts, label):
                continue
            label_pt = _LABELS_PT.get(label, label)
            event_type = "pessoa_detectada" if label == "person" else "objeto_detectado"
            findings.append(
                Finding(
                    type=event_type,
                    severity="alerta",
                    message=f"{label_pt.capitalize()} detectado(a) ({conf:.0%})",
                    details={
                        "classe": label,
                        "confianca": round(conf, 3),
                        "box": [round(v) for v in box.xyxy[0].tolist()],
                    },
                )
            )
        return findings
