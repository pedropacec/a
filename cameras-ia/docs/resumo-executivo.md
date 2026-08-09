# Sentinela IA — Resumo executivo

> Resumo do projeto até aqui. Detalhes em `visao-produto.md` (produto) e
> `estrategia-empresa.md` (negócio). Última atualização: 2026-08-09.

## O que é

O Sentinela IA é um software de gestão de câmeras com inteligência
artificial que não apenas grava: **assiste, entende e responde**. A proposta
é ser a camada de inteligência sobre as câmeras que a empresa já tem — sem
trocar hardware — transformando vídeo bruto em três produtos:

**1. Produtividade industrial.** A IA mede, por estação de trabalho e por
funcionário: tempo de presença, tempo ativo × ocioso, pausas, unidades
produzidas e tempo de ciclo. Os relatórios saem por turno, dia e semana. A
identificação começa por estação + escala de turnos (sem biometria, LGPD
simples); reconhecimento facial fica como opção futura, desligada por padrão.

**2. Vigilância que entende a cena.** Em vez de "movimento detectado", o
sistema entende o que está acontecendo e avisa: um modelo de visão e
linguagem descreve a cena ("duas pessoas forçando a porta do box 14"),
classifica a gravidade e entrega o trecho exato da gravação para análise. A
inteligência é em camadas — heurísticas baratas vigiam tudo o tempo todo;
detecção de objetos e IA generativa só entram quando algo foi sinalizado —
o que mantém o custo sob controle.

**3. Conversa com as gravações.** O usuário pergunta em linguagem natural
("por volta das 14h sumiu uma ferramenta no setor B — descobre o que
aconteceu") e um agente de IA investiga: restringe pelo horário, busca
semanticamente na linha do tempo indexada e responde com uma narrativa
cronológica e os clipes como prova. O segredo técnico: indexar
continuamente (legendas + embeddings de quadros), nunca varrer vídeo bruto
na hora da pergunta.

## O que já está construído e funcionando

- Plataforma base em Python/FastAPI: cadastro de câmeras (RTSP, HTTP,
  webcam, arquivo e fontes sintéticas de teste), um worker por câmera com
  reconexão automática, painel web com visão ao vivo e eventos em tempo real.
- Pipeline de análise plugável com cinco analisadores: movimento, intrusão
  em zonas restritas, atividade fora de horário, sabotagem de câmera
  (lente coberta/borrada) e detecção de pessoas/objetos (YOLO, opcional).
- **Área de notificação**: um motor de regras agrega os eventos brutos em
  pontos de atenção acionáveis para o cliente — câmera sem sinal,
  monitoramento parado, intrusões recorrentes, pico de eventos críticos —
  com estados lida/resolvida, reacendimento quando há novas ocorrências e
  auto-resolução quando a situação normaliza.
- 21 testes automatizados cobrindo analisadores, API e notificações.

## A estratégia

Não competir como VMS genérico contra Intelbras, Digifort e Milestone —
guerra de preço perdida. O posicionamento é **camada de inteligência sobre
infraestrutura existente**, entrando por verticais: indústria (vende
produtividade, ROI mensurável) e self storage/galpões (vende segurança
inteligente, com a Guarde Tudo como laboratório vivo e primeiro caso).

Arquitetura comercial: **edge + nuvem** — uma box no cliente processa o
vídeo localmente (a internet não aguenta subir vídeo; a LGPD agradece) e a
nuvem concentra painéis, alertas e o agente de busca. Receita por
**assinatura por câmera/mês** em três planos (Monitorar / Entender /
Produzir), com **integradores de CFTV como canal de vendas** — milhares de
técnicos instalando câmeras todo dia levam o produto em troca de comissão
recorrente.

## Próximos passos

1. **Fase 1 — Gravação contínua + clipes** (fundação dos pilares 2 e 3):
   cada alerta passa a apontar o trecho exato do vídeo.
2. **Fase 2 — YOLO + produtividade v1** por estação de trabalho.
3. **Fase 3 — Triagem por IA generativa + WhatsApp** nos alertas.
4. **Fase 4 — Busca conversacional** nas gravações.
5. Em paralelo: primeiro piloto real, medição de custo por câmera e as
   decisões de fundador (dedicação, capital, nome/marca no INPI).
