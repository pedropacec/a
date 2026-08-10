# Pesquisa de mercado — vigilância no Brasil e concorrência global

> Deep research realizada em 09/08/2026 (~90 buscas em PT/EN por três frentes
> de pesquisa). Números sempre com (valor, ano, fonte). Onde fontes divergem,
> as duas versões estão registradas.

## A resposta direta: já existe uma solução como a nossa?

**A proposta completa — segurança + produtividade industrial + busca
conversacional, sobre câmeras existentes, no Brasil — não foi encontrada em
nenhum player, nacional ou global.** Mas cada pedaço existe em alguém:

- A categoria "camada de IA sobre câmeras existentes com busca em linguagem
  natural" está **validada e bem capitalizada nos EUA**: Spot AI (US$ 93M
  captados; agente conversacional IRIS), Coram AI (US$ 66M; agentes de
  investigação), Lumana (US$ 64M; VLM + edge/nuvem), Ambient.ai (US$ 146M;
  VLM próprio "Pulsar" — o benchmark técnico do nosso "agente investigador":
  o operador pergunta "o que levou ao incidente?" e o sistema monta a linha
  do tempo). Verkada (hardware próprio) vale US$ 5,8 bi (dez/2025).
- **Busca por linguagem natural virou commodity nos incumbentes** em
  2024–2026: Verkada, Rhombus, Eagle Eye (inclusive em português), Genetec,
  Avigilon/Motorola e Milestone (VLM próprio "Project Hafnia" + VLM-as-a-
  service com NVIDIA). Conclusão dura: **"busca em linguagem natural"
  sozinha deixou de ser diferencial defensável.**
- O lado de **produtividade industrial por vídeo** vive em outro grupo
  (Drishti, Invisible AI, Retrocausal, PowerArena) que NÃO tem busca
  conversacional nem plataforma de segurança — e o líder histórico
  (Drishti, US$ 35M captados) foi absorvido pela Apple em 2023, deixando o
  nicho sem dono.
- **Nenhuma das startups AI-first atua na América Latina** (sem português,
  sem LGPD, sem canal local, preço em dólar). No Brasil só há peças
  parciais: Noleak (regras em linguagem natural, ~R$ 85/câm/mês, pequena),
  Vigiaê (alega busca NL, escala desconhecida), Monuv (nuvem sobre qualquer
  câmera, sem NL).

**Onde não há ocupante: a combinação segurança + produtividade + agente
investigador conversacional, localizada para o Brasil (LGPD, português,
canal de integradores, edge para internet ruim, preço em reais).**

---

## 1. Mercado nacional de segurança eletrônica

### Tamanho e crescimento (ABESE — Panoramas anuais)

| Ano | Faturamento | Crescimento |
|---|---|---|
| 2021 | R$ 9,24 bi | +14% |
| 2022 | R$ 11 bi | — |
| 2024 | R$ 14 bi | +16,1% |
| 2025 | R$ 16 bi | +16,2% (projeção 2026: +18,8%) |

- Crescimento acumulado de 73% desde 2021 (InvestNews, 2026). Setor com
  33,5 mil empresas e ~5,8 milhões de empregos (ABESE, 2026).
- **IA embarcada saltou de 54% para 85,7% dos produtos fabricados no país
  entre os Panoramas 2024 e 2025** — a onda de IA é agora.
- Recorte vídeo (consultorias divergem): US$ 0,5–1,5 bi em 2024/25, CAGR
  3,4–10,7% até 2030 (Grand View, Mordor, M&M). Vídeo IP ≈ 36% das vendas
  do setor (proxy ABESE 2018).

### Hardware — quem domina

- **Intelbras**: receita R$ 4,75 bi (2024, +15,9%); ~43–54% de share em
  CFTV (fontes divergem); capilaridade imbatível: ~170 distribuidores e
  +80 mil revendas, 98% dos municípios. Software próprio Defense IA (LPR,
  facial, busca forense) e nuvem Mibo (só câmeras próprias).
- **Hikvision** (fábrica em Manaus, gestão Multilaser) e **Dahua**
  (WizSense/WizMind com IA): preço agressivo, IA embarcada. **Giga**
  (+1 milhão de câmeras instaladas), **JFL**, **Motorola/Avigilon/Pelco**
  (premium governo/enterprise).

### Software e monitoramento — o dado mais importante do canal

