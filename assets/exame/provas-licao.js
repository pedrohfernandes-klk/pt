/* Provas em cartões (29/10/2026): o que as lições de exame/provas/ juntam ao motor dos cartões (jogo.js).
   1. O tipo «item»: um item de escolha múltipla da prova, com as quatro opções pela ordem da prova, de (A) a (D).
      O tipo «escolha» do motor mostra só três opções e baralha-as; aqui ficam as quatro, como na prova, e as citações
      ficam em redondo (o motor põe em itálico as citações longas; na prova não estão).
   2. Em projeção, «Mostrar resposta» também no tipo «item» e no tipo «rever» (rever-frase.js): marca a resposta certa e a faixa
      diz «Resposta», sem pontos, como nos outros tipos; assim, só com R e →, a turma percorre a lição toda.
   3. Os cartões com o rótulo «Item n da prova» ganham a classe «oficial», para as citações aparecerem como na prova.
   4. No Grupo III, enquanto a imagem não estiver no sítio, o campo «ver» traz uma ligação para a página da prova: a figura deixa
      de ser um botão de ampliar, para a ligação funcionar com o rato e com o teclado.
   5. Na impressão, os desdobráveis («A grelha oficial», «As linhas do item», …) abrem-se e voltam a fechar no fim. */
(function(){"use strict";
var T=window.EPITipos=window.EPITipos||{};
function proj(){return /[?&]projetar=1(&|$)/.test(location.search)||document.documentElement.classList.contains("epi-projection")}
function letra(j){return "("+String.fromCharCode(65+j)+")"}
function redondo(h){return String(h).replace(/<span class="cit">([^<]*)<\/span>/g,"$1")}
function mostrar(api,botao){if(api.estado.fechado)return;if(botao)botao.classList.add("bom");api.fecha(true,botao);
 var f=document.querySelector("[data-c-folha]");if(f){var sp=f.querySelectorAll(".c-veredito > span");if(sp[1])sp[1].textContent="Resposta";var pts=f.querySelector(".c-pts");if(pts)pts.parentNode.removeChild(pts)}
 var fr=api.el.querySelector(".cartao .f-rev:last-of-type b");if(fr&&/^Certo/.test(fr.textContent))fr.textContent="Resposta:"}
function botaoMostrar(fn){return {t:"Mostrar resposta",cls:"sec",attrs:{"data-mostrar":""},onclick:fn}}
T.item={rot:"Item da prova",como:"escolher",
 html:function(x,api){return '<p class="q">'+redondo(api.it(x.p))+'</p><div class="ops ops-item">'+x.o.map(function(o,j){return '<button class="op" type="button" data-j="'+j+'"><span class="tx"><span class="letra">'+letra(j)+'</span> '+redondo(api.it(o))+'</span></button>'}).join("")+'</div>'},
 acoes:function(x,api){return proj()?[botaoMostrar(function(){mostrar(api,api.$('button.op[data-j="'+Number(x.c)+'"]',api.el))})]:[]},
 ligar:function(x,api){var bs=api.$$("button.op",api.el);bs.forEach(function(b){b.onclick=function(){if(api.estado.fechado)return;var j=+b.dataset.j,ok=j===Number(x.c);b.classList.add(ok?"bom":"mau");bs.forEach(function(o){if(+o.dataset.j===Number(x.c))o.classList.add("bom")});api.fecha(ok,b)}})}};
function embrulharRever(){var R=T.rever;if(!R||R.__provas)return;var a0=R.acoes;R.__provas=true;
 R.acoes=function(x,api){var a=(a0?a0.call(R,x,api):[])||[];if(!proj())return a;return a.concat([botaoMostrar(function(){if(api.estado.fechado)return;
  var b=api.$('[data-rever-op="'+Number(x.c)+'"]',api.el),p=api.$("[data-rever-prev]",api.el),l=api.$("[data-rever-label]",api.el),at=x.frase.indexOf(x.trecho);
  if(p&&at>=0)p.innerHTML=api.esc(x.frase.slice(0,at))+"<strong>"+api.esc(x.o[x.c])+"</strong>"+api.esc(x.frase.slice(at+x.trecho.length));if(l)l.textContent="Versão revista";
  var c=api.C&&api.C.acao?api.C.acao("[data-rever-confirmar]"):null;if(c)c.disabled=true;mostrar(api,b)})])}}
function marcar(){var b=document.getElementById("baralho"),c=b&&b.querySelector(".cartao"),r=c&&c.querySelector(".rot");if(c&&r)c.classList.toggle("oficial",/\bItem \d+ da prova\b/.test(r.textContent));
 if(b)Array.prototype.forEach.call(b.querySelectorAll("figure.ver-fig"),function(f){if(!f.querySelector("a.ver-pdf")||f.classList.contains("ver-ligacao"))return;f.classList.add("ver-ligacao");["role","tabindex","aria-label"].forEach(function(a){f.removeAttribute(a)});f.onclick=null;f.onkeydown=null})}
function iniciar(){embrulharRever();var b=document.getElementById("baralho");if(!b||!window.MutationObserver)return;new MutationObserver(marcar).observe(b,{childList:true,subtree:true});marcar()}
window.addEventListener("beforeprint",function(){Array.prototype.forEach.call(document.querySelectorAll("#baralho details.mais:not([open])"),function(d){d.setAttribute("open","");d.setAttribute("data-aberto-impressao","")})});
window.addEventListener("afterprint",function(){Array.prototype.forEach.call(document.querySelectorAll("#baralho details[data-aberto-impressao]"),function(d){d.removeAttribute("open");d.removeAttribute("data-aberto-impressao")})});
embrulharRever();
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",iniciar);else iniciar();
})();
