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

/* INICIO F2 CONTRATO 1: peças sem alteração do motor. */
(function(root){
 'use strict';
 var T=root.EPITiposMais, anteriores=new Map();
 function indices(n){return Array.from({length:n},function(_,i){return i});}
 function topo(x,a,dica){return '<p class="q">'+a.it(x.p)+'</p>'+(x.cita?'<p class="tm-cita">'+a.it(x.cita)+'</p>':'')+'<p class="dica">'+a.it(dica)+'</p>';}
 function papel(x,a){
  var h='<h2>'+a.it(x.p)+'</h2>'+(x.cita?'<p>'+a.it(x.cita)+'</p>':''),items=[];
  if(x.t==='lacunas'){h+='<p>'+a.it(x.texto).replace(/\[(\d+)\]/g,'____ ($1)')+'</p>';items=x.espacos.concat(x.distratores).slice().sort();}
  if(x.t==='montar'){items=x.blocos.concat(x.distratores||[]).slice().sort();h+='<p>Escreve a frase e termina com '+a.esc(x.fim)+'</p>';}
  if(x.t==='varias')items=x.o;
  if(x.t==='corrigir')h+='<p>'+a.esc(Array.isArray(x.partes)?x.partes.join(' '):x.texto)+'</p><p>Identifica os erros e escreve as formas corretas.</p>';
  if(x.t==='intruso'||x.t==='razao'){h+='<ol>'+x.itens.map(function(v){return '<li>'+(typeof v==='string'?a.it(v):'<figure><img src="'+a.esc(v.img)+'" alt="'+a.esc(v.alt)+'"><figcaption>'+a.esc([v.autor,v.obra,v.data,v.origem,v.licenca].join('; '))+'</figcaption></figure>')+'</li>'}).join('')+'</ol>';items=x.razoes;}
  if(items.length)h+='<ol>'+items.map(function(v){return '<li>'+a.it(v)+'</li>'}).join('')+'</ol>';
  return '<section class="tm-impressao" aria-label="Material para papel">'+h+'</section>';
 }
 function rodape(x,a){return '<p class="tm-conta"></p><p class="tm-viva c-sr" aria-live="polite"></p>'+papel(x,a);}
 function radio(a,name,i,text,attrs){return '<label class="tm-r uma"><input type="radio" name="'+a.esc(name)+'" value="'+i+'" '+(attrs||'')+'><span>'+a.it(text)+'</span></label>';}
 function ouvirRadios(el,cb){el.querySelectorAll('input[type=radio]').forEach(function(inp){inp.onchange=function(){el.querySelectorAll('input[type=radio]').forEach(function(r){r.closest('label').classList.toggle('sel',r.checked)});cb(Number(inp.value));};});}
 function res(total, falhas, erros){return {ok:falhas.length===0,certas:total-falhas.length,total:total,erros:erros.filter(Boolean).slice(0,2),falhas:falhas};}
 function marca(el,ok,text){el.classList.add(ok?'bom':'mau');var s=document.createElement('span');s.className='tm-retorno';s.textContent=(ok?'✓ ':'✗ ')+(text||'');el.appendChild(s);}
 function enter(a){a.el.querySelector('[data-tipo-ext]').addEventListener('keydown',function(ev){if(ev.key==='Enter'&&ev.target.matches('input[type=radio],input[type=checkbox]')){ev.preventDefault();var b=a.C.acao('[data-confirmar]');if(b&&!b.disabled)b.click();}});}

 T.registar('varias',{rot:'Escolhe as certas',como:'escolher-certas',criar:function(x,a,c){
  var rev=c.repeticao, alvos=rev&&c.falhas&&c.falhas.length?c.falhas.filter(Number.isInteger):indices(x.o.length), vals={}, feito=false;
  function certo(i){return x.certas.indexOf(i)>=0;}
  function mudar(){var n=Object.keys(vals).filter(function(k){return vals[k]}).length;c.atualizar(rev?Object.keys(vals).length===alvos.length:n>0,rev?'Revistas '+Object.keys(vals).length+' de '+alvos.length+'.':'Marcaste '+n+(x.diz_quantas?' de '+x.certas.length:'')+'.');}
  function pintar(){alvos.forEach(function(i){if(rev){a.el.querySelectorAll('[name="v-'+x.id+'-'+i+'"]').forEach(function(r){r.checked=(r.value==='1')===vals[i];r.closest('label').classList.toggle('sel',r.checked)});}else{var r=a.el.querySelector('[data-op="'+i+'"]');r.checked=!!vals[i];r.closest('label').classList.toggle('sel',r.checked);}});}
  function fim(){feito=true;var fs=[],es=[];alvos.forEach(function(i){var ok=!!vals[i]===certo(i);if(!ok){fs.push(i);es.push(x.fe[i]);}marca(a.el.querySelector('[data-item="'+i+'"]'),ok,!ok?(certo(i)?'Falta. ':'A mais. ')+x.fe[i]:'');});return res(alvos.length,fs,es);}
  return {html:function(){return topo(x,a,rev?'Revê cada afirmação que ficou por resolver. Decide se é verdadeira ou falsa.':'Marca todas as certas. Tocar outra vez tira a marca.')+'<div class="tm-varias">'+alvos.map(function(i){return '<div data-item="'+i+'">'+(rev?'<fieldset><legend>'+a.it(x.o[i])+'</legend>'+radio(a,'v-'+x.id+'-'+i,1,'Verdadeiro')+radio(a,'v-'+x.id+'-'+i,0,'Falso')+'</fieldset>':'<label class="tm-r varias"><input type="checkbox" data-op="'+i+'"><span>'+a.it(x.o[i])+'</span></label>')+'</div>';}).join('')+'</div>'+rodape(x,a);},
   ligar:function(){alvos.forEach(function(i){if(rev){var group=a.el.querySelector('[data-item="'+i+'"]');ouvirRadios(group,function(v){if(feito)return;vals[i]=v===1;mudar();});}else a.el.querySelector('[data-op="'+i+'"]').onchange=function(ev){if(feito)return;vals[i]=ev.target.checked;pintar();mudar();};});enter(a);mudar();},
   confirmar:fim,revelar:function(){alvos.forEach(function(i){vals[i]=certo(i);});pintar();return fim();}};
 }});

 ['intruso','razao'].forEach(function(tipo){T.registar(tipo,{rot:tipo==='intruso'?'Encontra o intruso':'Escolhe com razão',como:tipo==='intruso'?'intruso':'escolher-com-razao',criar:function(x,a,c){
  var item=null,razao=null,rev=c.repeticao,feito=false;
  if(rev)item=x.certos[0][0];
  function textoItem(i){return typeof x.itens[i]==='string'?x.itens[i]:x.itens[i].alt;}
  function escolhas(){return x.itens.map(function(v,i){
   if(typeof v==='string')return radio(a,'i-'+x.id,i,v);
   return '<div class="tm-imagem">'+radio(a,'i-'+x.id,i,String.fromCharCode(65+i)+'. '+v.alt)+'<img src="'+a.esc(v.img)+'" alt="'+a.esc(v.alt)+'"><p class="tm-credito">'+a.esc(v.autor)+'; <i>'+a.esc(v.obra)+'</i>; '+a.esc(v.data)+'</p><button type="button" class="tm-ampliar" data-ampliar="'+i+'" aria-label="Ampliar '+a.esc(v.alt)+'">Ampliar</button></div>';
  }).join('');}
  function abrirRazoes(){var el=a.el.querySelector('.tm-razoes');el.hidden=false;var p=a.el.querySelector('.tm-passo');p.textContent='Passo 2 de 2: '+(tipo==='intruso'?'diz porquê.':'escolhe o indício.');c.atualizar(razao!==null,'Uma escolha feita. Falta o indício.');var first=el.querySelector('input');c.focar(first);first.scrollIntoView({block:'nearest'});}
  function pintar(){a.el.querySelectorAll('input').forEach(function(r){r.checked=Number(r.value)===(r.name==='i-'+x.id?item:razao);r.closest('label').classList.toggle('sel',r.checked);});}
  function fim(){feito=true;var pair=x.certos.some(function(p){return p[0]===item&&p[1]===razao}),itok=x.certos.some(function(p){return p[0]===item}),er=[];
   var chosen=a.el.querySelector('[name="i-'+x.id+'"][value="'+item+'"]');if(chosen)marca(chosen.closest('label'),itok,x.fe_item[item]);
   var rr=a.el.querySelector('[name="r-'+x.id+'"][value="'+razao+'"]');if(rr)marca(rr.closest('label'),pair,pair?'':x.fe_razao[razao]||'O indício não distingue esta leitura. Relê os dois elementos em conjunto.');
   if(!itok)er.push(x.fe_item[item]);if(!pair)er.push(x.fe_razao[razao]||'A razão tem de justificar o elemento escolhido. Relê o par.');
   if(x.certos.length>1){var extra=document.createElement('p');extra.className='tm-alternativas';extra.textContent='Também se defende: '+x.certos.filter(function(p){return p[0]!==item||p[1]!==razao}).map(function(p){return textoItem(p[0])+', porque '+x.razoes[p[1]]}).join('; ');a.el.querySelector('.tm-duplo').appendChild(extra);}
   return {ok:pair,certas:pair?2:itok?1:0,total:2,erros:er.filter(Boolean).slice(0,2),falhas:pair?[]:itok?['razao']:['item','razao']};}
  return {html:function(){return topo(x,a,rev?'O elemento está fixo. Revê apenas a razão que o distingue.':'Escolhe primeiro um elemento; depois, a razão que o distingue.')+'<div class="tm-duplo"><p class="tm-passo">Passo '+(rev?'2':'1')+' de 2: '+(rev?'escolhe a razão.':'escolhe um elemento.')+'</p><fieldset class="tm-itens" '+(rev?'disabled':'')+'><legend>'+(tipo==='intruso'?'O intruso':'A leitura')+'</legend>'+escolhas()+'</fieldset>'+x.itens.filter(function(v){return typeof v==='object'}).map(function(v){return '<p class="tm-credito">'+a.esc(v.autor)+'; '+a.it('_'+v.obra+'_')+'; '+a.esc(v.data)+'; '+a.esc(v.licenca)+'. <a href="'+a.esc(v.origem)+'">Fonte</a></p>'}).join('')+'<fieldset class="tm-razoes" '+(rev?'':'hidden')+'><legend>'+(tipo==='intruso'?'Porquê?':'O indício')+'</legend>'+x.razoes.map(function(r,i){return radio(a,'r-'+x.id,i,r);}).join('')+'</fieldset></div>'+rodape(x,a);},
   ligar:function(){ouvirRadios(a.el.querySelector('.tm-itens'),function(v){if(feito)return;item=v;abrirRazoes();});ouvirRadios(a.el.querySelector('.tm-razoes'),function(v){if(feito)return;razao=v;c.atualizar(item!==null,'Elemento e razão escolhidos.');});
    a.el.querySelectorAll('[data-ampliar]').forEach(function(b){b.onclick=function(){var v=x.itens[Number(b.dataset.ampliar)],im=b.closest('.tm-imagem').querySelector('img');if(!root.EPIAmpliar)throw new Error('O cartão com imagem exige o visor comum');root.EPIAmpliar.abre(im,[v.autor,v.obra,v.data,v.origem,v.licenca].join('; '),b);};});
    pintar();enter(a);c.atualizar(false,rev?'Falta escolher a razão.':'Falta escolher um elemento.');},confirmar:fim,revelar:function(){item=x.certos[0][0];razao=x.certos[0][1];a.el.querySelector('.tm-razoes').hidden=false;pintar();return fim();}};
 }});});

 T.registar('lacunas',{rot:'Completa o texto',como:'completar-texto',criar:function(x,a,c){
  var banco=x.espacos.concat(x.distratores),ordem=c.ordem(indices(banco.length)),values=x.espacos.map(function(){return null}),slot=null,block=null,feito=false,rev=c.repeticao;
  var alvos=rev&&c.falhas&&c.falhas.length?c.falhas.filter(Number.isInteger):indices(values.length);
  if(rev)values.forEach(function(_,i){if(alvos.indexOf(i)<0)values[i]=i;});
  function ok(i){var s=banco[values[i]];return s===x.espacos[i]||Array.isArray((x.aceita||{})[i+1])&&x.aceita[i+1].indexOf(s)>=0;}
  function sync(){
   a.el.querySelectorAll('[data-espaco]').forEach(function(b){var i=Number(b.dataset.espaco),v=values[i];b.textContent=v===null?String(i+1):banco[v];b.setAttribute('aria-label','Espaço '+(i+1)+' de '+values.length+(v===null?', vazio':': '+banco[v]));b.classList.toggle('sel',slot===i);b.classList.toggle('preenchido',v!==null);b.disabled=feito||alvos.indexOf(i)<0;});
   a.el.querySelectorAll('[data-bloco]').forEach(function(b){var i=Number(b.dataset.bloco),usado=values.indexOf(i)>=0;b.disabled=feito||usado;b.classList.toggle('usado',usado);b.setAttribute('aria-pressed',String(block===i));});
   var n=values.filter(function(v){return v===null}).length;c.atualizar(n===0,n?'Faltam '+n+' espaços.':'Todos os espaços têm um bloco.');
  }
  function colocar(i,j){values[i]=j;slot=null;block=null;sync();var next=a.el.querySelector('[data-espaco="'+values.indexOf(null)+'"]');if(next)c.focar(next);}
  function fim(){feito=true;var fs=[],es=[];alvos.forEach(function(i){var certo=ok(i),b=a.el.querySelector('[data-espaco="'+i+'"]');if(!certo){fs.push(i);var f=(x.fe_bloco||{})[banco[values[i]]];if(f&&typeof f==='object')f=f[String(i+1)]||f['*'];if(f)es.push(f);if(x.fe_espaco)es.push(x.fe_espaco[i]);}marca(b,certo,certo?'':'Aqui vai: '+x.espacos[i]);});a.el.querySelector('.tm-banco').style.position='static';return res(alvos.length,fs,es);}
  return {html:function(){return topo(x,a,rev?'Revê os espaços falhados. Os restantes já estão preenchidos.':'Toca num bloco e no espaço, ou começa pelo espaço. Tocar num espaço preenchido devolve o bloco.')+'<div class="tm-lacunas"><div class="tm-texto">'+a.it(x.texto).replace(/\[(\d+)\]/g,function(_,n){return '<button type="button" class="tm-espaco" data-espaco="'+(Number(n)-1)+'">'+n+'</button>';})+'</div><div class="tm-banco" role="region" aria-label="Blocos"><span class="tm-banco-titulo">Blocos</span><div class="tm-blocos">'+ordem.map(function(i){return '<button type="button" data-bloco="'+i+'" aria-pressed="false">'+a.esc(banco[i])+'</button>';}).join('')+'</div></div></div>'+rodape(x,a);},
   ligar:function(){a.el.querySelectorAll('[data-espaco]').forEach(function(b){b.onclick=function(){if(feito)return;var i=Number(b.dataset.espaco);if(values[i]!==null){values[i]=null;sync();return;}if(block!==null){colocar(i,block);return;}slot=i;sync();var bank=a.el.querySelector('.tm-banco');if(bank.style.position==='static')b.insertAdjacentElement('afterend',bank);c.focar(a.el.querySelector('[data-bloco]:not(:disabled)'));};});a.el.querySelectorAll('[data-bloco]').forEach(function(b){b.onclick=function(){if(feito)return;var i=Number(b.dataset.bloco);if(slot!==null){colocar(slot,i);return;}block=block===i?null:i;sync();};});a.el.querySelector('.tm-lacunas').onkeydown=function(ev){if(ev.key==='Escape'&&(slot!==null||block!==null)){ev.preventDefault();ev.stopPropagation();var focus=slot!==null?a.el.querySelector('[data-espaco="'+slot+'"]'):a.el.querySelector('[data-bloco="'+block+'"]');slot=null;block=null;sync();c.focar(focus);}};sync();var bank=a.el.querySelector('.tm-banco');bank.style.position=bank.getBoundingClientRect().height<=innerHeight*.35?'sticky':'static';},
   confirmar:fim,revelar:function(){values=indices(x.espacos.length);sync();return fim();}};
 }});

 T.registar('montar',{rot:'Monta a frase',como:'montar-frase',criar:function(x,a,c){
  var bank=x.blocos.concat(x.distratores||[]),seq=[],feito=false,rev=c.repeticao,choice=null,key=String(a.cfg.chave)+'|'+x.id;
  var aceites=[indices(x.blocos.length)].concat((x.aceita||[]).map(function(o){return Array.isArray(o[0])?o[0]:o;}));
  function frase(s){var escrita=(x.aceita||[]).find(function(o){return Array.isArray(o[0])&&JSON.stringify(o[0])===JSON.stringify(s)});if(escrita)return escrita[1];var words=s.map(function(i){return bank[i]});if(words.length)words[0]=words[0].charAt(0).toUpperCase()+words[0].slice(1);return words.join(' ')+(words.length?x.fim:'');}
  var order=c.ordem(indices(bank.length));if(aceites.some(function(o){return JSON.stringify(o)===JSON.stringify(order)}))order.push(order.shift());
  var errado=anteriores.get(key)||indices(x.blocos.length).reverse(),dist=indices(x.blocos.length);if(bank.length>x.blocos.length)dist[1]=x.blocos.length;else dist.push(dist.shift());
  var frases=[frase(aceites[0]),frase(errado),frase(dist)].filter(function(v,i,arr){return arr.indexOf(v)===i});
  if(frases.length<3){var extra=indices(x.blocos.length);extra.push(extra.shift());if(frases.indexOf(frase(extra))<0)frases.push(frase(extra));}
  function draw(){var line=a.el.querySelector('.tm-linha');line.innerHTML=seq.map(function(i,k){return '<li><button type="button" data-linha="'+k+'">'+a.esc((k===0?bank[i].charAt(0).toUpperCase()+bank[i].slice(1):bank[i])+(k===seq.length-1?x.fim:''))+'</button></li>';}).join('');line.querySelectorAll('button').forEach(function(b){b.onclick=function(){if(feito)return;seq.splice(Number(b.dataset.linha),1);draw();c.focar(a.el.querySelector('[data-monta]:not(:disabled)'));};});a.el.querySelectorAll('[data-monta]').forEach(function(b){b.disabled=seq.indexOf(Number(b.dataset.monta))>=0;});c.atualizar(seq.length>=x.blocos.length,'Montaste '+seq.length+' blocos.');}
  function finish(){feito=true;if(rev){var ok=choice===0;marca(a.el.querySelector('[value="'+choice+'"]').closest('label'),ok,ok?'':x.fe_ordem);return res(1,ok?[]:[0],ok?[]:[x.fe_ordem]);}
   anteriores.set(key,seq.slice());var best=aceites.slice().sort(function(u,v){function n(s){return s.filter(function(i,k){return seq[k]===i}).length}return n(v)-n(u)})[0];var fs=[],es=[];
   var total=Math.max(seq.length,best.length);for(var k=0;k<total;k++){var i=seq[k],ok=i===best[k],el=a.el.querySelector('[data-linha="'+k+'"]');if(!ok){fs.push(k);if(i>=x.blocos.length)es.push(x.fe_bloco[bank[i]]);}if(el)marca(el,ok,ok?'':i>=x.blocos.length?'A mais':'Vai em '+(best.indexOf(i)+1)+'.º');}
   if(fs.length)es.push(x.fe_ordem);return res(total,fs,es);}
  return {html:function(){return topo(x,a,rev?'Compara a frase principal, a tentativa anterior e uma alternativa. Escolhe a forma que respeita a relação pedida.':'Toca nos blocos pela ordem da frase. Tocar num bloco da linha devolve-o.')+'<div class="tm-montar">'+(rev?'<fieldset><legend>Qual das formas está certa?</legend>'+frases.map(function(s,i){return radio(a,'m-'+x.id,i,s)}).join('')+'</fieldset>':'<ol class="tm-linha" aria-label="A tua frase"></ol><div class="tm-blocos">'+order.map(function(i){return '<button type="button" data-monta="'+i+'">'+a.esc(bank[i])+'</button>'}).join('')+'</div>')+'</div>'+rodape(x,a);},
   ligar:function(){if(rev){ouvirRadios(a.el.querySelector('fieldset'),function(i){choice=i;c.atualizar(true,'Uma frase escolhida.');});c.atualizar(false,'Falta escolher uma frase.');}else{a.el.querySelectorAll('[data-monta]').forEach(function(b){b.onclick=function(){if(feito)return;seq.push(Number(b.dataset.monta));draw();c.focar(a.el.querySelector('[data-monta]:not(:disabled)'));};});draw();}enter(a);},confirmar:finish,revelar:function(){if(rev){choice=0;var r=a.el.querySelector('input[value="0"]');r.checked=true;r.closest('label').classList.add('sel');}else{seq=aceites[0].slice();draw();if(aceites.length>1){var p=document.createElement('p');p.textContent='Também certo: '+aceites.slice(1).map(frase).join(' / ');a.el.querySelector('.tm-montar').appendChild(p);}}return finish();}};
 }});

 T.registar('corrigir',{rot:'Corrige o erro',como:'corrigir-erro',criar:function(x,a,c){
  var parts=c.partes(),marks=new Set(),vals={},locvals={},step=c.repeticao?2:1,feito=false;
  function isError(i){return x.erros.some(function(e){return e.em===i});}
  var failed=c.falhas||[],alvo=x.erros.slice(),loc=[];
  if(c.repeticao&&failed.length){
   alvo=x.erros.filter(function(e){return failed.indexOf('forma:'+e.em)>=0||failed.indexOf(e.em)>=0});
   loc=failed.filter(function(v){return typeof v==='string'&&v.indexOf('local:')===0}).map(function(v){return Number(v.split(':')[1])});
  }
  function pronto(){return alvo.every(function(e){return vals[e.em]!==undefined})&&loc.every(function(i){return locvals[i]!==undefined});}
  function atualizar(){c.atualizar(pronto(),'Revistas '+(Object.keys(vals).length+Object.keys(locvals).length)+' de '+(alvo.length+loc.length)+'.','Confirmar');}
  function fase2(){
   step=2;a.el.querySelectorAll('[data-palavra]').forEach(function(b){
    var i=Number(b.dataset.palavra),n=x.erros.findIndex(function(e){return e.em===i});b.disabled=true;
    if(n>=0){var s=document.createElement('sup');s.textContent=String(n+1);b.appendChild(s);}
    if(!c.repeticao&&marks.has(i)&&n<0)marca(b,false,(x.armadilhas||{})[i]||'Esta forma já estava correta. Relê a frase com ela.');
   });
   a.el.querySelector('.tm-trocas').hidden=false;
   a.el.querySelector('.tm-passo').textContent=c.repeticao?'Revê apenas as decisões falhadas.':'Passo 2 de 2: escolhe a palavra certa.';
   atualizar();c.focar(a.el.querySelector('.tm-trocas input'));
  }
  function localFeedback(i){var err=x.erros.find(function(e){return e.em===i});return err?err.fe:(x.armadilhas||{})[i]||'Esta forma já estava correta. Relê a palavra no contexto da frase.';}
  function final(){
   feito=true;var fs=[],es=[],localTotal=c.repeticao?loc.length:parts.length,localCertas=0,formasCertas=0;
   (c.repeticao?loc:indices(parts.length)).forEach(function(i){var ok=(c.repeticao?locvals[i]:marks.has(i))===isError(i);if(ok)localCertas++;else{fs.push('local:'+i);es.push(localFeedback(i));}var g=a.el.querySelector('[data-local="'+i+'"]');if(g)marca(g,ok,ok?'':localFeedback(i));});
   alvo.forEach(function(e){
    var ok=vals[e.em]===e.c;if(ok)formasCertas++;else{fs.push('forma:'+e.em);es.push(e.fe);}
    marca(a.el.querySelector('[data-erro="'+e.em+'"]'),ok,ok?'':e.fe);
    var b=a.el.querySelector('[data-palavra="'+e.em+'"]'),punct=(parts[e.em].match(/[.,;:!?…]+$/)||[''])[0];
    b.textContent=e.o[e.c]+punct;var sup=document.createElement('sup');sup.textContent=String(x.erros.indexOf(e)+1);b.appendChild(sup);b.classList.toggle('mau',!ok);b.classList.toggle('bom',ok);
   });
   var p=document.createElement('p');p.className='tm-balanco';p.textContent='Identificação: '+localCertas+' de '+localTotal+' decisões corretas. Formas: '+formasCertas+' de '+alvo.length+' correções.';a.el.querySelector('.tm-corrigir').appendChild(p);
   return res(localTotal+alvo.length,fs,es);
  }
  return {
   html:function(){
    var forms=alvo.map(function(e){return '<fieldset data-erro="'+e.em+'"><legend>Erro '+(x.erros.indexOf(e)+1)+': '+a.esc(parts[e.em])+'</legend>'+e.o.map(function(o,i){return radio(a,'c-'+x.id+'-'+e.em,i,o)}).join('')+'</fieldset>';}).join('');
    var locations=loc.map(function(i){return '<fieldset data-local="'+i+'"><legend>A forma '+a.esc(parts[i])+' precisa de correção?</legend>'+radio(a,'l-'+x.id+'-'+i,1,'Precisa de correção.')+radio(a,'l-'+x.id+'-'+i,0,'Já está correta.')+'</fieldset>';}).join('');
    return topo(x,a,c.repeticao?'Revê as decisões que falharam: localizar uma forma e escolher a correção são operações diferentes.':'Marca primeiro as palavras erradas. Só depois verás as formas de correção.')+'<div class="tm-corrigir"><p class="tm-passo">Passo '+step+' de 2: '+(step===1?'encontra os erros.':'revê as decisões.')+'</p><div class="tm-texto tm-corrigir-texto">'+parts.map(function(w,i){return '<button class="w" type="button" data-palavra="'+i+'" aria-pressed="false">'+a.esc(w)+'</button>';}).join(' ')+'</div><div class="tm-trocas" '+(step===1?'hidden':'')+'>'+locations+forms+'</div></div>'+rodape(x,a);
   },
   ligar:function(){
    a.el.querySelectorAll('[data-palavra]').forEach(function(b){b.onclick=function(){if(step!==1||feito)return;var i=Number(b.dataset.palavra);if(marks.has(i))marks.delete(i);else marks.add(i);b.setAttribute('aria-pressed',String(marks.has(i)));b.classList.toggle('sel',marks.has(i));c.atualizar(marks.size>0,'Marcaste '+marks.size+' palavras.','Ver os erros');};});
    alvo.forEach(function(e){ouvirRadios(a.el.querySelector('[data-erro="'+e.em+'"]'),function(i){vals[e.em]=i;atualizar();});});
    loc.forEach(function(i){ouvirRadios(a.el.querySelector('[data-local="'+i+'"]'),function(v){locvals[i]=v===1;atualizar();});});
    if(step===2)fase2();else c.atualizar(false,'Falta marcar uma palavra.','Ver os erros');enter(a);
   },
   confirmar:function(){if(step===1){fase2();return null;}return final();},
   revelar:function(){
    x.erros.forEach(function(e){marks.add(e.em)});if(step===1)fase2();
    alvo.forEach(function(e){vals[e.em]=e.c;var r=a.el.querySelector('[name="c-'+x.id+'-'+e.em+'"][value="'+e.c+'"]');r.checked=true;r.closest('label').classList.add('sel');});
    loc.forEach(function(i){locvals[i]=isError(i);var r=a.el.querySelector('[name="l-'+x.id+'-'+i+'"][value="'+(isError(i)?1:0)+'"]');r.checked=true;r.closest('label').classList.add('sel');});
    return final();
   }
  };
 }});
})(window);
/* FIM F2 CONTRATO 1 */