- **Segware Sigma gerencia mais de 80% dos ambientes monitorados por
  empresas de segurança no Brasil** (~1 milhão de contas). Tradução:
  quem vende IA para o mercado de monitoramento PRECISA integrar com o
  Sigma (a Monuv faz isso via webhook). Segware pertence ao grupo
  ESMG/Crescera Capital (consolidador de software de segurança).
- **Digifort**: maior VMS brasileiro, 3,5–4,5 mi de licenças, 130 países;
  licença modular por câmera; sem busca conversacional encontrada.
- **Monuv**: nuvem + IA sobre qualquer câmera, foco em centrais; captou
  R$ 10 mi; plano PRO a partir de R$ 899/mês.
- **Camerite**: rede de franquias de videomonitoramento (300 mil usuários,
  600–800 cidades); integra o consórcio vencedor do **Smart Sampa**.
- **Gabriel**: R$ 101 mi captados (SoftBank, Qualcomm, Astella, Globo);
  modelo diferente — câmeras próprias em comodato para condomínios
  (R$ 399–699/mês), integrada ao Smart Sampa e polícias.
- Startups de IA em centrais: Octos.ai, Ôguen (filtragem de alarmes),
  Avantia, CoSecurity (12 mil câmeras de calçada), Noleak (Agatha).

### Canal e tendências

- Estrutura: fabricante → distribuidor regional → ~4 mil+ integradores/
  revendas de CFTV → cliente final. Centrais de monitoramento
  terceirizadas ("atacadistas" de monitoramento) crescendo.
- **Portaria remota é o segmento que mais cresce** (+23–24% a.a.;
  condomínios usuários +86% em 3 anos) — comprador natural de IA que
  reduz operadores por conta monitorada.
- VSaaS/nuvem: migração CAPEX→OPEX apontada como tendência estrutural
  2026; Bosch lançou VSaaS no Brasil.
- Setor público puxando escala: Smart Sampa com 50 mil câmeras (20 mil
  próprias + 30 mil privadas integradas), R$ 588 mi/60 meses; RJ +R$ 180
  mi/ano; 525 projetos de reconhecimento facial público no país (R$ 2,65
  bi desde 2019). Integração de câmeras privadas a sistemas públicos é o
  padrão emergente.

### Regulação (LGPD/ANPD)

- Imagem identificável = dado pessoal; biometria facial = dado SENSÍVEL.
  CFTV não exige consentimento, mas exige base legal, finalidade, avisos
  visíveis, retenção definida, DPO e contrato controlador × operador
  (nós seremos tipicamente OPERADOR dos dados do cliente).
- ANPD fiscalizando ativamente (23 clubes de futebol notificados em 2025
  por reconhecimento facial); PL 2338/2023 (marco da IA) pode restringir
  biometria à distância; falso positivo do Smart Sampa deteve idoso
  inocente por 10h (risco reputacional documentado).
- **Nosso posicionamento "sem biometria por padrão" é defensivo e vira
  argumento de venda.**

---

## 2. Concorrência global — mapa resumido

### Startups AI-first sobre câmeras existentes (concorrência direta)

| Empresa | Funding | Busca NL/VLM | Produtividade | Semelhança |
|---|---|---|---|---|
| Spot AI (EUA) | US$ 93M | Sim + agente IRIS | A mais forte (agentes p/ fábrica/logística) | **#1 mais parecida** |
| Coram AI (EUA) | US$ 66M | Sim, agentes de investigação | Parcial (casos, sem métricas) | #2 — DNA quase idêntico |
| Lumana (EUA/IL) | US$ 64M | Sim (VLM, Text Search) | Parcial (heatmaps, near-miss) | #3 |
| Ambient.ai (EUA) | US$ 146M | Pulsar VLM + forense 20x | Não (só segurança) | Benchmark do "agente investigador" |
| Hakimo (EUA) | US$ 20,5M | Parcial | Não | Modelo "guarda virtual" (serviço) |
| Camio (EUA) | seed | Sim (pioneiro) | Parcial | **Preço público: US$ 4,99/câm/mês** |
| Conntour (YC 2024) | US$ 7M | Sim, 100% on-prem | Não | Valida edge/on-prem |
| icetana (AUS) | ASX, pequena | Não (anomalia estatística) | Não | Valida "linha de base" |

Consolidação em curso (sinal de mercado quente e possíveis compradores
futuros): Vintra→Alarm.com (2023), Calipsa→Motorola (2022),
BriefCam→Milestone (2024/25), Drishti→Apple (2023), Brivo+Eagle Eye (2025).

### Incumbentes que já têm busca em linguagem natural

