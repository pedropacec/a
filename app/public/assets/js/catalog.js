/* =============================================================
   VÈSSE CLUB — catalog.js (o Shopify fake)
   Porte Shopify (seção 9): produtos reais; `code` → campo vendor;
   `siblings` → metafield; print/type/material/gender → metafields
   de faceta. Metafields a criar já: Categoria · Cor · Material ·
   Estampa · Gênero.
   Tags operacionais NUNCA vazam em superfície — no Shopify real,
   mantê-las privadas.
   ============================================================= */

/* Estampas REAIS da casa (catálogo vivo + drop Divine Therapy):
   Directed By · Divine Therapy · Therapy Bureau · Vèsse Records ·
   Shields · Vèsset · Disco Project · Forms of Hedonism            */

/* Slots de foto com significado fixo (brief do fotógrafo):
   _01 packshot frente · _02 packshot costas · _04 macro do logo/estampa
   _06 on-model frente (vestindo a peça coordenada do conjunto)
   _07 on-model costas · _08 on-model lateral/detalhe
   _09 crop de peito com rosto meio cortado.
   ORDEM ÚNICA de galeria: 01 → 06 → 07 → 08 → 09 → 04 → 02        */
var GALLERY_ORDER = ["01", "06", "07", "08", "09", "04", "02"];

/* Especificação por slot — masters de produto 2400×3000 WebP (4:5). */
var SLOT_SPECS = {
  "01": { desc: "packshot frontal, peça sem corpo, fundo seamless claro", master: "2400×3000 WebP (4:5)" },
  "02": { desc: "packshot de costas", master: "2400×3000 WebP (4:5)" },
  "04": { desc: "macro do logo/estampa com textura de costura", master: "2400×3000 WebP (4:5)" },
  "06": { desc: "on-model corpo inteiro, FRENTE", master: "2400×3000 WebP (4:5)" },
  "07": { desc: "on-model corpo inteiro, COSTAS", master: "2400×3000 WebP (4:5)" },
  "08": { desc: "on-model pose alternativa / lateral", master: "2400×3000 WebP (4:5)" },
  "09": { desc: "crop de peito com rosto meio cortado", master: "2400×3000 WebP (4:5)" }
};

/* Regra do conjunto DENTRO da foto: nos slots _06/_07 de produto SETS,
   o modelo veste a peça junto com a peça coordenada do conjunto — o
   cross-sell acontece dentro da fotografia, antes de qualquer
   "compre junto". Produtos sem SETS: styling livre, corpo inteiro. */
function slotDesc(p, slot) {
  var spec = SLOT_SPECS[slot];
  var base = spec ? spec.desc : "imagem de campanha";
  if (slot === "06" || slot === "07") {
    if (hasTag(p, "SETS") && p.desc && p.desc.partner) {
      base += " — modelo veste a peça junto com a peça coordenada do conjunto (" + p.desc.partner + ")";
    } else {
      base += " — styling livre, sempre corpo inteiro";
    }
  }
  return base;
}

/* Stills editoriais existentes (um por módulo subcollection) —
   master 2000×2800 WebP (5:7).                                  */
var EDITORIAL_STILLS = [
  { code: "EDITORIAL-DT26", slot: "S1", page: "pages/divine-therapy.html", note: "a sessão Prescrição — o divã, o receituário, o hoodie pendurado" },
  { code: "EDITORIAL-DT26", slot: "S2", page: "pages/divine-therapy.html", note: "o balcão do Therapy Bureau, carimbo do emblema, jersey dobrado" },
  /* par full-bleed da home (substituiu o módulo Winter) */
  { code: "EDITORIAL-DUO", slot: "S1", page: "index.html", note: "par da home, imagem esquerda — a peça-assinatura em detalhe", master: "2000×2500 WebP (4:5)" },
  { code: "EDITORIAL-DUO", slot: "S2", page: "index.html", note: "par da home, imagem direita — o look no corpo, rua de BH", master: "2000×2500 WebP (4:5)" },
  /* colagem das Music Sessions — 4 fotos em tamanhos diferentes */
  { code: "EDITORIAL-MS", slot: "S1", page: "pages/vemaison.html", note: "Music Session — a pista em movimento, flash direto", master: "2400×1800 WebP (4:3)" },
  { code: "EDITORIAL-MS", slot: "S2", page: "pages/vemaison.html", note: "Music Session — retrato do público, luz baixa", master: "1500×2000 WebP (3:4)" },
  { code: "EDITORIAL-MS", slot: "S3", page: "pages/vemaison.html", note: "Music Session — a cabine, mãos no controle", master: "1600×1600 WebP (1:1)" },
  { code: "EDITORIAL-MS", slot: "S4", page: "pages/vemaison.html", note: "Music Session — a sala inteira vista de cima", master: "2400×1350 WebP (16:9)" },
  /* módulo de vídeo da home (substituiu o promo do conjunto) */
  { code: "CAMPANHA-VIDEO", slot: "V1", page: "index.html", note: "vídeo de campanha — o conjunto moletom Prescrição em movimento, a pista, o transe", master: "1920×1080 MP4 (16:9), loop 10–20s, sem áudio" }
];

