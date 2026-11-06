// 05/11/2026: decisão 153. Melhora a peça «i» dos créditos, igual byte a byte no Português e no Lente. Sem este ficheiro,
// a <details> abre e fecha na mesma (toque, clique, Enter e Espaço); com ele, Escape fecha e devolve o foco ao «i», um
// toque ou clique fora fecha, abrir um fecha o outro (o name="info-i" já o faz nos navegadores atuais) e, na projeção,
// fica tudo fechado. Nunca abre nada sozinho e não grava nada no aparelho.
(function (d, w) {
  'use strict';
  if (w.EPIInfoI) return;
  var SEL = 'details.info-i', html = d.documentElement;
  function abertos() { return [].slice.call(d.querySelectorAll(SEL + '[open]')); }
  // Um só aberto de cada vez.
  d.addEventListener('toggle', function (e) {
    var t = e.target;
    if (!t || !t.matches || !t.matches(SEL) || !t.open) return;
    abertos().forEach(function (x) { if (x !== t) x.open = false; });
  }, true);
  // Escape fecha o «i» aberto e devolve o foco ao seu «i». Com um diálogo aberto por cima (o ampliador das imagens, por
  // exemplo), o Escape é desse diálogo: este ouvinte corre na captura, antes dos outros, e deixa-o passar.
  // 05/11/2026: um «i» aberto dentro do próprio diálogo (um cartão montado num ecrã sobreposto) fecha-se primeiro; o diálogo
  // só se fecha com o Escape seguinte.
  function dialogoPorCima(x) {
    var L = d.querySelectorAll('.amp-ov,[aria-modal="true"]');
    for (var i = 0; i < L.length; i++) if (L[i].getClientRects().length && !L[i].contains(x)) return true;
    return false;
  }
  w.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    var x = abertos()[0];
    if (!x || e.defaultPrevented || dialogoPorCima(x)) return;
    var a = d.activeElement, dentro = x.contains(a) || !a || a === d.body || a === html;
    x.open = false;
    if (dentro) { var s = x.querySelector('summary'); if (s) s.focus(); }
    e.stopPropagation();
  }, true);
  // Um toque ou clique fora fecha.
  d.addEventListener('click', function (e) {
    abertos().forEach(function (x) { if (!x.contains(e.target)) x.open = false; });
  });
  // Quando a projeção começa, tudo fechado (o «i» continua a abrir se o docente lhe tocar).
  function projetada() {
    return /[?&]projetar=1(&|$)/.test(location.search) || /(^|\s)(em-projecao|epi-projection)(\s|$)/.test(html.className) ||
      html.hasAttribute('data-cz-projection');
  }
  var antes = false;
  function fechaNaProjecao() {
    var agora = projetada();
    if (agora && !antes) abertos().forEach(function (x) { x.open = false; });
    antes = agora;
  }
  // As lições projetadas com ?projetar=1 não marcam o <html>: esta marca dá ao «i» o aspeto da projeção.
  if (/[?&]projetar=1(&|$)/.test(location.search)) html.setAttribute('data-ii-projecao', '');
  fechaNaProjecao();
  if ('MutationObserver' in w) new MutationObserver(fechaNaProjecao).observe(html, { attributes: true, attributeFilter: ['class', 'data-cz-projection'] });
  w.EPIInfoI = { fechar: function () { abertos().forEach(function (x) { x.open = false; }); } };
})(document, window);
