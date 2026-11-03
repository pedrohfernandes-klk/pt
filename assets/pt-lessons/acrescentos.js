/* 02/11/2026: F0. Preserva índices de progresso quando entram cartões novos.
   Não altera versões, resultados ou conclusão. Só se ativa com data-chave/data-lote/data-novos. */
(function (root) {
  'use strict';
  function objeto(x) { return x !== null && typeof x === 'object' && !Array.isArray(x); }
  function posicoes(novos) {
    if (typeof novos === 'string' && !/^\s*\d+\s*(,\s*\d+\s*)*$/.test(novos)) throw new Error('Posições inválidas');
    var r = typeof novos === 'string' ? novos.split(',').map(function (x) { return Number(x.trim()); }) : novos;
    if (!Array.isArray(r) || !r.length || (typeof novos === 'string' && !novos.trim())) throw new Error('Posições em falta');
    r = r.slice().sort(function (a, b) { return a - b; });
    if (r.some(function (x, i) { return !Number.isSafeInteger(x) || x < 0 || (i && r[i - 1] === x); })) throw new Error('Posições inválidas');
    return r;
  }
  function indice(k, novos) {
    var n = Number(k);
    novos.forEach(function (p) { if (n >= p) n++; });
    return n;
  }
  function remapear(estado, novos) {
    var p = posicoes(novos), r = Object.assign({}, estado);
    if (objeto(estado.exposicoes)) {
      r.exposicoes = {};
      Object.keys(estado.exposicoes).forEach(function (k) {
        var j = /^\d+$/.test(k) && Number.isSafeInteger(Number(k)) ? String(indice(k, p)) : k;
        Object.defineProperty(r.exposicoes, j, {value: estado.exposicoes[k], enumerable: true, writable: true, configurable: true});
      });
    }
    if (typeof estado.ult === 'string' && /^\d+(,\d+)*$/.test(estado.ult)) {
      r.ult = estado.ult.split(',').map(function (k) { return String(indice(k, p)); }).sort().join(',');
    }
    return r;
  }
  function lotes(raw) {
    var r = raw == null ? [] : JSON.parse(raw);
    if (!Array.isArray(r) || r.some(function (x) { return typeof x !== 'string'; })) throw new Error('Registo de lotes inválido');
    return r;
  }
  function aplicar(storage, chave, lote, novos, projecao) {
    if (projecao) return {estado: 'projecao'};
    if (!chave || !lote) return {estado: 'invalido'};
    var marca = chave + '-acrescentos', anterior, bruto, lista, estado, p, muda;
    try {
      p = posicoes(novos); anterior = storage.getItem(marca); lista = lotes(anterior);
      if (lista.indexOf(lote) >= 0) return {estado: 'aplicado'};
      bruto = storage.getItem(chave); estado = bruto == null ? null : JSON.parse(bruto);
      if (estado !== null && !objeto(estado)) return {estado: 'invalido'};
      muda = estado && ((Number(estado.tentativas) > 0) || (objeto(estado.exposicoes) && Object.keys(estado.exposicoes).length > 0));
      // A marca é independente de K, mesmo na primeira visita e nas lições com versao.
      // Se a escrita de K falhar, repõe-se a marca anterior antes de permitir nova tentativa.
      storage.setItem(marca, JSON.stringify(lista.concat(lote)));
      if (muda) {
        try { storage.setItem(chave, JSON.stringify(remapear(estado, p))); }
        catch (erro) {
          if (anterior === null) storage.removeItem(marca); else storage.setItem(marca, anterior);
          throw erro;
        }
      }
      return {estado: muda ? 'migrado' : 'marcado'};
    } catch (erro) { return {estado: 'indisponivel'}; }
  }
  function protegerImportacao(recebido, lotesAtuais, lotesRecebidos) {
    if (!objeto(recebido)) return recebido;
    var a = lotes(lotesAtuais), b = lotes(lotesRecebidos);
    if (!a.some(function (lote) { return b.indexOf(lote) < 0; })) return recebido;
    var r = Object.assign({}, recebido);
    delete r.exposicoes; delete r.ult;
    return r;
  }
  var api = {versaoContrato: 1, remapear: remapear, aplicar: aplicar, protegerImportacao: protegerImportacao};
  root.EPIAcrescentos = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined') {
    var s = document.currentScript;
    if (s && s.dataset.chave && s.dataset.lote) {
      var proj = /[?&]projetar=1(?:&|$)/.test(location.search) || document.documentElement.classList.contains('epi-projection') || document.documentElement.classList.contains('em-projecao');
      if (!proj) {
        try { aplicar(localStorage, s.dataset.chave, s.dataset.lote, s.dataset.novos, false); } catch (erro) { /* O conteúdo continua disponível sem armazenamento. */ }
      }
    }
  }
})(typeof window === 'undefined' ? globalThis : window);
