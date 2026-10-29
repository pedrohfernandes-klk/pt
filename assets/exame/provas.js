/* Provas em cartões (29/10/2026): o estado de cada grupo neste aparelho, lido das chaves que as lições gravam
   (prova-AAAA-Nf-gN, com versao, lida, melhor e totalMelhor; só conta a versão da lição, data-versao). Conquistado com 80 % ou mais, como nos índices dos módulos. */
(function(){"use strict";
function ler(k){try{return JSON.parse(localStorage.getItem(k)||"null")}catch(e){return null}}
function pintar(){Array.prototype.forEach.call(document.querySelectorAll("[data-chave]"),function(el){
 var st=ler(el.getAttribute("data-chave")),out=el.querySelector("[data-estado]"),v=el.getAttribute("data-versao");if(!out)return;
 /* uma lição refeita (outra versão) recomeça do zero no motor: aqui, volta a «Por fazer» */
 if(!st||!st.lida||(v&&st.versao!==v)){el.setAttribute("data-feito","nao");out.textContent="Por fazer";return}
 var m=Number(st.melhor)||0,t=Number(st.totalMelhor)||Number(st.total)||0,conq=t>0&&m>=Math.ceil(.8*t);
 el.setAttribute("data-feito",conq?"conquistado":"feito");out.textContent=(conq?"Conquistado":"Feito")+": melhor resultado "+m+" de "+t;
});}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",pintar);else pintar();
window.addEventListener("pageshow",pintar);
})();
