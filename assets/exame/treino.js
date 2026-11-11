/* 11/11/2026: motor dos treinos da preparação de exame (exame/treinos/).
   Cada treino traz os seus passos em <script type="application/json" id="treino-dados">; a entrada só mostra o estado guardado. */
(function(){
'use strict';
var PREFIXO='exame-treino:';
/* entrada dos treinos: o que está guardado neste dispositivo */
Array.prototype.forEach.call(document.querySelectorAll('[data-estado]'),function(e){
  var t='Ainda não começaste.';
  try{var s=window.localStorage.getItem(PREFIXO+e.getAttribute('data-estado')+':v2');
    if(s){var o=JSON.parse(s),n=0,k,v1=false,v2=false;
      for(k in o.q){if(o.q[k]&&o.q[k].r)n++;}
      for(k in o.txt){if(o.txt[k].g)v1=true;if(o.txt[k].g2||o.txt[k].papel2)v2=true;}
      if(n||v1){t='Neste dispositivo: '+n+(n===1?' pergunta respondida':' perguntas respondidas')+(v1?'; primeira versão guardada':'')+(v2?'; versão revista guardada':'')+'.';}}
  }catch(x){t='';}
  e.textContent=t;
});
var DADOS=document.getElementById('treino-dados');
if(!DADOS)return;
var P=JSON.parse(DADOS.textContent), CH=PREFIXO+P.id+':v2';
window.TREINO=P;
var VIU=P.viu||'os critérios';
var S=ler();
function vazio(){return {v:2,q:{},txt:{},campos:{},passo:0,recolhido:false};}
function ler(){
  try{var t=window.localStorage.getItem(CH);if(t){var o=JSON.parse(t);if(o&&o.v===2){o.q=o.q||{};o.txt=o.txt||{};o.campos=o.campos||{};return o;}}}catch(e){}
  return vazio();
}
var guardaOk=true;
var PE_OK='As tuas respostas e as duas versões do teu texto ficam só neste dispositivo (localStorage). Nada é enviado.';
var PE_NAO='Este navegador não deixa guardar: as tuas respostas ficam só enquanto esta página estiver aberta. Nada é enviado.';
function guardar(){
  try{window.localStorage.setItem(CH,JSON.stringify(S));guardaOk=true;}catch(e){guardaOk=false;}
  var a=document.getElementById('aviso-guarda');
  if(a){a.hidden=guardaOk;}
  var pe=document.getElementById('pe-guarda');
  if(pe){pe.textContent=guardaOk?PE_OK:PE_NAO;}
}
function el(tag,at,fi){
  var e=document.createElement(tag),k;
  if(at){for(k in at){if(!Object.prototype.hasOwnProperty.call(at,k))continue;
    if(k==='html'){e.innerHTML=at[k];}
    else if(k==='text'){e.textContent=at[k];}
    else if(k==='on'){for(var ev in at.on){e.addEventListener(ev,at.on[ev]);}}
    else if(at[k]===true){e.setAttribute(k,'');}
    else if(at[k]!==false&&at[k]!=null){e.setAttribute(k,at[k]);}
  }}
  if(fi){(Array.isArray(fi)?fi:[fi]).forEach(function(f){if(f==null)return;e.appendChild(typeof f==='string'?document.createTextNode(f):f);});}
  return e;
}
function palavras(t){t=(t||'').trim();return t?t.split(/\s+/).length:0;}
function nPal(n){return n+(n===1?' palavra':' palavras');}
function hora(ts){try{var d=new Date(ts);return ('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2);}catch(e){return '';}}
var ETQ={oficial:'Item oficial',adaptado:'Item adaptado',treino:'Exercício de treino'};
function etq(t){return t?el('span',{'class':'etq '+t,text:ETQ[t]}):null;}
/* traz um elemento para a parte do ecrã que o texto de apoio fixo não tapa */
function aVista(e){
  try{
    var r=e.getBoundingClientRect(),topo=parseInt(document.documentElement.style.scrollPaddingTop,10)||12,vh=window.innerHeight,d=0;
    if(r.top<topo){d=r.top-topo;}
    else if(r.bottom>vh-8){d=Math.min(r.bottom-vh+8,r.top-topo);}
    if(d){window.scrollBy(0,d);}
  }catch(x){}
}

/* ---------- retorno ---------- */
var RES=['c1','c2','c3'];
function mostraRetorno(cx,tipo,titulo,html){
  cx.className='retorno '+tipo;cx.innerHTML='';
  cx.appendChild(el('span',{'class':'r-t',text:titulo}));
  cx.appendChild(el('div',{html:html}));
}
function certo(r){return r==='c1'||r==='c2'||r==='c3';}
function titCerto(q){return q.r==='c1'?'Certo, à primeira e sem ajuda':(q.r==='c2'?'Certo, à segunda, depois da pista':'Certo, à terceira, depois de duas pistas');}
function titPista(t){return t===1?'Pista':'Segunda pista';}
function restam(n){return n===1?'Tens mais uma tentativa.':'Tens mais duas tentativas.';}
function titExpl(max){return 'Explicação (depois de '+(max===3?'três':'duas')+' tentativas)';}

/* ---------- escolha ---------- */
function blocoEscolha(b){
  var q=S.q[b.id]||(S.q[b.id]={t:0,r:null,ten:[]});
  /* três tentativas; com três opções, a terceira já não seria uma escolha */
  var MAX=Math.min(3,b.o.length-1);
  var cx=el('div',{'class':'bloco q'});
  var e=etq(b.etq);if(e)cx.appendChild(e);
  var pid='p-'+b.id;
  cx.appendChild(el('p',{'class':'q-p',id:pid,html:b.p}));
  var ul=el('ul',{'class':'ops',role:'group','aria-labelledby':pid});
  var ret=el('div',{'class':'retorno',role:'status','aria-live':'polite',tabindex:'-1'});
  var bts=[];
  b.o.forEach(function(o,i){
    var bt=el('button',{type:'button','class':'op',on:{click:function(){escolhe(i);}}},[
      el('span',{'class':'l','aria-hidden':'true',text:'ABCDEF'.charAt(i)}),
      el('span',{'class':'m',html:'<span class="so-leitor">'+'ABCDEF'.charAt(i)+'. </span>'+o.t})]);
    bts.push(bt);ul.appendChild(el('li',null,bt));
  });
  cx.appendChild(ul);cx.appendChild(ret);
  function pinta(){
    bts.forEach(function(bt,i){
      var tent=q.ten.indexOf(i)>=0;
      bt.classList.toggle('tentada',tent);
      bt.classList.toggle('certa',!!q.r&&i===b.c);
      /* aria-disabled em vez de disabled: o foco do teclado não se perde */
      if(q.r||tent){bt.setAttribute('aria-disabled','true');}else{bt.removeAttribute('aria-disabled');}
    });
    if(certo(q.r)){mostraRetorno(ret,'certo',titCerto(q),b.f);}
    else if(q.r==='ex'){mostraRetorno(ret,'expl',titExpl(MAX),'<p>A opção adequada é a '+'ABCDEF'.charAt(b.c)+'.</p>'+b.f);}
    else if(q.ten.length){
      var n=q.ten.length;
      mostraRetorno(ret,'pista',titPista(n),(n===1?b.o[q.ten[0]].pista:(b.pista2||b.o[q.ten[n-1]].pista))+'<p><b>'+restam(MAX-n)+'</b></p>');
    }
  }
  function escolhe(i){
    if(q.r||q.ten.indexOf(i)>=0)return;
    if(i===b.c){q.r=RES[q.t];}
    else{q.t+=1;q.ten.push(i);if(q.t>=MAX){q.r='ex';}}
    guardar();pinta();atualizaPassos();aVista(ret);
  }
  pinta();
  return cx;
}

/* ---------- tocar ---------- */
function blocoTocar(b){
  var q=S.q[b.id]||(S.q[b.id]={t:0,r:null,sel:[]});
  var MAX=3;
  var cx=el('div',{'class':'bloco q'});
  var e=etq(b.etq);if(e)cx.appendChild(e);
  var pid='p-'+b.id;
  cx.appendChild(el('p',{'class':'q-p',id:pid,html:b.p}));
  var seg=el('div',{'class':'seg'+(b.modo==='versos'?' versos':''),role:'group','aria-labelledby':pid});
  var bts={};
  b.tokens.forEach(function(t,i){
    if(t.nl){seg.appendChild(el('span',{'class':'ln'}));return;}
    if(t.fixo){seg.appendChild(el('span',{'class':'fx',html:t.x}));seg.appendChild(document.createTextNode(' '));return;}
    var bt;
    if(b.modo==='versos'){
      bt=el('button',{type:'button','class':'tk','aria-pressed':'false',on:{click:function(){alterna(i);}}},[
        el('span',{'class':'vn',text:String(t.n)}),el('span',{html:'<span class="so-leitor">verso '+t.n+': </span>'+t.x})]);
    }else{
      bt=el('button',{type:'button','class':'tk','aria-pressed':'false',html:t.x,on:{click:function(){alterna(i);}}});
    }
    bts[i]=bt;seg.appendChild(bt);
    if(b.modo!=='versos')seg.appendChild(document.createTextNode(t.cola?'':' '));
  });
  cx.appendChild(seg);
  var ver=el('button',{type:'button','class':'btn forte',text:'Verificar',on:{click:verifica}});
  var lim=el('button',{type:'button','class':'btn leve',text:'Limpar a seleção',on:{click:function(){if(q.r)return;q.sel=[];av.textContent='';guardar();pinta(true);}}});
  cx.appendChild(el('div',{'class':'acoes'},[ver,lim]));
  var av=el('p',{'class':'estado',role:'status','aria-live':'polite'});
  cx.appendChild(av);
  var ret=el('div',{'class':'retorno',role:'status','aria-live':'polite',tabindex:'-1'});
  cx.appendChild(ret);
  function alterna(i){
    if(q.r)return;
    var k=q.sel.indexOf(i);if(k>=0)q.sel.splice(k,1);else q.sel.push(i);
    av.textContent='';
    guardar();pinta(true);
  }
  function contem(a,sub){return sub.every(function(x){return a.indexOf(x)>=0;});}
  function avalia(sel){
    var dentro=sel.every(function(x){return b.permitidos.indexOf(x)>=0;});
    var nuc=b.nucleos.some(function(n){return contem(sel,n);});
    return dentro&&nuc;
  }
  function pistaPara(sel){
    for(var i=0;i<b.pistas.length;i++){
      var r=b.pistas[i];
      if(r.so){if(sel.length&&sel.every(function(x){return r.so.indexOf(x)>=0;}))return r.x;}
      else if(r.se.some(function(x){return sel.indexOf(x)>=0;}))return r.x;
    }
    return b.falta;
  }
  function notas(sel){
    var out='';if(!b.notas)return out;
    sel.slice().sort(function(a,c){return a-c;}).forEach(function(x){if(b.notas[x]&&out.indexOf(b.notas[x])<0)out+='<p>'+b.notas[x]+'</p>';});
    return out;
  }
  function chaveSel(){return q.sel.slice().sort(function(a,c){return a-c;}).join(',');}
  function verifica(){
    if(q.r)return;
    if(!q.sel.length){av.textContent=b.modo==='versos'?'Ainda não escolheste: toca primeiro num verso.':'Ainda não escolheste: toca primeiro numa palavra.';aVista(av);return;}
    if(avalia(q.sel)){q.r=RES[q.t];}
    else{
      var k=chaveSel();
      /* a mesma seleção errada, verificada outra vez, não gasta tentativa */
      if(q.us===k){av.textContent='Já verificaste esta seleção e não gastaste outra tentativa. Muda a seleção antes de verificares de novo.';aVista(ret);return;}
      q.us=k;q.t+=1;
      if(q.t>=MAX){q.r='ex';}
      else{q.ult=q.t===1?pistaPara(q.sel):(b.pista2||pistaPara(q.sel));}
    }
    av.textContent='';
    guardar();pinta();atualizaPassos();aVista(ret);
  }
  function pinta(soSel){
    Object.keys(bts).forEach(function(k){
      var i=+k,bt=bts[k];
      var on=q.sel.indexOf(i)>=0;
      bt.setAttribute('aria-pressed',on?'true':'false');
      bt.disabled=!!q.r;
      bt.classList.toggle('ok',q.r==='ex'&&b.mostra.indexOf(i)>=0);
      if(q.r==='ex'){bt.setAttribute('aria-pressed',b.mostra.indexOf(i)>=0?'true':'false');}
    });
    ver.disabled=!!q.r;lim.disabled=!!q.r;
    if(soSel)return;
    if(certo(q.r)){mostraRetorno(ret,'certo',titCerto(q),notas(q.sel)+b.f);}
    else if(q.r==='ex'){mostraRetorno(ret,'expl',titExpl(MAX),'<p>Fica marcada uma resposta adequada.</p>'+b.f);}
    else if(q.t>0&&q.ult){mostraRetorno(ret,'pista',titPista(q.t),q.ult+'<p><b>'+restam(MAX-q.t)+'</b> Muda a seleção e verifica de novo.</p>');}
  }
  pinta();
  return cx;
}

/* ---------- campos, listas, grelhas ---------- */
function ligaCampo(inp,chave){
  if(S.campos[chave]!=null)inp.value=S.campos[chave];
  inp.addEventListener('input',function(){S.campos[chave]=inp.value;guardar();});
}
function blocoCampos(b){
  var cx=el('div',{'class':'bloco'});
  if(b.titulo)cx.appendChild(el('h3',{html:b.titulo}));
  if(b.intro)cx.appendChild(el('div',{html:b.intro}));
  b.campos.forEach(function(c){
    var id='c-'+b.id+'-'+c.id,chave=b.id+':'+c.id;
    cx.appendChild(el('label',{'class':'campo','for':id,html:c.rotulo}));
    if(c.ajuda)cx.appendChild(el('p',{'class':'ajuda',id:id+'-a',html:c.ajuda}));
    var inp;
    if(c.linhas&&c.linhas>1){inp=el('textarea',{id:id,rows:String(c.linhas)});}
    else{inp=el('input',{type:'text',id:id});}
    if(c.ajuda)inp.setAttribute('aria-describedby',id+'-a');
    ligaCampo(inp,chave);
    cx.appendChild(inp);
  });
  return cx;
}
function blocoLista(b){
  var cx=el('div',{'class':'bloco'});
  if(b.titulo)cx.appendChild(el('h3',{html:b.titulo}));
  if(b.intro)cx.appendChild(el('div',{html:b.intro}));
  b.itens.forEach(function(t,i){
    var chave=b.id+':'+i;
    var c=el('input',{type:'checkbox'});c.checked=!!S.campos[chave];
    c.addEventListener('change',function(){S.campos[chave]=c.checked;guardar();});
    cx.appendChild(el('label',{'class':'marca-l'},[c,el('span',{html:t})]));
  });
  return cx;
}
function blocoGrelha(b){
  var cx=el('div',{'class':'bloco'});
  if(b.titulo)cx.appendChild(el('h3',{html:b.titulo}));
  if(b.intro)cx.appendChild(el('div',{html:b.intro}));
  b.aspetos.forEach(function(t,i){
    var chave=b.id+':'+i,nome='g-'+b.id+'-'+i;
    var fs=el('fieldset',{'class':'radios'},[el('legend',{html:t})]);
    b.opcoes.forEach(function(o,j){
      var r=el('input',{type:'radio',name:nome,value:String(j)});
      if(String(S.campos[chave])===String(j))r.checked=true;
      r.addEventListener('change',function(){S.campos[chave]=j;guardar();});
      fs.appendChild(el('label',null,[r,el('span',{text:o})]));
    });
    cx.appendChild(fs);
  });
  return cx;
}
/* ---------- escrever e rever ---------- */
function txtDe(id){return S.txt[id]||(S.txt[id]={v1:'',papel:false,g:false});}
/* a primeira versão pode mudar sempre; se mudar depois de abertos os critérios, a página di-lo */
function alterada(T){
  if(!T.viu||!T.s)return false;
  return T.s.v1!==(T.v1||'')||T.s.papel!==!!T.papel||T.s.op!==(T.op==null?null:T.op);
}
function marcaAlt(T){
  var p=el('p',{'class':'alt',role:'status','aria-live':'polite'});
  p.at=function(){var a=alterada(T);p.hidden=!a;p.textContent=a?'Primeira versão alterada depois de veres '+VIU+'.':'';};
  p.at();return p;
}
function contador(ta){
  var p=el('p',{'class':'conta',role:'status','aria-live':'off'});
  function at(){p.innerHTML='<b>'+nPal(palavras(ta.value))+'</b> (contagem pela regra dos critérios: sequências separadas por espaços).';}
  ta.addEventListener('input',at);at();
  return p;
}
function radiosOp(b,T,nome,aoMudar){
  var fs=el('fieldset',{'class':'radios col'},[el('legend',{html:b.opRotulo||'A opção que assinalas'})]);
  b.opcoes.forEach(function(o,i){
    var r=el('input',{type:'radio',name:nome,value:String(i)});
    if(T.op===i)r.checked=true;
    r.addEventListener('change',function(){T.op=i;guardar();aoMudar();});
    fs.appendChild(el('label',null,[r,el('span',{html:o})]));
  });
  return fs;
}
function blocoEscrever(b){
  var T=txtDe(b.id);
  var cx=el('div',{'class':'bloco'});
  var id='t-'+b.id;
  var marca=marcaAlt(T);
  var est=el('p',{'class':'estado',role:'status','aria-live':'polite',tabindex:'-1'});
  var btG=el('button',{type:'button','class':'btn forte',text:'Guardar a primeira versão',on:{click:function(){
    if(b.opcoes&&T.op==null){est.className='estado';est.textContent='Escolhe primeiro uma opção.';return;}
    if(!(T.v1||'').trim()&&!T.papel){est.className='estado';est.textContent='Escreve na caixa ou marca que escreveste no papel.';return;}
    T.g=true;T.q=Date.now();guardar();pintaEst();atualizaPassos();pintaNav();est.focus({preventScroll:true});aVista(est);
  }}});
  var acoes=el('div',{'class':'acoes'},[btG]);
  function pintaEst(){
    marca.at();acoes.hidden=!!T.g;
    if(!T.g){est.className='estado';est.textContent='';return;}
    est.className='estado ok';
    if(!guardaOk){est.textContent='Primeira versão registada só enquanto esta página estiver aberta: este navegador não deixa guardar. Copia-a para o caderno. Podes passar ao passo seguinte.';}
    else{est.textContent='Primeira versão guardada neste dispositivo'+(T.q?' às '+hora(T.q):'')+'.'+(T.viu?'':' Feita sem pistas à vista.')+' Podes passar ao passo seguinte e podes alterá-la em qualquer altura.';}
  }
  function mudou(){pintaEst();atualizaPassos();pintaNav();}
  if(b.opcoes)cx.appendChild(radiosOp(b,T,'o-'+b.id,mudou));
  cx.appendChild(el('label',{'class':'campo','for':id,html:b.rotulo}));
  if(b.ajuda)cx.appendChild(el('p',{'class':'ajuda',html:b.ajuda}));
  var ta=el('textarea',{id:id,rows:String(b.linhas||8),spellcheck:'false'});
  ta.value=T.v1||'';
  ta.addEventListener('input',function(){T.v1=ta.value;guardar();marca.at();});
  cx.appendChild(ta);
  if(b.conta)cx.appendChild(contador(ta));
  var pc=el('input',{type:'checkbox'});pc.checked=!!T.papel;
  pc.addEventListener('change',function(){T.papel=pc.checked;guardar();marca.at();});
  cx.appendChild(el('label',{'class':'marca-l'},[pc,el('span',{html:b.papel||'Escrevi no papel (no caderno). Deixo a caixa vazia.'})]));
  cx.appendChild(marca);
  cx.appendChild(el('p',{'class':'ajuda antes-bt',html:guardaOk
    ?'O rascunho guarda-se automaticamente enquanto escreves, só neste dispositivo. Nada é enviado. «Guardar a primeira versão» abre o passo seguinte e não a fecha: podes alterá-la em qualquer altura. Se a alterares depois de veres '+VIU+', a página diz isso junto dela.'
    :'Este navegador não deixa guardar: o que escreves fica só enquanto esta página estiver aberta. Copia o teu texto para o caderno. Nada é enviado. «Guardar a primeira versão» abre o passo seguinte e não a fecha: podes alterá-la em qualquer altura.'}));
  cx.appendChild(acoes);
  cx.appendChild(est);
  pintaEst();
  return cx;
}
/* a primeira versão à vista (comparar e rever), com a possibilidade de a alterar */
function caixaV1(b,T,titulo,papelTxt){
  var cx=el('div');
  cx.appendChild(el('p',{'class':'col-t',text:titulo}));
  var marca=marcaAlt(T);
  var corpo=el('div');
  var aberto=false;
  var bt=el('button',{type:'button','class':'btn leve',on:{click:function(){aberto=!aberto;d();var f=aberto?corpo.querySelector('textarea'):bt;if(f)f.focus();}}});
  function d(){
    corpo.innerHTML='';marca.at();
    bt.textContent=aberto?'Fechar a alteração':'Alterar a primeira versão';
    bt.setAttribute('aria-expanded',aberto?'true':'false');
    if(aberto){
      if(b.opcoes)corpo.appendChild(radiosOp(b,T,'e-o-'+b.de,function(){marca.at();desenhaRegistos();}));
      var ta=el('textarea',{id:'e-'+b.de,rows:String(b.linhas||8),spellcheck:'false','aria-label':'A tua primeira versão'});
      ta.value=T.v1||'';
      ta.addEventListener('input',function(){T.v1=ta.value;guardar();marca.at();desenhaRegistos();});
      corpo.appendChild(ta);
      if(b.conta)corpo.appendChild(contador(ta));
      return;
    }
    if(b.opcoes&&T.op!=null)corpo.appendChild(el('p',{html:'<b>Opção que escolheste:</b> '+b.opcoes[T.op]}));
    corpo.appendChild(el('p',{'class':'v1',id:'v1-'+b.de,text:T.papel&&!T.v1?papelTxt:(T.v1||'')}));
    if(b.conta&&T.v1)corpo.appendChild(el('p',{'class':'conta',html:'<b>'+nPal(palavras(T.v1))+'</b>.'}));
  }
  d();
  cx.appendChild(marca);cx.appendChild(corpo);cx.appendChild(el('div',{'class':'acoes'},[bt]));
  return cx;
}
function blocoRever(b){
  var T=txtDe(b.de);
  var cx=el('div',{'class':'bloco'});
  if(!T.g){cx.appendChild(el('p',{text:'Ainda não guardaste a primeira versão.'}));return cx;}
  if(T.v2==null){T.v2=T.v1||'';}
  var id='r-'+b.de;
  var esq=caixaV1(b,T,'Primeira versão (por ti, sem pistas)','Escreveste a primeira versão no papel. Revê-a no papel, com outra cor, ou escreve aqui a versão revista.');
  var ta=el('textarea',{id:id,rows:String(b.linhas||8),spellcheck:'false'});ta.value=T.v2;
  var est=el('p',{'class':'estado',role:'status','aria-live':'polite'});
  function guardada(){
    est.className='estado ok';
    est.textContent=guardaOk?'Versão revista guardada neste dispositivo'+(T.q2?' às '+hora(T.q2):'')+'. As duas versões ficam lado a lado.'
      :'Versão revista registada só enquanto esta página estiver aberta: este navegador não deixa guardar. Copia-a para o caderno.';
  }
  if(T.g2)guardada();
  ta.addEventListener('input',function(){T.v2=ta.value;T.g2=false;guardar();est.className='estado';
    est.textContent=guardaOk?'Alterações por guardar como versão revista (o rascunho já ficou neste dispositivo).':'Alterações por guardar como versão revista.';
    atualizaPassos();desenhaRegistos();});
  var dir=el('div',null,[el('label',{'class':'col-t','for':id,text:'Versão revista (depois de veres '+VIU+')'}),ta]);
  if(b.conta)dir.appendChild(contador(ta));
  var pc=el('input',{type:'checkbox'});pc.checked=!!T.papel2;
  pc.addEventListener('change',function(){T.papel2=pc.checked;guardar();atualizaPassos();desenhaRegistos();});
  dir.appendChild(el('label',{'class':'marca-l'},[pc,el('span',{text:'Revi no papel, com outra cor.'})]));
  dir.appendChild(el('div',{'class':'acoes'},[el('button',{type:'button','class':'btn forte',text:'Guardar a versão revista',on:{click:function(){
    var t=(T.v2||'').trim();
    if(!T.papel2&&(!t||t===(T.v1||'').trim())){est.className='estado';est.textContent='Ainda não mudaste nada na versão revista. Altera o texto ou marca que reviste no papel.';return;}
    T.g2=true;T.q2=Date.now();guardar();guardada();atualizaPassos();desenhaRegistos();
  }}})]));
  dir.appendChild(est);
  cx.appendChild(el('div',{'class':'duas'},[esq,dir]));
  return cx;
}

function blocoVerCampos(b){
  var d=el('details',{'class':'dobra'},[el('summary',{text:b.titulo})]);
  var dentro=el('div',{'class':'dentro'});
  var algum=false;
  b.campos.forEach(function(c){
    var v=S.campos[b.id+':'+c.id];
    if(v&&String(v).trim()){algum=true;dentro.appendChild(el('p',null,[el('b',{text:c.rotulo+': '}),String(v)]));}
  });
  if(!algum)dentro.appendChild(el('p',{text:b.vazio}));
  d.appendChild(dentro);
  return el('div',{'class':'bloco'},d);
}
function blocoVer1(b){
  var T=txtDe(b.de);
  var cx=el('div',{'class':'bloco'});
  cx.appendChild(caixaV1(b,T,'A tua primeira versão (por ti, sem pistas)','Escreveste a primeira versão no papel. Tem-na à tua frente.'));
  return cx;
}
/* ---------- registo ---------- */
var registos=[];
function desenhaRegistos(){registos.forEach(function(f){f();});}
function blocoRegisto(){
  var cx=el('div',{'class':'bloco'});
  function d(){
    cx.innerHTML='';
    cx.appendChild(el('h3',{text:'O teu registo: o que fizeste sem ajuda e o que fizeste com ajuda'}));
    var linhas='';
    P.passos.forEach(function(p,pi){
      p.blocos.forEach(function(b){
        if(b.t==='escolha'||b.t==='tocar'){
          var q=S.q[b.id],r=q&&q.r,pl;
          if(r==='c1'){pl='<span class="pill s">Por ti, à primeira</span>';}
          else if(r==='c2'){pl='<span class="pill p">Com pista, à segunda</span>';}
          else if(r==='c3'){pl='<span class="pill p2">Com pista, à terceira</span>';}
          else if(r==='ex'){pl='<span class="pill e">Com explicação</span>';}
          else{pl='<span class="pill">Por fazer</span>';}
          linhas+='<tr><td>Passo '+(pi+1)+'</td><td>'+b.curto+'</td><td>'+pl+'</td></tr>';
        }
        if(b.t==='escrever'){
          var T=S.txt[b.id]||{};
          linhas+='<tr><td>Passo '+(pi+1)+'</td><td>'+b.curto+'</td><td>'+(T.g?(alterada(T)?'<span class="pill p">Alterada depois de veres '+VIU+'</span>':'<span class="pill s">Por ti, sem pistas à vista</span>'):'<span class="pill">Por fazer</span>')+'</td></tr>';
        }
        if(b.t==='rever'){
          var T2=S.txt[b.de]||{};
          linhas+='<tr><td>Passo '+(pi+1)+'</td><td>'+b.curto+'</td><td>'+((T2.g2||T2.papel2)?'<span class="pill p">Depois de veres '+VIU+'</span>':'<span class="pill">Por fazer</span>')+'</td></tr>';
        }
      });
    });
    cx.appendChild(el('div',{'class':'rolo',tabindex:'0',role:'region','aria-label':'Tabela do registo',html:'<table class="reg"><thead><tr><th>Onde</th><th>O quê</th><th>Como</th></tr></thead><tbody>'+linhas+'</tbody></table>'}));
    cx.appendChild(el('p',{'class':'ajuda',text:guardaOk?'Este registo fica só neste dispositivo. Mostra-o ao docente no ecrã ou copia-o para o caderno.':'Este navegador não deixa guardar: o registo perde-se se recarregares a página. Mostra-o já ao docente no ecrã ou copia-o para o caderno.'}));
  }
  registos.push(d);d();
  return cx;
}

/* ---------- passos ---------- */
var area=document.getElementById('area'),cxPasso=document.getElementById('passo'),apoio=document.getElementById('apoio');
var olPassos=document.getElementById('passos'),btsPasso=[];
function trancado(i){var p=P.passos[i];if(!p.precisa)return false;var T=S.txt[p.precisa];return !(T&&T.g);}
function feito(i){
  var p=P.passos[i],tem=false,ok=true;
  p.blocos.forEach(function(b){
    if(b.t==='escolha'||b.t==='tocar'){tem=true;if(!(S.q[b.id]&&S.q[b.id].r))ok=false;}
    if(b.t==='escrever'){tem=true;if(!(S.txt[b.id]&&S.txt[b.id].g))ok=false;}
    if(b.t==='rever'){tem=true;var T=S.txt[b.de];if(!(T&&(T.g2||T.papel2)))ok=false;}
  });
  return tem&&ok;
}
function atualizaPassos(){
  btsPasso.forEach(function(bt,i){
    bt.disabled=trancado(i);
    var f=feito(i);bt.classList.toggle('feito',f);bt.querySelector('.fe').hidden=!f;
    if(i===S.passo)bt.setAttribute('aria-current','step');else bt.removeAttribute('aria-current');
    bt.title=trancado(i)?'Guarda primeiro a tua primeira versão.':'';
  });
}
var navAnt,navSeg,navMsg;
function pintaNav(){
  if(!navAnt)return;
  navAnt.disabled=S.passo===0;
  var ult=S.passo===P.passos.length-1;
  navSeg.hidden=ult;
  var tr=!ult&&trancado(S.passo+1);
  navSeg.disabled=tr;
  navMsg.textContent=tr?'Para veres '+VIU+', guarda primeiro a tua primeira versão.':'';
}
function fazBloco(b){
  switch(b.t){
    case 'html':return el('div',{'class':'bloco',html:b.h});
    case 'escolha':return blocoEscolha(b);
    case 'tocar':return blocoTocar(b);
    case 'campos':return blocoCampos(b);
    case 'lista':return blocoLista(b);
    case 'grelha':return blocoGrelha(b);
    case 'escrever':return blocoEscrever(b);
    case 'rever':return blocoRever(b);
    case 'ver1':return blocoVer1(b);
    case 'vercampos':return blocoVerCampos(b);
    case 'registo':return blocoRegisto();
  }
  return el('div');
}
function hist(i,troca){
  try{window.history[troca?'replaceState':'pushState']({passo:i},'','#passo-'+(i+1));}catch(e){}
}
function mostraPasso(i,foco,semHist){
  if(i<0||i>=P.passos.length||trancado(i))return;
  var muda=i!==S.passo;
  S.passo=i;
  var p=P.passos[i];
  if(p.precisa){
    /* primeira vez que os critérios ficam à vista: guarda-se o estado da primeira versão nesse momento */
    var Tv=S.txt[p.precisa];
    if(Tv&&Tv.g&&!Tv.viu){Tv.viu=Date.now();Tv.s={v1:Tv.v1||'',papel:!!Tv.papel,op:Tv.op==null?null:Tv.op};}
  }
  guardar();
  if(!semHist&&muda){hist(i,false);}
  registos=[];
  cxPasso.innerHTML='';
  cxPasso.appendChild(el('p',{'class':'passo-n',text:'Passo '+(i+1)+' de '+P.passos.length}));
  var h=el('h2',{tabindex:'-1',id:'passo-t',html:p.titulo});
  cxPasso.appendChild(h);
  if(p.o)cxPasso.appendChild(el('p',{'class':'passo-o',html:p.o}));
  p.blocos.forEach(function(b){cxPasso.appendChild(fazBloco(b));});
  navAnt=el('button',{type:'button','class':'btn',text:'← Passo anterior',on:{click:function(){mostraPasso(S.passo-1,true);}}});
  navSeg=el('button',{type:'button','class':'btn forte',text:'Passo seguinte →',on:{click:function(){mostraPasso(S.passo+1,true);}}});
  navMsg=el('p',{'class':'tranca',role:'status','aria-live':'polite'});
  cxPasso.appendChild(el('div',{'class':'nav-p'},[navAnt,navSeg,navMsg]));
  /* texto de apoio */
  var tem=false;
  Array.prototype.forEach.call(apoio.querySelectorAll('[data-apoio]'),function(d){var on=d.getAttribute('data-apoio')===p.apoio;d.hidden=!on;if(on)tem=true;});
  apoio.hidden=!tem;area.classList.toggle('com-apoio',tem);
  if(tem){document.getElementById('apoio-rot').textContent=p.apoioRot||'Texto de apoio';}
  atualizaPassos();pintaNav();margemTopo();
  if(foco){h.focus({preventScroll:true});var y=area.getBoundingClientRect().top+window.pageYOffset-8;window.scrollTo(0,y);}
}
P.passos.forEach(function(p,i){
  var bt=el('button',{type:'button',on:{click:function(){mostraPasso(i,true);}}},[
    el('b',null,[('0'+(i+1)).slice(-2),el('span',{'class':'fe',hidden:true,html:'<span aria-hidden="true"> ✓</span> feito'})]),el('span',{text:p.curto})]);
  btsPasso.push(bt);olPassos.appendChild(el('li',null,bt));
});
/* recolher o texto */
var btRec=document.getElementById('apoio-bt');
function margemTopo(){
  /* em ecrãs estreitos o texto de apoio fica fixo por cima: o que recebe foco não pode ficar tapado por ele */
  var alto=(!apoio.hidden&&window.innerWidth<980)?apoio.offsetHeight+12:12;
  document.documentElement.style.scrollPaddingTop=alto+'px';
}
window.addEventListener('resize',margemTopo);
function pintaRec(){apoio.classList.toggle('recolhido',!!S.recolhido);btRec.setAttribute('aria-expanded',S.recolhido?'false':'true');btRec.textContent=S.recolhido?'Mostrar':'Recolher';margemTopo();}
btRec.addEventListener('click',function(){S.recolhido=!S.recolhido;guardar();pintaRec();});
pintaRec();
/* recomeçar */
var btZ=document.getElementById('recomecar'),arm=false;
btZ.addEventListener('click',function(){
  if(!arm){arm=true;btZ.textContent='Apagar as minhas respostas deste treino? Toca outra vez para confirmar.';setTimeout(function(){arm=false;btZ.textContent='Recomeçar este treino';},6000);return;}
  try{window.localStorage.removeItem(CH);}catch(e){}
  S=vazio();S.passo=-1;arm=false;btZ.textContent='Recomeçar este treino';pintaRec();mostraPasso(0,true);
});
/* os passos entram no histórico: voltar atrás no navegador volta ao passo anterior */
function passoDoEndereco(){var m=/^#passo-(\d+)$/.exec(window.location.hash||'');return m?parseInt(m[1],10)-1:-1;}
window.addEventListener('popstate',function(ev){
  var i=(ev.state&&typeof ev.state.passo==='number')?ev.state.passo:passoDoEndereco();
  if(i>=0&&i<P.passos.length&&i!==S.passo){mostraPasso(i,true,true);}
});
var ini=passoDoEndereco();
if(ini<0||ini>=P.passos.length||trancado(ini))ini=S.passo||0;
if(ini>=P.passos.length||trancado(ini))ini=0;
mostraPasso(ini,false,true);
hist(ini,true);
})();
