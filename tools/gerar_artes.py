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


def pendente(altura=170, selo_diam=104, cor_linha="#FFFFFF"):
    """Linha vertical com o selo do cubo pendurado."""
    return f'''<div style="display:flex;flex-direction:column;align-items:center;">
      <div style="width:9px;height:{altura}px;background:{cor_linha};"></div>
      <div style="margin-top:-6px;">{selo(selo_diam, fundo=cor_linha, faces=False,
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


# ---------------------------------------------------------------- posts

def rodape_post(claro=False):
    """Rodapé padrão dos posts: site à esquerda, logo à direita."""
    cor_site = "rgba(255,255,255,.95)" if not claro else GRAFITE
    return f'''
    <div style="position:absolute;left:64px;bottom:56px;font-weight:700;font-size:27px;color:{cor_site};">
      <b>guardetudobh</b><span style="opacity:.75;">.com.br</span>
    </div>
    <div style="position:absolute;right:56px;bottom:34px;">{logo("cor" if claro else "branco", 210)}</div>'''


def post_01():
    corpo = f'''<div class="canvas" style="background:linear-gradient(160deg,{VERDE_CLARO} 0%,{VERDE} 45%,#6ab31f 100%);">
      {marca_dagua(tam=820, css="left:-300px;top:330px;")}
      {marca_dagua(tam=420, css="right:-140px;top:-90px;opacity:.2;")}
      <div style="position:absolute;left:0;right:0;top:0;display:flex;justify-content:center;">{pendente(200)}</div>
      <div style="position:absolute;left:80px;right:80px;top:520px;text-align:center;color:#fff;">
        <div style="font-size:64px;font-weight:300;font-style:italic;">Afinal, o que é</div>
        <div style="font-size:124px;font-weight:900;letter-spacing:4px;line-height:1.04;margin-top:14px;">SELF<br>STORAGE?</div>
        <div style="margin:56px auto 0;max-width:760px;font-size:36px;font-weight:400;line-height:1.45;">
          Um box <b>individual, seguro e flexível</b> para guardar o que não cabe
          na sua casa ou na sua empresa. Vem entender &rarr;
        </div>
      </div>
      {rodape_post()}
    </div>'''
    return pagina("O que é Self Storage — Guarde Tudo", corpo, 1080, 1350)


def post_02():
    tarja = (f'<span style="background:{VERDE};color:#fff;padding:6px 22px;'
             f'box-decoration-break:clone;-webkit-box-decoration-break:clone;">')
    corpo = f'''<div class="canvas" style="background:linear-gradient(150deg,#f4f4f4,{CINZA});">
      {marca_dagua(VERDE, 900, "left:-330px;bottom:-260px;opacity:.25;")}
      {marca_dagua(GRAFITE, 360, "right:-110px;top:200px;opacity:.08;")}
      <div style="position:absolute;right:120px;top:0;">{pendente(150, cor_linha=VERDE)}</div>
      <div style="position:absolute;left:84px;top:400px;color:{GRAFITE};">
        <div style="font-size:110px;font-weight:900;line-height:1.12;letter-spacing:2px;">
          MUDOU E<br>FALTOU<br>ESPAÇO?
        </div>
        <div style="margin-top:54px;font-size:66px;font-weight:900;letter-spacing:3px;line-height:1.35;">
          {tarja}ARMAZENE AQUI!</span>
        </div>
        <div style="margin-top:52px;font-size:34px;font-weight:400;max-width:660px;line-height:1.45;">
          Boxes de <b>4 a 1.000&nbsp;m²</b>, sem fiador e sem burocracia,
          pelo tempo que você precisar.
        </div>
      </div>
      {rodape_post(claro=True)}
    </div>'''
    return pagina("Mudou e faltou espaço — Guarde Tudo", corpo, 1080, 1350)


def post_03():
    def card(ic, titulo, sub):
        return f'''<div style="background:#fff;border-radius:26px;padding:38px 42px;display:flex;align-items:center;gap:34px;box-shadow:0 10px 24px rgba(0,0,0,.10);">
          <div style="flex:0 0 92px;height:92px;border-radius:50%;background:{VERDE};display:flex;align-items:center;justify-content:center;">{icone(ic, 48)}</div>
          <div><div style="font-size:40px;font-weight:900;color:{GRAFITE};">{titulo}</div>
          <div style="font-size:29px;color:#6b6b68;margin-top:4px;">{sub}</div></div>
        </div>'''
    corpo = f'''<div class="canvas" style="background:linear-gradient(165deg,{VERDE_CLARO},{VERDE} 55%,#68b01e);">
      {marca_dagua(tam=780, css="right:-280px;top:-160px;")}
      <div style="position:absolute;left:84px;top:96px;color:#fff;max-width:900px;">
        <div style="font-size:40px;font-weight:700;letter-spacing:6px;">PARA PESSOA JURÍDICA</div>
        <div style="font-size:88px;font-weight:900;line-height:1.12;margin-top:18px;">
          SUA EMPRESA<br>PRECISA DE ESPAÇO?
        </div>
      </div>
      <div style="position:absolute;left:84px;right:84px;top:470px;display:flex;flex-direction:column;gap:30px;">
        {card("caixa", "Estoque e mercadorias", "Espaço que cresce junto com as vendas")}
        {card("doc", "Documentos e arquivo morto", "Organização com sigilo e controle de acesso")}
        {card("sofa", "Móveis e equipamentos", "Guarde a estrutura entre projetos e reformas")}
      </div>
      <div style="position:absolute;left:84px;bottom:170px;background:{GRAFITE};color:#fff;border-radius:60px;padding:24px 44px;display:flex;align-items:center;gap:20px;font-size:33px;font-weight:700;">
        {icone("zap", 40)} Solicite um orçamento &middot; {ZAP}
      </div>
      {rodape_post()}
    </div>'''
    return pagina("Para empresas — Guarde Tudo", corpo, 1080, 1350)


def post_04():
    def chip(ic, txt):
        return f'''<div style="display:flex;align-items:center;gap:26px;background:rgba(56,52,53,.92);border-radius:60px;padding:20px 46px 20px 24px;">
          <div style="flex:0 0 72px;height:72px;border-radius:50%;background:{VERDE};display:flex;align-items:center;justify-content:center;">{icone(ic, 40)}</div>
          <div style="color:#fff;font-size:44px;font-weight:700;"><span style="color:{VERDE_CLARO};font-weight:900;">+</span> {txt}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="background:linear-gradient(160deg,{VERDE_CLARO},{VERDE} 50%,#66ae1d);">
      {marca_dagua(tam=860, css="left:-330px;bottom:-230px;")}
      <div style="position:absolute;right:110px;top:0;">{pendente(120)}</div>
      <div style="position:absolute;left:84px;top:110px;color:#fff;">
        <div style="font-size:82px;font-weight:900;line-height:1.15;">INFRAESTRUTURA<br>COMPLETA:</div>
      </div>
      <div style="position:absolute;left:84px;top:420px;display:flex;flex-direction:column;gap:26px;">
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
        return f'''<div style="flex:1;background:#fff;border-radius:28px;padding:44px 26px 38px;text-align:center;box-shadow:0 10px 24px rgba(0,0,0,.10);">
          <div style="width:118px;height:118px;margin:0 auto;border-radius:50%;background:{VERDE};color:#fff;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center;">{letra}</div>
          <div style="font-size:44px;font-weight:900;color:{GRAFITE};margin-top:26px;">{faixa}</div>
          <div style="font-size:27px;color:#6b6b68;margin-top:14px;line-height:1.4;">{exemplos}</div>
        </div>'''
    tarja = (f'<span style="background:{GRAFITE};color:#fff;padding:8px 26px;'
             f'box-decoration-break:clone;-webkit-box-decoration-break:clone;">')
    corpo = f'''<div class="canvas" style="background:linear-gradient(150deg,#f6f6f6,{CINZA});">
      {marca_dagua(VERDE, 760, "right:-260px;top:-200px;opacity:.22;")}
      <div style="position:absolute;left:84px;right:84px;top:120px;text-align:center;color:{GRAFITE};">
        <div style="font-size:56px;font-weight:400;">De <b>A a Z</b>, do pequeno ao <b>GRANDE:</b></div>
        <div style="margin-top:30px;font-size:64px;font-weight:900;letter-spacing:2px;">{tarja}TEMOS ESPAÇO PARA TUDO!</span></div>
      </div>
      <div style="position:absolute;left:70px;right:70px;top:470px;">
        <div style="text-align:center;font-size:34px;font-weight:700;color:{GRAFITE};letter-spacing:5px;margin-bottom:34px;">TAMANHOS DOS BOXES</div>
        <div style="display:flex;gap:28px;">
          {card("P", "4 a 12 m²", "Caixas, malas,<br>documentos, bicicletas")}
          {card("M", "13 a 24 m²", "Mudanças, móveis,<br>pequenos estoques")}
          {card("G", "25 a 1.000 m²", "Estoques, maquinário,<br>operações inteiras")}
        </div>
      </div>
      <div style="position:absolute;left:0;right:0;bottom:190px;text-align:center;font-size:33px;color:{GRAFITE};">
        Box dimensionado sob medida &middot; contrato flexível &middot; <b>sem fiador</b>
      </div>
      {rodape_post(claro=True)}
    </div>'''
    return pagina("Tamanhos dos boxes — Guarde Tudo", corpo, 1080, 1350)


