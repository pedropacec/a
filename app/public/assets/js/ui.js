/* =============================================================
   VÈSSE CLUB — ui.js
   Porte Shopify (seção 9): JS do tema + cart nativo; back-in-stock
   → Klaviyo; ícone "Conta" → customer account Shopify; CTA
   "Finalizar compra" → checkout Shopify.
   ============================================================= */
/* Portão do link PROVISÓRIO (só existe nesta cópia publicada, não no
   vesse-ref local): senha simples de staging, conferida por hash no
   cliente; liberação fica no navegador. NÃO é segurança de produção. */
(function () {
  var OK = "vesse_gate_ok";
  var HASH = 2088542297;
  try { if (localStorage.getItem(OK) === "1") return; } catch (e) { return; }
  function djb2(s) {
    var h = 5381;
    for (var i = 0; i < s.length; i++) h = (h * 33 + s.charCodeAt(i)) >>> 0;
    return h;
  }
  var gate = document.createElement("div");
  gate.setAttribute("style",
    "position:fixed;inset:0;z-index:99999;background:#FFFFFF;display:flex;" +
    "align-items:center;justify-content:center;text-align:center;");
  gate.innerHTML =
    '<form style="display:grid;gap:16px;max-width:280px;width:90%;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;">' +
    '<p style="font-family:Helvetica Neue,Helvetica,Arial,sans-serif;font-size:26px;letter-spacing:.04em;color:#1C1C1C;margin:0;">V&Egrave;SSE CLUB</p>' +
    '<p style="font-size:12px;color:#6E6E6E;margin:0;">Acesso restrito &mdash; pr&eacute;via da casa.</p>' +
    '<input type="password" inputmode="numeric" autocomplete="off" placeholder="Senha" aria-label="Senha"' +
    ' style="border:1px solid #E3E3E3;border-radius:999px;padding:13px 20px;text-align:center;outline:none;font-size:15px;">' +
    '<button type="submit" style="background:#1C1C1C;color:#fff;border:0;border-radius:999px;padding:13px 20px;' +
    'font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;">Entrar</button>' +
    '<p data-err style="font-size:12px;color:#CE363C;margin:0;visibility:hidden;">Senha incorreta.</p></form>';
  function mount() {
    document.body.appendChild(gate);
    var form = gate.querySelector("form"), input = gate.querySelector("input");
    input.focus();
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (djb2(input.value) === HASH) {
        try { localStorage.setItem(OK, "1"); } catch (err) { }
        gate.remove();
      } else {
        gate.querySelector("[data-err]").style.visibility = "visible";
        input.value = "";
        input.focus();
      }
    });
  }
  if (document.body) mount();
  else document.addEventListener("DOMContentLoaded", mount);
})();
(function () {
  "use strict";

  var ROOT = document.body.getAttribute("data-root") || "";
  var PAGE = document.body.getAttribute("data-page") || "page";

  /* ---------------- utilitários ---------------- */
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function href(u) {
    if (/^(https?:|mailto:|#)/.test(u)) return u;
    return ROOT + u;
  }
  function param(name) {
    try { return new URLSearchParams(location.search).get(name); } catch (e) { return null; }
  }
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null");
      localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
  }
  function plain(html) { return html.replace(/<br\s*\/?>/gi, " ").replace(/\s+/g, " ").trim(); }
  function joinAnd(list) {
    if (list.length <= 1) return list.join("");
    return list.slice(0, -1).join(", ") + " e " + list[list.length - 1];
  }

  var ICONS = {
    burger: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M2 5h16M2 10h16M2 15h16"/></svg>',
    search: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="9" cy="9" r="6"/><path d="M13.5 13.5 18 18"/></svg>',
    account: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="10" cy="6.5" r="3.5"/><path d="M3 17.5c1.4-3.2 4-4.7 7-4.7s5.6 1.5 7 4.7"/></svg>',
    cart: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 6h12l-1 11H5L4 6Z"/><path d="M7 6a3 3 0 0 1 6 0"/></svg>',
    close: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 3l12 12M15 3 3 15"/></svg>',
    heart: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 20s-7.5-4.6-9.3-9A5.2 5.2 0 0 1 12 6.4 5.2 5.2 0 0 1 21.3 11c-1.8 4.4-9.3 9-9.3 9Z"/></svg>',
    chevron: '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.4"><path d="m5 3 4 4-4 4"/></svg>',
    instagram: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="2.5" width="15" height="15" rx="4.5"/><circle cx="10" cy="10" r="3.6"/><circle cx="14.6" cy="5.4" r=".9" fill="currentColor" stroke="none"/></svg>',
    whatsapp: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M10 3a7 7 0 0 0-6 10.6L3 17l3.5-.9A7 7 0 1 0 10 3Z"/><path d="M7.6 7.3c-.2 1.6 2.3 4.7 4.4 5.1.5.1 1.1-.2 1.3-.7l.1-.5-1.6-.8-.7.7c-.8-.4-1.8-1.4-2.2-2.2l.7-.7-.8-1.6-.5.1c-.4.1-.6.3-.7.6Z" stroke-width="1.1"/></svg>',
    email: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="4.5" width="15" height="11" rx="2"/><path d="m3.2 5.6 6.8 5.2 6.8-5.2"/></svg>',
    tiktok: '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12.5 2.5v9.7a3.6 3.6 0 1 1-3.1-3.6"/><path d="M12.5 4.5c.6 1.8 2 3 4 3.2"/></svg>'
  };

  var STATE_LABEL = { "in": "Disponível", "low": "Últimas peças", "out": "Esgotado" };

  /* ---------------- image well ----------------
     Alt real e descritivo (anti-Casablanca, seção 8.1): descreve a
     foto FUTURA. Quando a foto existir, <img alt> assume.          */
  function wellAlt(p, slot) {
    var real = p.photos && p.photos[slot];
    return (real ? "" : "Foto futura: ") + p.title + " — " + slotDesc(p, slot) + ".";
  }
  /* aria-label + title com a mesma descrição de slot: o site inteiro
     se autodocumenta (Alterações 02, 2.3.5). */
  function wellAttrs(p, slot) {
    var a = esc(wellAlt(p, slot));
    return ' role="img" aria-label="' + a + '" title="' + a + '"';
  }
  /* Ordem de galeria com FOTOS REAIS primeiro (direção do Pedro):
     os slots com foto abrem a sequência — e a foto de COSTAS (02)
     lidera quando existe ("parte de trás na imagem 1"). Placeholders
     vêm depois. */
  function galleryOrder(p) {
    var order = GALLERY_ORDER.filter(function (s) { return p.slots.indexOf(s) !== -1; });
    var com = order.filter(function (s) { return p.photos && p.photos[s]; });
    var sem = order.filter(function (s) { return !(p.photos && p.photos[s]); });
    var i = com.indexOf("02");
    if (i > 0) { com.splice(i, 1); com.unshift("02"); }
    /* `cover` do catálogo vence tudo: a foto de PRODUTO (packshot)
       abre card e galeria — nunca uma editorial (direção do Pedro,
       01/08, Collections pág. 2). */
    if (p.cover) {
      var j = com.indexOf(p.cover);
      if (j > 0) { com.splice(j, 1); com.unshift(p.cover); }
    }
    return com.concat(sem);
  }
  function mainSlot(p) {
    return galleryOrder(p)[0] || "01";
  }
  function faceSpan(code, slot, cls) {
    /* Foto REAL quando o produto tiver o slot no mapa `photos`;
       senão, o well placeholder se autodocumenta com code_slot. */
    var p = byCode(code);
    var img = "";
    if (p && p.photos && p.photos[slot]) {
      img = '<img src="' + ROOT + p.photos[slot] + '" alt="" loading="lazy">';
    }
    return '<span class="well__face ' + (cls || "") + '" data-code="' + esc(code) + '" data-slot="' + esc(slot) + '">' + img + "</span>";
  }

  /* ---------------- card de produto ----------------
     Sem badge e sem linha de cores no card (direção do Pedro):
     imagem → título → preço, e pronto. O badge vive só na PDP. */
  function cardHTML(p, opts) {
    opts = opts || {};
    var url = href("produto.html?code=" + encodeURIComponent(p.code));
    /* Card (direção do Pedro): imagem 1 = COSTAS (a foto real de trás),
       hover = FRENTE quando existir; senão a 2ª foto real; senão o
       placeholder do _06 (que ensina qual foto falta). */
    var main = mainSlot(p);
    var reais = galleryOrder(p).filter(function (s) { return p.photos && p.photos[s]; });
    var hoverSlot = (p.photos && p.photos["01"] && main !== "01") ? "01" :
      (reais.filter(function (s) { return s !== main; })[0] || "06");
    var chips = Object.keys(p.sizes).map(function (sz) {
      var st = p.sizes[sz];
      return '<button type="button" class="chip chip--' + st + '" data-code="' + esc(p.code) + '" data-size="' + esc(sz) +
        '" aria-label="' + esc(sz + " — " + STATE_LABEL[st]) + '" title="' + esc(STATE_LABEL[st]) + '"' +
        (st === "out" ? " disabled" : "") + '>' + esc(sz) + "</button>";
    }).join("");
    /* Esgotado no card (direção do Pedro, 01/08): nome e preço em
       cinza + "Sold out" discreto embaixo. Sem badge — o card segue
       imagem → título → preço. */
    var soldout = allOut(p);
    return '' +
      '<article class="card' + (soldout ? " card--soldout" : "") + '" data-code="' + esc(p.code) + '">' +
      '  <div class="card__media">' +
      '    <a class="card__link" href="' + url + '" aria-label="' + esc("Ver " + p.title) + '">' +
      '      <figure class="well well--card"' + wellAttrs(p, main) + '>' +
      faceSpan(p.code, main, "face--a") + faceSpan(p.code, hoverSlot, "face--b") +
      '      </figure>' +
      '    </a>' +
      '    <button type="button" class="card__arrow card__arrow--prev" aria-label="Imagem anterior">&#8249;</button>' +
      '    <button type="button" class="card__arrow card__arrow--next" aria-label="Próxima imagem">&#8250;</button>' +
      (opts.quickAdd !== false ?
        '<div class="quickadd"><div class="quickadd__chips">' + chips + '</div>' +
        '<a class="quickadd__details" href="' + url + '">Ver detalhes</a></div>' : "") +
      '  </div>' +
      '  <div class="card__info">' +
      '    <a class="card__title" href="' + url + '">' + esc(p.title) + "</a>" +
      '    <div class="card__price">' + fmtPrice(p.price) + "</div>" +
      (soldout ? '<div class="card__soldout">Sold out</div>' : "") +
      '  </div>' +
      "</article>";
  }
  function bindCards(scope) {
    $$(".card", scope).forEach(function (card) {
      var p = byCode(card.getAttribute("data-code"));
      if (!p) return;
      var order = galleryOrder(p);
      var idx = 0;
      var faceA = $(".face--a", card);
      function step(d) {
        idx = (idx + d + order.length) % order.length;
        /* reconstruir a face troca também a FOTO, não só o rótulo */
        faceA.outerHTML = faceSpan(p.code, order[idx], "face--a");
        faceA = $(".face--a", card);
      }
      var prev = $(".card__arrow--prev", card), next = $(".card__arrow--next", card);
      if (prev) prev.addEventListener("click", function (e) { e.preventDefault(); step(-1); });
      if (next) next.addEventListener("click", function (e) { e.preventDefault(); step(1); });
      $$(".chip", card).forEach(function (chip) {
        chip.addEventListener("click", function (e) {
          e.preventDefault();
          if (chip.disabled) return;
          addToCart(chip.getAttribute("data-code"), chip.getAttribute("data-size"));
          openCart();
        });
      });
    });
  }

  /* ---------------- carrinho (localStorage) ---------------- */
  function cartGet() { return store("vesse_cart") || []; }
  function cartSet(items) { store("vesse_cart", items); updateCartCount(); }
  function addToCart(code, size) {
    var items = cartGet();
    for (var i = 0; i < items.length; i++) {
      if (items[i].code === code && items[i].size === size) { items[i].qty += 1; cartSet(items); return; }
    }
    items.push({ code: code, size: size, qty: 1 });
    cartSet(items);
  }
  function cartCount() {
    return cartGet().reduce(function (n, it) { return n + it.qty; }, 0);
  }
  function updateCartCount() {
    var n = cartCount();
    $$(".cart-count").forEach(function (el) {
      el.textContent = n;
      el.style.display = n > 0 ? "" : "none";
    });
  }
  function cartHTML() {
    var items = cartGet();
    if (!items.length) {
      return '<div class="cart-empty"><p>Seu carrinho está vazio</p>' +
        '<a class="btn btn--ink" href="' + href("colecao.html") + '">Descobrir</a></div>';
    }
    var rows = items.map(function (it, i) {
      var p = byCode(it.code);
      if (!p) return "";
      return '<div class="cart-line">' +
        '<figure class="well well--mini"' + wellAttrs(p, mainSlot(p)) + '>' + faceSpan(p.code, mainSlot(p)) + '</figure>' +
        '<div class="cart-line__info">' +
        '<a class="cart-line__title" href="' + href("produto.html?code=" + encodeURIComponent(p.code)) + '">' + esc(p.title) + "</a>" +
        '<span class="cart-line__meta">Tam. ' + esc(it.size) + (it.qty > 1 ? " · " + it.qty + " un." : "") + "</span>" +
        '<span class="cart-line__price">' + fmtPrice(p.price * it.qty) + "</span>" +
        '</div>' +
        '<button type="button" class="cart-line__remove" data-index="' + i + '">Remover</button>' +
        "</div>";
    }).join("");
    var subtotal = items.reduce(function (n, it) {
      var p = byCode(it.code); return n + (p ? p.price * it.qty : 0);
    }, 0);
    /* Se algum dia existir valor mínimo p/ entrega cortesia, o medidor de
       progresso de frete mora AQUI, nunca na PDP. */
    var gift = store("vesse_gift") || "";
    var lookKey = null;
    items.forEach(function (it) { if (!lookKey && COMPLETE_LOOK[it.code]) lookKey = it.code; });
    var lookHTML = "";
    if (lookKey) {
      lookHTML = '<div class="cart-look"><p class="label">Style it</p><div class="cart-look__grid">' +
        COMPLETE_LOOK[lookKey].cards.slice(0, 2).map(function (c) {
          var lp = byCode(c);
          if (!lp) return "";
          return '<a class="cart-look__item" href="' + href("produto.html?code=" + encodeURIComponent(lp.code)) + '">' +
            '<figure class="well well--mini"' + wellAttrs(lp, mainSlot(lp)) + '>' + faceSpan(lp.code, mainSlot(lp)) + '</figure>' +
            '<span>' + esc(lp.title) + '</span><span class="cart-look__price">' + fmtPrice(lp.price) + "</span></a>";
        }).join("") + "</div></div>";
    }
    return '<div class="cart-body">' + rows + "</div>" +
      '<div class="cart-gift">' +
      '<button type="button" class="cart-gift__toggle">Adicionar mensagem de presente</button>' +
      '<textarea class="cart-gift__text" rows="3" placeholder="Escreva sua mensagem" style="display:none">' + esc(gift) + "</textarea>" +
      "</div>" + lookHTML +
      '<div class="cart-foot">' +
      '<div class="cart-subtotal"><span>Subtotal</span><span>' + fmtPrice(subtotal) + "</span></div>" +
      '<p class="cart-note">Entrega cortesia calculada na finalização.</p>' +
      /* Porte: no Shopify real, este CTA leva ao checkout nativo. */
      '<a class="btn btn--ink cart-checkout" href="#">Finalizar compra</a>' +
      "</div>";
  }
  function openCart() {
    openDrawer("Carrinho", cartHTML(), "drawer--cart");
    bindCart();
  }
  function bindCart() {
    $$(".cart-line__remove").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var items = cartGet();
        items.splice(parseInt(btn.getAttribute("data-index"), 10), 1);
        cartSet(items);
        $(".drawer__body").innerHTML = cartHTML();
        bindCart();
      });
    });
    var t = $(".cart-gift__toggle"), ta = $(".cart-gift__text");
    if (t && ta) {
      t.addEventListener("click", function () {
        ta.style.display = ta.style.display === "none" ? "" : "none";
        if (ta.style.display === "") ta.focus();
      });
      ta.addEventListener("input", function () { store("vesse_gift", ta.value); });
    }
  }

  /* ---------------- drawers (um componente, 666ms) ---------------- */
  var drawerEl = null, scrimEl = null;
  function ensureDrawer() {
    if (drawerEl) return;
    scrimEl = document.createElement("div");
    scrimEl.className = "scrim";
    scrimEl.addEventListener("click", closeDrawer);
    document.body.appendChild(scrimEl);
    drawerEl = document.createElement("aside");
    drawerEl.className = "drawer";
    drawerEl.setAttribute("role", "dialog");
    drawerEl.setAttribute("aria-modal", "true");
    document.body.appendChild(drawerEl);
  }
  function openDrawer(title, bodyHTML, cls) {
    ensureDrawer();
    drawerEl.className = "drawer" + (cls ? " " + cls : "");
    drawerEl.innerHTML =
      '<div class="drawer__head"><span class="drawer__title label">' + title + "</span>" +
      '<button type="button" class="drawer__close" aria-label="Fechar">' + ICONS.close + "</button></div>" +
      '<div class="drawer__body">' + bodyHTML + "</div>";
    $(".drawer__close", drawerEl).addEventListener("click", closeDrawer);
    requestAnimationFrame(function () {
      drawerEl.classList.add("drawer--open");
      scrimEl.classList.add("scrim--show");
      document.body.classList.add("no-scroll");
    });
  }
  function closeDrawer() {
    if (!drawerEl) return;
    drawerEl.classList.remove("drawer--open");
    scrimEl.classList.remove("scrim--show");
    document.body.classList.remove("no-scroll");
  }

  /* ---------------- header + navegação ---------------- */
  /* Logo padrão da casa: o lockup completo do vetor master
     (VÈSSE + CLUB©), fill herdado — branco sobre o banner da home,
     tinta nas páginas internas. */
  var LOCK_FULL =
    '<svg class="lock__mark" viewBox="0 0 1000 486" fill="currentColor" aria-hidden="true" focusable="false">' +
    '<path d="M265.894 422.126C265.894 386.835 289.823 359.867 325.099 359.867C354.523 359.867 374.101 377.346 376.61 399.986H352.537C350.362 388.003 339.137 380.173 325.099 380.173C303.035 380.173 293.037 397.955 293.037 421.596C293.037 445.237 305.21 462.859 325.266 462.859C339.478 462.859 351.704 451.543 353.204 439.059H376.944C376.277 449.55 369.561 463.579 361.542 471.068C353.348 478.724 341.805 483.938 325.251 483.938C291.65 483.938 265.894 457.917 265.894 422.126Z"/>' +
    '<path d="M750.379 422.005C750.379 406.035 761.21 393.824 777.173 393.824C793.136 393.824 799.351 404.466 800.488 414.714H789.596C788.611 409.286 783.532 403.018 777.173 403.018C767.183 403.018 762.658 411.068 762.658 421.763C762.658 432.458 768.168 440.439 777.249 440.439C783.676 440.439 789.217 435.315 789.899 429.668H800.64C800.336 434.413 797.297 440.765 793.666 444.16C789.96 447.624 784.73 449.989 777.241 449.989C762.036 449.989 750.379 438.21 750.379 422.013V422.005Z"/>' +
    '<path d="M390.921 359.791H417.639V460.912H479.557V483.946H390.921V359.791Z"/>' +
    '<path d="M488.554 442.652V359.897H516.508V442.652C516.508 455.28 522.989 464.148 539.982 464.148C556.104 464.148 563.639 454.931 563.639 442.311V359.897H591.683V442.652C591.683 468.757 572.575 483.946 540.505 483.946C508.436 483.946 488.547 469.098 488.547 442.652H488.554Z"/>' +
    '<path d="M607.54 359.905H665.775C679.789 359.905 690.522 363.202 697.261 368.925C704.355 374.996 707.637 382.455 707.637 392.172C707.637 404.838 699.444 412.993 687.255 416.98V417.496C701.634 421.49 711.457 432.935 711.457 448.201C711.457 459.82 707.637 467.802 699.997 474.047C692.531 480.293 681.07 483.931 667.238 483.931H607.548V359.89L607.54 359.905ZM662.5 409.87C673.968 409.87 681.79 404.663 681.79 394.954C681.79 385.76 674.696 380.378 663.046 380.378H633.932V409.87H662.5ZM633.932 463.125H664.327C677.068 463.125 684.709 456.356 684.709 446.298C684.709 434.504 675.605 428.433 663.599 428.433H633.932V463.133V463.125Z"/>' +
    '<path d="M775.513 369.804C746.581 369.804 723.122 393.263 723.122 422.195C723.122 451.126 746.581 474.585 775.513 474.585C804.444 474.585 827.903 451.126 827.903 422.195C827.903 393.263 804.444 369.804 775.513 369.804ZM775.513 461.245C753.949 461.245 736.462 443.759 736.462 422.195C736.462 400.63 753.949 383.144 775.513 383.144C797.077 383.144 814.563 400.63 814.563 422.195C814.563 443.759 797.077 461.245 775.513 461.245Z"/>' +
    '<path d="M7.42807 74.0305H127.482V90.4405H108.988C108.988 90.4405 95.0262 89.6219 95.0262 100.688C95.0262 112.656 109.352 133.872 109.352 133.872L170.285 252.835L233.757 109.753C233.757 109.753 237.744 99.051 230.308 94.5184C222.872 89.9857 204.014 89.8038 204.014 89.8038V74.0229H288.073L170.558 322.742H152.328C152.328 322.742 63.7298 155.8 35.6244 99.4224C32.3273 92.7978 31.1373 89.9706 7.42807 90.4481V74.0381V74.0305Z"/>' +
    '<path d="M318.619 65.1472L330.951 52.8151L274.005 7.11734C274.005 7.11734 261.855 -1.94794 251.152 8.74697C241.981 17.9184 245.71 26.7032 256.049 32.1378C266.387 37.5724 318.611 65.1397 318.611 65.1397L318.619 65.1472Z"/>' +
    '<path d="M275.278 96.7922H336.848C364.597 96.7922 361.876 133.698 361.876 133.698H381.03V74.0305H286.367L275.286 96.7847L275.278 96.7922Z"/>' +
    '<path d="M237.198 175.045H293.644C293.644 175.045 314.321 174.499 323.295 149.607H342.881L312.957 235.023H295.137C295.137 235.023 303.573 203.332 285.208 203.332H224.82L237.198 175.045Z"/>' +
    '<path d="M351.901 252.842L367.045 259.823L314.814 322.75H168.284L181.791 294.462H262.491C262.491 294.462 302.838 297.229 351.893 252.842H351.901Z"/>' +
    '<path d="M552.671 74.0305L561.305 156.202H543.894C543.894 156.202 533.828 96.8226 481.908 96.8226C467.317 96.8226 449.55 103.409 449.55 126.618C449.55 149.827 474.578 162.523 497.787 174.135C520.996 185.74 568.695 213.307 568.695 252.842C568.695 292.378 536.413 322.75 487.084 322.75C437.756 322.75 443.562 310.326 429.418 310.326C418.625 310.326 419.512 322.75 419.512 322.75H402.033L392.513 238.153H409.241C409.241 238.153 422.885 299.904 480.604 299.904C500.205 299.904 507.982 292.188 514.515 284.26C527.219 268.851 522.292 246.187 499.993 232.711C490.609 227.041 479.952 219.477 467.862 212.852C436.467 195.639 401.76 174.726 401.76 135.054C401.76 115.241 412.167 102.477 421.482 93.3662C437.999 77.214 454.196 74.0305 478.254 74.0305C506.761 74.0305 510.293 84.5966 525.256 84.5966C537.565 84.5966 536.951 74.0305 536.951 74.0305H552.664H552.671Z"/>' +
    '<path d="M744.899 74.0305L753.532 156.202H736.122C736.122 156.202 726.056 96.8226 674.135 96.8226C659.544 96.8226 641.778 103.409 641.778 126.618C641.778 149.827 666.806 162.523 690.015 174.135C713.224 185.74 760.922 213.307 760.922 252.842C760.922 292.378 728.641 322.75 679.312 322.75C629.984 322.75 635.79 310.326 621.646 310.326C610.853 310.326 611.739 322.75 611.739 322.75H594.261L584.741 238.153H601.469C601.469 238.153 615.112 299.904 672.831 299.904C692.432 299.904 700.209 292.188 706.743 284.26C719.446 268.851 714.52 246.187 692.22 232.711C682.837 227.041 672.18 219.477 660.09 212.852C628.695 195.639 593.988 174.726 593.988 135.054C593.988 115.241 604.395 102.477 613.71 93.3662C630.226 77.214 646.424 74.0305 670.482 74.0305C698.989 74.0305 702.521 84.5966 717.483 84.5966C729.793 84.5966 729.179 74.0305 729.179 74.0305H744.891H744.899Z"/>' +
    '<path d="M975.601 252.842C975.601 252.842 956.425 299.632 919.565 299.632H855.229C849.309 299.632 847.884 300.041 847.884 286.299V206.872H908.953C924.052 206.872 935.202 207.236 935.202 240.192H953.158V149.289H935.474C935.474 149.289 936.983 166.98 927.129 176.674C923.15 180.593 916.813 182.48 908.544 182.48H848.02V107.176C848.02 107.176 847.156 96.8301 865.294 96.8301H888.89V96.7998H929.578C957.327 96.7998 954.606 133.705 954.606 133.705H973.759V74.0381H764.189V90.4481C764.189 90.4481 797.282 88.4091 797.282 108.806V289.156C797.282 289.156 799.867 306.703 765.933 306.703V322.75H972.259L992.731 252.842H975.594H975.601Z"/>' +
    '</svg>';
  /* Monograma VÈ (glifos V + È do vetor oficial) — usado como segunda
     linha dos H1 de vista no lugar do texto "Vèsse Club" (o nome
     estava repetindo demais). */
  var VE_MARK =
    '<svg class="ve-mark" viewBox="0 -2 388 325" fill="currentColor" aria-label="Vèsse Club" role="img" focusable="false">' +
    '<path d="M7.42807 74.0305H127.482V90.4405H108.988C108.988 90.4405 95.0262 89.6219 95.0262 100.688C95.0262 112.656 109.352 133.872 109.352 133.872L170.285 252.835L233.757 109.753C233.757 109.753 237.744 99.051 230.308 94.5184C222.872 89.9857 204.014 89.8038 204.014 89.8038V74.0229H288.073L170.558 322.742H152.328C152.328 322.742 63.7298 155.8 35.6244 99.4224C32.3273 92.7978 31.1373 89.9706 7.42807 90.4481V74.0381V74.0305Z"/>' +
    '<path d="M318.619 65.1472L330.951 52.8151L274.005 7.11734C274.005 7.11734 261.855 -1.94794 251.152 8.74697C241.981 17.9184 245.71 26.7032 256.049 32.1378C266.387 37.5724 318.611 65.1397 318.611 65.1397L318.619 65.1472Z"/>' +
    '<path d="M275.278 96.7922H336.848C364.597 96.7922 361.876 133.698 361.876 133.698H381.03V74.0305H286.367L275.286 96.7847L275.278 96.7922Z"/>' +
    '<path d="M237.198 175.045H293.644C293.644 175.045 314.321 174.499 323.295 149.607H342.881L312.957 235.023H295.137C295.137 235.023 303.573 203.332 285.208 203.332H224.82L237.198 175.045Z"/>' +
    '<path d="M351.901 252.842L367.045 259.823L314.814 322.75H168.284L181.791 294.462H262.491C262.491 294.462 302.838 297.229 351.893 252.842H351.901Z"/>' +
    '</svg>';
  function chromeHeaderHTML() {
    /* Estrutura do cabeçalho (direção do Pedro, ref. Casablanca):
       desktop → Menu + Busca (só ícones) à esquerda · marca no centro ·
       coração, conta e carrinho à direita; mobile → coração + carrinho
       à esquerda · marca no centro · busca + hambúrguer à direita.
       O Menu abre o drawer lateral VERTICAL (mesmo componente do
       mobile) com as 4 abas empilhadas — sem painel horizontal, nada
       corta o wordmark no topo.                                       */
    return '' +
      '<header class="site-header">' +
      '  <div class="header__grid">' +
      '    <div class="header__left">' +
      /* Ícones sem rótulo (direção do Pedro) — o nome fica no aria-label.
         Mobile na ordem NORMAL: menu + busca à esquerda. */
      '      <button type="button" class="icon-btn btn-menu only-desktop" aria-label="Menu">' + ICONS.burger + "</button>" +
      '      <button type="button" class="icon-btn nav-burger only-mobile" aria-label="Abrir menu">' + ICONS.burger + "</button>" +
      '      <button type="button" class="icon-btn js-search" aria-label="Busca">' + ICONS.search + "</button>" +
      "    </div>" +
      /* Logo padrão (lockup completo do vetor), estática — branca sobre
         o banner da home, tinta nas internas. Sem animação de scroll. */
      '    <a class="lock" href="' + href("index.html") + '" aria-label="Vèsse Club — início">' + LOCK_FULL + "</a>" +
      '    <div class="header__icons">' +
      /* Direita, em qualquer tela: conta (desktop) · sacola. */
      /* Conta: leva à página do clube (sem login POR DECISÃO — a lista
         É o clube). Porte: customer account Shopify. */
      '      <a class="icon-btn only-desktop" href="' + href("pages/members.html") + '" aria-label="Conta">' + ICONS.account + "</a>" +
      '      <button type="button" class="icon-btn js-cart" aria-label="Carrinho">' + ICONS.cart +
      '        <span class="cart-count" style="display:none">0</span></button>' +
      "    </div>" +
      "  </div>" +
      "</header>";
  }
  function initHeader() {
    var header = $(".site-header");
    var menuBtn = $(".btn-menu", header);
    /* Menu (desktop) abre o MESMO drawer vertical do mobile — um só
       componente, itens empilhados, clique (não hover). */
    if (menuBtn) menuBtn.addEventListener("click", openMobileNav);
    $(".nav-burger").addEventListener("click", openMobileNav);
    $$(".js-search").forEach(function (b) { b.addEventListener("click", openSearch); });
    $$(".js-cart").forEach(function (b) { b.addEventListener("click", openCart); });
  }

  function openMobileNav() {
    var body = NAV.map(function (item) {
      if (!item.mega) {
        return '<a class="mnav__link" href="' + href(item.href) + '">' + esc(item.label) + "</a>";
      }
      var cols = MEGA[item.mega].map(function (col) {
        var links = col.links.length ? col.links : [[col.title, col.href]];
        return '<p class="mnav__group label">' + esc(col.title) + "</p>" +
          links.map(function (l) {
            return '<a class="mnav__sublink" href="' + href(l[1]) + '">' + esc(l[0]) + "</a>";
          }).join("");
      }).join("");
      return '<div class="mnav__acc">' +
        '<button type="button" class="mnav__link mnav__toggle">' + esc(item.label) +
        '<span class="mnav__chevron">' + ICONS.chevron + "</span></button>" +
        '<div class="mnav__panel">' + cols + "</div></div>";
    }).join("");
    /* No cabeçalho da gaveta, o monograma VÈ — clicável, leva à home.
       No PÉ, a conta (ref. AMIRI). */
    openDrawer(
      '<a class="drawer__home" href="' + href("index.html") + '" aria-label="Vèsse Club — início">' + VE_MARK + "</a>",
      '<nav class="mnav" aria-label="Menu">' + body + "</nav>" +
      '<div class="mnav__foot"><a class="mnav__account" href="' + href("pages/members.html") + '">' +
      ICONS.account + "<span>Conta</span></a></div>", "drawer--nav");
    $$(".mnav__toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        btn.parentElement.classList.toggle("is-open");
      });
    });
  }
  function openSearch() {
    var html = '<div class="search">' +
      '<input type="search" class="search__input" placeholder="Buscar" aria-label="Buscar produtos">' +
      '<div class="search__results"></div>' +
      /* Quem busca é convidado ao mundo antes do produto. */
      '<a class="search__world display" href="' + href("pages/vemaison.html") + '">Vèsse World</a>' +
      "</div>";
    openDrawer("Busca", html, "drawer--search");
    var input = $(".search__input"), out = $(".search__results");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      if (!q) { out.innerHTML = ""; return; }
      var hits = CATALOG.filter(function (p) {
        return p.title.toLowerCase().indexOf(q) !== -1 || p.print.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 6);
      out.innerHTML = hits.length ? hits.map(function (p) {
        return '<a class="search__hit" href="' + href("produto.html?code=" + encodeURIComponent(p.code)) + '">' +
          '<figure class="well well--mini"' + wellAttrs(p, mainSlot(p)) + '>' + faceSpan(p.code, mainSlot(p)) + "</figure>" +
          '<span>' + esc(p.title) + '</span><span class="search__price">' + fmtPrice(p.price) + "</span></a>";
      }).join("") : '<p class="search__none">0 produtos</p>';
    });
    input.focus();
  }

  /* ---------------- members club + footer ---------------- */
  /* Canais do Bureau: SÓ os ícones (WhatsApp, e-mail, Instagram),
     sem horário — direção do Pedro. Fonte única p/ footer e bureau. */
  function contactIconsHTML() {
    return '<a class="icon-btn" href="' + CONTACT.whatsapp + '" aria-label="WhatsApp" title="WhatsApp">' + ICONS.whatsapp + "</a>" +
      '<a class="icon-btn" href="' + CONTACT.email + '" aria-label="E-mail" title="E-mail">' + ICONS.email + "</a>" +
      '<a class="icon-btn" href="' + CONTACT.instagram + '" aria-label="Instagram DM" title="Instagram DM">' + ICONS.instagram + "</a>" +
      '<a class="icon-btn" href="' + CONTACT.tiktok + '" aria-label="TikTok" title="TikTok">' + ICONS.tiktok + "</a>";
  }
  /* Bloco do clube — NÃO é mais global (muito convite = pouco valor).
     Renderiza só onde houver [data-members]: hoje, no Vèsse World
     depois das Music Sessions. A página do clube é pages/members.html. */
  function membersBlockHTML() {
    /* 3 benefícios (sem convite de festa — direção do Pedro, 01/08)
       e a entrada se PEDE — tom especial sem exagero. */
    var benefits = MEMBERS_BENEFITS.map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("");
    return '<section class="members" id="members">' +
      '  <h2 class="display members__title">Vèsse Club Members</h2>' +
      '  <ul class="members__benefits">' + benefits + "</ul>" +
      '  <form class="members__form" novalidate>' +
      '    <input type="email" required placeholder="Seu e-mail" aria-label="Seu e-mail">' +
      '    <label class="members__consent"><input type="checkbox" required> ' +
      '      Autorizo o uso do meu e-mail conforme a <a href="' + href("pages/legal.html#privacidade") + '">Política de Privacidade</a>.</label>' +
      '    <button type="submit" class="btn btn--ink">Pedir entrada</button>' +
      "  </form>" +
      "</section>";
  }
  function chromeFooterHTML() {
    var channels = contactIconsHTML();
    return '' +
      '<footer class="site-footer">' +
      '  <div class="foot-cols">' +
      '    <div><p class="label">Suporte</p><ul>' +
      '      <li><a href="' + href("pages/bureau.html#faq") + '">FAQ</a></li>' +
      '      <li><a href="' + href("pages/bureau.html#entrega") + '">Entrega e trocas</a></li>' +
      '      <li><a href="' + href("pages/bureau.html#contato") + '">Contato</a></li></ul></div>' +
      /* Casa: Vèsse World + o clube (o rodapé é um dos DOIS únicos
         lugares onde o clube é citado). */
      '    <div><p class="label">Casa</p><ul>' +
      '      <li><a href="' + href("pages/vemaison.html") + '">Vèsse World</a></li>' +
      '      <li><a href="' + href("pages/members.html") + '">Vèsse Club Members</a></li></ul></div>' +
      '    <div><p class="label">Legal</p><ul>' +
      '      <li><a href="' + href("pages/legal.html#termos") + '">Termos</a></li>' +
      '      <li><a href="' + href("pages/legal.html#privacidade") + '">Privacidade</a></li>' +
      '      <li><a href="' + href("pages/legal.html#acessibilidade") + '">Acessibilidade</a></li></ul></div>' +
      "  </div>" +
      /* No lugar do rótulo "Therapy Bureau": o monograma VÈ. */
      '  <div class="bureau-block"><p class="bureau-block__mark">' + VE_MARK + "</p>" +
      '    <p class="bureau-block__line">' + channels + "</p></div>" +
      '  <p class="payline">Pague com ' + CONTACT.pay + "</p>" +
      /* Sem linha de sociais própria: os canais (incl. TikTok) vivem
         nos ícones do Therapy Bureau acima. */
      '  <p class="copyright">©2026 Vèsse Club</p>' +
      "</footer>";
  }
  function initMembersForms() {
    $$(".members__form").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var email = $('input[type="email"]', form);
        var consent = $('input[type="checkbox"]', form);
        if (!email.value || email.value.indexOf("@") === -1) { email.focus(); return; }
        if (!consent.checked) { consent.focus(); return; }
        /* Sem "você está dentro" na hora — mas sem teatro: a casa
           responde por e-mail (direção do Pedro, 01/08). */
        form.innerHTML = '<p class="members__ok">Pedido recebido. A casa responde por e-mail.</p>';
      });
    });
  }

  /* ---------------- PLP universal ---------------- */
  var plp = null;
  function initPLP() {
    var c = param("c");
    var key = (c && VIEWS[c]) ? c : "novidades";
    var view = VIEWS[key];
    plp = { key: key, view: view, sort: view.sort, page: 1, filters: {} };
    document.title = plain(view.h1).replace("[VÈ]", "").trim() + " — Vèsse Club";
    renderPLP();
  }
  function plpBase() {
    return CATALOG.filter(plp.view.filter);
  }
  function plpItems() {
    var items = plpBase().filter(function (p) {
      var f = plp.filters;
      if (f.Categoria && f.Categoria.length && f.Categoria.indexOf(typePlural(p.type)) === -1) return false;
      if (f.Cor && f.Cor.length) {
        var ok = p.colors.some(function (col) { return f.Cor.indexOf(col.name) !== -1; });
        if (!ok) return false;
      }
      if (f.Material && f.Material.length && f.Material.indexOf(p.material) === -1) return false;
      if (f.Tamanho && f.Tamanho.length) {
        var okT = f.Tamanho.some(function (sz) { return p.sizes[sz] && p.sizes[sz] !== "out"; });
        if (!okT) return false;
      }
      if (f.Gênero && f.Gênero.length && f.Gênero.indexOf(p.gender) === -1) return false;
      return true;
    });
    if (plp.sort === "menor") items.sort(function (a, b) { return a.price - b.price; });
    else if (plp.sort === "maior") items.sort(function (a, b) { return b.price - a.price; });
    else if (plp.sort === "az") items.sort(function (a, b) { return a.title.localeCompare(b.title, "pt"); });
    return items;
  }
  var PAGE_SIZE = 8;
  function renderPLP() {
    var rootEl = $("#plp-root");
    var view = plp.view;
    var items = plpItems();
    var pages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));
    if (plp.page > pages) plp.page = pages;
    var slice = items.slice((plp.page - 1) * PAGE_SIZE, plp.page * PAGE_SIZE);

    var cells = slice.map(function (p) { return cardHTML(p); });
    /* Promo cards injetados na grade — só na 1ª página, sem facetas ativas */
    var noFilters = !Object.keys(plp.filters).some(function (k) { return plp.filters[k] && plp.filters[k].length; });
    if (view.promos && plp.page === 1 && noFilters) {
      view.promos.forEach(function (pr) {
        var promo;
        if (pr.ve) {
          /* célula do monograma VÈ — fecha a linha da grade */
          promo = '<div class="ve-cell">' + VE_MARK + "</div>";
        } else {
          promo = '<a class="promo promo--' + pr.size + '" href="' + href(pr.href) + '">' +
            '<figure class="well well--promo" role="img" aria-label="' + esc("Foto futura de campanha: " + pr.title) +
            '" title="' + esc("Foto futura de campanha: " + pr.title) + '">' +
            faceSpan(pr.code, pr.slot) + "</figure>" +
            '<span class="promo__title display">' + esc(pr.title) + "</span>" +
            '<span class="promo__cta">Descobrir</span></a>';
        }
        if (pr.at <= cells.length) cells.splice(pr.at, 0, promo); else cells.push(promo);
      });
    }

    var sortHTML;
    if (view.sort === "az") {
      /* Vistas conjuntos*: A–Z forçado — é o que faz o par cair lado a lado. */
      sortHTML = '<span class="sort-fixed label">A–Z</span>';
    } else {
      sortHTML = '<label class="sort label">Ordenar' +
        '<select class="sort-select">' +
        '<option value="recentes">Mais recentes</option>' +
        '<option value="menor">Menor preço</option>' +
        '<option value="maior">Maior preço</option>' +
        "</select></label>";
    }

    var pag = "";
    if (pages > 1) {
      var nums = "";
      for (var i = 1; i <= pages; i++) {
        nums += '<button type="button" class="page-num' + (i === plp.page ? " is-current" : "") + '" data-page="' + i + '">' + i + "</button>";
      }
      pag = '<nav class="pagination" aria-label="Paginação">' +
        '<button type="button" class="page-arrow" data-page="' + (plp.page - 1) + '"' +
        (plp.page === 1 ? ' style="visibility:hidden"' : "") + ' aria-label="Página anterior">&#8249;</button>' +
        nums +
        '<button type="button" class="page-arrow" data-page="' + (plp.page + 1) + '"' +
        (plp.page === pages ? ' style="visibility:hidden"' : "") + ' aria-label="Próxima página">&#8250;</button>' +
        "</nav>";
    }

    /* Bloco SEO abaixo da grade REMOVIDO da tela (direção do Pedro).
       Os dados view.seo continuam no catalog.js para o porte Shopify
       (meta description / conteúdo de collection). */
    rootEl.innerHTML =
      '<h1 class="display plp-h1">' + view.h1.replace("[VÈ]", VE_MARK) + "</h1>" +
      (view.desc ? '<p class="plp-desc">' + esc(view.desc) + "</p>" : "") +
      '<div class="refine-bar">' +
      '  <button type="button" class="refine-btn label">Refinar</button>' +
      '  <span class="plp-count label">' + items.length + (items.length === 1 ? " produto" : " produtos") + "</span>" +
      sortHTML +
      "</div>" +
      (items.length ? '<div class="plp-grid">' + cells.join("") + "</div>" : '<p class="plp-empty">0 produtos</p>') +
      pag;

    bindCards(rootEl);
    var sel = $(".sort-select", rootEl);
    if (sel) {
      sel.value = plp.sort;
      sel.addEventListener("change", function () { plp.sort = sel.value; plp.page = 1; renderPLP(); });
    }
    $(".refine-btn", rootEl).addEventListener("click", openRefine);
    $$(".page-num, .page-arrow", rootEl).forEach(function (b) {
      b.addEventListener("click", function () {
        plp.page = parseInt(b.getAttribute("data-page"), 10);
        renderPLP();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    });
  }
  /* Facetas: no máximo 5 — Categoria · Cor · Material · Tamanho · Gênero.
     NÃO EXISTE filtro de preço.                                          */
  function openRefine() {
    var base = plpBase();
    function count(fn) { return base.filter(fn).length; }
    var facets = [
      {
        name: "Categoria",
        values: uniq(base.map(function (p) { return typePlural(p.type); })).map(function (v) {
          return { v: v, n: count(function (p) { return typePlural(p.type) === v; }) };
        })
      },
      {
        name: "Cor", swatch: true,
        values: uniqColors(base).map(function (c) {
          return { v: c.name, hex: c.hex, n: count(function (p) { return p.colors.some(function (x) { return x.name === c.name; }); }) };
        })
      },
      {
        name: "Material",
        values: uniq(base.map(function (p) { return p.material; })).map(function (v) {
          return { v: v, n: count(function (p) { return p.material === v; }) };
        })
      },
      {
        name: "Tamanho", chips: true,
        values: uniq(base.reduce(function (acc, p) { return acc.concat(Object.keys(p.sizes)); }, [])).map(function (v) {
          return { v: v, n: count(function (p) { return p.sizes[v] && p.sizes[v] !== "out"; }) };
        })
      },
      {
        name: "Gênero",
        values: uniq(base.map(function (p) { return p.gender; })).map(function (v) {
          return { v: v, n: count(function (p) { return p.gender === v; }) };
        })
      }
    ];
    var html = facets.map(function (f) {
      var sel = plp.filters[f.name] || [];
      var list;
      if (f.chips) {
        list = '<div class="size-chips">' + f.values.map(function (val) {
          return '<label class="size-chip' + (sel.indexOf(val.v) !== -1 ? " is-on" : "") + '">' +
            '<input type="checkbox" name="' + f.name + '" value="' + esc(val.v) + '"' +
            (sel.indexOf(val.v) !== -1 ? " checked" : "") + '>' + esc(val.v) + "</label>";
        }).join("") + "</div>";
      } else {
        list = '<ul class="facet__list">' + f.values.map(function (val) {
          return "<li><label>" +
            '<input type="checkbox" name="' + f.name + '" value="' + esc(val.v) + '"' +
            (sel.indexOf(val.v) !== -1 ? " checked" : "") + '>' +
            (val.hex ? '<i class="swatch" style="background:' + val.hex + '"></i>' : "") +
            "<span>" + esc(val.v) + "</span>" +
            '<span class="facet__count">' + val.n + "</span></label></li>";
        }).join("") + "</ul>";
      }
      return '<div class="facet"><p class="facet__title label">' + f.name + "</p>" + list + "</div>";
    }).join("");
    openDrawer("Refinar resultados",
      '<form class="refine-form">' + html +
      '<button type="submit" class="btn btn--ink refine-apply">Aplicar</button></form>',
      "drawer--refine");
    $(".refine-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var filters = {};
      $$(".refine-form input:checked").forEach(function (input) {
        var n = input.getAttribute("name");
        (filters[n] = filters[n] || []).push(input.value);
      });
      plp.filters = filters;
      plp.page = 1;
      closeDrawer();
      renderPLP();
    });
    $$(".size-chip input").forEach(function (input) {
      input.addEventListener("change", function () {
        input.parentElement.classList.toggle("is-on", input.checked);
      });
    });
  }
  function uniq(arr) {
    return arr.filter(function (v, i) { return arr.indexOf(v) === i; });
  }
  function uniqColors(items) {
    var seen = {}, out = [];
    items.forEach(function (p) {
      p.colors.forEach(function (c) {
        if (!seen[c.name]) { seen[c.name] = true; out.push(c); }
      });
    });
    return out;
  }

  /* ---------------- PDP universal ---------------- */
  var pdp = null;
  function descParagraph(p) {
    var fitWord = p.bullets.fit.indexOf("oversized") !== -1 ? "oversized" :
      (p.bullets.fit.indexOf("regular") !== -1 ? "regular" : "unissex");
    var s1 = "O " + p.title + " é um design " + p.desc.adj +
      " com a estampa " + p.print + " da casa " + p.desc.where + ".";
    var s2 = "Finalizado com " + joinAnd(p.desc.details) + ", fechando na silhueta " + fitWord + ".";
    var s3 = p.desc.partner ? " Feito para vestir com " + p.desc.partner + "." : "";
    return s1 + " " + s2 + s3;
  }
  function detailsTabHTML(p) {
    /* Estrutura fixa: exatamente um <p> e um <ul>. */
    var colorLine = "Cor: " + p.colors.map(function (c) { return c.name; }).join("/");
    var bullets = [
      p.bullets.fabric, p.bullets.comp, p.bullets.signature,
      colorLine, p.bullets.care, p.bullets.origin, p.bullets.fit
    ].map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("");
    return "<p>" + esc(descParagraph(p)) + "</p><ul>" + bullets + "</ul>" +
      '<p class="model-line">O modelo tem 1,84 m e veste M.</p>';
  }
  function guideTableHTML(key) {
    var g = SIZE_GUIDES[key];
    return '<table class="size-table"><thead><tr>' +
      g.cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") +
      "</tr></thead><tbody>" +
      g.rows.map(function (r) {
        return "<tr>" + r.map(function (c) { return "<td>" + esc(c) + "</td>"; }).join("") + "</tr>";
      }).join("") + "</tbody></table>" +
      '<p class="model-line">O modelo tem 1,84 m e veste M.</p>' +
      '<a class="tab-link" href="' + href("pages/" + g.page) + '">Guia completo de ' + esc(g.label.toLowerCase()) + "</a>";
  }
  /* Accordion vertical da PDP (ref. Off-White): Descrição · Guia de
     tamanhos · Entrega e trocas, empilhados e abrindo inline. O bind
     de clique é o global de .acc__q em initHooks. */
  function pdpAccHTML(p) {
    var items = [
      ["Descrição", detailsTabHTML(p)],
      ["Guia de tamanhos", guideTableHTML(guideForType(p.type))],
      ["Entrega e trocas", SHIPPING_HTML]
    ];
    return items.map(function (it) {
      return '<div class="acc__item">' +
        '<button type="button" class="acc__q">' + it[0] +
        '<span class="mnav__chevron">' + ICONS.chevron + "</span></button>" +
        '<div class="acc__a"><div class="tabpane">' + it[1] + "</div></div></div>";
    }).join("");
  }
  function openNotify(p, size) {
    ensureDrawer();
    var modal = document.createElement("div");
    modal.className = "modal";
    modal.innerHTML = '<div class="modal__box">' +
      '<button type="button" class="modal__close" aria-label="Fechar">' + ICONS.close + "</button>" +
      '<p class="label">Avise-me quando voltar</p>' +
      '<p class="modal__body">Cadastre-se para receber um aviso quando este item voltar ao estoque.</p>' +
      /* Porte: Klaviyo back-in-stock — a melhor superfície de captação
         de lista que existe.                                          */
      '<form class="modal__form"><input type="email" required placeholder="Seu e-mail" aria-label="Seu e-mail">' +
      '<button type="submit" class="btn btn--ink">Enviar</button></form></div>';
    document.body.appendChild(modal);
    $(".modal__close", modal).addEventListener("click", function () { modal.remove(); });
    modal.addEventListener("click", function (e) { if (e.target === modal) modal.remove(); });
    $(".modal__form", modal).addEventListener("submit", function (e) {
      e.preventDefault();
      $(".modal__box", modal).innerHTML = '<p class="modal__body">Pronto! Avisaremos quando voltar.</p>';
      setTimeout(function () { modal.remove(); }, 1800);
    });
  }
  function allOut(p) {
    return Object.keys(p.sizes).every(function (sz) { return p.sizes[sz] === "out"; });
  }
  function syncBuybox() {
    var p = pdp.product;
    $$(".size-opt").forEach(function (btn) {
      var on = btn.getAttribute("data-size") === pdp.size;
      btn.classList.toggle("is-on", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    var ctas = $$(".pdp-cta");
    ctas.forEach(function (btn) {
      if (allOut(p)) {
        btn.className = "btn btn--ink pdp-cta";
        btn.textContent = "Avise-me quando voltar";
      } else if (!pdp.size) {
        btn.className = "btn btn--muted pdp-cta";
        btn.textContent = "Selecionar tamanho";
      } else {
        btn.className = "btn btn--ink pdp-cta";
        btn.textContent = pdp.added ? "Adicionado" : "Adicionar ao carrinho";
      }
    });
  }
  function initPDP() {
    var code = param("code");
    var p = byCode(code) || byCode("U-DT26-HDY-101-01");
    /* Boné não tem seletor nenhum (direção do Pedro): tamanho único,
       CTA já nasce ativo. */
    pdp = { product: p, size: p.type === "Boné" ? "Único" : null, added: false };
    document.title = p.title + " — Vèsse Club";
    recentPush(p.code);
    injectProductJSONLD(p);

    /* Galeria: swipe horizontal no mobile; no desktop as fotos
       empilham e rolam com a página (direção do Pedro, 05/08), com as
       fotos reais primeiro e a de costas liderando.                  */
    var order = galleryOrder(p);
    var figures = order.map(function (slot, i) {
      return '<figure class="well well--pdp"' + wellAttrs(p, slot) + ' tabindex="0" data-idx="' + i + '">' +
        faceSpan(p.code, slot) + "</figure>";
    }).join("");
    var bullets = order.map(function (_, i) {
      return '<span class="gallery__bullet' + (i === 0 ? " is-active" : "") + '"></span>';
    }).join("");

    /* A página Archive 71 foi removida (direção do Pedro): as peças de
       arquivo apontam para Collections. */
    var collLink = isA71(p) ?
      '<a href="' + href("colecao.html?c=collections") + '">Collections</a>' :
      '<a href="' + href("colecao.html?c=divine-therapy") + '">Divine Therapy</a>';
    /* Só o badge Members sobrevive na PDP — o título de drop
       ("Drop 01") foi removido (direção do Pedro). */
    var badgeTag = hasTag(p, "MEMBERS") ? "MEMBERS" : null;
    var priceHTML = fmtPrice(p.price) +
      (p.compareAt ? " <s>" + fmtPrice(p.compareAt) + "</s>" : "");

    /* Seletor de tamanhos INLINE (mockup do Pedro): esgotado riscado,
       selecionado com caixa. Boné não renderiza seletor. */
    var sizePicker = "";
    if (p.type !== "Boné") {
      sizePicker = '<div class="size-picker" role="group" aria-label="Tamanho">' +
        Object.keys(p.sizes).map(function (sz) {
          var st = p.sizes[sz];
          return '<button type="button" class="size-opt size-opt--' + st + '"' +
            ' data-size="' + esc(sz) + '"' +
            (st === "out" ? ' disabled aria-label="' + esc(sz) + ' esgotado"' : ' aria-pressed="false"') +
            ">" + esc(sz) + "</button>";
        }).join("") + "</div>";
    }

    var root = $("#pdp-root");
    root.innerHTML =
      '<div class="pdp">' +
      '  <div class="pdp__gallery">' +
      '    <div class="gallery">' + figures + "</div>" +
      '    <div class="gallery__bullets">' + bullets + "</div>" +
      "  </div>" +
      '  <div class="pdp__buybox">' +
      /* Exatamente 6 elementos visíveis, nesta ordem. */
      '    <div class="utilities"><span class="util-coll">' + collLink + "</span>" +
      '      <span class="util-actions">' +
      '        <button type="button" class="icon-btn btn-fav" aria-label="Favoritar" aria-pressed="false">' + ICONS.heart + "</button>" +
      "      </span></div>" +
      (badgeTag ? '<span class="badge pdp-badge">' + esc(BADGES[badgeTag].label) + "</span>" : "") +
      '    <h1 class="display pdp-h1">' + esc(p.title) + "</h1>" +
      /* O riscado só existe AQUI, nunca na grade. */
      '    <p class="pdp-price">' + priceHTML + "</p>" +
      sizePicker +
      '    <button type="button" class="btn btn--muted pdp-cta">Selecionar tamanho</button>' +
      /* Descrição, guia e entrega EMPILHADOS em accordion vertical
         (ref. Off-White) — abrem inline, sem drawer. */
      '    <div class="pdp-acc">' + pdpAccHTML(p) + "</div>" +
      '    <p class="help-row">Ajuda: <a href="' + CONTACT.whatsapp + '">WhatsApp</a> · ' +
      '<a href="' + CONTACT.email + '">E-mail</a></p>' +
      "  </div>" +
      "</div>" +
      '<div class="sticky-atc"><span class="sticky-atc__price">' + fmtPrice(p.price) + "</span>" +
      '  <button type="button" class="btn btn--muted pdp-cta">Selecionar tamanho</button></div>' +
      belowFoldHTML(p);

    syncBuybox();
    bindPDP(p, order);
    bindCards(root);
  }
  function belowFoldHTML(p) {
    var out = "";
    /* 1. Complete o look — curado à mão, não algoritmo. Renderiza vazio
       na maioria dos produtos.                                        */
    var look = COMPLETE_LOOK[p.code];
    if (look) {
      out += '<section class="complete-look"><h2 class="display">Style it</h2>' +
        '<div class="complete-look__grid">' +
        '<figure class="well well--editorial" role="img" aria-label="Foto futura de campanha: o look completo Prescrição em movimento." title="Foto futura de campanha: o look completo Prescrição em movimento.">' +
        faceSpan(look.well.code, look.well.slot) + "</figure>" +
        '<div class="complete-look__cards">' +
        look.cards.map(byCode).filter(Boolean).map(function (lp) {
          return cardHTML(lp, { lookChips: true });
        }).join("") +
        "</div></div></section>";
    }
    /* 2. Vistos recentemente (limit 4, localStorage). */
    var recent = (store("vesse_recent") || []).filter(function (c) { return c !== p.code; })
      .map(byCode).filter(Boolean).slice(0, 4);
    if (recent.length) {
      out += '<section class="recent"><h2 class="display">Vistos recentemente</h2>' +
        '<div class="rail__grid">' + recent.map(function (rp) { return cardHTML(rp); }).join("") + "</div></section>";
    }
    /* (breadcrumb visível removido — direção do Pedro, 06/08. O
       BreadcrumbList do JSON-LD continua para SEO.) */
    return out;
  }
  function bindPDP(p, order) {
    $$(".size-opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.disabled) return;
        pdp.size = btn.getAttribute("data-size");
        pdp.added = false;
        syncBuybox();
      });
    });
    $$(".pdp-cta").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (allOut(p)) { openNotify(p, null); return; }
        /* Sem drawer: o CTA fica mudo até o Pedro escolher um tamanho
           no seletor inline. */
        if (!pdp.size) {
          var picker = $(".size-picker");
          if (picker) {
            picker.classList.add("is-nudge");
            setTimeout(function () { picker.classList.remove("is-nudge"); }, 666);
          }
          return;
        }
        addToCart(p.code, pdp.size);
        pdp.added = true;
        syncBuybox();
        openCart();
        setTimeout(function () { pdp.added = false; syncBuybox(); }, 2000);
      });
    });
    var fav = $(".btn-fav");
    fav.addEventListener("click", function () {
      var favs = store("vesse_favs") || [];
      var i = favs.indexOf(p.code);
      if (i === -1) favs.push(p.code); else favs.splice(i, 1);
      store("vesse_favs", favs);
      fav.setAttribute("aria-pressed", i === -1 ? "true" : "false");
      fav.classList.toggle("is-on", i === -1);
    });
    var favs0 = store("vesse_favs") || [];
    if (favs0.indexOf(p.code) !== -1) { fav.setAttribute("aria-pressed", "true"); fav.classList.add("is-on"); }
    /* zoom full-viewport com trilho de thumbs de 100px */
    $$(".well--pdp").forEach(function (fig) {
      fig.addEventListener("click", function () {
        openZoom(p, order, parseInt(fig.getAttribute("data-idx"), 10));
      });
    });
    /* bullets do swipe mobile + gatilho do ATC fixo (mobile) */
    var gallery = $(".gallery");
    window.addEventListener("scroll", function () {
      var rect = gallery.getBoundingClientRect();
      var atc = $(".sticky-atc");
      if (atc) atc.classList.toggle("is-show", rect.top < -200);
    }, { passive: true });
    gallery.addEventListener("scroll", function () {
      var i = Math.round(gallery.scrollLeft / gallery.clientWidth);
      $$(".gallery__bullet").forEach(function (b, j) { b.classList.toggle("is-active", j === i); });
    }, { passive: true });
  }
  function openZoom(p, order, start) {
    var overlay = document.createElement("div");
    overlay.className = "zoom";
    overlay.innerHTML =
      '<button type="button" class="zoom__close icon-btn" aria-label="Fechar">' + ICONS.close + "</button>" +
      '<figure class="well zoom__main"' + wellAttrs(p, order[start]) + '>' +
      faceSpan(p.code, order[start]) + "</figure>" +
      '<div class="zoom__thumbs">' + order.map(function (slot, i) {
        return '<figure class="well zoom__thumb' + (i === start ? " is-active" : "") + '" data-slot-idx="' + i +
          '"' + wellAttrs(p, slot) + ' tabindex="0">' +
          faceSpan(p.code, slot) + "</figure>";
      }).join("") + "</div>";
    document.body.appendChild(overlay);
    document.body.classList.add("no-scroll");
    function close() { overlay.remove(); document.body.classList.remove("no-scroll"); }
    $(".zoom__close", overlay).addEventListener("click", close);
    $$(".zoom__thumb", overlay).forEach(function (th) {
      th.addEventListener("click", function () {
        var i = parseInt(th.getAttribute("data-slot-idx"), 10);
        $(".zoom__main .well__face", overlay).setAttribute("data-slot", order[i]);
        $$(".zoom__thumb", overlay).forEach(function (x, j) { x.classList.toggle("is-active", j === i); });
      });
    });
  }
  function recentPush(code) {
    var list = store("vesse_recent") || [];
    list = [code].concat(list.filter(function (c) { return c !== code; })).slice(0, 8);
    store("vesse_recent", list);
  }
  function injectProductJSONLD(p) {
    var base = "https://www.vesseclub.com/produto.html?code=" + encodeURIComponent(p.code);
    var group = {
      "@context": "https://schema.org", "@type": "ProductGroup",
      "name": p.title, "url": base, "brand": { "@type": "Brand", "name": "Vèsse Club" },
      "productGroupID": p.code, "variesBy": ["size"],
      "hasVariant": Object.keys(p.sizes).map(function (sz) {
        return {
          "@type": "Product", "name": p.title + " — " + sz, "size": sz,
          "offers": {
            "@type": "Offer", "priceCurrency": "BRL", "price": p.price,
            "availability": p.sizes[sz] === "out" ? "https://schema.org/OutOfStock" : "https://schema.org/InStock"
          }
        };
      })
    };
    var crumbs = {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.vesseclub.com/" },
        { "@type": "ListItem", "position": 2, "name": "Collections" },
        { "@type": "ListItem", "position": 3, "name": p.title }
      ]
    };
    [group, crumbs].forEach(function (obj) {
      var s = document.createElement("script");
      s.type = "application/ld+json";
      s.textContent = JSON.stringify(obj);
      document.head.appendChild(s);
    });
  }

  /* ---------------- home ---------------- */
  function renderRail(el, viewKey) {
    var view = VIEWS[viewKey];
    var items = CATALOG.filter(view.filter).slice(0, 4);
    el.innerHTML = items.map(function (p) { return cardHTML(p); }).join("");
    bindCards(el);
  }
  function initHome() {
    /* Rail do drop — sem toggle (direção do Pedro). */
    var railDrop = $("#rail-drop .rail__grid");
    if (railDrop) renderRail(railDrop, "divine-therapy");
  }

  /* ---------------- brief de fotografia (Alterações 02, 2.3) ----------
     Ferramenta interna gerada 100% do CATALOG. FORA da nav e do footer
     — acessível só por URL direta (pages/brief-fotos.html).           */
  function initBrief() {
    var root = $("#brief-root");
    if (!root) return;
    var groups = [
      { label: "Moletons", types: ["Moletom"] },
      { label: "Camisetas", types: ["Camiseta"] },
      { label: "Calças / Shorts", types: ["Calça", "Shorts"] },
      { label: "Bonés", types: ["Boné"] },
      { label: "Meias", types: ["Meia"] }
    ];
    var totalShots = 0, existing = 0;
    CATALOG.forEach(function (p) {
      totalShots += p.slots.length;
      /* status "✓ existe" quando o produto ganhar o mapa `photos`
         (slot → arquivo) — hoje tudo é "produzir" */
      if (p.photos) existing += p.slots.filter(function (s) { return p.photos[s]; }).length;
    });
    function statusOf(p, slot) {
      return (p.photos && p.photos[slot]) ?
        '<span class="brief-ok">&#10003; existe</span>' :
        '<span class="brief-todo">— produzir</span>';
    }
    var blocks = groups.map(function (g) {
      var items = CATALOG.filter(function (p) { return g.types.indexOf(p.type) !== -1; });
      if (!items.length) return "";
      return '<h2 class="display brief-group">' + esc(g.label) + "</h2>" +
        items.map(function (p) {
          var rows = p.slots.map(function (slot) {
            return "<tr><td>_" + esc(slot) + "</td><td>" + esc(slotDesc(p, slot)) + "</td><td>" +
              esc(SLOT_SPECS[slot].master) + "</td><td>" + statusOf(p, slot) + "</td></tr>";
          }).join("");
          return '<section class="brief-block">' +
            '<p class="label">' + esc(p.code) + "</p>" +
            '<h3 class="brief-title">' + esc(p.title) + "</h3>" +
            '<table class="brief-table"><thead><tr><th>Slot</th><th>Descrição da foto</th><th>Master</th><th>Status</th></tr></thead>' +
            "<tbody>" + rows + "</tbody></table></section>";
        }).join("");
    }).join("");
    var stills = '<h2 class="display brief-group">Stills editoriais</h2>' +
      '<section class="brief-block">' +
      '<table class="brief-table"><thead><tr><th>Ref</th><th>Página</th><th>Descrição</th><th>Master</th><th>Status</th></tr></thead><tbody>' +
      EDITORIAL_STILLS.map(function (s) {
        return "<tr><td>" + esc(s.code + "_" + s.slot) + "</td><td>" + esc(s.page) + "</td><td>" + esc(s.note) +
          "</td><td>" + esc(s.master || "2000×2800 WebP (5:7)") +
          '</td><td><span class="brief-todo">— produzir</span></td></tr>';
      }).join("") + "</tbody></table></section>";
    root.innerHTML =
      '<header class="brief-head">' +
      '<h1 class="display">Brief de fotografia</h1>' +
      '<p class="brief-totals">' + CATALOG.length + " produtos · " + (totalShots - existing) +
      " fotos a produzir (" + existing + " existentes) · meta: mediana de 5 fotos por produto</p>" +
      '<p class="brief-note">Gerado do catálogo. Ordem de galeria: 01 → 06 → 07 → 08 → 09 → 04 → 02. ' +
      'Nos slots _06/_07 de produto de conjunto, o modelo veste a peça coordenada — o cross-sell acontece dentro da fotografia.</p>' +
      "</header>" + blocks + stills;
  }

  /* ---------------- hooks de conteúdo (bureau, guias, editoriais) ------ */
  function initHooks() {
    $$("[data-cards]").forEach(function (el) {
      var codes = el.getAttribute("data-cards").split(",");
      el.innerHTML = codes.map(function (c) {
        var p = byCode(c.trim());
        return p ? cardHTML(p) : "";
      }).join("");
      bindCards(el);
    });
    $$("[data-rail]").forEach(function (el) {
      renderRail(el, el.getAttribute("data-rail"));
    });
    $$("[data-shipping]").forEach(function (el) { el.innerHTML = SHIPPING_HTML; });
    $$("[data-pay]").forEach(function (el) { el.textContent = "Pague com " + CONTACT.pay; });
    $$("[data-contact-line]").forEach(function (el) {
      el.innerHTML = contactIconsHTML();
    });
    $$("[data-faq]").forEach(function (el) {
      el.innerHTML = FAQ.map(function (item) {
        return '<div class="acc__item">' +
          '<button type="button" class="acc__q">' + esc(item.q) +
          '<span class="mnav__chevron">' + ICONS.chevron + "</span></button>" +
          '<div class="acc__a"><p>' + esc(item.a) + "</p></div></div>";
      }).join("");
    });
    /* bloco do clube — só onde a página pedir explicitamente */
    $$("[data-members]").forEach(function (el) {
      el.innerHTML = membersBlockHTML();
    });
    /* accordions: um bind global cobre os gerados (FAQ) e os estáticos
       (página do clube) */
    $$(".acc__q").forEach(function (btn) {
      btn.addEventListener("click", function () {
        btn.parentElement.classList.toggle("is-open");
      });
    });
    $$("[data-guide]").forEach(function (el) {
      el.innerHTML = guideTableHTML(el.getAttribute("data-guide"));
    });
    /* módulos de vídeo: só mostram o <video> quando o master existir e
       carregar; qualquer erro mantém o well placeholder no lugar */
    $$(".video-mod").forEach(function (mod) {
      var video = $("video", mod);
      if (!video) return;
      function on() { mod.classList.add("has-video"); }
      function off() { mod.classList.remove("has-video"); }
      video.addEventListener("loadeddata", on);
      video.addEventListener("error", off);
      $$("source", video).forEach(function (s) { s.addEventListener("error", off); });
      if (video.readyState >= 2) on();
    });
  }

  /* ---------------- boot ---------------- */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeDrawer();
      $$(".zoom, .modal").forEach(function (el) { el.remove(); });
      document.body.classList.remove("no-scroll");
    }
  });

  function boot() {
    document.body.insertAdjacentHTML("afterbegin", chromeHeaderHTML());
    document.body.insertAdjacentHTML("beforeend", chromeFooterHTML());
    initHeader();
    updateCartCount();
    if (PAGE === "plp") initPLP();
    else if (PAGE === "pdp") initPDP();
    else if (PAGE === "home") initHome();
    else if (PAGE === "brief") initBrief();
    initHooks();
    initMembersForms();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
