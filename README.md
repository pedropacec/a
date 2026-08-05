# Guarde Tudo Self Storage — Kit de marca e redes sociais

Material criado a partir do estudo do PDF geral da marca (panfletos, posts,
folder, embalagens e banners originais).

## O que tem aqui

| Pasta | Conteúdo |
|---|---|
| `marca/` | [Guia da marca](marca/guia-da-marca.md): cores, logo, tipografia, tom de voz, públicos |
| `panfleto/` | Panfleto A4 atualizado — [PDF pronto para gráfica](panfleto/panfleto-a4.pdf), [preview PNG](panfleto/panfleto-preview.png) e o HTML editável |
| `posts/png/` | 6 posts de feed (1080×1350) + 1 story (1080×1920) prontos para publicar |
| `posts/html/` | Versões editáveis (HTML) de cada arte |
| `posts/legendas-e-calendario.md` | Legenda pronta para cada post, hashtags e calendário de 4 semanas |
| `tools/gerar_artes.py` | Gerador: edite os textos no script e rode para regravar tudo |

## Como editar e regerar as artes

Os textos e cores ficam em `tools/gerar_artes.py` (variáveis no topo do
arquivo: telefone, WhatsApp, endereço etc.). Depois de editar:

```bash
python3 tools/gerar_artes.py --render
```

Isso regrava os HTML, os PNG dos posts e o PDF do panfleto. Requer a fonte
**Lato** instalada (grátis no Google Fonts) e Chromium/Chrome no caminho
configurado na variável `CHROME` do script.

## Identidade em resumo

- Verde Guarde Tudo `#7BC628` · Grafite `#383435` · Cinza claro `#E7E7E7`
- Tipografia **Lato** (títulos em Black 900 caixa alta, corpo Regular 400)
- Símbolo: cubo isométrico; motivos de hexágono e overlay verde nas fotos
- Bordão: **"Temos espaço para tudo!"**
- Contatos: (31) 3288-1555 · WhatsApp (31) 9 8446-6482 · @guardetudobh ·
  guardetudobh.com.br
