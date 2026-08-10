# Estratégia — de projeto a empresa de gestão de câmeras com IA

> Anotações vivas de estratégia de produto e negócio.
> Última atualização: 2026-08-09. Complementa `visao-produto.md` (os 3 pilares).

## A decisão mais importante: NÃO competir como "VMS genérico"

O mercado de software de gestão de câmeras (VMS) já tem gigantes:

| Player | Posição |
|---|---|
| Intelbras (Defense IA, Sim+) | Domina hardware no Brasil e embute software de graça/barato |
| Digifort | VMS brasileiro consolidado, canal forte com integradores |
| Milestone, Genetec | Globais, corporativo/enterprise, caros |
| Hikvision/Dahua (HikCentral, DSS) | Ecossistemas fechados dos fabricantes |
| Frigate, ZoneMinder, Blue Iris | Open source/baratos, público técnico |

Competir de frente nisso é guerra de preço contra quem fabrica a câmera.
**A oportunidade é outra: ser a CAMADA DE INTELIGÊNCIA que funciona em cima
de qualquer infraestrutura existente** (RTSP/ONVIF — o cliente não troca
câmera nem DVR). Os três pilares são exatamente o que os incumbentes não
entregam bem:

1. **Produtividade industrial** — nicho com alta disposição a pagar (nos EUA,
   Invisible AI e Drishti provaram o modelo; no Brasil o espaço está vazio).
2. **Vigilância que ENTENDE a cena** (VLM descrevendo o que acontece) — os
   NVRs têm "análise de vídeo" de checkbox (linha, intrusão); descrição em
   linguagem natural + triagem inteligente ainda é raro.
3. **Busca conversacional nas gravações** — praticamente ninguém tem. É o
   diferencial mais defensável e o melhor demo de vendas.

## Posicionamento sugerido

> "Suas câmeras já enxergam. A gente faz elas entenderem."
> Camada de IA para as câmeras que a empresa já tem — sem trocar hardware.

Estratégia de entrada por **verticais** (beachhead), não horizontal:

- **Vertical 1 — Indústria/produção:** vende o pilar 1 (produtividade) com
  os pilares 2–3 de bônus. Dor clara, ROI mensurável (unidades/hora), quem
  compra é o dono/gerente de produção.
- **Vertical 2 — Self storage / condomínios / galpões:** vende os pilares
  2–3 (segurança inteligente). Já existe acesso a um cliente-piloto real
  (Guarde Tudo) para ser o laboratório vivo e o caso de sucesso.

## Arquitetura de produto: edge + nuvem (decisão estrutural)

Vídeo não sobe para a nuvem — a internet do cliente não aguenta e a LGPD
agradece. O produto vira duas peças:

```
NO CLIENTE (edge box: mini-PC, com GPU nos planos maiores)
  captura RTSP/ONVIF · gravação em anel local · heurísticas + YOLO
  extração de clipes · indexação (amostra quadros)
        │  sobem só: eventos, clipes, miniaturas, legendas/embeddings
        ▼
NA NUVEM (multi-tenant)
  contas/organizações/sites/usuários/permissões · painel e relatórios
  triagem VLM · alertas WhatsApp/Telegram · agente de busca conversacional
  faturamento · monitoramento da frota de edge boxes · auto-update
```

- O código atual (`cameras-ia/`) é a semente do **agente edge**.
- Edge funciona offline e sincroniza quando a conexão volta.
- Onboarding: ligar a box na rede → descoberta automática ONVIF → câmeras
  aparecem no painel. Instalável por um técnico de CFTV comum.

## Modelo de negócio

- **Assinatura por câmera/mês** (padrão do mercado), em planos:
  - *Monitorar* — gravação + alertas heurísticos + clipes
  - *Entender* — + triagem VLM, descrições, busca conversacional
  - *Produzir* — + módulo de produtividade industrial (por estação)
- Edge box vendida ou alugada (receita de hardware + previsibilidade).
- **Canal de vendas: integradores de CFTV.** O Brasil tem milhares deles
  instalando câmera todo dia; eles levam o produto ao cliente em troca de
  comissão recorrente/white-label. O produto precisa ser fácil de instalar
  POR ELES — isso é requisito de engenharia, não só de vendas.

