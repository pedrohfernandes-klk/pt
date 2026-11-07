/* 01/11/2026: aquecimentos do exame, sem alterar o progresso das lições. */
(function () {
  'use strict';
  const d = JSON.parse(document.getElementById('exame-aquecimento-dados').textContent);
  const params = new URLSearchParams(location.search);
  const projetado = params.get('projetar') === '1';
  const retorno = '../../' + (projetado ? '?projetar=1' : '') + '#' + d.sessao + '/';
  // O motor pede fe ao fechar o cartão. Nas lacunas, devolvemos só o retorno
  // das alternativas efetivamente escolhidas; f continua a explicar o conjunto.
  // 07/11/2026 (achado 65): na ronda «Só os que errei», o motor copia os cartões com JSON e o getter avalia-se
  // nessa altura, sem nenhuma lacuna escolhida; a cópia fica com o retorno próprio do cartão (fallback), que já
  // não é genérico. Limitação aceite: nessa ronda não há retorno por alternativa.
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
  // 07/11/2026 (achados 1 e 50): com ?projetar=1, o regresso e a continuação levam «projetar=1» no endereço, e
  // assets/projection-launcher.js trocava-os todos por «Projetar esta página · QR para a turma». Marcam-se como já
  // tratados antes de o lançador correr (este script vem antes no documento, e o seu observador também é criado
  // antes); só as ligações para a sessão (#sNN/…) são marcadas: a de «Projetar» do menu continua a ser do lançador.
  const paraSessao = 'a[href*="#' + d.sessao + '/"]:not([data-epi-projection-ready])';
  const marcar = () => document.querySelectorAll(paraSessao).forEach(a => a.setAttribute('data-epi-projection-ready', ''));
  document.querySelectorAll('[data-exame-voltar]').forEach(a => { a.href = retorno + 'aquecer'; });
  marcar();
  // 07/11/2026 (achados 13, 58 e 70): aula:true fica, porque conserva a ordem dos bancos: sem ele, o motor baralha os
  // cartões de fazer entre os de leitura (estes ficam no seu lugar) e as opções sem semente, e perdia-se a ordem que o
  // banco garante (nunca três cartões seguidos do mesmo tipo, perguntas antigas intercaladas, a mesma ordem na projeção e
  // nos telemóveis); o fim diz o que acabou: o aquecimento, não a aula nem a lição.
  // 07/11/2026 (revisão de 7/11, ponto 15): ao voltar depois de feito, o motor escreve «Já feita» (a lição); aqui é o
  // aquecimento, «Já feito».
  const FIM = [
    ['.cartao.fim .rot span', 'A aula acaba aqui', 'Aquecimento feito'],
    ['.cartao.fim .rot span', 'Já feita', 'Já feito'],
    ['.cartao.fim .grande.lido', 'Fim da lição.', 'Fim do aquecimento.'],
    ['.cartao.fim p', 'Já respondeste a esta lição', 'Já fizeste este aquecimento']
  ];
  const acertarFim = () => FIM.forEach(([sel, antes, depois]) => document.querySelectorAll(sel).forEach(el => {
    if (el.children.length === 0 && el.textContent.includes(antes)) el.textContent = el.textContent.replace(antes, depois);
  }));
  new MutationObserver(() => { marcar(); acertarFim(); }).observe(document.body, {childList: true, subtree: true});
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
