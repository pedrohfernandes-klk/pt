/* 02/11/2026: contrato F2/F3 v1. Fonte Português; nenhuma página o carrega antes da validação dos tipos.
   Peças registadas fora do motor. Não escreve armazenamento nem altera o banco. */
(function (root) {
  'use strict';
  if (root.EPITiposMais) throw new Error('O adaptador dos tipos adicionais já está carregado');
  root.EPITipos = root.EPITipos || {};
  var sessoes = new WeakMap(), memoria = new Map();
  function norm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9' ]/g, '').trim(); }
  // Mesmo algoritmo de pistaPara no motor; o teste compara as duas funções.
  function pistaPara(x, pistas) {
    if (!pistas || !pistas.length) return null;
    var q = norm((x.p || '') + ' ' + (x.frase || '')).split(' ').filter(function (w) { return w.length > 3; });
    var melhor = null, m = -1;
    pistas.forEach(function (p) {
      var n = 0, pw = norm(p).split(' ');
      q.forEach(function (w) { if (pw.indexOf(w) >= 0) n++; });
      if (n > m) { m = n; melhor = p; }
    });
    return melhor;
  }
  function projecao() {
    return /[?&]projetar=1(?:&|$)/.test(location.search) || document.documentElement.classList.contains('epi-projection') || document.documentElement.classList.contains('em-projecao');
  }
  function semente(texto) {
    var n = 2166136261;
    for (var i = 0; i < texto.length; i++) n = Math.imul(n ^ texto.charCodeAt(i), 16777619);
    return function () { n += 0x6D2B79F5; var t = n; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  function resultado(r) {
    if (!r || typeof r.ok !== 'boolean' || !Number.isInteger(r.certas) || !Number.isInteger(r.total) || r.total <= 0 || r.certas < 0 || r.certas > r.total || r.ok !== (r.certas === r.total)) throw new Error('Resultado incoerente');
    if (!Array.isArray(r.erros) || r.erros.length > 2 || r.erros.some(function (s) { return typeof s !== 'string'; })) throw new Error('Retornos de erro inválidos');
    if (!Array.isArray(r.falhas) || r.falhas.some(function (k) { return typeof k !== 'string' && typeof k !== 'number'; })) throw new Error('Identificadores de falhas inválidos');
    return r;
  }
  function congelar(api) {
    api.el.querySelectorAll('[data-tipo-ext] input,[data-tipo-ext] button,[data-tipo-ext] select,[data-tipo-ext] textarea').forEach(function (e) {
      if ('checked' in e) { if (e.checked) e.setAttribute('checked', ''); else e.removeAttribute('checked'); }
      if (e.tagName === 'SELECT') Array.from(e.options).forEach(function (o) { if (o.selected) o.setAttribute('selected', ''); else o.removeAttribute('selected'); });
      e.disabled = true; e.setAttribute('disabled', '');
    });
  }
  function restaurar(obj, chave, tinha, valor) { if (tinha) obj[chave] = valor; else delete obj[chave]; }
  function terminar(x, api, ctx, r, revelar) {
    if (api.estado.fechado) return;
    r = resultado(r);
    congelar(api);
    if (!ctx.projecao) memoria.set(ctx.chaveMemoria, r.falhas.slice());
    var tinhaF = Object.prototype.hasOwnProperty.call(x, 'f'), f = x.f;
    var tinhaFe = Object.prototype.hasOwnProperty.call(x, 'fe'), fe = x.fe;
    var folha = api.C && api.C.folha, abrir = folha && folha.abrir;
    x.f = (revelar ? '' : 'Acertaste ' + r.certas + ' de ' + r.total + '. ') + (f || '');
    x.fe = r.erros.join(' ');
    // A faixa e a fotografia recebem «Resposta» antes de foto(), sem tocar no motor.
    if (revelar && abrir) folha.abrir = function (o) {
      o.titulo = 'Resposta'; o.pontos = '';
      var b = api.el.querySelector('.cartao .f-rev:last-of-type b');
      if (b) b.textContent = 'Resposta:';
      return abrir.call(folha, o);
    };
    try { api.fecha(revelar || r.ok, null, !r.ok && r.certas > 0); }
    finally {
      if (revelar && abrir) folha.abrir = abrir;
      restaurar(x, 'f', tinhaF, f); restaurar(x, 'fe', tinhaFe, fe);
    }
  }
  function criarContexto(x, api) {
    var chave = String(api.cfg.chave || '') + '\u0000' + x.id;
    var ctx = {
      projecao: projecao(),
      repeticao: Array.isArray(api.cfg.itens) && api.cfg.itens.indexOf(x) < 0,
      falhas: memoria.has(chave) ? memoria.get(chave).slice() : null,
      chaveMemoria: chave,
      partes: function () { return Array.isArray(x.partes) ? x.partes.slice() : String(x.texto || '').trim().split(/\s+/).filter(Boolean); },
      ordem: function (indices) {
        var a = indices.slice(), aleatorio = ctx.projecao || api.cfg.aula ? semente(String(api.cfg.chave || '') + '|' + x.id + '|' + x.p) : Math.random;
        for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(aleatorio() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
        return a;
      },
      atualizar: function (completa, mensagem, rotulo) {
        var b = api.C && api.C.acao('[data-confirmar]');
        if (b) { b.disabled = api.estado.fechado || !completa; if (rotulo) b.textContent = rotulo; }
        var conta = api.el.querySelector('.tm-conta'), viva = api.el.querySelector('.tm-viva');
        if (conta) conta.textContent = mensagem;
        if (viva) viva.textContent = mensagem;
      },
      focar: function (e) {
        if (!e || !e.isConnected || e.disabled) e = api.el.closest('.casca-corpo') || api.el;
        if (!e.hasAttribute('tabindex') && !/^(BUTTON|INPUT|SELECT|TEXTAREA|A)$/.test(e.tagName)) e.setAttribute('tabindex', '-1');
        e.focus({preventScroll: true});
      }
    };
    return ctx;
  }
  function registar(nome, def) {
    if (!nome || root.EPITipos[nome]) throw new Error('Tipo repetido: ' + nome);
    if (!def || !def.rot || !def.como || typeof def.criar !== 'function') throw new Error('Definição incompleta');
    function obter(x, api) {
      var s = sessoes.get(api.estado);
      if (!s) {
        if (!x.id) throw new Error('O cartão adicional precisa de id');
        var ctx = criarContexto(x, api), pec = def.criar(x, api, ctx);
        ['html', 'ligar', 'confirmar', 'revelar'].forEach(function (m) { if (!pec || typeof pec[m] !== 'function') throw new Error('Método em falta: ' + m); });
        s = {ctx: ctx, pec: pec}; sessoes.set(api.estado, s);
      }
      return s;
    }
    root.EPITipos[nome] = {
      rot: def.rot, como: def.como,
      html: function (x, api) { return obter(x, api).pec.html(); },
      ligar: function (x, api) { obter(x, api).pec.ligar(); },
      acoes: function (x, api) {
        var s = obter(x, api), a = [], pista = pistaPara(x, api.cfg.pistas);
        if (pista) a.push({t: 'Pista', cls: 'sec', attrs: {'data-pista-ess': ''}, onclick: function (ev) {
          if (api.estado.fechado || api.estado.pista) return;
          api.estado.pista = true;
          var q = api.el.querySelector('.q'), p = document.createElement('p');
          p.className = 'pista'; p.innerHTML = 'Pista: ' + api.it(pista);
          if (q) q.insertAdjacentElement('afterend', p);
          if (ev && ev.currentTarget) ev.currentTarget.disabled = true;
        }});
        if (s.ctx.projecao) a.push({t: 'Mostrar resposta', cls: 'sec', attrs: {'data-mostrar': ''}, onclick: function () {
          if (api.estado.fechado) return;
          terminar(x, api, s.ctx, s.pec.revelar(), true);
        }});
        a.push({t: 'Confirmar', cls: 'prim', attrs: {'data-confirmar': ''}, disabled: true, onclick: function () {
          if (api.estado.fechado) return;
          var r = s.pec.confirmar();
          if (r !== null) terminar(x, api, s.ctx, r, false);
        }});
        return a;
      }
    };
  }
  root.EPITiposMais = {versaoContrato: 1, registar: registar, pistaPara: pistaPara};
})(window);
