#!/usr/bin/env python3
"""Gera as artes da Guarde Tudo (panfleto + posts) em HTML e renderiza PNG/PDF.

Uso:
    python3 tools/gerar_artes.py            # gera HTML
    python3 tools/gerar_artes.py --render   # gera HTML e renderiza com Chromium

Requer a fonte Lato instalada no sistema (300/400/700/900) para renderizar.
"""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- tokens
VERDE = "#7BC628"
VERDE_CLARO = "#8ED44A"
VERDE_ESCURO = "#5FA51F"
GRAFITE = "#383435"
CINZA = "#E7E7E7"

SITE = "guardetudobh.com.br"
FONE = "31 3288.1555"
ZAP = "31 9.8446.6482"
EMAIL = "comercial@guardetudobh.com.br"
INSTA = "@guardetudobh"
ENDERECO = "Rua dos Moicanos, 512 | Olhos d'Água | Belo Horizonte | MG"

# ---------------------------------------------------------------- logo


def cubo(stroke, top="none", left="none", right="none", sw=7):
    """Cubo isométrico da marca (viewBox 0 0 100 100)."""
    return f'''
      <g stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">
        <polygon points="50,7 87,28.5 50,50 13,28.5" fill="{top}"/>
        <polygon points="13,28.5 50,50 50,93 13,71.5" fill="{left}"/>
        <polygon points="50,50 87,28.5 87,71.5 50,93" fill="{right}"/>
      </g>'''


def cubo_colorido(sw=7):
    return cubo(GRAFITE, top="#FFFFFF", left=VERDE_CLARO, right="#6FB427", sw=sw)


def cubo_outline(cor, sw=7):
    return cubo(cor, sw=sw)


def logo(variante="cor", largura=300):
    """Lockup vertical: cubo + guarde.tudo + SELF STORAGE."""
    if variante == "cor":
        cubo_svg = cubo_colorido()
        texto, sub, ponto = GRAFITE, "#8B8B85", VERDE
    elif variante == "escuro":  # para fundos verde-noite
        cubo_svg = cubo("#0F1A08", top="#F4F2EC", left=VERDE_CLARO, right="#6FB427")
        texto, sub, ponto = "#FFFFFF", "rgba(255,255,255,.6)", VERDE_CLARO
    else:  # branco, para fundos verdes
        cubo_svg = cubo_outline("#FFFFFF")
        texto, sub, ponto = "#FFFFFF", "rgba(255,255,255,.85)", "#FFFFFF"
    return f'''<svg viewBox="0 0 400 258" width="{largura}" xmlns="http://www.w3.org/2000/svg">
      <g transform="translate(150,0)">{cubo_svg}</g>
      <text x="200" y="188" text-anchor="middle" font-family="Lato" font-weight="900"
            font-size="66" letter-spacing="-1.5" fill="{texto}">guarde<tspan fill="{ponto}">.</tspan>tudo</text>
      <text x="337" y="222" text-anchor="end" font-family="Lato" font-weight="700"
            font-size="19" letter-spacing="7" fill="{sub}">SELF STORAGE</text>
    </svg>'''


def selo(diam=110, fundo="#FFFFFF", cor_cubo=GRAFITE, faces=True):
    """Cubo dentro de um círculo (o 'selo pendente' dos posts)."""
    interno = cubo_colorido(sw=8) if faces else cubo_outline(cor_cubo, sw=8)
    return f'''<svg viewBox="0 0 130 130" width="{diam}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="65" cy="65" r="62" fill="{fundo}"/>
      <g transform="translate(23,23) scale(0.84)">{interno}</g>
    </svg>'''


def pendente(altura=170, selo_diam=94, cor_linha="#FFFFFF"):
    """Linha vertical com o selo do cubo pendurado."""
    return f'''<div style="display:flex;flex-direction:column;align-items:center;">
      <div style="width:6px;height:{altura}px;background:{cor_linha};border-radius:3px;"></div>
      <div style="margin-top:-5px;filter:drop-shadow(0 12px 26px rgba(20,50,0,.28));">{selo(selo_diam, fundo=cor_linha, faces=False,
        cor_cubo=GRAFITE if cor_linha == "#FFFFFF" else "#FFFFFF")}</div>
    </div>'''


# ---------------------------------------------------------------- ícones

IC = {
    "fone": '<path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/>',
    "zap": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z" fill="none" stroke-width="1.8"/><path transform="translate(5.4,5.4) scale(0.55)" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/>',
    "pin": '<path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2" fill="none" stroke-width="1.8"/><path d="M3 6.5l9 6.5 9-6.5" fill="none" stroke-width="1.8"/>',
    "globo": '<circle cx="12" cy="12" r="9.2" fill="none" stroke-width="1.8"/><ellipse cx="12" cy="12" rx="4.2" ry="9.2" fill="none" stroke-width="1.6"/><path d="M3 12h18M4.3 7h15.4M4.3 17h15.4" fill="none" stroke-width="1.6"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.5"/>',
    "face": '<path d="M14 8.5V7c0-.8.2-1.2 1.3-1.2H17V3h-2.6C11.7 3 10.5 4.4 10.5 7v1.5H8.5V12h2v9H14v-9h2.6l.4-3.5H14z"/>',
    "camera": '<rect x="2" y="7" width="14" height="10" rx="2"/><path d="M16.5 10.5L22 8v8l-5.5-2.5z"/>',
    "cadeado": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" fill="none" stroke-width="2.2"/>',
    "grade": '<rect x="4" y="4" width="7" height="7" rx="1.4"/><rect x="13" y="4" width="7" height="7" rx="1.4"/><rect x="4" y="13" width="7" height="7" rx="1.4"/><rect x="13" y="13" width="7" height="7" rx="1.4" fill="none" stroke-width="2"/>',
    "relogio": '<circle cx="12" cy="12" r="9.2" fill="none" stroke-width="2"/><path d="M12 6.5V12l4 2.4" fill="none" stroke-width="2.2" stroke-linecap="round"/>',
    "brilho": '<path d="M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2z"/>',
    "caixa": '<path d="M12 2.5L21 7.5v9l-9 5-9-5v-9z" fill="none" stroke-width="2" stroke-linejoin="round"/><path d="M3 7.5l9 5 9-5M12 12.5v9" fill="none" stroke-width="2" stroke-linejoin="round"/>',
    "doc": '<path d="M6 2h9l5 5v15H6z" fill="none" stroke-width="2" stroke-linejoin="round"/><path d="M15 2v5h5M9 12h8M9 16h8" fill="none" stroke-width="2"/>',
    "sofa": '<path d="M5 10V8a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v2" fill="none" stroke-width="2"/><path d="M4 10a2.2 2.2 0 0 1 2.2 2.2V14h11.6v-1.8A2.2 2.2 0 1 1 21 14v5h-2v-1.6H5V19H3v-5a2.2 2.2 0 0 1 1-4z"/>',
    "wifi": '<path d="M2.5 9.5a14 14 0 0 1 19 0M5.5 13a9.5 9.5 0 0 1 13 0M8.6 16.4a5 5 0 0 1 6.8 0" fill="none" stroke-width="2.1" stroke-linecap="round"/><circle cx="12" cy="19.6" r="1.8" stroke="none"/>',
    "seta": '<path d="M4 12h14.5M12.5 5l7 7-7 7" fill="none" stroke-width="2.8"/>',
}


