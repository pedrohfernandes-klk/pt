/* 06/11/2026: decisão 148. Recursos nativos dos nove índices (nasce de cartaz-m4-piloto.js); sem novo estado de progresso. */
(function () {
  'use strict';
  const main = document.querySelector('main[data-cz-indice]');
  if (!main) return;
  const resources = main.querySelector('.cz-recursos');
  if (!resources) return;
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || !resources.open || !resources.contains(document.activeElement)) return;
    resources.open = false;
    resources.querySelector('summary').focus();
  });

  /* 06/11/2026: decisão 173. Abaixo de 640 px, o modo noturno passa para a barra de cima (nav.migalhas, a seguir ao botão de
     projetar que projection-launcher.js lá põe) e o acesso do docente passa para o menu «Recursos do módulo», como no M4
     publicado; nada flutua por cima do texto. A partir de 640 px, os dois voltam ao sítio de sempre, a flutuar no fim do
     <body>. Só se mudam de lugar elementos que já existem (os mesmos rótulos, a mesma ordem entre eles); nada se escreve. */
  /* 06/11/2026: decisão 173, revisão de 6/11: telemóvel é tudo o que não cumpre (min-width: 640px), o mesmo limite do CSS;
     com (max-width: 639px), uma janela com zoom (639,2 px a 125 %) não cumpria nenhum dos dois e os botões flutuavam por
     cima do texto. */
  const desktop = window.matchMedia('(min-width: 640px)');
  function phone() { return !desktop.matches; }
  const bar = document.querySelector('body > nav.migalhas');
  const tools = document.querySelector('body > details.route-teacher-tools');
  /* No M3, no M5 e no M6 há, logo antes, a ligação direta aos guiões (a.teacher-access), no mesmo canto: acompanha o menu e
     fica por baixo do botão, como estava (sai num pedido próprio, decisão 173). */
  const twin = tools && tools.previousElementSibling && tools.previousElementSibling.matches('a.teacher-access')
    ? tools.previousElementSibling : null;
  const home = tools ? tools.nextSibling : null;
  const menu = tools ? tools.querySelector(':scope > nav') : null;
  /* O menu dos materiais traz no HTML o lugar flutuante (position:fixed); dentro dos recursos fica no fluxo. */
  const floatingStyle = menu ? menu.getAttribute('style') : null;
  const holder = document.createElement('div');
  holder.className = 'cz-docente';

  function keepFocus(move) {
    const active = document.activeElement;
    move();
    if (active && active !== document.body && active.isConnected && document.activeElement !== active) {
      active.focus({preventScroll: true});
    }
  }

  function placeTeacher() {
    if (!tools) return;
    if (phone()) { // 06/11/2026: decisão 173, revisão de 6/11 (era phone.matches).
      if (holder.parentNode === resources) return;
      if (twin) holder.appendChild(twin);
      holder.appendChild(tools);
      if (menu) menu.removeAttribute('style');
      resources.appendChild(holder);
    } else {
      if (holder.parentNode !== resources) return;
      const back = home && home.parentNode === document.body ? home : null;
      if (twin) document.body.insertBefore(twin, back);
      document.body.insertBefore(tools, back);
      if (menu && floatingStyle !== null) menu.setAttribute('style', floatingStyle);
      holder.remove();
    }
  }

  function placeNight() {
    const slot = document.querySelector('[data-appearance-control]');
    if (!slot || !bar) return;
    if (phone()) { // 06/11/2026: decisão 173, revisão de 6/11 (era phone.matches).
      if (slot.parentNode === bar) return;
      slot.removeAttribute('data-appearance-floating');
      bar.appendChild(slot);
    } else {
      if (slot.parentNode !== bar) return;
      slot.setAttribute('data-appearance-floating', '');
      document.body.appendChild(slot);
    }
  }

  function place() { keepFocus(function () { placeTeacher(); placeNight(); }); }

  /* O acesso do docente muda já (está no HTML, antes deste script); o modo noturno nasce com appearance.js no
     DOMContentLoaded, e esse ouvinte foi registado antes deste. */
  placeTeacher();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', placeNight, {once: true});
  else placeNight();
  /* 06/11/2026: decisão 173, revisão de 6/11: a mudança ouve-se no (min-width: 640px). */
  if (desktop.addEventListener) desktop.addEventListener('change', place);
  else if (desktop.addListener) desktop.addListener(place);
}());
