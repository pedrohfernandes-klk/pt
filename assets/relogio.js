/* Relógio do aluno (27/10/2026). O aluno escolhe a duração, até ao máximo previsto para a produção.
   Pode pausar duas vezes; depois disso, parar obriga a recomeçar do início. Não avalia nem envia nada:
   o estado fica só neste dispositivo, quando o navegador o permite.
   Uso: <div data-relogio data-max="60" data-passo="5" data-rotulo="Produção" data-chave="..."></div>
   ou EPIRelogio.criar(elemento, {max, min, passo, valor, rotulo, chave, aoTerminar, aoMudar}). */
(function () {
 "use strict";
 if (window.EPIRelogio) return;
 var PAUSAS = 2, todos = [], ciclo = null, conta = 0;

 function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }
 function mmss(s) { s = Math.max(0, Math.round(s)); return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }
 function minutos(s) { var m = s / 60; return (Math.round(m * 10) / 10).toLocaleString("pt-PT"); }
 function ler(chave) { if (!chave) return null; try { var v = JSON.parse(localStorage.getItem(chave) || "null"); return v && typeof v === "object" && !Array.isArray(v) ? v : null; } catch (_) { return null; } }
 function gravar(chave, v) { if (!chave) return; try { localStorage.setItem(chave, JSON.stringify(v)); } catch (_) { /* Continua a funcionar nesta página. */ } }
 function numero(v, d) { v = Number(v); return Number.isFinite(v) ? v : d; }

 function criar(host, o) {
  o = o || {};
  var passo = Math.max(1, Math.round(numero(o.passo, 1) * 60)),
      max = Math.max(passo, Math.round(numero(o.max, 10) * 60 / passo) * passo),
      min = Math.min(max, Math.max(passo, Math.round(numero(o.min, o.passo || 1) * 60 / passo) * passo)),
      rotulo = o.rotulo || "Tempo", id = "relogio-" + (++conta);
  function ajusta(s) { s = Math.round(numero(s, max) / passo) * passo; return Math.min(max, Math.max(min, s)); }
  var s = { dur: ajusta(numero(o.valor, max / 60) * 60), resto: 0, fim: 0, corre: false, usadas: 0, iniciado: false };
  s.resto = s.dur;
  var g = ler(o.chave);
  if (g && numero(g.dur, -1) === ajusta(g.dur) && numero(g.resto, -1) >= 0 && g.resto <= g.dur && [0, 1, 2].indexOf(g.usadas) >= 0) {
   s.dur = g.dur; s.resto = Math.round(g.resto); s.usadas = g.usadas; s.iniciado = !!g.iniciado;
   s.corre = !!g.corre && numero(g.fim, 0) > 0; s.fim = s.corre ? g.fim : 0;
  }

  var raiz = el("div", "relogio"); raiz.id = id; raiz.setAttribute("role", "group"); raiz.setAttribute("aria-labelledby", id + "-rotulo");
  var cab = el("div", "relogio-cab"), nome = el("p", "relogio-rotulo", rotulo); nome.id = id + "-rotulo";
  var limite = el("p", "relogio-max", "até " + minutos(max) + " min");
  cab.append(nome, limite);
  var mostrador = el("output", "relogio-mostrador"); mostrador.id = id + "-tempo"; mostrador.setAttribute("aria-label", "Tempo que falta");
  var barra = el("span", "relogio-barra"), enchimento = el("i"); barra.setAttribute("aria-hidden", "true"); barra.appendChild(enchimento);
  var duracao = el("div", "relogio-duracao"), legenda = el("label", "", "Duração"), menos = el("button", "relogio-passo", "−"),
      campo = el("input"), unidade = el("span", "", "min"), mais = el("button", "relogio-passo", "+");
  legenda.htmlFor = id + "-duracao"; campo.id = id + "-duracao"; campo.type = "number"; campo.inputMode = "decimal";
  campo.min = String(min / 60); campo.max = String(max / 60); campo.step = String(passo / 60);
  menos.type = mais.type = "button"; menos.setAttribute("aria-label", "Menos " + minutos(passo) + " min"); mais.setAttribute("aria-label", "Mais " + minutos(passo) + " min");
  duracao.append(legenda, menos, campo, unidade, mais);
  var botoes = el("div", "relogio-botoes"), principal = el("button", "relogio-principal"), recomecar = el("button", "relogio-recomecar", "Recomeçar");
  principal.type = recomecar.type = "button"; botoes.append(principal, recomecar);
  var pausas = el("p", "relogio-pausas"), pontos = el("span", "relogio-pontos"), pausasTexto = el("span");
  pontos.setAttribute("aria-hidden", "true"); for (var i = 0; i < PAUSAS; i++) pontos.appendChild(el("i"));
  pausas.append(pontos, pausasTexto);
  var estado = el("p", "relogio-estado"); estado.setAttribute("role", "status"); estado.setAttribute("aria-live", "polite");
  raiz.append(cab, mostrador, barra, duracao, botoes, pausas, estado);
  host.replaceChildren(raiz);
  var espelhos = [], avisouMinuto = false, terminou = s.iniciado && !s.corre && s.resto === 0;

  function resto() { return s.corre ? Math.max(0, Math.min(s.resto, Math.ceil((s.fim - Date.now()) / 1000))) : s.resto; }
  function guarda() { gravar(o.chave, { dur: s.dur, resto: s.resto, fim: s.fim, corre: s.corre, usadas: s.usadas, iniciado: s.iniciado }); }
  function anuncia(t) { estado.textContent = t; if (o.aoMudar) try { o.aoMudar(t, api.estado()); } catch (_) {} }
  function congela() { s.resto = resto(); s.corre = false; s.fim = 0; }
  function poeAoInicio(texto) { s.corre = false; s.fim = 0; s.resto = s.dur; s.usadas = 0; s.iniciado = false; avisouMinuto = false; terminou = false; guarda(); pinta(); if (texto) anuncia(texto); }

  function pinta() {
   var r = resto();
   if (s.corre && r === 0) { s.corre = false; s.resto = 0; s.fim = 0; guarda(); }
   if (r === 0 && s.iniciado && !terminou) { terminou = true; anuncia("Tempo terminado. Relê o que escreveste."); if (o.aoTerminar) try { o.aoTerminar(); } catch (_) {} }
   if (s.corre && r <= 60 && r > 0 && s.dur > 120 && !avisouMinuto) { avisouMinuto = true; anuncia("Falta um minuto."); }
   mostrador.textContent = mmss(r);
   enchimento.style.width = (s.dur ? 100 * r / s.dur : 0) + "%";
   raiz.dataset.estado = r === 0 && s.iniciado ? "fim" : s.corre ? "corre" : s.iniciado ? "pausa" : "pronto";
   raiz.dataset.pausas = String(PAUSAS - s.usadas);
   var livre = !s.iniciado;
   campo.disabled = menos.disabled = mais.disabled = !livre;
   if (document.activeElement !== campo) campo.value = String(s.dur / 60);
   menos.disabled = !livre || s.dur <= min; mais.disabled = !livre || s.dur >= max;
   principal.disabled = r === 0 && s.iniciado;
   principal.textContent = !s.iniciado ? "Iniciar" : r === 0 ? "Terminado" : s.corre ? (s.usadas < PAUSAS ? "Pausar" : "Parar e recomeçar") : "Continuar";
   recomecar.disabled = !s.iniciado;
   Array.prototype.forEach.call(pontos.children, function (p, k) { p.classList.toggle("usada", k < s.usadas); });
   pausasTexto.textContent = s.usadas < PAUSAS ? (PAUSAS - s.usadas === 1 ? "Resta 1 pausa" : "Restam " + (PAUSAS - s.usadas) + " pausas") : "Sem pausas: parar recomeça do início";
   espelhos.forEach(function (e) { e.textContent = mmss(r); e.dataset.estado = raiz.dataset.estado; });
   gere();
  }

  function carrega() {
   if (!s.iniciado) { s.iniciado = true; s.resto = s.dur; s.fim = Date.now() + s.resto * 1000; s.corre = true; guarda(); pinta(); anuncia("Relógio a contar: " + minutos(s.dur) + " min."); return; }
   if (resto() === 0) return;
   if (s.corre) {
    if (s.usadas >= PAUSAS) { poeAoInicio("Usaste as duas pausas: o relógio voltou ao início (" + minutos(s.dur) + " min). Inicia de novo quando estiveres pronto."); return; }
    congela(); s.usadas++; guarda(); pinta();
    anuncia(s.usadas < PAUSAS ? "Pausa 1 de 2, em " + mmss(s.resto) + "." : "Pausa 2 de 2, em " + mmss(s.resto) + ". Se parares outra vez, o relógio recomeça do início.");
    return;
   }
   s.fim = Date.now() + s.resto * 1000; s.corre = true; guarda(); pinta(); anuncia("O relógio continua.");
  }
  function muda(delta) { if (s.iniciado) return; s.dur = ajusta(s.dur + delta); s.resto = s.dur; guarda(); pinta(); }
  principal.addEventListener("click", carrega);
  recomecar.addEventListener("click", function () { poeAoInicio("Relógio de volta ao início: " + minutos(s.dur) + " min."); });
  menos.addEventListener("click", function () { muda(-passo); });
  mais.addEventListener("click", function () { muda(passo); });
  campo.addEventListener("change", function () { if (s.iniciado) return; s.dur = ajusta(numero(String(campo.value).replace(",", "."), s.dur / 60) * 60); s.resto = s.dur; guarda(); pinta(); });

  var api = {
   elemento: raiz,
   // Uma paragem vinda de fora (por exemplo, mudar de exercício) conta como pausa.
   pausar: function () { if (s.corre && resto() > 0) { carrega(); return true; } return false; },
   recomecar: function () { poeAoInicio(); },
   espelhar: function (n) { espelhos.push(n); pinta(); return n; },
   estado: function () { return { duracao: s.dur, resto: resto(), corre: s.corre, iniciado: s.iniciado, pausasUsadas: s.usadas, max: max, min: min }; },
   destruir: function () { var k = todos.indexOf(api); if (k >= 0) todos.splice(k, 1); gere(); },
   _pinta: pinta
  };
  todos.push(api); pinta();
  return api;
 }

 function gere() {
  var algum = todos.some(function (r) { return r.estado().corre; });
  if (algum && !ciclo) ciclo = setInterval(function () { todos.slice().forEach(function (r) { if (!document.body.contains(r.elemento)) r.destruir(); else r._pinta(); }); }, 250);
  else if (!algum && ciclo) { clearInterval(ciclo); ciclo = null; }
 }

 function automatico() {
  document.querySelectorAll("[data-relogio]:not([data-relogio-pronto])").forEach(function (n) {
   n.setAttribute("data-relogio-pronto", "");
   n.relogio = criar(n, { max: n.dataset.max, min: n.dataset.min, passo: n.dataset.passo, valor: n.dataset.valor, rotulo: n.dataset.rotulo, chave: n.dataset.chave });
  });
 }
 window.EPIRelogio = { criar: criar, automatico: automatico, formato: mmss, PAUSAS: PAUSAS };
 if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", automatico); else automatico();
})();