Verkada (AI Search, 2024), Rhombus (AI Search), **Eagle Eye Networks**
(Smart Video Search multi-idioma **incluindo português**; expansão
declarada Brasil/México/Argentina — o incumbente mais próximo de nós),
Genetec (NL search 2025, forte no Brasil), Milestone (VLM próprio +
VLMaaS com NVIDIA), Avigilon/Motorola. Nenhum tem agente investigador
multi-turno nem produtividade industrial.

### Produtividade industrial por vídeo (pilar 1)

- **Drishti** (EUA): o benchmark — tempo de ciclo por estação, US$ 35M
  captados, clientes DENSO/HELLA → absorvida pela Apple (2023) num asset
  deal. O nicho ficou sem líder.
- **Invisible AI** (US$ 21M): câmeras edge PRÓPRIAS; Toyota nas 14
  plantas norte-americanas.
- **PowerArena** (HK): sobre câmeras EXISTENTES; Foxconn/Jabil/Wistron;
  receita ~US$ 2,9M com 29 pessoas.
- **Retrocausal** (US$ 8,75M): "Kaizen Copilot" com GenAI.
- Adjacentes de segurança do trabalho (mesmo comprador): Voxel (US$ 61M),
  Intenseye (US$ 93M), Protex AI (US$ 36M) — todos sobre CFTV existente.
- **ROI publicado no nicho** (argumento de venda): PowerArena: +5,2% UPH,
  ROI 5x em ~4 semanas; Toyota/Invisible AI: ROI 3–5x por dispositivo,
  estação eliminada ≈ US$ 200 mil/ano; Drishti: payback < 6 meses;
  HELLA: +7% de produtividade em linha "já otimizada".
- **Brasil: monitoramento contínuo de produtividade por estação via IA
  nas câmeras existentes — NÃO ENCONTRADO.** Só cronoanálise por vídeo
  assistida (Easypro) e EHS/EPI (Quickium, Pix Force, Meeting/Irisity).

### Fricções jurídicas do pilar produtividade (moldam o produto)

- **TST**: monitoramento por câmera é lícito dentro do poder
  fiscalizatório SE: geral e não individualizado, sem câmeras ocultas,
  nunca em banheiros/vestiários/refeitórios. Câmera apontada para vigiar
  UM empregado específico tende a gerar condenação (dano moral/assédio).
- **Precedente europeu** (CNIL x Amazon France, 2024): multa de € 32M por
  medir produtividade e pausas individuais com precisão excessiva
  ("alertas de inatividade >10 min"). É o alerta mundial sobre o nosso
  caso de uso.
- **EU AI Act**: reconhecimento de emoções no trabalho proibido (2025);
  monitoramento de trabalhadores por IA = alto risco (2026). Relevante se
  um dia exportarmos.
- **Consequência de design**: medir ESTAÇÕES e agregados (linha, turno,
  célula), não ranking individual exposto; transparência com política
  interna assinada; métricas individuais somente com assessoria jurídica.
  Valida a decisão "estação + escala, sem biometria" da visão de produto.

### Números globais (contexto)

- Video analytics: US$ 12,4 bi (2025) → US$ 33,7 bi (2030), CAGR ~19–22%
  (Mordor; Grand View e Fortune BI na mesma faixa). Cresce 2–3x mais
  rápido que vigilância total (US$ 83 bi 2025 → 205 bi 2033, CAGR 11,7%).
- VSaaS puro: CAGR ~18% (2022–2030).

---

## 3. Implicações para a nossa estratégia

**O que a pesquisa VALIDA:**
1. Camada de IA sobre câmeras existentes (Coram/Spot/Lumana provam o
   modelo; heterogeneidade Hikvision/Dahua/Intelbras no Brasil o exige).
2. Edge + nuvem (Conntour on-prem e Lumana híbrida validam; internet
   brasileira e LGPD reforçam).
3. Entrada por verticais com produtividade industrial — nicho sem líder
   global (Drishti→Apple) e SEM NENHUM player no Brasil.
4. Canal de integradores + agora **centrais de monitoramento e portaria
   remota** como segmento comprador (o que mais cresce no setor).
5. Sem biometria por padrão (ANPD ativa, PL 2338, TST).

**O que a pesquisa MUDA ou ACRESCENTA:**
1. **Busca NL sozinha não é fosso** — já é commodity. O fosso é a
   combinação (produtividade + investigação conversacional + localização
   Brasil) e a distribuição local.
