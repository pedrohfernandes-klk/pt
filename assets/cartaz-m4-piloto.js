/* 02/11/2026: recursos nativos do piloto M4; sem novo estado de progresso. */
(function () {
  'use strict';
  const main = document.querySelector('main[data-m4-piloto]');
  if (!main) return;
  const resources = main.querySelector('.m4-recursos');
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape' || !resources.open || !resources.contains(document.activeElement)) return;
    resources.open = false;
    resources.querySelector('summary').focus();
  });
}());
