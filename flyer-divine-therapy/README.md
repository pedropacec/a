# Divine Therapy — flyer animado

Versão animada do flyer **Divine Therapy / Vèsse (August 29th)**, inspirada na
referência de story em que o personagem do flyer dança em animação frame a frame
enquanto a tipografia fica parada.

## O efeito

- **Linhas fervilhando (boiling lines)**: as linhas neon da ilustração tremem a
  8 quadros/s, como animação desenhada à mão (feTurbulence + feDisplacementMap).
- **Personagem dançando**: cabeça, braço com o cigarro, pernas e a rosa se
  movem em passos discretos, no mesmo ritmo da fervura.
- **Neon vivo**: o glow pulsa lentamente e o título "DIVINE THERAPY" dá uma
  piscada de letreiro de neon no meio do loop.
- **Deriva de câmera + granulação** para dar textura de filme.
- Loop perfeito de 6 s a 24 fps.

## Arquivos

| Arquivo | O que é |
|---|---|
| `flyer.html` | A arte animada. Abra no navegador para ver ao vivo. |
| `render.mjs` | Renderiza os MP4 (Playwright + ffmpeg). |
| `out/divine-therapy-feed.mp4` | 1080×1350 (feed 4:5), loop de 6 s |
| `out/divine-therapy-story.mp4` | 1080×1920 (story 9:16), loop de 6 s |
| `fonts/` | Poppins 800, Inter 700/800, Archivo Narrow 700, Playfair 700 (Google Fonts, licença OFL) |

## Como regerar

```bash
node render.mjs feed    # out/divine-therapy-feed.mp4
node render.mjs story   # out/divine-therapy-story.mp4
node render.mjs still   # out/preview-still.png (frame parado)
```

Requer `playwright` (com Chromium) e `ffmpeg` no PATH.

## Modo "flyer original" (idêntico, só com movimento)

Para animar o flyer original sem redesenhar nada: salve a imagem em
`arte/flyer-original.png` (1080×1350 ou proporção 4:5) e rode:

```bash
node render.mjs orig-feed    # out/divine-therapy-original-feed.mp4
node render.mjs orig-story   # out/divine-therapy-original-story.mp4
node render.mjs orig-still   # out/preview-still-original.png
```

O `flyer-original.html` mantém a arte 100% intocada e adiciona: fumaça
subindo do cigarro (com tremido de traço à mão), brasa pulsando,
respiração sutil de brilho, leve deriva de câmera e granulação de filme.
A posição da ponta do cigarro é configurável — abra
`flyer-original.html?sx=0.545&sy=0.45` no navegador e ajuste os valores
até a fumaça nascer no lugar certo (frações da largura/altura).

## Observações

- A ilustração é um redesenho vetorial (SVG) feito a partir do flyer original —
  não é o traço original. Cada parte (cabeça, braço, pernas, rosa, fumaça) é um
  grupo `<g id="...">` separado, o que permite a "dança". Para ajustar o
  movimento, edite os padrões `armPat`, `headPat` etc. no `<script>` do
  `flyer.html`.
- Com o PNG original do flyer (ou só da ilustração, em fundo preto), dá para
  aplicar o mesmo tratamento de fervura/glow direto na arte original — basta
  substituir o SVG por um `<img>` dentro de `.illo`.
