# Adendos ao escopo — estudo aprofundado dos concorrentes

> Derivado do inventário funcional de 27 produtos (3 frentes de pesquisa,
> ~80 buscas, 09/08/2026): startups AI-first (Spot AI, Coram, Lumana,
> Ambient.ai, Hakimo, Camio, Conntour, Vaidio, Solink, icetana),
> incumbentes (Verkada, Rhombus, Eagle Eye, Genetec, Milestone/BriefCam,
> Avigilon), brasileiros (Digifort, Intelbras Defense IA, Monuv, Noleak,
> Camerite, Segware, Gabriel) e industriais/EHS (PowerArena, Invisible AI,
> Retrocausal, Dori, Tulip Vision, Arvist, Drishti-legado, Voxel,
> Intenseye, Protex, viAct).
>
> Legenda: **[TS]** = table-stakes (cliente espera; sem isso perde RFP/demo)
> · **[DIF]** = diferencial (poucos têm; vale copiar ou superar).

## As três maiores lacunas estruturais do nosso escopo

1. **O alerta é o começo do trabalho, não o fim.** Todos os líderes tratam
   a detecção como gatilho de um FLUXO DE OPERADOR (triagem → verificação
   → ação → escalonamento → registro). Nosso escopo termina no alerta.
2. **Higiene de plataforma.** Health monitoring, app mobile, RBAC,
   auditoria e API/webhooks aparecem em TODO RFP. Não são diferenciais —
   são o ingresso.
3. **Detectores nomeados que o cliente pergunta na primeira demo:** LPR,
   contagem/ocupação, EPI, loitering. Nosso YOLO genérico não responde
   "vocês têm LPR?".

---

## A. Higiene de plataforma [TS, quase tudo]

| Adendo | Referência |
|---|---|
| Health monitoring GERENCIAL: câmera offline/degradada/virada/desfocada, HD do gravador, com histórico, relatório para o cliente e falha virando evento tratável | Genetec KiwiVision CIM, Sigma Image, Lumana |
| App mobile (iOS/Android): push, ao vivo, playback, compartilhar clipe | Todos |
| RBAC granular (papéis por câmera/site/função) + trilha de auditoria (quem viu/exportou o quê) | Todos os enterprise |
| API pública + webhooks entrada/saída documentados | Camio, Lumana, Monuv |
| Canais de alerta: e-mail, SMS, push, Slack/Teams e **ligação de voz com override de "Não Perturbe"** [DIF barato] | Coram, Camio |
| Retenção configurável por câmera (7d–5 anos) como eixo comercial | Eagle Eye, Verkada |
| Failover de gravação + buffer local com re-upload após queda de link | Digifort, Eagle Eye, Genetec |
| Exportação com valor probatório: assinatura digital + marca d'água (operador/data/câmera) + senha + player standalone | Genetec (EdDSA), Milestone |
| Máscaras de privacidade por câmera | Todos os VMS |

## B. Detectores a adicionar

| Adendo | Classe | Referência |
|---|---|---|
| **LPR** + listas de placas/veículo de interesse (e, depois, integração com órgãos: HELIOS/DETECTA) | [TS] no BR | Todos; Intelbras integra com polícia |
| Contagem de pessoas/veículos, ocupação, superlotação, filas, dwell time, heatmap | [TS] | Verkada, Vaidio, BriefCam, Digifort |
| Loitering como detector nomeado | [TS] | Quase todos |
| EPI (capacete/colete/máscara) | [TS] no industrial | Spot AI, Lumana, Vaidio, Avigilon |
| Objetos abandonados/removidos; tailgating | [TS] avançado | Digifort, Eagle Eye, BriefCam |
| Anomalia self-learning por câmera (aprende o "normal", alerta o desvio, sem regras) | [DIF] — já era nossa "linha de base"; virou prioridade | icetana (núcleo), Noleak Agatha, Avigilon UMD |
| Queda de pessoa; arma; fumaça/fogo | [DIF] | Coram, Hakimo, Vaidio |
| Analítico de áudio (vidro, distúrbio, disparo) | [DIF] | Avigilon, Vaidio |

## C. Fluxo de operador e ciclo da ocorrência (maior lacuna)