def icone(nome, tam=24, cor="#FFFFFF"):
    return (f'<svg viewBox="0 0 24 24" width="{tam}" height="{tam}" '
            f'fill="{cor}" stroke="{cor}" stroke-linejoin="round" stroke-linecap="round" '
            f'xmlns="http://www.w3.org/2000/svg">{IC[nome]}</svg>')


# ---------------------------------------------------------------- base css

def css_base(extra=""):
    return f'''
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    :root {{
      --verde:{VERDE}; --verde-claro:{VERDE_CLARO}; --verde-escuro:{VERDE_ESCURO};
      --grafite:{GRAFITE}; --cinza:{CINZA};
    }}
    body {{ font-family:'Lato', sans-serif; }}
    .canvas {{ position:relative; overflow:hidden; }}
    .marca-dagua {{ position:absolute; opacity:.16; pointer-events:none; }}
    {extra}'''


def marca_dagua(cor="#FFFFFF", tam=760, css=""):
    return (f'<div class="marca-dagua" style="{css}">'
            f'<svg viewBox="0 0 100 100" width="{tam}">{cubo_outline(cor, sw=3.2)}</svg></div>')


def pagina(titulo, corpo, w, h, extra_css=""):
    return f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>
<style>{css_base(extra_css)}
.canvas {{ width:{w}px; height:{h}px; }}</style></head>
<body>{corpo}</body></html>'''


# ---------------------------------------------------------------- posts v2

FUNDO_VERDE = (
    "background:"
    "radial-gradient(1100px 800px at 88% -12%, rgba(255,255,255,.30), transparent 60%),"
    "radial-gradient(1100px 900px at -18% 112%, rgba(20,70,0,.30), transparent 58%),"
    f"linear-gradient(160deg,{VERDE_CLARO},{VERDE} 48%,#5da21a);")

FUNDO_CLARO = (
    "background:"
    "radial-gradient(820px 560px at 12% 6%, rgba(123,198,40,.16), transparent 62%),"
    "radial-gradient(900px 700px at 108% 96%, rgba(123,198,40,.12), transparent 60%),"
    "linear-gradient(150deg,#FAFAF8,#EEEEEC);")

GLASS = ("background:rgba(255,255,255,.15);border:2.5px solid rgba(255,255,255,.38);"
         "backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);")

SOMBRA = "box-shadow:0 24px 50px rgba(30,60,0,.14);"


def ruido(op=.05):
    """Textura de granulado sutil por cima do fundo."""
    return (f'<svg style="position:absolute;inset:0;width:100%;height:100%;opacity:{op};" '
            'xmlns="http://www.w3.org/2000/svg"><filter id="nz">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" stitchTiles="stitch"/>'
            '<feColorMatrix type="saturate" values="0"/></filter>'
            '<rect width="100%" height="100%" filter="url(#nz)"/></svg>')


def tag(txt, sobre_verde=True):
    """Etiqueta pill em outline no topo do post."""
    estilo = ('border:3px solid rgba(255,255,255,.6);color:#fff;' if sobre_verde
              else f'border:3px solid {VERDE};color:{VERDE_ESCURO};')
    return (f'<div style="display:inline-block;{estilo}border-radius:44px;'
            f'padding:12px 34px;font-size:27px;font-weight:700;letter-spacing:6px;">{txt}</div>')


def marcador(txt, bg=VERDE, cor="#fff", rot=-1.5):
    """Palavra com tarja estilo marca-texto, levemente rotacionada."""
    return (f'<span style="display:inline-block;background:{bg};color:{cor};'
            f'padding:4px 30px 10px;border-radius:18px;transform:rotate({rot}deg);'
            f'box-shadow:0 16px 36px rgba(60,110,10,.25);">{txt}</span>')


def vazado(txt, cor="#fff", esp=4):
    """Texto só com contorno (outline)."""
    return f'<span style="color:transparent;-webkit-text-stroke:{esp}px {cor};">{txt}</span>'


def rodape_post(claro=False):
    """Rodapé: pill do Instagram à esquerda, logo à direita."""
    if claro:
        pill = f"background:#fff;border:2.5px solid #E0E0DC;color:{GRAFITE};"
        ic_cor, logo_v = VERDE_ESCURO, "cor"
    else:
        pill = "background:rgba(255,255,255,.16);border:2.5px solid rgba(255,255,255,.4);color:#fff;"
        ic_cor, logo_v = "#fff", "branco"
    return f'''
    <div style="position:absolute;left:56px;bottom:56px;display:flex;align-items:center;gap:14px;{pill}border-radius:50px;padding:15px 30px;font-size:29px;font-weight:900;">{icone("insta", 30, ic_cor)} @guardetudobh</div>
    <div style="position:absolute;right:56px;bottom:34px;">{logo(logo_v, 200)}</div>'''


def post_01():
    corpo = f'''<div class="canvas" style="{FUNDO_VERDE}">
      {marca_dagua(tam=860, css="left:-320px;top:400px;")}
      {marca_dagua(tam=440, css="right:-150px;top:-100px;opacity:.2;")}
      {ruido()}
      <div style="position:absolute;left:64px;top:64px;">{tag("SELF STORAGE &bull; BH")}</div>
      <div style="position:absolute;right:120px;top:0;">{pendente(130)}</div>
      <div style="position:absolute;left:80px;right:80px;top:420px;text-align:center;color:#fff;">
        <div style="font-size:62px;font-weight:300;font-style:italic;">Afinal, o que é</div>
        <div style="font-size:146px;font-weight:900;letter-spacing:2px;line-height:1.04;margin-top:10px;">SELF<br>{vazado("STORAGE?")}</div>
      </div>
      <div style="position:absolute;left:110px;right:110px;top:930px;{GLASS}{SOMBRA}border-radius:34px;padding:38px 46px;text-align:center;color:#fff;font-size:34px;line-height:1.5;">
        Um box <b>individual, seguro e flexível</b> para guardar o que não cabe
        na sua casa ou na sua empresa. Vem entender &rarr;
      </div>
      {rodape_post()}
    </div>'''
    return pagina("O que é Self Storage — Guarde Tudo", corpo, 1080, 1350)


def post_02():
    corpo = f'''<div class="canvas" style="{FUNDO_CLARO}">
      {marca_dagua(VERDE, 900, "left:-330px;bottom:-260px;opacity:.2;")}
      {ruido(.04)}
      <div style="position:absolute;left:64px;top:64px;">{tag("MUDANÇA &bull; ORGANIZAÇÃO", sobre_verde=False)}</div>
      <div style="position:absolute;right:120px;top:0;">{pendente(140, cor_linha=VERDE)}</div>
      <div style="position:absolute;left:84px;top:270px;color:{GRAFITE};">
        <div style="font-size:118px;font-weight:900;line-height:1.16;letter-spacing:1px;">
          MUDOU E<br>FALTOU<br>{marcador("ESPAÇO?", rot=-2)}
        </div>
        <div style="margin-top:64px;font-size:33px;font-weight:400;max-width:640px;line-height:1.5;">
          Boxes de <b>4 a 1.000&nbsp;m²</b>, sem fiador e sem burocracia,
          pelo tempo que você precisar.
        </div>
      </div>
      <div style="position:absolute;left:84px;top:1010px;display:inline-flex;align-items:center;gap:22px;
                  background:linear-gradient(135deg,{VERDE_CLARO},{VERDE_ESCURO});color:#fff;border-radius:70px;
                  padding:28px 52px;font-size:52px;font-weight:900;letter-spacing:1px;
                  box-shadow:0 22px 48px rgba(95,165,31,.38);">
        ARMAZENE AQUI {icone("seta", 52)}
      </div>
      {rodape_post(claro=True)}
    </div>'''
    return pagina("Mudou e faltou espaço — Guarde Tudo", corpo, 1080, 1350)


def post_03():
    def card(ic, titulo, sub):
        return f'''<div style="{GLASS}{SOMBRA}border-radius:32px;padding:34px 40px;display:flex;align-items:center;gap:34px;">
          <div style="flex:0 0 96px;height:96px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 26px rgba(20,50,0,.18);">{icone(ic, 48, VERDE_ESCURO)}</div>
          <div><div style="font-size:40px;font-weight:900;color:#fff;">{titulo}</div>
          <div style="font-size:28px;color:rgba(255,255,255,.88);margin-top:5px;">{sub}</div></div>
        </div>'''
    corpo = f'''<div class="canvas" style="{FUNDO_VERDE}">
      {marca_dagua(tam=800, css="right:-290px;top:-170px;")}
      {ruido()}
      <div style="position:absolute;left:84px;top:76px;">{tag("PARA PESSOA JURÍDICA")}</div>
      <div style="position:absolute;left:84px;top:190px;color:#fff;max-width:940px;">
        <div style="font-size:92px;font-weight:900;line-height:1.14;">
          SUA EMPRESA<br>PRECISA DE {vazado("ESPAÇO?")}
        </div>
      </div>
      <div style="position:absolute;left:84px;right:84px;top:500px;display:flex;flex-direction:column;gap:28px;">
        {card("caixa", "Estoque e mercadorias", "Espaço que cresce junto com as vendas")}
        {card("doc", "Documentos e arquivo morto", "Organização com sigilo e controle de acesso")}
        {card("sofa", "Móveis e equipamentos", "Guarde a estrutura entre projetos e reformas")}
      </div>
      <div style="position:absolute;left:84px;top:1075px;display:inline-flex;align-items:center;gap:20px;background:{GRAFITE};color:#fff;border-radius:60px;padding:24px 46px;font-size:33px;font-weight:700;box-shadow:0 20px 44px rgba(20,40,0,.30);">
        {icone("zap", 40)} Solicite um orçamento &middot; {ZAP}
      </div>
      {rodape_post()}
    </div>'''
    return pagina("Para empresas — Guarde Tudo", corpo, 1080, 1350)


def post_04():
    def chip(ic, txt):
        return f'''<div style="display:inline-flex;align-items:center;gap:24px;{GLASS}border-radius:60px;padding:16px 44px 16px 20px;">
          <div style="flex:0 0 78px;height:78px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 22px rgba(20,50,0,.16);">{icone(ic, 42, VERDE_ESCURO)}</div>
          <div style="color:#fff;font-size:43px;font-weight:700;"><span style="font-weight:900;">+</span> {txt}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="{FUNDO_VERDE}">
      {marca_dagua(tam=880, css="left:-340px;bottom:-240px;")}
      {ruido()}
      <div style="position:absolute;left:84px;top:76px;">{tag("POR QUE GUARDE TUDO?")}</div>
      <div style="position:absolute;right:110px;top:0;">{pendente(110)}</div>
      <div style="position:absolute;left:84px;top:190px;color:#fff;">
        <div style="font-size:84px;font-weight:900;line-height:1.15;">INFRAESTRUTURA<br>{vazado("COMPLETA:")}</div>
      </div>
      <div style="position:absolute;left:84px;top:480px;display:flex;flex-direction:column;align-items:flex-start;gap:24px;">
        {chip("camera", "Segurança 24 horas")}
        {chip("cadeado", "Privacidade total")}
        {chip("grade", "+40 opções de boxes")}
        {chip("relogio", "Prazos flexíveis")}
        {chip("brilho", "Espaços higienizados")}
      </div>
      {rodape_post()}
    </div>'''
    return pagina("Infraestrutura — Guarde Tudo", corpo, 1080, 1350)


def post_05():
    def card(letra, faixa, exemplos):
        return f'''<div style="flex:1;background:#fff;border-radius:36px;padding:46px 26px 40px;text-align:center;box-shadow:0 24px 50px rgba(40,60,0,.10);">
          <div style="width:120px;height:120px;margin:0 auto;border-radius:50%;background:linear-gradient(145deg,{VERDE_CLARO},{VERDE_ESCURO});color:#fff;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(95,165,31,.35);">{letra}</div>
          <div style="font-size:43px;font-weight:900;color:{GRAFITE};margin-top:28px;">{faixa}</div>
          <div style="font-size:27px;color:#6b6b68;margin-top:14px;line-height:1.4;">{exemplos}</div>
        </div>'''
    def mini(txt):
        return (f'<div style="display:inline-block;border:3px solid {VERDE};color:{VERDE_ESCURO};'
                f'border-radius:44px;padding:10px 30px;font-size:28px;font-weight:700;">{txt}</div>')
    corpo = f'''<div class="canvas" style="{FUNDO_CLARO}">
      {marca_dagua(VERDE, 780, "right:-270px;top:-210px;opacity:.18;")}
      {ruido(.04)}
      <div style="position:absolute;left:0;right:0;top:80px;text-align:center;">{tag("TAMANHOS DOS BOXES", sobre_verde=False)}</div>
      <div style="position:absolute;left:60px;right:60px;top:200px;text-align:center;color:{GRAFITE};">
        <div style="font-size:54px;font-weight:400;">De <b>A a Z</b>, do pequeno ao {vazado("GRANDE:", VERDE, 3)}</div>
        <div style="margin-top:36px;font-size:62px;font-weight:900;letter-spacing:1px;">{marcador("TEMOS ESPAÇO PARA TUDO!", rot=-1.2)}</div>
      </div>
      <div style="position:absolute;left:70px;right:70px;top:520px;display:flex;gap:28px;">
        {card("P", "4 a 12 m²", "Caixas, malas,<br>documentos, bicicletas")}
        {card("M", "13 a 24 m²", "Mudanças, móveis,<br>pequenos estoques")}
        {card("G", "25 a 1.000 m²", "Estoques, maquinário,<br>operações inteiras")}
      </div>
      <div style="position:absolute;left:0;right:0;top:1080px;display:flex;justify-content:center;gap:22px;">
        {mini("box sob medida")} {mini("contrato flexível")} {mini("sem fiador")}
      </div>
      {rodape_post(claro=True)}
    </div>'''
    return pagina("Tamanhos dos boxes — Guarde Tudo", corpo, 1080, 1350)


def post_06():
    def bloco(num, t1, t2):
        return f'''<div style="flex:1;background:#F6F6F4;border-radius:34px;padding:64px 34px 40px;text-align:center;position:relative;box-shadow:0 20px 44px rgba(40,60,0,.08);">
          <div style="position:absolute;left:50%;top:-34px;transform:translateX(-50%);width:68px;height:68px;border-radius:50%;background:linear-gradient(145deg,{VERDE_CLARO},{VERDE_ESCURO});color:#fff;font-size:36px;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 26px rgba(95,165,31,.35);">{num}</div>
          <div style="font-size:50px;font-weight:900;color:{GRAFITE};line-height:1.2;">{t1}</div>
          <div style="font-size:33px;font-weight:700;font-style:italic;color:{VERDE_ESCURO};margin-top:16px;line-height:1.3;">{t2}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="background:radial-gradient(760px 460px at 50% -10%, rgba(123,198,40,.28), transparent 65%),linear-gradient(180deg,#FFFFFF,#F7F7F5);">
      {marca_dagua(VERDE, 720, "left:-270px;bottom:-190px;opacity:.12;")}
      {ruido(.035)}
      <div style="position:absolute;left:0;right:0;top:80px;text-align:center;">
        <div style="display:inline-block;background:{VERDE};color:#fff;border-radius:44px;padding:12px 40px;font-size:28px;font-weight:900;letter-spacing:8px;box-shadow:0 14px 32px rgba(95,165,31,.3);">PROMOÇÃO</div>
      </div>
      <div style="position:absolute;left:0;right:0;top:200px;text-align:center;color:{GRAFITE};">
        <div style="font-size:116px;font-weight:900;line-height:1.14;">QUEM INDICA<br>{marcador("AMIGO", rot=-2)} É</div>
      </div>
      <div style="position:absolute;left:0;right:0;top:590px;display:flex;justify-content:center;filter:drop-shadow(0 16px 34px rgba(95,165,31,.35));">{selo(140, fundo=VERDE, faces=False, cor_cubo="#FFFFFF")}</div>
      <div style="position:absolute;left:80px;right:80px;top:820px;display:flex;gap:34px;">
        {bloco("1", "INDIQUE<br>1 AMIGO", "você ganha<br>e ele também")}
        {bloco("2", "DESCONTO<br>PRA CADA UM", "na próxima<br>mensalidade")}
      </div>
      <div style="position:absolute;left:0;right:0;top:1130px;text-align:center;font-size:29px;color:#6b6b68;">
        Consulte as condições com o nosso time &darr;
      </div>
      <div style="position:absolute;left:64px;bottom:56px;display:flex;gap:16px;align-items:center;">
        <div style="background:{GRAFITE};color:#fff;border-radius:50px;padding:14px 28px;font-size:28px;font-weight:700;display:flex;gap:12px;align-items:center;">{icone("fone", 28)} {FONE}</div>
        <div style="background:linear-gradient(135deg,{VERDE_CLARO},{VERDE_ESCURO});color:#fff;border-radius:50px;padding:14px 28px;font-size:28px;font-weight:700;display:flex;gap:12px;align-items:center;box-shadow:0 12px 28px rgba(95,165,31,.3);">{icone("zap", 28)} {ZAP}</div>
      </div>
      <div style="position:absolute;right:56px;bottom:34px;">{logo("cor", 200)}</div>
    </div>'''
    return pagina("Indique um amigo — Guarde Tudo", corpo, 1080, 1350)


def story_01():
    corpo = f'''<div class="canvas" style="{FUNDO_VERDE}">
      {marca_dagua(tam=920, css="left:-330px;top:1150px;")}
      {ruido()}
      <div style="position:absolute;left:0;right:0;top:0;display:flex;justify-content:center;">{pendente(170)}</div>
      <div style="position:absolute;left:0;right:0;top:400px;text-align:center;">{tag("SELF STORAGE EM BH")}</div>
      <div style="position:absolute;left:80px;right:80px;top:520px;text-align:center;color:#fff;">
        <div style="font-size:52px;font-weight:300;font-style:italic;">Venha conhecer o</div>
        <div style="font-size:110px;font-weight:900;letter-spacing:2px;margin-top:8px;">GUARDE {vazado("TUDO")}</div>
      </div>
      <div style="position:absolute;left:90px;right:90px;top:830px;{GLASS}{SOMBRA}border-radius:38px;padding:54px 48px;text-align:center;color:#fff;">
        <div style="display:flex;justify-content:center;"><div style="width:96px;height:96px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 26px rgba(20,50,0,.2);">{icone("pin", 52, VERDE_ESCURO)}</div></div>
        <div style="font-size:41px;font-weight:900;margin-top:24px;line-height:1.35;">Rua dos Moicanos, 512<br>Olhos d'Água &middot; BH/MG</div>
        <div style="font-size:30px;color:rgba(255,255,255,.88);margin-top:16px;">a 5 minutos do BH Shopping<br>área coberta para carga e descarga</div>
      </div>
      <div style="position:absolute;left:90px;right:90px;top:1400px;background:#fff;color:{GRAFITE};border-radius:70px;padding:30px 40px;display:flex;align-items:center;justify-content:center;gap:20px;font-size:37px;font-weight:900;box-shadow:0 22px 48px rgba(20,50,0,.25);">
        {icone("zap", 44, VERDE_ESCURO)} CHAMA NO WHATS &middot; {ZAP}
      </div>
      <div style="position:absolute;left:0;right:0;bottom:175px;text-align:center;color:#fff;font-size:33px;font-weight:700;">
        {INSTA} &middot; guardetudobh.com.br
      </div>
      <div style="position:absolute;left:0;right:0;bottom:14px;display:flex;justify-content:center;">{logo("branco", 215)}</div>
    </div>'''
    return pagina("Story Visite — Guarde Tudo", corpo, 1080, 1920)


# ------------------------------------------------------- carrossel premium

VERDE_NOITE = "#16220E"

FUNDO_NOITE = (
    "background:"
    "radial-gradient(1000px 720px at 80% -10%, rgba(123,198,40,.20), transparent 60%),"
    "radial-gradient(900px 700px at -10% 108%, rgba(123,198,40,.10), transparent 55%),"
    f"linear-gradient(165deg,#223313,{VERDE_NOITE} 55%,#101A08);")

FUNDO_CREME = (
    "background:"
    "radial-gradient(800px 560px at 90% -6%, rgba(123,198,40,.10), transparent 60%),"
    "linear-gradient(160deg,#FAF8F2,#F0EEE6);")


def risco(cor=VERDE):
    """Traço curto de destaque sob os títulos."""
    return f'<div style="width:74px;height:7px;border-radius:4px;background:{cor};margin-top:18px;"></div>'


def pagina_pill(n, escuro=True):
    estilo = (f"background:{VERDE_NOITE};color:#fff;border:2px solid rgba(123,198,40,.5);" if escuro
              else "background:rgba(255,255,255,.12);color:#fff;border:2px solid rgba(255,255,255,.35);")
    return (f'<div style="position:absolute;left:50%;transform:translateX(-50%);bottom:44px;'
            f'{estilo}border-radius:40px;padding:10px 34px;font-size:27px;font-weight:900;">{n}/6</div>')


def check_item(txt):
    return f'''<div style="display:flex;align-items:center;gap:22px;">
      <div style="flex:0 0 52px;height:52px;border-radius:50%;background:linear-gradient(145deg,{VERDE_CLARO},{VERDE_ESCURO});display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(123,198,40,.3);">
        <svg viewBox="0 0 24 24" width="28" height="28"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div style="color:#fff;font-size:34px;">{txt}</div>
    </div>'''


def mini_feat(ic, t1, t2):
    return f'''<div style="flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;padding:0 6px;">
      <div style="width:84px;height:84px;border-radius:50%;border:3px solid {VERDE_CLARO};display:flex;align-items:center;justify-content:center;">{icone(ic, 40, VERDE_CLARO)}</div>
      <div style="color:#fff;font-size:25px;font-weight:900;line-height:1.2;">{t1}</div>
      <div style="color:rgba(255,255,255,.65);font-size:20px;line-height:1.3;">{t2}</div>
    </div>'''


def carrossel_01():
    corpo = f'''<div class="canvas" style="{FUNDO_NOITE}">
      {marca_dagua("#FFFFFF", 560, "right:-180px;top:-140px;opacity:.05;")}
      {ruido(.05)}
      <div style="position:absolute;left:64px;top:56px;">{logo("escuro", 195)}</div>
      <div style="position:absolute;left:64px;top:330px;width:430px;">
        {risco()}
        <div style="margin-top:22px;font-size:56px;font-weight:900;color:#fff;line-height:1.2;">FLEXIBILIDADE<br>E SEGURANÇA</div>
        <div style="margin-top:6px;font-size:44px;font-weight:900;color:{VERDE_CLARO};line-height:1.25;">PARA GUARDAR<br>O QUE PRECISAR!</div>
        <div style="margin-top:30px;font-size:28px;color:rgba(255,255,255,.75);line-height:1.5;">
          Espaços inteligentes e seguros para facilitar a sua vida e dar
          mais espaço ao que realmente importa.
        </div>
      </div>
      <div style="position:absolute;right:56px;top:270px;width:470px;height:600px;border-radius:44px;overflow:hidden;border:3px solid rgba(123,198,40,.45);box-shadow:0 30px 70px rgba(0,0,0,.5);">
        <img src="assets/casal-caixa.jpg" style="width:100%;height:100%;object-fit:cover;">
      </div>
      <div style="position:absolute;left:56px;right:56px;top:950px;border:2.5px solid rgba(123,198,40,.35);background:rgba(255,255,255,.05);border-radius:40px;padding:34px 22px;display:flex;">
        {mini_feat("camera", "SEGURANÇA<br>24 HORAS", "Monitoramento e<br>acesso controlado")}
        {mini_feat("cadeado", "PRIVACIDADE<br>TOTAL", "Sua tranquilidade em<br>primeiro lugar")}
        {mini_feat("grade", "FLEXIBILIDADE<br>DE ESPAÇO", "Do tamanho que você<br>precisa, pelo tempo que precisar")}
        {mini_feat("relogio", "SEM FIADOR,<br>SEM BUROCRACIA", "Locação simples,<br>rápida e sem complicações")}
      </div>
      {pagina_pill(1, escuro=False)}
    </div>'''
    return pagina("Carrossel 1/6 — Capa", corpo, 1080, 1350)


def carrossel_02():
    corpo = f'''<div class="canvas" style="{FUNDO_CREME}">
      {marca_dagua(VERDE, 640, "right:-220px;top:-160px;opacity:.10;")}
      {ruido(.035)}
      <div style="position:absolute;left:84px;top:110px;">
        <div style="font-size:70px;font-weight:900;color:{GRAFITE};">QUEM SOMOS</div>
        {risco()}
      </div>
      <div style="position:absolute;left:84px;top:320px;width:600px;color:#4A4744;font-size:33px;line-height:1.6;">
        <p>O <b>Guarde Tudo</b> é um self storage que oferece soluções para a
        autogestão de espaços com <b>flexibilidade e segurança</b>. O processo de
        locação é simplificado, sem necessidade de fiador ou avalista.</p>
        <p style="margin-top:34px;">Aqui o cliente tem <b>comodidade e privacidade</b>
        para sentir que seu box é parte da sua casa ou do seu negócio.</p>
      </div>
      <div style="position:absolute;right:70px;top:660px;filter:drop-shadow(0 30px 60px rgba(60,90,20,.3));">
        <svg viewBox="0 0 100 100" width="330">{cubo_colorido(sw=6)}</svg>
      </div>
      <div style="position:absolute;left:84px;top:1010px;display:flex;gap:20px;">
        <div style="border:3px solid {VERDE};color:{VERDE_ESCURO};border-radius:44px;padding:12px 32px;font-size:28px;font-weight:700;">+40 boxes</div>
        <div style="border:3px solid {VERDE};color:{VERDE_ESCURO};border-radius:44px;padding:12px 32px;font-size:28px;font-weight:700;">pessoa física e jurídica</div>
        <div style="border:3px solid {VERDE};color:{VERDE_ESCURO};border-radius:44px;padding:12px 32px;font-size:28px;font-weight:700;">a 5 min do BH Shopping</div>
      </div>
      {pagina_pill(2)}
    </div>'''
    return pagina("Carrossel 2/6 — Quem somos", corpo, 1080, 1350)


def carrossel_03():
    def obj(ic, t):
        return f'''<div style="background:#fff;border-radius:30px;padding:34px 20px;text-align:center;box-shadow:0 18px 40px rgba(60,90,20,.10);">
          <div style="width:88px;height:88px;margin:0 auto;border-radius:50%;background:linear-gradient(145deg,{VERDE_CLARO},{VERDE_ESCURO});display:flex;align-items:center;justify-content:center;">{icone(ic, 44)}</div>
          <div style="margin-top:18px;font-size:29px;font-weight:900;color:{GRAFITE};">{t}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="{FUNDO_CREME}">
      {marca_dagua(VERDE, 640, "left:-240px;bottom:-200px;opacity:.10;")}
      {ruido(.035)}
      <div style="position:absolute;left:84px;top:110px;">
        <div style="font-size:70px;font-weight:900;color:{GRAFITE};">O QUE GUARDAR</div>
        {risco()}
      </div>
      <div style="position:absolute;left:84px;top:320px;width:520px;color:#4A4744;font-size:32px;line-height:1.6;">
        <p>No Guarde Tudo você pode armazenar <b>de A a Z, do pequeno ao
        grande</b>, de muito a pouco.</p>
        <p style="margin-top:30px;">De cadeira a barco, de estoque a arquivo
        morto, de malas a bicicletas.</p>
        <p style="margin-top:30px;font-size:27px;color:#77746F;">Só não permitimos armazenagem de
        combustíveis, explosivos, perecíveis, produtos ilícitos e de alto
        valor agregado.</p>
      </div>
      <div style="position:absolute;right:70px;top:320px;width:360px;display:grid;grid-template-columns:1fr 1fr;gap:24px;">
        {obj("sofa", "Móveis")}
        {obj("doc", "Documentos")}
        {obj("caixa", "Estoques")}
        {obj("grade", "Coleções")}
      </div>
      <div style="position:absolute;left:84px;right:84px;top:1030px;background:{VERDE_NOITE};color:#fff;border-radius:34px;padding:30px 40px;text-align:center;font-size:31px;">
        <b style="color:{VERDE_CLARO};">Temos espaço para tudo!</b> &nbsp;Boxes de 4 a 1.000 m²
      </div>
      {pagina_pill(3)}
    </div>'''
    return pagina("Carrossel 3/6 — O que guardar", corpo, 1080, 1350)


def carrossel_04():
    itens = ["Para pessoa física e jurídica", "Segurança 24 horas",
             "Espaços flexíveis e higienizados", "Área coberta para carga e descarga",
             "Excelente localização", "Locação sem avalista e fiador",
             "Prazos flexíveis", "Total privacidade e sigilo"]
    lista = "".join(f'<div style="margin-top:26px;">{check_item(t)}</div>' for t in itens)
    corpo = f'''<div class="canvas" style="{FUNDO_NOITE}">
      {ruido(.05)}
      <div style="position:absolute;right:-140px;top:340px;opacity:.9;filter:drop-shadow(0 30px 70px rgba(0,0,0,.5));">
        <svg viewBox="0 0 100 100" width="520">{cubo("#0F1A08", top="#F4F2EC", left=VERDE_CLARO, right="#6FB427", sw=5)}</svg>
      </div>
      <div style="position:absolute;left:84px;top:110px;">
        <div style="font-size:70px;font-weight:900;color:#fff;">INFRAESTRUTURA</div>
        {risco(VERDE_CLARO)}
      </div>
      <div style="position:absolute;left:84px;top:300px;width:700px;">{lista}</div>
      <div style="position:absolute;right:64px;bottom:110px;">{logo("escuro", 185)}</div>
      {pagina_pill(4, escuro=False)}
    </div>'''
    return pagina("Carrossel 4/6 — Infraestrutura", corpo, 1080, 1350)


def carrossel_05():
    corpo = f'''<div class="canvas" style="{FUNDO_CREME}">
      {marca_dagua(VERDE, 700, "right:-260px;bottom:-220px;opacity:.10;")}
      {ruido(.035)}
      <div style="position:absolute;left:0;right:0;top:150px;display:flex;justify-content:center;">
        <div style="width:190px;height:190px;border-radius:50%;border:5px solid {VERDE};display:flex;align-items:center;justify-content:center;background:#fff;box-shadow:0 24px 50px rgba(60,90,20,.15);">{icone("wifi", 100, VERDE_ESCURO)}</div>
      </div>
      <div style="position:absolute;left:80px;right:80px;top:420px;text-align:center;color:{GRAFITE};">
        <div style="font-size:66px;font-weight:900;line-height:1.25;">SALA DE REUNIÕES<br>COM WI-FI</div>
        <div style="margin-top:14px;font-size:40px;font-weight:900;color:{VERDE_ESCURO};letter-spacing:3px;">PARA CLIENTES</div>
        <div style="display:flex;justify-content:center;">{risco()}</div>
        <div style="margin-top:40px;font-size:32px;color:#4A4744;line-height:1.6;max-width:760px;margin-left:auto;margin-right:auto;">
          Precisa receber um cliente, assinar um contrato ou trabalhar
          perto do seu estoque? Aqui a sua empresa tem uma
          <b>estrutura de apoio completa</b>, sem custo extra.
        </div>
      </div>
      <div style="position:absolute;left:0;right:0;top:1010px;display:flex;justify-content:center;gap:20px;">
        <div style="border:3px solid {VERDE};color:{VERDE_ESCURO};border-radius:44px;padding:12px 32px;font-size:28px;font-weight:700;">Wi-Fi liberado</div>
        <div style="border:3px solid {VERDE};color:{VERDE_ESCURO};border-radius:44px;padding:12px 32px;font-size:28px;font-weight:700;">agende com o time</div>
      </div>
      {pagina_pill(5)}
    </div>'''
    return pagina("Carrossel 5/6 — Sala de reuniões", corpo, 1080, 1350)


def carrossel_06():
    def contato(ic, txt):
        return f'''<div style="display:flex;align-items:center;gap:24px;margin-top:28px;">
          <div style="flex:0 0 60px;height:60px;border-radius:50%;border:3px solid {VERDE_CLARO};display:flex;align-items:center;justify-content:center;">{icone(ic, 30, VERDE_CLARO)}</div>
          <div style="color:#fff;font-size:33px;">{txt}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="{FUNDO_NOITE}">
      {marca_dagua("#FFFFFF", 620, "right:-220px;bottom:-180px;opacity:.05;")}
      {ruido(.05)}
      <div style="position:absolute;right:64px;top:56px;">{logo("escuro", 195)}</div>
      <div style="position:absolute;left:84px;top:130px;">
        <div style="font-size:72px;font-weight:900;color:#fff;line-height:1.2;">SOLICITE UM<br><span style="color:{VERDE_CLARO};">ORÇAMENTO</span></div>
        {risco(VERDE_CLARO)}
      </div>
      <div style="position:absolute;left:84px;top:420px;width:850px;">
        {contato("fone", "31 3288.1555")}
        {contato("zap", "<b>31 9.8446.6482</b>")}
        {contato("mail", EMAIL)}
        {contato("globo", "guardetudobh.com.br")}
        {contato("pin", "Rua dos Moicanos, 512 | Olhos d'Água<br>Belo Horizonte | MG | CEP 30.390-050")}
        {contato("insta", "<b>@guardetudobh</b>")}
        {contato("face", "/guardetudobh")}
      </div>
      <div style="position:absolute;left:84px;bottom:120px;color:rgba(255,255,255,.65);font-size:28px;font-style:italic;">
        Salve este post e chame a gente quando precisar de espaço. 💚
      </div>
      {pagina_pill(6, escuro=False)}
    </div>'''
    return pagina("Carrossel 6/6 — Contato", corpo, 1080, 1350)


# ---------------------------------------------------------------- panfleto

def panfleto():
    hexagono = "polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%)"

    def infra_item(ic, txt):
        return f'''<div style="display:flex;align-items:center;gap:4.2mm;">
          <div style="flex:0 0 9.5mm;height:9.5mm;border-radius:50%;background:{VERDE};display:flex;align-items:center;justify-content:center;">{icone(ic, 19)}</div>
          <div style="font-size:3.7mm;color:{GRAFITE};line-height:1.25;">{txt}</div>
        </div>'''

    def tam_chip(letra, faixa):
        return f'''<div style="text-align:center;">
          <div style="width:13mm;height:13mm;margin:0 auto;border-radius:50%;background:{VERDE};color:#fff;font-weight:900;font-size:6.5mm;display:flex;align-items:center;justify-content:center;">{letra}</div>
          <div style="font-size:3.5mm;font-weight:900;color:{GRAFITE};margin-top:1.6mm;">{faixa}</div>
        </div>'''

    corpo = f'''<div class="pagina">
      <!-- faixa superior verde com curva -->
      <div style="position:absolute;left:0;top:0;right:0;height:74mm;background:linear-gradient(120deg,{VERDE_CLARO},{VERDE} 60%,#6cb31f);border-radius:0 0 0 55mm;"></div>
      {marca_dagua(tam=340, css="right:-28mm;top:-20mm;opacity:.18;")}
      <div style="position:absolute;left:12mm;top:10mm;">{selo(92)}</div>
      <div style="position:absolute;left:47mm;top:12mm;right:12mm;color:#fff;">
        <div style="font-size:9.4mm;font-weight:900;font-style:italic;line-height:1.16;letter-spacing:.2mm;">
          FLEXIBILIDADE E SEGURANÇA<br>PARA GUARDAR O QUE PRECISAR!
        </div>
        <div style="margin-top:4mm;font-size:4.1mm;line-height:1.5;max-width:120mm;">
          O <b>Guarde Tudo</b> é um self storage com soluções para a autogestão de espaços.
          Locação simplificada, <b>sem fiador ou avalista</b>, com comodidade e privacidade
          para sentir que o box é parte da sua casa ou do seu negócio.
        </div>
      </div>

      <!-- coluna esquerda: infraestrutura -->
      <div style="position:absolute;left:12mm;top:84mm;width:92mm;">
        <div style="font-size:5.6mm;font-weight:900;color:{GRAFITE};border-left:2.2mm solid {VERDE};padding-left:3.5mm;letter-spacing:.4mm;">INFRAESTRUTURA</div>
        <div style="display:flex;flex-direction:column;gap:3.6mm;margin-top:5mm;">
          {infra_item("camera", "<b>Segurança 24 horas</b> e proteção individual por box")}
          {infra_item("cadeado", "<b>Total privacidade e sigilo:</b> o acesso é só seu")}
          {infra_item("grade", "<b>+40 opções de boxes</b> para pessoa física e jurídica")}
          {infra_item("relogio", "<b>Prazos flexíveis</b> e locação sem avalista e fiador")}
          {infra_item("brilho", "<b>Espaços flexíveis e higienizados</b>")}
          {infra_item("caixa", "<b>Área coberta</b> para carga e descarga")}
          {infra_item("wifi", "<b>Sala de reuniões com Wi-Fi</b> para clientes")}
          {infra_item("pin", "<b>Excelente localização:</b> a 5 min do BH Shopping")}
        </div>
      </div>

      <!-- coluna direita: foto no hexágono + tamanhos -->
      <div style="position:absolute;right:10mm;top:82mm;width:88mm;">
        <div style="width:88mm;height:88mm;clip-path:{hexagono};background:{VERDE};display:flex;align-items:center;justify-content:center;">
          <img src="assets/casal-caixa.jpg" style="width:96%;height:96%;clip-path:{hexagono};object-fit:cover;">
        </div>
        <div style="text-align:center;font-size:4.4mm;font-weight:900;font-style:italic;color:{VERDE_ESCURO};margin-top:2.5mm;">
          De A a Z, do pequeno ao grande:<br>temos espaço para tudo!
        </div>
        <div style="margin-top:4mm;background:{CINZA};border-radius:5mm;padding:4mm 5mm;">
          <div style="font-size:4mm;font-weight:900;color:{GRAFITE};letter-spacing:.5mm;text-align:center;">TAMANHOS DOS BOXES</div>
          <div style="display:flex;justify-content:space-between;margin-top:2.5mm;padding:0 3mm;">
            {tam_chip("P", "4 a 12 m²")}
            {tam_chip("M", "13 a 24 m²")}
            {tam_chip("G", "25 a 1.000 m²")}
          </div>
        </div>
      </div>

      <!-- faixa CTA -->
      <div style="position:absolute;left:12mm;right:12mm;top:229mm;">
        <div style="text-align:center;font-size:5mm;font-weight:900;color:{GRAFITE};letter-spacing:.6mm;">SOLICITE UM ORÇAMENTO</div>
        <div style="display:flex;justify-content:center;gap:5mm;margin-top:2.8mm;">
          <div style="background:{GRAFITE};color:#fff;border-radius:12mm;padding:2.6mm 7mm;font-size:4.4mm;font-weight:700;display:flex;align-items:center;gap:2.5mm;">{icone("fone", 16)} {FONE}</div>
          <div style="background:{VERDE};color:#fff;border-radius:12mm;padding:2.6mm 7mm;font-size:4.4mm;font-weight:700;display:flex;align-items:center;gap:2.5mm;">{icone("zap", 16)} {ZAP}</div>
        </div>
        <div style="text-align:center;font-style:italic;font-size:3.5mm;color:#6b6b68;margin-top:2mm;">{EMAIL}</div>
      </div>

      <!-- rodapé -->
      <div style="position:absolute;left:0;right:0;bottom:0;height:42mm;background:{CINZA};">
        <div style="position:absolute;left:12mm;top:5mm;">{logo("cor", 150)}</div>
        <div style="position:absolute;left:68mm;top:7mm;color:{GRAFITE};font-size:3.6mm;line-height:1.75;">
          <div style="display:flex;gap:2.5mm;align-items:center;">{icone("globo", 14, VERDE_ESCURO)} guardetudobh.com.br</div>
          <div style="display:flex;gap:2.5mm;align-items:center;">{icone("pin", 14, VERDE_ESCURO)} Rua dos Moicanos, 512 | Olhos d'Água<br></div>
          <div style="margin-left:6.5mm;">Belo Horizonte | MG | CEP 30.390-050</div>
          <div style="display:flex;gap:2.5mm;align-items:center;">{icone("insta", 14, VERDE_ESCURO)} <b>@guardetudobh</b>&nbsp;&nbsp;{icone("face", 14, VERDE_ESCURO)} /guardetudobh</div>
        </div>
        <div style="position:absolute;right:12mm;top:5.5mm;text-align:center;">
          <img src="assets/qr-site.png" style="width:26mm;height:26mm;border:1.2mm solid #fff;border-radius:2mm;">
          <div style="font-size:3mm;font-weight:700;color:{GRAFITE};margin-top:1.2mm;">Aponte a câmera<br>e visite o site</div>
        </div>
      </div>
    </div>'''
    extra = '''
    @page { size: A4; margin: 0; }
    .pagina { width:210mm; height:297mm; position:relative; overflow:hidden; background:#fff; }
    .marca-dagua { position:absolute; pointer-events:none; }'''
    return f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Panfleto Guarde Tudo</title>
<style>{css_base(extra)}</style></head>
<body>{corpo}</body></html>'''


# ---------------------------------------------------------------- build

ARTES = {
    "posts/html/feed-01-o-que-e-self-storage.html": (post_01, 1080, 1350),
    "posts/html/feed-02-mudou-faltou-espaco.html": (post_02, 1080, 1350),
    "posts/html/feed-03-para-empresas.html": (post_03, 1080, 1350),
    "posts/html/feed-04-infraestrutura.html": (post_04, 1080, 1350),
    "posts/html/feed-05-tamanhos-boxes.html": (post_05, 1080, 1350),
    "posts/html/feed-06-indique-um-amigo.html": (post_06, 1080, 1350),
    "posts/html/story-01-venha-conhecer.html": (story_01, 1080, 1920),
    "posts/carrossel/html/slide-1-capa.html": (carrossel_01, 1080, 1350),
    "posts/carrossel/html/slide-2-quem-somos.html": (carrossel_02, 1080, 1350),
    "posts/carrossel/html/slide-3-o-que-guardar.html": (carrossel_03, 1080, 1350),
    "posts/carrossel/html/slide-4-infraestrutura.html": (carrossel_04, 1080, 1350),
    "posts/carrossel/html/slide-5-sala-reunioes.html": (carrossel_05, 1080, 1350),
    "posts/carrossel/html/slide-6-contato.html": (carrossel_06, 1080, 1350),
}

CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
FLAGS = ["--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--virtual-time-budget=4000"]


def gerar_qr():
    import qrcode
    qr = qrcode.QRCode(border=1, box_size=10,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data("https://guardetudobh.com.br")
    qr.make(fit=True)
    img = qr.make_image(fill_color=GRAFITE, back_color="white")
    dest = os.path.join(RAIZ, "panfleto", "assets", "qr-site.png")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)


def main():
    render = "--render" in sys.argv

    for rel, (fn, w, h) in ARTES.items():
        caminho = os.path.join(RAIZ, rel)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w") as f:
            f.write(fn())
        print("html:", rel)
        if render:
            png = caminho.replace("/html/", "/png/").replace(".html", ".png")
            os.makedirs(os.path.dirname(png), exist_ok=True)
            subprocess.run([CHROME, *FLAGS, f"--window-size={w},{h}",
                            f"--screenshot={png}", f"file://{caminho}"],
                           check=True, capture_output=True)
            print("png :", os.path.relpath(png, RAIZ))

    pan = os.path.join(RAIZ, "panfleto", "panfleto-a4.html")
    os.makedirs(os.path.dirname(pan), exist_ok=True)
    with open(pan, "w") as f:
        f.write(panfleto())
    print("html: panfleto/panfleto-a4.html")
    if render:
        gerar_qr()
        subprocess.run([CHROME, *FLAGS, "--no-pdf-header-footer",
                        f"--print-to-pdf={pan.replace('.html', '.pdf')}",
                        f"file://{pan}"], check=True, capture_output=True)
        subprocess.run([CHROME, *FLAGS, "--force-device-scale-factor=1.6",
                        "--window-size=794,1123",
                        f"--screenshot={os.path.join(RAIZ, 'panfleto', 'panfleto-preview.png')}",
                        f"file://{pan}"], check=True, capture_output=True)
        print("pdf : panfleto/panfleto-a4.pdf")


if __name__ == "__main__":
    main()
