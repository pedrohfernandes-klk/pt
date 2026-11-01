/* 01/11/2026: aquecimentos do exame, sem alterar o progresso das lições. */
(function () {
  'use strict';
  const d = JSON.parse(document.getElementById('exame-aquecimento-dados').textContent);
  const params = new URLSearchParams(location.search);
  const projetado = params.get('projetar') === '1';
  const retorno = '../../' + (projetado ? '?projetar=1' : '') + '#' + d.sessao + '/';
  // O motor pede fe ao fechar o cartão. Nas lacunas, devolvemos só o retorno
  // das alternativas efetivamente escolhidas; f continua a explicar o conjunto.
  d.cartoes.filter(c => c.t === 'completar').forEach(c => {
    const fallback = c.fe;
    Object.defineProperty(c, 'fe', {enumerable: true, get() {
      const errors = c.lacunas.map((gap, k) => {
        const select = document.querySelector('#baralho select[data-k="' + k + '"]');
        if (!select || select.value === '') return '';
        const chosen = Number(select.value);
        return chosen !== gap.c && gap.fe ? gap.fe[chosen] || '' : '';
      }).filter(Boolean);
      return errors.length ? errors.join(' ') : fallback;
    }});
  });
  document.querySelectorAll('[data-exame-voltar]').forEach(a => { a.href = retorno + 'aquecer'; });
  const relogio = EPIRelogio.criar(document.getElementById('relogio-aquecer'), {
    max: 10, passo: 1, rotulo: 'Tempo para aquecer',
    chave: projetado ? null : 'pt-exame-relogio-v2-' + d.sessao + '-aquecer'
  });
  document.addEventListener('click', ev => {
    const a = ev.target.closest('a');
    if (a && a.hash === '#' + d.sessao + '/ler' && relogio.estado().corre) relogio.pausar();
  });
  EPIJogo.montar({
    casca: EPICasca.pagina(), el: document.getElementById('baralho'), itens: d.cartoes,
    chave: 'aquecimento-exame-' + d.sessao, versao: d.versao,
    titulo: 'Aquecer: ' + d.titulo, marca: 'Exame', variar: false, aula: true, gestalt: true,
    mostrarAnterior: params.get('recomecar') !== '1',
    percurso: retorno + 'aquecer', percursoRotulo: 'Voltar à sessão',
    seguinte: retorno + 'ler', seguinteRotulo: 'Continuar a sessão',
    depois: '<p>Volta à sessão para ler, planear e escrever no caderno.</p>'
  });
}());