| Adendo | Classe | Referência |
|---|---|---|
| Fila de triagem/livewall: console de verificação de alto volume, priorizado por IA (nossa "área de notificação" é o embrião) | [TS] p/ operação | icetana Triage Agent, Avigilon Focus of Attention, Solink VerifEye |
| Verificação por vídeo em 1 clique: evento → pop-up com pré/pós-alarme + ao vivo | [TS] | Sigma Image Monitoring, Verkada |
| Ciclo de tratativa com estados (não atendido → em espera → deslocamento → viatura no local → observação) + procedimento por tipo de evento | [TS] p/ centrais BR | Segware Sigma (padrão canônico) |
| Talk-down por alto-falante (ao vivo/gravado; automático ou pós-verificação) + dissuasão (sirene/luz) | [DIF] forte | Hakimo (120 dB em 5 s), Verkada, Lumana |
| Ações físicas automatizadas (lockdown, desligar equipamento) | [DIF] | Lumana, Spot AI Iris, Ambient |
| Escalonamento estruturado (cadeia de contato → ligação → despacho → 190/911) + app tático de viatura com baixa em campo | [TS] p/ pronta-resposta | Coram, Segware VTR Mobile |
| **Ronda virtual programada** (verificações preventivas em horários fixos/aleatórios com relatório) | [TS] p/ centrais BR | Segware, Seventh |
| Gestão de casos: dossiê com clipes + anotações + arquivos, compartilhamento externo seguro (polícia), status até fechamento | [DIF] | Spot AI Cases (benchmark), Genetec Clearance |
| Registro/auditoria de ações do operador + KPIs de SOC (tempo de resposta, volume) | [TS] enterprise | Ambient, Sigma |
| Tratamento automatizado de eventos de rotina (falta de energia, falha de comunicação auto-fechadas por regra) | [TS] p/ centrais | Sigma |

## D. Integração com o ecossistema brasileiro (go-to-market)

1. **[TS absoluto] Conector de centrais**: cada detecção nossa vira evento
   na fila do **Sigma** (e Moni, D-Guard, Commbox, Gear) com clipe/imagem
   acoplados — o modelo exato da Monuv. Sem isso, central não compra.
2. **[TS] Botão de pânico** no app do cliente final virando evento.
3. **[TS] App white label** para a central oferecer ao cliente dela.
4. **[TS] Gravação por evento atrelada à tratativa** (grava da recepção da
   ocorrência ao fechamento — economiza banda/disco da central).
5. **[DIF/modelo de negócio] Monitoramento como serviço** (humano+IA 24/7,
   estilo Hakimo/Verkada) — possível linha de receita futura, não v1.

## E. Investigação forense (além da busca conversacional)

| Adendo | Classe | Referência |
|---|---|---|
| Busca estruturada por atributos combináveis (pessoa+roupa+objeto+veículo) como UX complementar ao chat | [TS] emergente | Lumana, Ambient, Avigilon Appearance Search |
| Re-identificação NÃO-biométrica entre câmeras com timeline (journey) | [DIF] | Coram Journey Path, Ambient (postura sem-facial igual à nossa) |
| **Qualquer busca vira alerta permanente com 1 clique** | [DIF] barato e de alto valor | Camio, Conntour |
| Extração de dados estruturados por pergunta ("quantas picapes entraram ontem?") | [DIF] | Conntour — encaixa direto no nosso agente |
| Análise de arquivo de vídeo enviado (upload forense), não só streams | [DIF] | Vaidio, Ambient Pulsar |
| Video synopsis (horas → minutos de revisão) | [DIF] | BriefCam |
| Pareamento evento de negócio ↔ vídeo: controle de acesso (porta), POS/transações; análogo industrial: MES/apontamento | [TS] acesso; [DIF] POS/MES | Coram/Camio/Hakimo (acesso), Solink (POS), Verkada Helix |

## F. Módulo de produtividade industrial — pacote mínimo p/ vender

**Essenciais (sem isso não é produto de produtividade):**
1. **Vídeo pesquisável por unidade/número de série** (scanner/RFID/MES na
   estação → ciclo completo daquela unidade, estação por estação) —
   Drishti Trace, PowerArena Digital Station. Killer feature de root-cause.
2. **Golden cycle**: ciclo de referência do melhor operador; comparação de
   todos contra ele; biblioteca de treinamento — Drishti, Invisible AI.
3. **Playlist de outliers**: ciclos anômalos (curtos/longos) viram fila de
   revisão com vídeo — Drishti Flow.
4. **Yamazumi/line balance ratio/takt**: a linguagem do engenheiro
   industrial — PowerArena, Retrocausal, Drishti.
5. **Variação entre operadores/turnos** no mesmo posto — Invisible AI.
6. **Alerta em tempo real de estação acima do ciclo padrão com link para o
   vídeo** — PowerArena.