def post_06():
    def bloco(t1, t2):
        return f'''<div style="flex:1;background:#fff;border:5px solid {VERDE};border-radius:30px;padding:40px 34px;text-align:center;">
          <div style="font-size:52px;font-weight:900;color:{GRAFITE};line-height:1.2;">{t1}</div>
          <div style="font-size:34px;font-weight:700;font-style:italic;color:{VERDE_ESCURO};margin-top:16px;line-height:1.3;">{t2}</div>
        </div>'''
    corpo = f'''<div class="canvas" style="background:#fff;">
      <div style="position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient(120deg,{VERDE_CLARO},{VERDE});border-radius:0 0 60% 60%/0 0 120px 120px;"></div>
      {marca_dagua(VERDE, 700, "left:-260px;bottom:-180px;opacity:.14;")}
      <div style="position:absolute;left:0;right:0;top:72px;text-align:center;color:#fff;">
        <div style="font-size:44px;font-weight:700;font-style:italic;letter-spacing:14px;">P R O M O Ç Ã O</div>
      </div>
      <div style="position:absolute;left:0;right:0;top:210px;text-align:center;color:{GRAFITE};">
        <div style="font-size:120px;font-weight:900;line-height:1.08;">QUEM INDICA<br>AMIGO É</div>
      </div>
      <div style="position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center;">{selo(150, fundo=VERDE, faces=False, cor_cubo="#FFFFFF")}</div>
      <div style="position:absolute;left:80px;right:80px;top:770px;display:flex;gap:30px;">
        {bloco("INDIQUE<br>1 AMIGO", "você ganha<br>e ele também")}
        {bloco("DESCONTO<br>PRA CADA UM", "na próxima<br>mensalidade")}
      </div>
      <div style="position:absolute;left:0;right:0;bottom:200px;text-align:center;font-size:30px;color:#6b6b68;">
        Consulte as condições com o nosso time &darr;
      </div>
      <div style="position:absolute;left:64px;bottom:56px;display:flex;gap:16px;align-items:center;">
        <div style="background:{GRAFITE};color:#fff;border-radius:50px;padding:14px 28px;font-size:28px;font-weight:700;display:flex;gap:12px;align-items:center;">{icone("fone", 28)} {FONE}</div>
        <div style="background:{VERDE};color:#fff;border-radius:50px;padding:14px 28px;font-size:28px;font-weight:700;display:flex;gap:12px;align-items:center;">{icone("zap", 28)} {ZAP}</div>
      </div>
      <div style="position:absolute;right:56px;bottom:34px;">{logo("cor", 210)}</div>
    </div>'''
    return pagina("Indique um amigo — Guarde Tudo", corpo, 1080, 1350)


