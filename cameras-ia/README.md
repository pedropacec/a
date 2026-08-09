# Sentinela IA — Gestão de Câmeras com Análise por Inteligência Artificial

Sistema de monitoramento que assiste cada câmera continuamente e analisa
**cada quadro por várias razões diferentes** — cada "razão" é um analisador
plugável no pipeline de IA. Feito para vigiar instalações como um self
storage: corredores, portaria, docas e áreas restritas.

## O que ele detecta hoje

| Analisador | Evento gerado | O que vigia |
|---|---|---|
| `motion` | `movimento` | Movimento na cena (subtração de fundo MOG2) |
| `zones` | `intrusao_zona` | Movimento dentro de zonas restritas desenhadas por polígono |
| `schedule` | `fora_de_horario` | Qualquer atividade fora do horário de funcionamento |
| `tamper` | `sabotagem_camera` | Lente coberta/escura (blackout) ou borrada (defocus) |
| `objects`* | `pessoa_detectada`, `objeto_detectado` | Pessoas e objetos via YOLO |
| — | `camera_offline` / `camera_online` | Queda e retorno do sinal da câmera |

\* opcional: requer `pip install ultralytics` (descomente em `requirements.txt`).
Sem ele, o analisador é ignorado com aviso e o resto segue funcionando.

Severidades: `info` · `alerta` · `critico`.

## Como rodar

```bash
cd cameras-ia
pip install -r requirements.txt
python run.py            # painel em http://localhost:8000
```

Rodar os testes:

```bash
python -m pytest tests/ -v
```

## Adicionando câmeras

Pelo painel (formulário "Adicionar câmera") ou pela API:

```bash
# Câmera IP real (RTSP) com movimento + sabotagem + horário comercial
curl -X POST localhost:8000/api/cameras -H 'Content-Type: application/json' -d '{
  "name": "Corredor A",
  "url": "rtsp://usuario:senha@192.168.0.10:554/stream1",
  "location": "Bloco 1",
  "fps": 5,
  "analyzers": ["motion", "tamper", "schedule", "zones"],
  "config": {
    "schedule": {"open": "08:00", "close": "18:00", "days": [0,1,2,3,4,5]},
    "zones": {"zones": [{"name": "porta dos fundos",
                          "polygon": [[400,100],[640,100],[640,480],[400,480]]}]}
  }
}'

# Sem câmera à mão? Fonte sintética para demonstração/testes:
curl -X POST localhost:8000/api/cameras -H 'Content-Type: application/json' \
  -d '{"name": "Demo", "url": "synthetic://motion", "analyzers": ["motion"]}'
```

Fontes aceitas: `rtsp://…`, `http(s)://…`, índice de webcam (`"0"`),
caminho de arquivo de vídeo e `synthetic://motion|static|black`.

## API

| Rota | Função |
|---|---|
| `GET/POST /api/cameras` · `GET/PATCH/DELETE /api/cameras/{id}` | Cadastro de câmeras |
| `POST /api/cameras/{id}/start` · `/stop` | Liga/desliga o monitoramento |
| `GET /api/cameras/{id}/snapshot` | Último quadro em JPEG |
| `GET /api/events` (filtros: câmera, tipo, severidade, desde, ack) | Histórico de eventos |
| `POST /api/events/{id}/ack` | Marca evento como tratado |
| `GET /api/status` | Resumo: câmeras online, eventos 24h, analisadores |
| `WS /ws/events` | Eventos ao vivo (alimenta o painel) |
| `GET /docs` | Documentação interativa (Swagger) |

## Arquitetura

```
┌─ câmera 1 ─ CameraWorker (thread) ─┐            ┌─ persiste no SQLite
├─ câmera 2 ─ CameraWorker (thread) ─┼─ EventBus ─┤
└─ câmera N ─ CameraWorker (thread) ─┘            └─ WebSocket → painel
        │
        └─ pipeline por quadro: motion → zones → schedule → tamper → objects
           (analisadores compartilham resultados via ctx.shared —
            ex.: as caixas de movimento alimentam zonas e horário)
```

- `app/analytics/` — analisadores; para criar um novo, herde de `Analyzer`,
  decore com `@register` e implemente `process(ctx)`.
- `app/core/` — fontes de vídeo, workers, barramento de eventos, gerenciador.
- `app/api/` — REST + WebSocket (FastAPI).
- `web/` — painel (uma página, sem build).

Cada worker reconecta sozinho em caso de queda e emite `camera_offline` /
`camera_online`. Cooldown por analisador evita rajadas de eventos repetidos.

## Roadmap

- [ ] Detecção de pessoas/veículos com YOLO ativada por padrão (`objects`)
- [ ] Gravação de clipes dos eventos (pré/pós alarme) e miniaturas
- [ ] Notificações: WhatsApp/Telegram/e-mail em eventos críticos
- [ ] Autenticação e perfis de usuário (operador × administrador)
- [ ] Editor visual de zonas restritas sobre o snapshot no painel
- [ ] Contagem de pessoas, permanência (loitering) e cruzamento de linha
- [ ] Descrição de cena por modelo de visão (VLM) para busca em linguagem natural