7. **Work Definition**: usuário marca os passos sobre o clipe e o sistema
   cronometra (time study assistido) — Drishti.
8. **API/webhook MES/ERP** (receber serial/ordem; publicar tempos).
9. **Privacidade operária como pré-requisito**: blur irreversível de rosto,
   agregação por estação/turno sem ranking punitivo, RBAC sobre vídeo,
   opção 100% on-prem ("nenhum vídeo sai da fábrica") — Intenseye, Voxel,
   Protex. Confirma nossa decisão TST/LGPD e é exigência de compra.

**Fase 2 do módulo (avançado):**
breakdown do ciclo em passos VA/NVA (Retrocausal faz a partir de 1 vídeo
de celular — ótimo "wedge" comercial), poka-yoke com feedback ao operador
e parada de linha via PLC/OPC UA, root-cause automático com Pareto,
evento→ação com dono/prazo (CLCA), dashboards multi-planta, copilot LLM
sobre os dados (LeanGPT/Chief — nossa busca conversacional é a fundação),
ergonomia por esqueleto, módulo EHS (near-miss empilhadeira, zonas de
perigo dinâmicas) como upsell nas mesmas câmeras.

**Tática comercial comprovada:** oferta de entrada empacotada ("1 linha,
100 dias" — Invisible AI One Line Offer) e modos de anonimização por
níveis (blur → ghosting → videoless — Protex) para vencer sindicato/RH.

## G. Customização de IA — a fronteira competitiva atual

**Builder no-code de detector custom**: usuário descreve em linguagem
natural o que quer detectar (+ ~20 exemplos, refino por
aprovação/rejeição) e o agente entra em produção em minutos — Spot AI
Iris (benchmark), Conntour, Vaidio 9 (ajuste por frase CLIP), Noleak
("escrever para a câmera"). **[DIF] que devemos tratar como pilar**: nossa
arquitetura analisador-plugável + VLM foi desenhada exatamente para isso;
é a evolução natural dos nossos analisadores fixos.

## H. Privacidade como produto

- Anonimização dinâmica com desanonimização por permissão extra +
  auditoria de quem desanonimizou (Genetec Privacy Protector) — [DIF]
  perfeito para LGPD.
- Toggles de compliance por tenant/site (desligar facial/LPR) — [TS].
- Modos por nível: blur rosto → blur corpo → silhueta → videoless
  (Protex/Intenseye) — [DIF] no módulo industrial.

---

## Priorização recomendada (roadmap revisado)

| Fase | Conteúdo (revisado com os adendos) |
|---|---|
| **1 — Fundação de vídeo** | Gravação contínua + clipes + player; retenção por câmera; buffer/failover; exportação probatória básica; **health monitoring gerencial**; máscaras de privacidade |
| **2 — Plataforma vendável** | RBAC + auditoria; API/webhooks; app mobile (ou PWA); canais de alerta (e-mail/SMS/push/WhatsApp); **LPR + contagem/ocupação + loitering + EPI**; **conector Sigma/centrais com clipe acoplado** |
| **3 — Operação inteligente** | Triagem VLM com descrição de cena; fila de triagem/livewall com verificação 1-clique; ciclo de tratativa com estados; ronda virtual; talk-down; anomalia self-learning; busca→alerta em 1 clique |
| **4 — Investigação** | Agente investigador conversacional; busca por atributos; re-ID não-biométrica com journey; gestão de casos; extração de dados por pergunta; upload forense |
| **5 — Produtividade industrial** | Pacote mínimo F.1–F.9 (serial-search, golden cycle, outliers, yamazumi, alerta tempo real, work definition, API MES, privacidade operária); oferta "1 linha" |
| **6 — Fronteira** | Builder no-code de detectores (Iris-like); copilot operacional; poka-yoke/PLC; módulo EHS; monitoramento como serviço; facial opt-in com governança |

## Aprendizados de modelo comercial

- Todos os AI-first vendem **appliance edge com GPU** junto do software
  (Spot IVR, Coram NVR, Camio Box, Vaidio VSA) — confirma nossa "edge box"
  como parte do produto, não acessório.
- Precificação: por câmera+retenção (Lumana, Eagle Eye, Rhombus US$
  149–199/câm/ano público) vs por LOCAL flat (Spot AI, Solink) vs por
  porta (Camio US$ 125/porta/mês). Para o Brasil: por câmera/mês simples
  e público (diferencial de transparência), com white label para centrais.
- Freemium à la Intelbras Defense IA Lite (grátis até 16 câmeras) é uma
  arma de adoção a considerar contra a capilaridade deles.