def story_01():
    corpo = f'''<div class="canvas" style="background:linear-gradient(170deg,{VERDE_CLARO},{VERDE} 45%,#63aa1c);">
      {marca_dagua(tam=900, css="left:-320px;top:1100px;")}
      <div style="position:absolute;left:0;right:0;top:0;display:flex;justify-content:center;">{pendente(190)}</div>
      <div style="position:absolute;left:80px;right:80px;top:470px;text-align:center;color:#fff;">
        <div style="font-size:52px;font-weight:300;font-style:italic;">Venha conhecer o</div>
        <div style="font-size:108px;font-weight:900;letter-spacing:3px;margin-top:8px;">GUARDE TUDO</div>
      </div>
      <div style="position:absolute;left:90px;right:90px;top:800px;background:#fff;border-radius:34px;padding:54px 48px;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.16);">
        <div style="display:flex;justify-content:center;">{icone("pin", 64, VERDE)}</div>
        <div style="font-size:40px;font-weight:900;color:{GRAFITE};margin-top:20px;line-height:1.35;">Rua dos Moicanos, 512<br>Olhos d'Água &middot; BH/MG</div>
        <div style="font-size:31px;color:#6b6b68;margin-top:18px;">a 5 minutos do BH Shopping<br>área coberta para carga e descarga</div>
      </div>
      <div style="position:absolute;left:90px;right:90px;top:1330px;background:{GRAFITE};color:#fff;border-radius:60px;padding:30px 40px;display:flex;align-items:center;justify-content:center;gap:20px;font-size:37px;font-weight:900;">
        {icone("zap", 44)} CHAMA NO WHATS &middot; {ZAP}
      </div>
      <div style="position:absolute;left:0;right:0;bottom:170px;text-align:center;color:#fff;font-size:33px;font-weight:700;">
        {INSTA} &middot; guardetudobh.com.br
      </div>
      <div style="position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;">{logo("branco", 220)}</div>
    </div>'''
    return pagina("Story Visite — Guarde Tudo", corpo, 1080, 1920)


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
