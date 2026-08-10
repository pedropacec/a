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

## Área de notificação (pontos de atenção)

Acima dos eventos brutos, um motor de regras (`app/core/notifier.py`) roda a
cada 30 s e mantém **pontos de atenção** legíveis para o cliente — com
agregação (rollup), releitura automática quando há novas ocorrências e
auto-resolução quando a situação normaliza:

| Ponto de atenção | Regra |
|---|---|
| `camera_sem_sinal` | Câmera caiu e não voltou (auto-resolve quando volta) |
| `monitoramento_parado` | Câmera habilitada mas worker morto (auto-resolve) |
| `sabotagem` | Eventos de sabotagem nas últimas 24h (agregado) |
| `intrusao_recorrente` | Intrusões em zona restrita nas últimas 24h (agregado) |
| `atividade_fora_horario` | Atividade fora do expediente nas últimas 24h (agregado) |
| `pico_criticos` | 10+ eventos críticos na última hora (global) |

No painel: card "Pontos de atenção" com contador no topo, ações de marcar
lida e resolver.

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
| `GET /api/notifications` · `/summary` · `POST …/refresh` | Pontos de atenção (área de notificação) |
| `POST /api/notifications/{id}/read` · `/resolve` · `/read-all` | Gestão dos pontos de atenção |
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

A visão completa do produto — os três pilares (produtividade industrial,
vigilância inteligente com clipes e busca conversacional nas gravações),
arquitetura alvo, fases, custos e LGPD — está em
[`docs/visao-produto.md`](docs/visao-produto.md). A estratégia de negócio
(posicionamento, edge+nuvem, modelo de assinatura, canal de integradores,
etapas até virar empresa) está em
[`docs/estrategia-empresa.md`](docs/estrategia-empresa.md). A pesquisa de
mercado (Brasil + global) está em
[`docs/pesquisa-mercado.md`](docs/pesquisa-mercado.md), e o estudo
funcional dos concorrentes com os adendos de escopo priorizados (roadmap
revisado em 6 fases) em [`docs/adendos-escopo.md`](docs/adendos-escopo.md).

- [ ] **Fase 1** — Gravação contínua + clipes de evento + player no painel
- [ ] **Fase 2** — YOLO + rastreamento + `presence`/`activity`/`cycle_count` (produtividade v1)
- [ ] **Fase 3** — Triagem VLM dos alertas + notificações WhatsApp/Telegram
- [ ] **Fase 4** — Indexação semântica das gravações + agente de busca conversacional
- [ ] **Fase 5** — Relatórios avançados, linha de base estatística, pose/EPI, autenticação
