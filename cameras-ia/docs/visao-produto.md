# Visão do produto — Sentinela IA

> Anotações vivas da visão do produto. Atualizar a cada conversa de definição.
> Última atualização: 2026-08-09.

O Sentinela IA é uma plataforma de inteligência de vídeo com **três pilares**,
todos alimentados pela mesma base: câmeras monitoradas continuamente, gravação
indexada e um pipeline de IA em camadas.

---

## Pilar 1 — Produtividade industrial

**Objetivo:** medir, por funcionário e por estação de trabalho: quanto
produziu, tempo ativo, tempo de pausa, ausências, ritmo (tempo de ciclo).

### Métricas (KPIs)

| Métrica | Como a visão computacional mede |
|---|---|
| Presença na estação | Pessoa detectada dentro da zona da estação (YOLO + zonas) |
| Tempo ativo × ocioso | Presente + nível de movimento na zona acima do limiar = ativo |
| Pausas (nº e duração) | Ausência da estação entre dois períodos de presença |
| Unidades produzidas | Contagem de ciclos: objeto cruzando uma linha virtual (esteira, bancada de saída) ou padrão de movimento cíclico na estação |
| Tempo de ciclo | Intervalo entre unidades consecutivas |
| Ranking/tendências | Agregação por turno, dia, semana; comparação entre estações |

### Como identificar QUEM é o funcionário — decisão importante

Três estratégias, da mais simples/segura à mais complexa:

1. **Por estação + escala de turno (recomendada para v1):** a câmera mede a
   ESTAÇÃO; o sistema cruza com a escala ("estação 3, turno da manhã = João").
   Zero biometria, LGPD tranquila, implementação rápida. Limitação: rodízio
   de pessoas na mesma estação precisa ser registrado.
2. **Marcador visual:** colete/capacete com número ou cor, crachá ArUco.
   Identificação direta sem biometria; exige adesão operacional.
3. **Reconhecimento facial:** identifica qualquer um em qualquer lugar, mas é
   dado biométrico sensível na LGPD (exige consentimento explícito, DPO,
   relatório de impacto). Deixar como opção futura, desligada por padrão.

### Implementação na arquitetura atual

- Novos analisadores plugáveis: `presence` (ocupação por zona-estação),
  `activity` (nível de movimento dentro da zona → ativo/ocioso),
  `cycle_count` (cruzamento de linha virtual para contar unidades).
- Nova tabela `observations` (série temporal): a cada N segundos, por
  estação: presente?, nível de atividade, contagens. Eventos são exceções;
  observações são o "filme" contínuo que vira relatório.
- Camada de agregação (job periódico): observações → sessões de trabalho,
  pausas, unidades/hora → relatórios por funcionário/estação/turno.
- Painel: linha do tempo por estação (presença/pausas coloridas), tabela de
  produção do dia, comparativo entre turnos.

---

## Pilar 2 — Vigilância inteligente (anormalidade + trecho da gravação)

**Objetivo:** a IA vigia, ENTENDE a cena, avisa sobre situações anormais e
entrega o trecho exato da gravação para análise humana.

### Fundação: gravação contínua indexada

- Gravação em anel por câmera: segmentos MP4 de 10–15 s via ffmpeg, retenção
  configurável (ex.: 15–30 dias), apagamento automático dos mais antigos.
- Todo evento ganha um **clipe** (pré-alarme 10 s + pós-alarme 20 s) e uma
  miniatura, montados a partir dos segmentos. O alerta aponta direto pro clipe.

### Camadas de entendimento (da mais barata à mais inteligente)

1. **Heurísticas (já implementadas):** movimento, zonas restritas, horário,
   sabotagem, câmera offline. Rodam em CPU, em todo quadro.
2. **Detecção de objetos (YOLO):** pessoa, veículo, EPI (capacete/colete
   ausente), aglomeração, pessoa correndo, queda (via pose). Roda em GPU ou
   em N quadros/s.