2. **Integração com Segware Sigma é requisito de produto** para vender ao
   mercado de monitoramento (>80% das centrais rodam Sigma).
3. Benchmarks de preço por câmera/mês: Camio US$ 4,99; Noleak R$ 85;
   Monuv R$ 899/mês mínimo por central; Gabriel R$ 399–699 com hardware.
   Nossa faixa provável: R$ 30–150/câmera/mês conforme plano.
4. O pilar produtividade deve nascer com guarda-corpos jurídicos
   (agregados por estação/linha, não vigilância individual) — isso é
   FEATURE, não limitação: reduz risco trabalhista do cliente.
5. Compradores estratégicos possíveis no longo prazo: Intelbras, grupo
   ESMG/Segware, Motorola, Eagle Eye (consolidação já em curso lá fora).

**Riscos registrados:** categoria lotada e capitalizada nos EUA (podem
descer para LatAm); incumbentes embarcando VLM (Milestone VLMaaS);
guerra de preço de hardware com IA embarcada "grátis" (Intelbras Defense
IA); divergência grande entre consultorias sobre o tamanho do mercado de
vídeo no Brasil (US$ 0,5–1,5 bi) — usar ABESE como âncora.

---

## 4. Nosso diferencial contra as soluções brasileiras

Três capacidades que nenhum player nacional tem + dois posicionamentos:

1. **Entendimento de cena (VLM), não só detecção.** O mercado nacional
   gera detecções (movimento, pessoa, placa, EPI); o mais avançado
   (Noleak/Agatha) permite ESCREVER regras em linguagem natural — ainda
   regra fixa. Nós descrevemos o que está acontecendo, com gravidade e
   ação sugerida. Intelbras Defense IA, Digifort, Monuv, Camerite e
   Gabriel não fazem.
2. **Investigação conversacional nas gravações** (agente multi-turno com
   linha do tempo e clipes como prova). Vigiaê alega busca NL one-shot;
   agente investigador não existe no país (e globalmente só Ambient/Coram
   estão começando — sem atuação aqui).
3. **Produtividade industrial na mesma plataforma.** Inexistente no
   Brasil (Easypro = cronoanálise manual assistida; Quickium/Pix Force =
   EPI/EHS). Segurança + produtividade + investigação juntos não existe
   nem globalmente (Drishti, que fazia só produtividade, virou Apple).
4. **Agnóstico de hardware** vs modelos presos: Intelbras prende ao
   ecossistema (Mibo só grava câmera própria); Gabriel instala câmeras
   próprias em comodato de 4 anos. Contra Monuv/Digifort (também
   agnósticos) o desempate são os itens 1–3.
5. **Biometria sob controle** (refinado após debate em 09/08/2026 — a
   ausência total seria malefício: perde checklist de concorrência, e
   estádios >20 mil têm biometria OBRIGATÓRIA por lei). Três níveis:
   (a) detecção/contagem de pessoas — sempre ligada, sem identificação;
   (b) **reidentificação por atributos** (aparência/roupa numa janela de
   tempo, sem template facial) — dá o "siga essa pessoa" do agente
   investigador com ~90% do valor forense e fração do risco;
   (c) reconhecimento facial como módulo OPT-IN premium com governança
   embutida (RIPD pré-preenchido, avisos, contrato controlador×operador,
   retenção, auditoria). O mercado vende facial no faroeste; nós
   vendemos "desligada por padrão, pronta quando precisar, blindada
   quando ligar".

Onde NÃO temos diferencial (e não devemos brigar): distribuição
(capilaridade Intelbras; Sigma em 80% das centrais — integração
obrigatória) e preço de detecção básica (commodity embarcada). A vitória
é vender o que eles estruturalmente não têm, PELO canal deles.

---

## Fontes principais

ABESE/Panoramas via NetSeg e IT Forum · Genial Investimentos (Intelbras) ·
Brazil Journal e Exame (Gabriel) · Prefeitura de SP (Smart Sampa) · ANPD ·
BusinessWire/PRNewswire (rodadas de Coram, Lumana, Spot AI, Voxel, Protex,
Intenseye) · TechCrunch (Conntour, Solink, Gabriel) · Tracxn/Crunchbase
(funding) · Grand View, Mordor, MarketsandMarkets, Fortune BI (mercado) ·
CNIL/EDPB e France24 (caso Amazon) · TST via Conexão Trabalho/pareceres ·
sites oficiais dos players citados. URLs completas nos registros da
pesquisa (disponíveis sob demanda).
