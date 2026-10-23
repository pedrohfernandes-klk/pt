/* 23/10/2026, aulas claras (plano de melhoria, padrão da Justiça do Lente): peças das lições refeitas.
   Vídeo: <div class="ju-video" data-yt="ID11" data-ini="s" data-fim="s" data-t="título" data-m="canal" data-dur="1 min" data-rot="Ver o excerto">
     o leitor (youtube-nocookie, com início e fim) só nasce ao toque; o motor guarda cópias dos cartões para rever, e uma cópia com o
     leitor volta a ser o botão.
   Conceito: <div class="cc" data-cc> com .cc-passo (o caso, mais perto, o nome, o que não é) e o botão [data-cc-mais]; cada toque
     mostra o passo seguinte; ao imprimir, tudo à vista.
   Lados (decidir e depois abrir) e «Ler mais» são <details> e não precisam de código. */
(function(){"use strict";
var vivos=typeof WeakSet==="function"?new WeakSet():null;
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function botao(c){var d=c.dataset;c.classList.remove("tocado");c.innerHTML='<p class="ju-t">'+esc(d.t)+'</p><p class="ju-m">'+esc(d.m)+'</p><button type="button">'+esc(d.rot||"Ver o vídeo")+(d.dur?' <span>('+esc(d.dur)+')</span>':'')+'</button>'}
var ROT=["Mais perto","O nome","O que não é"];
function arrumar(){
 [].forEach.call(document.querySelectorAll(".ju-video"),function(c){var f=c.querySelector("iframe");if(f&&!(vivos&&vivos.has(f)))botao(c)});
 [].forEach.call(document.querySelectorAll("[data-cc]"),function(c){var b=c.querySelector("[data-cc-mais]"),ps=c.querySelectorAll(".cc-passo"),k=[].filter.call(ps,function(p){return !p.hidden}).length;if(b&&k>=ps.length)b.hidden=true})}
document.addEventListener("click",function(ev){
 var b=ev.target.closest&&ev.target.closest(".ju-video button");
 if(b){var c=b.closest(".ju-video"),d=c.dataset;if(!/^[A-Za-z0-9_-]{11}$/.test(d.yt||""))return;
  [].forEach.call(document.querySelectorAll(".ju-video.tocado"),function(o){if(o!==c)botao(o)});
  var f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+d.yt+"?autoplay=1&rel=0&cc_load_policy=1&hl=pt-PT"+(d.ini?"&start="+d.ini:"")+(d.fim?"&end="+d.fim:"");f.title=d.titulo||d.t||"Vídeo";f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.setAttribute("allowfullscreen","");f.referrerPolicy="strict-origin-when-cross-origin";if(vivos)vivos.add(f);c.innerHTML="";c.classList.add("tocado");c.appendChild(f);try{f.focus()}catch(x){}return}
 var m=ev.target.closest&&ev.target.closest("[data-cc-mais]");
 if(m){var cc=m.closest("[data-cc]"),ps=[].slice.call(cc.querySelectorAll(".cc-passo")),k=ps.filter(function(p){return !p.hidden}).length;if(k<ps.length){ps[k].hidden=false;ps[k].classList.add("cc-novo")}k++;if(k>=ps.length){m.hidden=true;var u=ps[ps.length-1];if(u&&u.focus){u.setAttribute("tabindex","-1");try{u.focus({preventScroll:true})}catch(x){}}}else m.firstChild.nodeValue=ROT[k-1]+" "}});
var alvo=document.getElementById("baralho");if(alvo&&window.MutationObserver)new MutationObserver(arrumar).observe(alvo,{childList:true,subtree:true});
window.addEventListener("beforeprint",function(){[].forEach.call(document.querySelectorAll("[data-cc] .cc-passo"),function(p){p.hidden=false})});})();