3. **VLM — modelo de visão e linguagem (o "entende o que está acontecendo"):**
   quando as camadas 1–2 sinalizam algo, quadros-chave vão para um modelo
   como o Claude com o contexto da câmera ("corredor do bloco B, madrugada,
   local fechado ao público") e voltam com resposta estruturada:
   `{anormal: sim/não, descrição, severidade, ação sugerida}`. A descrição em
   linguagem natural entra no alerta — "duas pessoas forçando a porta do box
   14" em vez de só "movimento detectado".
4. **Linha de base estatística:** o sistema aprende o padrão normal de cada
   câmera por hora/dia da semana (nível de movimento, ocupação) e sinaliza
   desvios — atividade num lugar que nunca tem, porta aberta por tempo
   incomum — mesmo sem regra escrita.

### Fluxo do alerta

evento → clipe extraído → triagem VLM (descrição + severidade) →
notificação (WhatsApp/Telegram/e-mail) com miniatura + link → painel abre o
clipe → operador marca como tratado / falso positivo (vira feedback para
calibrar limiares).

---

## Pilar 3 — Conversa com a IA sobre as gravações (busca forense)

**Objetivo:** "Por volta das 14h sumiu uma ferramenta no setor B — descobre o
que aconteceu." A IA investiga as gravações e responde com achados + clipes.

### Segredo: indexar continuamente, não varrer vídeo na hora da pergunta

Analisar vídeo bruto sob demanda é lento e caro. Em vez disso, o sistema
constrói uma **linha do tempo pesquisável** o tempo todo:

- A cada N segundos por câmera: quadro-chave → (a) legenda curta gerada por
  VLM ("homem de camisa azul empurrando carrinho com caixas"), (b) embedding
  visual (busca semântica), (c) detecções estruturadas (nº de pessoas,
  objetos). Tudo com timestamp + câmera, em banco vetorial/SQLite.
- Os eventos e observações dos pilares 1–2 entram na mesma linha do tempo.

### O agente investigador

Chat no painel, por trás um agente (Claude via API) com ferramentas:

- `buscar_momentos(consulta, janela_de_tempo, cameras)` — busca semântica +
  filtros na linha do tempo
- `listar_eventos(...)` — eventos/observações estruturados
- `obter_clipe(camera, inicio, fim)` — extrai trecho da gravação
- `analisar_clipe(clipe, pergunta)` — VLM examina o trecho em detalhe

O agente planeja: restringe pela dica de horário → busca semântica ("pessoa
carregando ferramenta", "alguém no setor B") → analisa em profundidade só os
candidatos → responde com linha do tempo dos achados e clipes embutidos.

Exemplo de resposta: *"Às 13:52 a furadeira aparece na bancada (câmera 3).
Às 14:07 uma pessoa de colete laranja a pega e sai pelo corredor leste
(clipe 1). Às 14:11 ela entra no almoxarifado (câmera 7, clipe 2). Não há
registro de devolução até agora."*

---

## Arquitetura alvo

```
câmeras ──► workers ──┬─► analisadores tempo real (heurísticas + YOLO) ──► eventos ──► alertas
                      ├─► gravador contínuo (segmentos MP4, retenção) ◄── extração de clipes
                      └─► indexador (legendas VLM + embeddings + detecções)
                                        │
                        linha do tempo pesquisável (SQLite + vetores)
                                        │
              ┌─────────────────────────┼──────────────────────────┐
        relatórios de              alertas com clipe         agente de busca
        produtividade              e descrição               conversacional
```

## Roadmap por fases

| Fase | Entrega | Habilita |
|---|---|---|
| 1 | Gravação contínua + clipes de evento + player no painel | Base dos pilares 2 e 3 |
| 2 | YOLO + rastreamento + analisadores `presence`/`activity`/`cycle_count` + tabela `observations` | Pilar 1 v1 (por estação) |
| 3 | Triagem VLM dos alertas + notificações WhatsApp/Telegram + feedback de falso positivo | Pilar 2 completo |
| 4 | Indexador contínuo (legendas + embeddings) + agente de busca no chat | Pilar 3 |
| 5 | Relatórios avançados, linha de base estatística, pose/EPI, facial opcional | Aprofundamento |

## Custos e hardware — ordem de grandeza

- **Heurísticas:** CPU comum dá conta de dezenas de câmeras.
- **YOLO:** 1 GPU modesta (ex.: RTX 3060) processa ~8–16 câmeras a 5–10 fps;
  alternativa: rodar a 1–2 fps em CPU, ou edge (Jetson/Coral) por câmera.
- **VLM (API):** o custo escala com quadros enviados — por isso a estratégia
  em camadas: VLM só em alertas e na indexação esparsa (ex.: 1 quadro/15 s
  por câmera). Indexação de 10 câmeras ≈ 60 mil quadros/dia — dá para
  calibrar amostragem × custo. Investigações profundas só sob demanda.
- **Armazenamento:** ~1 câmera 1080p a 15 fps ≈ 20–40 GB/dia bruto; usar
  bitrate moderado + retenção por câmera.

## LGPD e privacidade (registrar desde já)

- Avisos visíveis de monitoramento por câmera; base legal documentada
  (legítimo interesse para segurança; para produtividade, transparência com
  os funcionários é obrigatória — política interna assinada).
- **Minimização:** medir estações/zonas em vez de biometria sempre que
  possível; reconhecimento facial só com consentimento explícito (dado
  biométrico sensível) e desligado por padrão.
- Retenção limitada e documentada; acesso ao vídeo com login e trilha de
  auditoria (quem assistiu o quê); clipes compartilhados expiram.

## Questões em aberto (responder para destravar)

1. **Ambiente:** que tipo de indústria/operação? Quantas câmeras e estações
   de trabalho na primeira instalação?
2. **Identificação:** começamos por estação+escala (recomendado) ou já é
   necessário identificar a pessoa diretamente?
3. **Hardware:** existe máquina com GPU no local, ou preferem edge/nuvem?
4. **Alertas:** WhatsApp é o canal principal? Quem recebe?
5. **Retenção:** quantos dias de gravação precisam ficar disponíveis?