## Economia de VLM (risco nº 1 da margem)

O custo de API de visão escala com quadros analisados. Defesas:

1. Camadas: VLM só em alertas e indexação esparsa (1 quadro/15–30 s).
2. Cache/dedupe: cena parada não re-analisa (hash perceptual do quadro).
3. Modelos abertos locais (LLaVA/Qwen-VL) na edge box com GPU para
   indexação bruta; API premium (Claude) só para triagem fina e chat.
4. Preço do plano dimensionado por câmera JÁ considerando o custo de
   inferência — modelar planilha de custo por câmera antes de precificar.

## Riscos e como mitigar

| Risco | Mitigação |
|---|---|
| Incumbentes adicionam IA de checkbox | Profundidade (busca conversacional, relatórios de produtividade), não lista de features |
| Compatibilidade infinita de câmeras/DVRs zumbis | Lista de marcas homologadas no início; ONVIF Profile S/T; expandir com demanda |
| Custo de VLM come a margem | Ver seção acima; medir custo/câmera desde o piloto |
| LGPD (biometria, monitoramento de funcionários) | Três níveis: contagem sem identificação (padrão) → reidentificação por atributos sem template facial (investigações) → facial como módulo opt-in premium com governança embutida (RIPD, avisos, contratos). "Biometria sob controle" vira produto, não limitação |
| Complexidade de operar frota edge | Auto-update, telemetria de saúde, acesso remoto de suporte desde a v1 |
| Solo founder / equipe pequena | Fatiar: 1 vertical, 1 cliente-piloto, 1 caso de sucesso antes de escalar |

## O caminho realista (fatiando a complexidade)

**Etapa A — Produto single-site funcionando de verdade (agora → ~3 meses)**
Fases 1–3 do roadmap técnico (gravação+clipes, YOLO+produtividade v1,
triagem VLM+WhatsApp) rodando em UM local real como laboratório vivo.
Meta: o demo que vende — "pergunta aí o que aconteceu ontem à noite".

**Etapa B — Design partners (3–6 meses)**
2–3 clientes-piloto pagantes (com desconto) — ao menos 1 industrial para o
pilar 1. Contrato simples, expectativa de co-construção. Medir: custo real
por câmera, falsos positivos, o que eles usam de verdade.

**Etapa C — Produto multi-tenant (6–12 meses)**
Separar edge/nuvem, contas e permissões, faturamento, auto-update da frota,
onboarding ONVIF automático. Primeiros integradores parceiros.

**Etapa D — Escala pelo canal**
Playbook de instalação para integradores, white-label, expansão de verticais.

## Veredito honesto sobre a oportunidade (09/08/2026, pós-pesquisa)

**Sim, condicional e específica.** NÃO há oportunidade em "VMS genérico"
(detecção virou commodity embarcada). HÁ oportunidade comprovada em:
(1) **produtividade industrial por vídeo** — ROI documentado, líder
mundial sumiu (Drishti→Apple), zero players nacionais encontrados; e
(2) **camada de IA para centrais/portaria remota** — dor aritmética
(custo de operador, falsos alarmes), distribuição já existe, empresas
como a Emive licenciariam em vez de construir. Busca conversacional =
demo que abre portas, não o negócio.

Janela estimada: 18–36 meses. Defesa: distribuição local + dados
verticais + serviço (tecnologia VLM nivelou — é o que permite equipe
pequena competir). Maior risco: EXECUÇÃO, não mercado (negócio de
campo, ciclo B2B, 12–18 meses até receita relevante — exige dedicação
e fôlego financeiro).

**Critério falsificável:** se em 6 meses de esforço comercial não
houver 1 indústria pagando piloto de produtividade OU 1 central de
porte testando o conector, revisar a tese sem dó.

## Questões em aberto (nível empresa)

1. Dedicação: fundador em tempo integral? Sócio técnico ou comercial?
2. Capital: bootstrapped (receita dos pilotos financia) ou buscar
   investimento após o caso de sucesso da Etapa B?
3. A Guarde Tudo topa ser o laboratório vivo/primeiro caso de sucesso?
4. Qual indústria da região seria o design partner ideal do pilar 1?
5. Nome/marca: "Sentinela IA" é placeholder — validar registro (INPI) antes
   de investir em marca.
