/* Revision cards use the existing lesson shell, scoring, feedback and retry flow. */
(function(){'use strict';
 window.EPITipos=window.EPITipos||{};
 function sentence(x,value,esc){var at=x.frase.indexOf(x.trecho);return esc(x.frase.slice(0,at))+'<strong>'+esc(value)+'</strong>'+esc(x.frase.slice(at+x.trecho.length));}
 window.EPITipos.rever={rot:'Experimenta e revê',como:'escolher',
  html:function(x,api){var esc=api.esc,order=EPIJogo.baralhar(x.o.map(function(_,i){return i;}));
   return '<p class="q">'+api.it(x.p)+'</p><p class="gl"><b>Passagem de apoio:</b> '+esc(x.apoio)+'</p><p class="gl" data-rever-label>Rascunho</p><p class="linha-ordem" data-rever-prev aria-live="polite" aria-atomic="true">'+sentence(x,x.trecho,esc)+'</p><div class="ops">'+order.map(function(i){return '<button class="op" type="button" data-rever-op="'+i+'" data-j="'+i+'" aria-pressed="false">'+esc(x.o[i])+'</button>';}).join('')+'</div><p class="gl">Experimenta uma substituição. Podes mudar antes de confirmar.</p><details><summary>Comparar com o rascunho</summary><p>'+sentence(x,x.trecho,esc)+'</p></details>';},
  acoes:function(){return [{t:'Confirmar revisão',cls:'prim',attrs:{'data-rever-confirmar':''},disabled:true}];},
  ligar:function(x,api){var buttons=api.$$('[data-rever-op]',api.el),preview=api.$('[data-rever-prev]',api.el),confirm=api.C.acao('[data-rever-confirmar]'),selected=null;
   buttons.forEach(function(button){button.onclick=function(){selected=Number(button.dataset.reverOp);buttons.forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});preview.innerHTML=sentence(x,x.o[selected],api.esc);api.$('[data-rever-label]',api.el).textContent='Versão em teste';confirm.disabled=false;};});
   confirm.onclick=function(){if(selected===null||api.estado.fechado)return;var button=buttons.filter(function(b){return Number(b.dataset.reverOp)===selected;})[0];api.fecha(selected===x.c,button);};
  }
 };
})();
