/* Leitura RTP opcional: nenhum pedido de media antes da ação do utilizador. */
(function(){'use strict';
 function button(){var b=document.createElement('button');b.type='button';b.setAttribute('data-rtp-load','');b.textContent='Carregar leitura (RTP)';return b}
 document.addEventListener('click',function(e){
  var b=e.target.closest('[data-rtp-load],[data-rtp-close]');if(!b)return;var box=b.closest('[data-rtp-leitura]');if(!box)return;
  if(b.hasAttribute('data-rtp-close')){var old=box.querySelector('video');if(old){old.pause();old.removeAttribute('src');old.load()}var again=button();box.replaceChildren(again);again.focus();return}
  var url;try{url=new URL(box.getAttribute('data-rtp-src'))}catch(x){return}
  if(url.protocol!=='https:'||url.hostname!=='cdn-ondemand.rtp.pt'||url.pathname.indexOf('/nas2.share/portaleducacao-videos/')!==0||!url.pathname.endsWith('.mp4'))return;
  var v=document.createElement('video');v.controls=true;v.preload='none';v.playsInline=true;v.setAttribute('aria-label',box.getAttribute('data-rtp-title')||'Leitura de poesia');v.src=url.href;
  var close=document.createElement('button');close.type='button';close.setAttribute('data-rtp-close','');close.textContent='Fechar leitor';
  v.addEventListener('error',function(){if(!v.isConnected||box.querySelector('[data-rtp-error]'))return;var p=document.createElement('p');p.setAttribute('data-rtp-error','');p.setAttribute('role','status');p.textContent='Não foi possível reproduzir aqui. Abre a fonte da RTP ou faz a tarefa com a alternativa sem vídeo.';box.appendChild(p)});
  box.replaceChildren(v,close);close.focus();
  var observer=new MutationObserver(function(){if(!v.isConnected){if(v.getAttribute("src")){v.pause();v.removeAttribute("src");v.load()}observer.disconnect()}});observer.observe(document.body,{childList:true,subtree:true});
 });
})();
