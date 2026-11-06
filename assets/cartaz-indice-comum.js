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
}());