/* Registro tag → badge. Merchandising cria badge aplicando tag, sem deploy.
   Sempre 12px, weight 450, não-caixa-alta, cor --badge.                  */
var BADGES = {
  "DT - D1":  { label: "Drop 01" },
  "DT - D2":  { label: "Drop 02" },
  "MEMBERS":  { label: "Members" },
  "UNISSEX":  { label: "Unissex" }
};
/* Card só badge com parcimônia: Members, ou o drop vigente. */
var CURRENT_DROP = "DT - D1";

/* Ordem do array = "Mais recentes". Tabela de preço por tipo (Pedro,
   01/08): Boné 145 · Camiseta 195 · Moletom 365. Sem centavos, nunca. */
var CATALOG = [
  {
    code: "U-DT26-TEE-101-01",
    handle: "directed-by-black-tee",
    title: "Directed By - Black Tee",
    print: "Directed By",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: ["U-DT26-TEE-101-02"],
    tags: ["DT", "DT - D1"],
    /* frente LISA por design — o print mora só nas costas */
    slots: ["01", "02", "06", "07"],
    photos: {
      "02": "assets/img/products/directed-preto-02.png",
      "07": "assets/img/products/directed-preto-07.jpg"
    },
    desc: {
      adj: "clássico", where: "nas costas",
      details: ["frente lisa", "gola canelada", "lettering serifado em serigrafia", "costura dupla na barra"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Lettering Directed By nas costas, frente lisa",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  /* Boné do drop — na 2ª posição para ocupar a vaga do off-white no
     rail da home (direção do Pedro). */
  {
    code: "U-DT26-CAP-101-01",
    handle: "therapy-bureau-services-cap",
    title: "Therapy Bureau Services - Cap",
    print: "Therapy Bureau",
    type: "Boné",
    gender: "Unissex",
    material: "Sarja 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 145,
    compareAt: null,
    sizes: { "Único": "in" },
    siblings: [],
    tags: ["DT", "DT - D1"],
    slots: ["01", "02", "06", "08"],
    photos: {
      "01": "assets/img/products/bureau-cap-01.png"
    },
    desc: {
      adj: "clássico", where: "no painel frontal",
      details: ["bordado Therapy Bureau Services", "a jam production sublinhado", "seis gomos", "fecho ajustável"],
      partner: null
    },
    bullets: {
      fabric: "Sarja firme de algodão", comp: "100% algodão",
      signature: "Therapy Bureau Services — a jam production",
      care: "Limpar com pano macio e seco", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-DT26-TEE-102-01",
    handle: "divine-therapy-tee",
    title: "Divine Therapy - Tee",
    print: "Divine Therapy",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: [],
    tags: ["DT", "DT - D1"],
    slots: ["01", "02", "04", "06", "07"],
    /* frente: monograma È no peito · costas: lettering Divine Therapy */
    photos: {
      "01": "assets/img/products/dt-tee-01.png",
      "02": "assets/img/products/dt-tee-02.png",
      "04": "assets/img/products/dt-tee-04.jpg"
    },
    desc: {
      adj: "descontraído", where: "nas costas",
      details: ["monograma È no peito", "lettering cromado desenhado à mão", "frase do consultório em tipografia de máquina", "gola canelada"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "È no peito, Divine Therapy nas costas",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-DT26-HDY-101-01",
    handle: "divine-therapy-hoodie",
    title: "Divine Therapy - Hoodie",
    print: "Divine Therapy",
    type: "Moletom",
    gender: "Unissex",
    material: "Moletom 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 365,
    compareAt: null,
    sizes: { PP: "in", P: "in", M: "in", G: "in" },
    siblings: [],
    tags: ["DT", "DT - D1"],
    slots: ["01", "02", "06", "07"],
    /* frente: "Say goodbye to your old heroes." · costas: os hippies */
    photos: {
      "01": "assets/img/products/dt-hoodie-01.png",
      "02": "assets/img/products/dt-hoodie-02.png"
    },
    desc: {
      adj: "descontraído", where: "nas costas",
      details: ["a frase de despedida dos velhos heróis no peito", "dois hippies dançando em traço contínuo", "capuz forrado duplo", "punhos e barra canelados"],
      partner: null
    },
    bullets: {
      fabric: "Moletom felpado de gramatura pesada", comp: "100% algodão",
      signature: "Say goodbye to your old heroes — os hippies nas costas",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Caimento oversized"
    }
  },
  {
    code: "U-DT26-TEE-103-01",
    handle: "vesse-records-white-tee",
    title: "Vèsse Records - White Tee",
    print: "Vèsse Records",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "branco", hex: "#FFFFFF" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: [],
    tags: ["DT", "DT - D1", "NEW"],
    slots: ["01", "02", "06", "07"],
    photos: {
      "01": "assets/img/products/records-tee-01.png",
      /* costas em 1ª (direção do Pedro, 02/08): o galleryOrder já
         promove o 02 quando existe. */
      "02": "assets/img/products/records-tee-02.png"
    },
    desc: {
      adj: "clássico", where: "no peito",
      details: ["selo Vèsse Records em vermelho", "verso Made by Music Priests", "gola canelada", "costura dupla"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Selo Vèsse Records — made by music priests",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-DT26-HDY-103-01",
    handle: "vesse-records-hoodie",
    title: "Vèsse Records - Hoodie",
    print: "Vèsse Records",
    type: "Moletom",
    gender: "Unissex",
    material: "Moletom 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 365,
    compareAt: null,
    sizes: { PP: "in", P: "in", M: "in", G: "in" },
    siblings: [],
    tags: ["DT", "DT - D1", "NEW"],
    slots: ["01", "02", "06", "07"],
    photos: {
      "01": "assets/img/products/records-hoodie-01.png",
      "02": "assets/img/products/records-hoodie-02.png"
    },
    desc: {
      adj: "descontraído", where: "nas costas",
      details: ["selo Vèsse Records no peito", "o músico da casa deitado sobre o lettering", "capuz forrado duplo", "punhos e barra canelados"],
      partner: null
    },
    bullets: {
      fabric: "Moletom felpado de gramatura pesada", comp: "100% algodão",
      signature: "Vèsse Records — made by music priests, Brazil 2026",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Caimento oversized"
    }
  },
  /* Camiseta branca do Bureau — o ? espiral no peito, a cascata de
     sentenças da sessão nas costas. Entrou no lugar da Directed By
     Off-White no rail New Arrivals (direção do Pedro, 01/08). */
  {
    code: "U-DT26-TEE-104-01",
    handle: "therapy-bureau-services-tee",
    title: "Therapy Bureau Services - Tee",
    print: "Therapy Bureau",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "branco", hex: "#FFFFFF" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: [],
    tags: ["DT", "DT - D1", "NEW"],
    slots: ["01", "02", "06", "07"],
    photos: {
      "01": "assets/img/products/bureau-tee-01.png",
      "02": "assets/img/products/bureau-tee-02.png"
    },
    desc: {
      adj: "clássico", where: "nas costas",
      details: ["o ? espiral do Bureau no peito", "cascata de sentenças da sessão em serigrafia", "selo Therapy Bureau Services — a Jam Production", "gola canelada com costura dupla"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Session length: 6 hours — insurance not accepted",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-DT26-TEE-101-02",
    handle: "directed-by-off-white-tee",
    title: "Directed By - Off-White Tee",
    print: "Directed By",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "off-white", hex: "#F2EEE4" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: ["U-DT26-TEE-101-01"],
    /* Saiu do New Arrivals — a vaga é da Therapy Bureau Services Tee
       (direção do Pedro, 01/08). */
    tags: ["DT", "DT - D1"],
    slots: ["01", "02", "06", "07"],
    photos: {
      "02": "assets/img/products/directed-offwhite-02.png"
    },
    desc: {
      adj: "clássico", where: "nas costas",
      details: ["gola canelada", "lettering serifado em serigrafia", "costura dupla na barra", "etiqueta interna macia"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Lettering Directed By nas costas",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  /* Boné Vèsse Records — fecha o rail New Arrivals. */
  {
    code: "U-DT26-CAP-102-01",
    handle: "vesse-records-cap",
    title: "Vèsse Records - Cap",
    print: "Vèsse Records",
    type: "Boné",
    gender: "Unissex",
    material: "Sarja 100% algodão",
    colors: [{ name: "branco", hex: "#FFFFFF" }, { name: "preto", hex: "#1C1C1C" }],
    price: 145,
    compareAt: null,
    sizes: { "Único": "in" },
    siblings: [],
    tags: ["DT", "DT - D1", "NEW"],
    slots: ["01", "02", "06", "08"],
    photos: {
      "01": "assets/img/products/records-cap-01.png"
    },
    desc: {
      adj: "clássico", where: "no painel frontal",
      details: ["bordado tridimensional Vèsse Records", "copa branca com aba preta", "seis gomos", "fecho ajustável"],
      partner: null
    },
    bullets: {
      fabric: "Sarja firme de algodão", comp: "100% algodão",
      signature: "Vèsse Records bordado em relevo, duas cores",
      care: "Limpar com pano macio e seco", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-VT25-TEE-001-01",
    handle: "vesset-2025-tee",
    title: "Vèsset 2025 - White Tee",
    print: "Vèsset",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "branco", hex: "#FFFFFF" }],
    price: 195,
    compareAt: null,
    sizes: { P: "in", M: "in", G: "in" },
    siblings: ["U-VT25-TEE-001-02"],
    tags: ["ESSENCIAIS"],
    slots: ["01", "02", "06", "07"],
    /* `cover`: slot que ABRE o card e a galeria — a foto de PRODUTO
       (packshot), nunca a editorial (direção do Pedro, 01/08). Nos
       5 produtos da loja viva as fotos 02/06/07 são de campanha. */
    cover: "01",
    photos: {
      "01": "assets/img/products/vesset-white-01.webp",
      "02": "assets/img/products/vesset-white-02.webp",
      "06": "assets/img/products/vesset-white-06.webp",
      "07": "assets/img/products/vesset-white-07.webp"
    },
    desc: {
      adj: "clássico", where: "no peito",
      details: ["a tee de estreia da casa", "gola canelada", "costura dupla", "etiqueta interna macia"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Estampa Vèsset 2025 — a primeira da casa",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-VT25-TEE-001-02",
    handle: "vesset-2025-black-tee",
    title: "Vèsset 2025 - Black Tee",
    print: "Vèsset",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 195,
    compareAt: null,
    sizes: { P: "out", M: "out", G: "out" },
    siblings: ["U-VT25-TEE-001-01"],
    tags: ["ESSENCIAIS"],
    slots: ["01", "02", "06", "07"],
    cover: "01",
    photos: {
      "01": "assets/img/products/vesset-black-01.webp",
      "02": "assets/img/products/vesset-black-02.webp",
      "06": "assets/img/products/vesset-black-06.webp",
      "07": "assets/img/products/vesset-black-07.webp"
    },
    desc: {
      adj: "clássico", where: "no peito",
      details: ["a tee de estreia da casa", "gola canelada", "costura dupla", "etiqueta interna macia"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Estampa Vèsset 2025 — a primeira da casa",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-VT25-HDY-001-01",
    handle: "vesse-club-disco-project-moletom",
    title: "Disco Project - Hoodie",
    print: "Disco Project",
    type: "Moletom",
    gender: "Unissex",
    material: "Moletom 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 365,
    compareAt: null,
    sizes: { PP: "out", P: "out", M: "out", G: "out" },
    siblings: [],
    tags: ["ESSENCIAIS"],
    slots: ["01", "02", "06", "07"],
    cover: "01",
    photos: {
      "01": "assets/img/products/disco-hoodie-01.webp",
      "02": "assets/img/products/disco-hoodie-02.webp",
      "06": "assets/img/products/disco-hoodie-06.webp",
      "07": "assets/img/products/disco-hoodie-07.webp"
    },
    desc: {
      adj: "descontraído", where: "nas costas",
      details: ["capuz forrado duplo", "bolso canguru", "punhos e barra canelados", "costuras reforçadas"],
      partner: null
    },
    bullets: {
      fabric: "Moletom felpado de gramatura pesada", comp: "100% algodão",
      signature: "Estampa Disco Project da casa",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Caimento oversized"
    }
  },
  {
    code: "U-VT25-TEE-002-01",
    handle: "vesse-club-disco-project-camisa",
    title: "Disco Project - Black Tee",
    print: "Disco Project",
    type: "Camiseta",
    gender: "Unissex",
    material: "Jersey 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 195,
    compareAt: null,
    sizes: { P: "out", M: "out", G: "out" },
    siblings: [],
    tags: ["ESSENCIAIS"],
    slots: ["01", "02", "06", "07"],
    cover: "01",
    photos: {
      "01": "assets/img/products/disco-tee-01.webp",
      "02": "assets/img/products/disco-tee-02.webp",
      "06": "assets/img/products/disco-tee-06.webp",
      "07": "assets/img/products/disco-tee-07.webp"
    },
    desc: {
      adj: "descontraído", where: "no peito",
      details: ["gola canelada", "reforço de ombro a ombro", "costura dupla", "barra reta"],
      partner: null
    },
    bullets: {
      fabric: "Jersey penteado de toque seco", comp: "100% algodão",
      signature: "Estampa Disco Project da casa",
      care: "Lavagem delicada à máquina", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  },
  {
    code: "U-VT25-CAP-001-01",
    handle: "sem-titulo-12dejun-_13-46",
    title: "Forms of Hedonism - Cap",
    print: "Forms of Hedonism",
    type: "Boné",
    gender: "Unissex",
    material: "Sarja 100% algodão",
    colors: [{ name: "preto", hex: "#1C1C1C" }],
    price: 145,
    compareAt: null,
    sizes: { "Único": "out" },
    siblings: [],
    tags: ["ESSENCIAIS"],
    slots: ["01", "02", "06", "08"],
    cover: "01",
    photos: {
      "01": "assets/img/products/cap-01.webp",
      "02": "assets/img/products/cap-02.webp",
      "06": "assets/img/products/cap-06.webp",
      "08": "assets/img/products/cap-08.webp"
    },
    desc: {
      adj: "clássico", where: "no painel frontal",
      details: ["seis gomos", "aba curvada", "fecho ajustável", "bordado em relevo"],
      partner: null
    },
    bullets: {
      fabric: "Sarja 100% algodão", comp: "100% algodão",
      signature: "Bordado Forms of Hedonism da casa",
      care: "Limpar com pano macio e seco", origin: "Feito no Brasil",
      fit: "Modelagem unissex, vista seu tamanho habitual"
    }
  }
];

/* ---------------- helpers de catálogo ---------------- */
function byCode(code) {
  for (var i = 0; i < CATALOG.length; i++) if (CATALOG[i].code === code) return CATALOG[i];
  return null;
}
function isA71(p) { return p.tags.indexOf("A71") !== -1; }
function hasTag(p, t) { return p.tags.indexOf(t) !== -1; }
/* Preço sem decimais, sempre: "R$ 390" */
function fmtPrice(n) { return "R$ " + n; }
function colorwayCount(p) { return 1 + p.siblings.length; }
function typePlural(t) {
  var map = { "Camiseta": "Camisetas", "Moletom": "Moletons", "Calça": "Calças", "Shorts": "Shorts", "Boné": "Bonés", "Meia": "Meias" };
  return map[t] || t;
}

/* ---------------- vistas da PLP universal ----------------
   colecao.html?c=<vista>. Sort: "recentes" (ordem do array) |
   "menor" | "maior" | "az" (FORÇADO nas vistas conjuntos*).    */
var SEO_DEFAULT = {
  h2: "Moletons e camisetas streetwear — Vèsse Club",
  text: "A Vèsse Club confecciona streetwear em Belo Horizonte: moletons oversized, camisetas de jersey penteado, calças, shorts e bonés com as estampas da casa. Cada peça carrega a assinatura Prescrição, Bureau Emblem ou o Monograma Vè'Maison, com entrega cortesia para todo o Brasil e troca facilitada em até 30 dias."
};

var VIEWS = {
  "novidades": {
    h1: "Divine Therapy <br> Vè'Maison", desc: "",
    filter: function (p) { return !isA71(p); }, sort: "recentes",
    seo: SEO_DEFAULT,
    promos: [
      { at: 4, size: "m", title: "Divine Therapy", href: "pages/divine-therapy.html", code: "CAMPANHA-DT26", slot: "P1" },
      { at: 9, size: "line", title: "Vè'Maison", href: "pages/vemaison.html", code: "CAMPANHA-VM", slot: "P2" }
    ]
  },
  "pecas": {
    h1: "Collections <br> [VÈ]", desc: "",
    filter: function (p) { return !isA71(p); }, sort: "recentes",
    seo: SEO_DEFAULT
  },
  /* A aba Collections: UMA página com TODOS os produtos (inclusive
     arquivo) e imagens editoriais AO MEIO da grade (direção do Pedro). */
  "collections": {
    h1: "Collections", desc: "",
    filter: function () { return true; }, sort: "recentes",
    seo: SEO_DEFAULT,
    promos: [
      /* célula do monograma VÈ fechando a 1ª linha da grade */
      { at: 3, ve: true }
    ]
  },
  "divine-therapy": {
    h1: "Divine Therapy <br> Drop 01", desc: "A nova estação da casa: o consultório, o transe, a música.",
    filter: function (p) { return hasTag(p, "DT"); }, sort: "recentes",
    seo: {
      h2: "Divine Therapy — o drop streetwear da Vèsse Club",
      text: "Divine Therapy é a estação em que a casa transforma o consultório em ritual: moletons oversized, camisetas de jersey e bonés com a estampa Prescrição. Peças unissex confeccionadas no Brasil, numeradas por drop, com entrega cortesia em todos os pedidos e troca facilitada em até 30 dias para membros do Vèsse Club Members."
    },
    promos: [
      { at: 4, size: "m", title: "Divine Therapy", href: "pages/divine-therapy.html", code: "CAMPANHA-DT26", slot: "P1" }
    ]
  },
  "essenciais": {
    h1: "Essenciais <br> [VÈ]", desc: "",
    filter: function (p) { return hasTag(p, "ESSENCIAIS"); }, sort: "recentes", seo: SEO_DEFAULT
  },
  /* Rail New Arrivals da home: os 3 produtos escolhidos + o boné
     Records (tag NEW, na ordem do catálogo). */
  "new-arrivals": {
    h1: "New Arrivals <br> [VÈ]", desc: "",
    filter: function (p) { return hasTag(p, "NEW"); }, sort: "recentes", seo: SEO_DEFAULT
  },
  "members": {
    h1: "Exclusivos <br> Vèsse Club Members", desc: "",
    filter: function (p) { return hasTag(p, "MEMBERS"); }, sort: "recentes", seo: SEO_DEFAULT
  },
  "conjuntos": {
    h1: "Conjuntos <br> [VÈ]", desc: "",
    filter: function (p) { return hasTag(p, "SETS"); }, sort: "az", seo: SEO_DEFAULT
  },
  "conjuntos-moletom": {
    h1: "Conjuntos Moletom <br> [VÈ]", desc: "",
    filter: function (p) { return hasTag(p, "SETS") && p.material.indexOf("Moletom") === 0; }, sort: "az", seo: SEO_DEFAULT
  },
  "conjuntos-jersey": {
    h1: "Conjuntos Jersey <br> [VÈ]", desc: "",
    filter: function (p) { return hasTag(p, "SETS") && p.material.indexOf("Jersey") === 0; }, sort: "az", seo: SEO_DEFAULT
  },
  "pos-sessao": {
    h1: "Pós-Sessão <br> [VÈ]",
    desc: "Pós-Sessão é o que se veste depois: moletom, calça e boné desenhados para o corpo que sai do transe — conforto, movimento e a calma de quem já dançou.",
    filter: function (p) { return !isA71(p) && (p.type === "Moletom" || p.type === "Calça" || p.type === "Boné"); },
    sort: "recentes",
    seo: {
      h2: "Pós-Sessão — moletons, calças e bonés Vèsse Club",
      text: "Pós-Sessão reúne as peças de descompressão da casa: moletons felpados de gramatura pesada, calças jogger e bonés de sarja, todos confeccionados no Brasil em modelagem unissex. É o vestuário do depois — do treino, da festa, da sessão — com entrega cortesia em todos os pedidos e troca facilitada em até 30 dias."
    }
  },
  "camisetas": { h1: "Camisetas <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Camiseta"; }, sort: "recentes", seo: SEO_DEFAULT },
  "moletons": { h1: "Moletons <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Moletom"; }, sort: "recentes", seo: SEO_DEFAULT },
  "calcas": { h1: "Calças <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Calça"; }, sort: "recentes", seo: SEO_DEFAULT },
  "shorts": { h1: "Shorts <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Shorts"; }, sort: "recentes", seo: SEO_DEFAULT },
  "bones": { h1: "Bonés <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Boné"; }, sort: "recentes", seo: SEO_DEFAULT },
  "meias": { h1: "Meias <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && p.type === "Meia"; }, sort: "recentes", seo: SEO_DEFAULT },
  "acessorios": { h1: "Acessórios <br> [VÈ]", desc: "", filter: function (p) { return !isA71(p) && (p.type === "Boné" || p.type === "Meia"); }, sort: "recentes", seo: SEO_DEFAULT },
  "dt-moletons": { h1: "Divine Therapy <br> Moletons", desc: "", filter: function (p) { return hasTag(p, "DT") && p.type === "Moletom"; }, sort: "recentes", seo: SEO_DEFAULT },
  "dt-camisetas": { h1: "Divine Therapy <br> Camisetas", desc: "", filter: function (p) { return hasTag(p, "DT") && p.type === "Camiseta"; }, sort: "recentes", seo: SEO_DEFAULT },
  "dt-bones": { h1: "Divine Therapy <br> Bonés", desc: "", filter: function (p) { return hasTag(p, "DT") && p.type === "Boné"; }, sort: "recentes", seo: SEO_DEFAULT },
  "dt-exclusivos": { h1: "Divine Therapy <br> Exclusivos", desc: "", filter: function (p) { return hasTag(p, "DT") && hasTag(p, "MEMBERS"); }, sort: "recentes", seo: SEO_DEFAULT }
  /* A página/família Archive 71 foi REMOVIDA (direção do Pedro).
     As peças de arquivo (tag A71, compareAt) seguem no catálogo e
     aparecem em Collections; o was/now continua só na buy box.     */
};

/* ---------------- Complete o look: curado à mão, nunca algorítmico ----- */
var COMPLETE_LOOK = {
  "U-DT26-HDY-101-01": {
    well: { code: "CAMPANHA-LOOK-01", slot: "06" },
    cards: ["U-DT26-TEE-101-01", "U-DT26-TEE-102-01", "U-DT26-TEE-103-01", "U-DT26-HDY-103-01"]
  }
};

/* ---------------- strings compartilhadas (fonte ÚNICA) ----------------
   Footer e Therapy Bureau usam EXATAMENTE estas strings.               */
var CONTACT = {
  /* canais exibidos SÓ como ícones, sem horário (direção do Pedro) */
  /* TODO: confirmar número de WhatsApp e e-mail reais antes de publicar */
  whatsapp: "https://wa.me/5531990000000",
  email: "mailto:contato@vesseclub.com",
  instagram: "https://www.instagram.com/vesseclub",
  tiktok: "https://www.tiktok.com/@vesseclub",
  /* Conferir com o checkout real da loja antes de publicar; PIX primeiro. */
  pay: "PIX · Visa · Mastercard · Elo · American Express · Boleto"
};

/* Entrega escrita como ESPECIFICIDADE, não promessa. Escrita UMA vez;
   reusada na aba "Entrega e trocas" do drawer da PDP e no Bureau.     */
var SHIPPING_HTML =
  '<p>Todos os pedidos da Vèsse Club saem de Belo Horizonte por Correios ou Jadlog, com código de rastreio enviado por e-mail assim que a etiqueta é emitida. Pedidos confirmados até 15h em dia útil são postados no mesmo dia; depois desse horário, a postagem acontece no primeiro dia útil seguinte.</p>' +
  '<p>Prazos estimados a partir da postagem: Belo Horizonte e região metropolitana, 1 a 2 dias úteis; demais capitais e interior do Sudeste, 2 a 4 dias úteis; Sul e Centro-Oeste, 3 a 5 dias úteis; Norte e Nordeste, 5 a 9 dias úteis. Os prazos são dos transportadores e podem variar conforme a região de entrega.*</p>' +
  '<p><strong>Entrega cortesia em todos os pedidos, sem valor mínimo.</strong> Em períodos de drop, o volume de pedidos aumenta e a postagem pode levar mais tempo que o habitual — a casa avisa por e-mail quando isso acontecer.</p>' +
  '<p>Trocas: membros têm até <strong>30 dias</strong> corridos a partir do recebimento para solicitar troca de tamanho ou de peça, desde que o item esteja sem uso, com etiquetas. Além disso, vale o direito de arrependimento do Código de Defesa do Consumidor: até <strong>7 dias</strong> corridos após o recebimento para desistir da compra, com reembolso integral. Para iniciar uma troca, fale com o Therapy Bureau por WhatsApp, e-mail ou Instagram DM — a primeira postagem de troca é por conta da casa.</p>' +
  '<p>Pagamento: ' + CONTACT.pay + '. Pedidos por PIX são confirmados em minutos; boletos, em até 2 dias úteis após o pagamento.</p>' +
  '<p class="note">*Os prazos acima são estimativas dos transportadores e podem variar em datas de alta demanda.</p>';

var FAQ = [
  {
    q: "Em quanto tempo meu pedido chega?",
    a: "Pedidos confirmados até 15h em dia útil são postados no mesmo dia. A partir da postagem: 1 a 2 dias úteis em Belo Horizonte e região, 2 a 4 no Sudeste, 3 a 5 no Sul e Centro-Oeste, 5 a 9 no Norte e Nordeste."
  },
  {
    q: "Como funciona a troca?",
    a: "Membros têm até 30 dias corridos após o recebimento para trocar tamanho ou peça, com o item sem uso e com etiquetas. O direito de arrependimento do CDC garante ainda 7 dias para desistir da compra com reembolso integral. A primeira postagem de troca é por conta da casa."
  },
  {
    q: "Como escolho meu tamanho?",
    a: "Cada peça tem um guia próprio com as medidas planas em centímetros — ombro, peito e comprimento. Consulte os guias de camiseta, moletom e boné; na dúvida entre dois tamanhos, a casa recomenda o maior para as peças de caimento oversized."
  },
  {
    q: "O que é um drop?",
    a: "Cada estação da Vèsse chega em drops numerados — lotes finitos, lançados em datas próprias. Quando um drop esgota, as peças só voltam se reeditadas no arquivo da casa, com o mesmo número de estilo do lançamento."
  },
];

/* ---------------- guias de tamanho (medidas planas da PEÇA, em cm) ----- */
var SIZE_GUIDES = {
  camiseta: {
    label: "Camisetas", page: "guia-camiseta.html",
    cols: ["Tamanho", "Ombro", "Peito", "Comprimento"],
    rows: [["P", "44", "52", "70"], ["M", "46", "54", "72"], ["G", "48", "56", "74"]]
  },
  moletom: {
    label: "Moletons e bottoms", page: "guia-moletom.html",
    cols: ["Tamanho", "Ombro", "Peito", "Comprimento"],
    rows: [["P", "58", "62", "70"], ["M", "60", "64", "72"], ["G", "62", "66", "74"]]
  },
  bone: {
    label: "Bonés", page: "guia-bone.html",
    cols: ["Tamanho", "Circunferência", "Aba"],
    rows: [["Único", "56–60 (ajustável)", "7"]]
  }
};
function guideForType(t) {
  if (t === "Boné") return "bone";
  if (t === "Moletom" || t === "Calça" || t === "Shorts") return "moletom";
  return "camiseta";
}

/* Announcement bar: [promessa de serviço] → [estação].
   Sem convite ao clube aqui (muito convite = pouco valor).
   Nunca cupom, nunca countdown, nunca verbo de urgência.            */
var ANNOUNCE = [
  "Envio em até 2 dias úteis",
  "Descubra Divine Therapy"
];

/* Vèsse Club Members: exatamente 3 benefícios, nesta ordem — SEM
   convite de festa/ingresso (direção do Pedro, 01/08). O último
   NUNCA é quantificado. */
var MEMBERS_BENEFITS = [
  "Acesso antecipado ao drop",
  "Music Sessions",
  "Condições especiais"
];

/* Nav nível 1 — EXATAMENTE 4 abas (direção do Pedro), todas links
   simples para UMA página cada: Home · Divine Therapy · Collections ·
   Vèsse World. Therapy Bureau NUNCA aparece na nav de topo.        */
var NAV = [
  { label: "Home", href: "index.html" },
  { label: "Divine Therapy", href: "pages/divine-therapy.html" },
  /* Collections: leva direto à página com todos os produtos;
     o refino por categoria acontece lá (Refinar). */
  { label: "Collections", href: "colecao.html?c=collections" },
  /* Vèsse World: uma página só (vemaison, com manifesto e sessions). */
  { label: "Vèsse World", href: "pages/vemaison.html" }
];

/* Sem submenus: as 4 abas são links diretos. (Objeto mantido vazio
   porque o drawer mobile consulta MEGA[item.mega] quando existir.) */
var MEGA = {};
