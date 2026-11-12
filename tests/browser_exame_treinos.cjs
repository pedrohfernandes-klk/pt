/* 11/11/2026: os três treinos da preparação de exame (exame/treinos/) no navegador, a 390x844 e a 1280x900, em claro e em escuro,
   e com o armazenamento bloqueado. O sítio serve-se em /pt/, como em produção, para os ficheiros partilhados (tema e projeção) correrem.
   PT_CAPTURAS=<pasta> guarda as capturas; sem a variável, não se escreve nada.
   12/11/2026: quatro treinos, com o da sessão 17 (poesia contemporânea, exame/treinos/poesia-contemporanea/), com a mesma cobertura dos outros três.
   12/11/2026: cinco treinos, com o da sessão 18 (conto, exame/treinos/conto/), com a mesma cobertura dos outros quatro. */
const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{let u=decodeURIComponent(req.url.split('?')[0]);if(!u.startsWith('/pt/')){res.writeHead(404).end();return;}let file=path.join(root,u.slice(3));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{if(fs.statSync(file).isDirectory()){if(!u.endsWith('/')){res.writeHead(301,{Location:u+'/'}).end();return;}file=path.join(file,'index.html');}res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.woff2':'font/woff2'})[path.extname(file)]||'text/plain; charset=utf-8');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
const CAP=process.env.PT_CAPTURAS?path.resolve(process.env.PT_CAPTURAS)+path.sep:null;
if(CAP)fs.mkdirSync(CAP,{recursive:true});
let BASE='';
let falhas=[],passes=0;
function ok(c,m){if(c){passes++;}else{falhas.push(m);console.log('FALHA',m);}}
const TXT210=Array.from({length:210},(_,i)=>'palavra'+i).join(' ');
const TXT196=Array.from({length:196},(_,i)=>'palavra'+i).join(' ');
const LONGA='https://exemplo.pt/'+'umapalavramuitolongasemespacos'.repeat(5);
const V1='Primeira versão do aluno sobre as rosas.';
const V1L=V1+' '+LONGA,V1A=V1+' Acrescento.';
(async()=>{
await new Promise(r=>server.listen(0,'127.0.0.1',r));
BASE='http://127.0.0.1:'+server.address().port+'/pt/exame/treinos/';
const b=await chromium.launch();
for(const [w,h] of [[390,844],[1280,900]]) for(const cs of ['light','dark']){
  const tag=w+'-'+(cs==='light'?'claro':'escuro');
  const estreito=w===390;const V1F=estreito?V1A:V1L;
  const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,colorScheme:cs});
  let p=await c.newPage();
  const erros=[];
  const escuta=(pg)=>{pg.on('pageerror',e=>erros.push(e.message));pg.on('console',m=>{if(m.type()==='error')erros.push(m.text());});};
  escuta(p);
  const semDeslize=async(onde)=>{const r=await p.evaluate(()=>[document.documentElement.scrollWidth,window.innerWidth]);ok(r[0]<=r[1],tag+' deslize horizontal em '+onde+' '+r);};
  const passo=async(n)=>{await p.click('#passos li:nth-child('+n+') button');await p.waitForTimeout(80);await semDeslize('passo '+n);};
  const Q=(id)=>p.locator('.q',{has:p.locator('#p-'+id)});
  // 11/11/2026: cada leitura do retorno confere também que nenhuma letra dele fica por baixo do controlo flutuante do tema.
  // Única exceção: um retorno mais alto do que o espaço livre entre o texto de apoio e o controlo; esse tem de começar no cimo do espaço livre.
  const tapadas=(loc)=>loc.evaluate((e)=>{const ct=document.querySelector('.epi-appearance-toggle');if(!ct)return null;const c=ct.getBoundingClientRect();if(!c.height)return null;
    const ap=document.getElementById('apoio'),q0=e.getBoundingClientRect(),topo=(ap&&!ap.hidden&&window.innerWidth<980)?ap.getBoundingClientRect().bottom:0;
    if(q0.height>c.top-topo-20&&q0.top>=topo-1&&q0.top<=topo+14)return '';
    const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n,fora='';const rg=document.createRange();
    while((n=w.nextNode())){const t=n.nodeValue;for(let i=0;i<t.length;i++){if(/\s/.test(t[i]))continue;rg.setStart(n,i);rg.setEnd(n,i+1);
      for(const q of rg.getClientRects()){if(q.width&&q.height&&q.left<c.right-0.5&&q.right>c.left+0.5&&q.top<c.bottom-0.5&&q.bottom>c.top+0.5){fora+=t[i];break;}}}}
    return fora;});
  const ret=async(id)=>{const L=Q(id).locator('.retorno');const tp=await tapadas(L);
    ok(tp==='',tag+' retorno de '+id+': nenhuma letra por baixo do controlo do tema (tapadas: «'+tp+'»)');
    return {cls:await L.getAttribute('class'),txt:await L.innerText()};};
  const op=async(id,i)=>{await Q(id).locator('.op').nth(i).click();};
  const tk=async(id,txts)=>{for(const t of txts){await Q(id).locator('.tk',{hasText:t}).first().click();}};
  const verif=async(id)=>{await Q(id).locator('button',{hasText:'Verificar'}).click();};
  const aviso=async(id)=>await Q(id).locator('p.estado').innerText();
  // o elemento está na parte do ecrã que o texto de apoio fixo não tapa (sem deslocar à mão)
  const aVista=async(loc,onde)=>{
    const r=await loc.evaluate((e)=>{const a=document.getElementById('apoio'),q=e.getBoundingClientRect();
      const topo=(!a.hidden&&window.innerWidth<980)?a.getBoundingClientRect().bottom:0;
      return {t:q.top,b:q.bottom,h:q.height,topo:topo,vh:window.innerHeight};});
    const livre=r.vh-r.topo;
    ok(r.h>0&&r.t>=r.topo-1&&(r.b<=r.vh+1||(r.h>livre-20&&r.t<=r.topo+14)),tag+' à vista no ecrã sem deslocar: '+onde+' '+JSON.stringify(r));
  };
  const juntos=async(id,onde)=>{ // texto de apoio e pergunta visíveis ao mesmo tempo
    await Q(id).locator('.q-p').scrollIntoViewIfNeeded();
    await p.evaluate((s)=>{const e=document.querySelector(s);const y=e.getBoundingClientRect().top+window.pageYOffset-(window.innerWidth<980?document.getElementById('apoio').offsetHeight+10:20);window.scrollTo(0,y);},'#p-'+id);
    await p.waitForTimeout(60);
    const r=await p.evaluate((s)=>{const a=document.getElementById('apoio').getBoundingClientRect(),q=document.querySelector(s).getBoundingClientRect();return {at:a.top,ab:a.bottom,qt:q.top,qb:q.bottom,vh:window.innerHeight,vw:window.innerWidth,oculto:document.getElementById('apoio').hidden};},'#p-'+id);
    ok(!r.oculto&&(Math.min(r.ab,r.vh)-Math.max(r.at,0))>=150&&r.qt>=Math.min(Math.max(r.ab,0),r.vh)*((r.vw<980)?1:0)-1&&r.qt>=0&&r.qb<=r.vh,tag+' texto de apoio junto da pergunta em '+onde+' '+JSON.stringify(r));
  };
  const cap=async(nome,full)=>{if(CAP)await p.screenshot({path:CAP+nome+'-'+tag+'.png',fullPage:!!full});};
  const ativo=()=>p.evaluate(()=>{const a=document.activeElement;const s=getComputedStyle(a);return {cls:a.className,tag:a.tagName,t:(a.textContent||'').slice(0,40),ow:s.outlineWidth,os:s.outlineStyle,fv:a.matches(':focus-visible')};});
  const reg=async()=>await p.locator('.reg').innerText();

  /* ===== índice ===== */
  await p.goto(BASE);await semDeslize('indice');await cap('0-indice',true);
  ok(/Três tentativas, duas pistas/.test(await p.locator('main').innerText())&&!/sozinh/i.test(await p.locator('body').innerText()),tag+' índice descreve as três tentativas e não usa formas com género');

  /* ===== página do sítio: cabeçalho, ligações, ficheiros partilhados e tema ===== */
  // 12/11/2026: mais a página do treino da sessão 17
  // 12/11/2026: e a do treino da sessão 18
  for(const pg of ['','interpretacao/','gramatica/','escrita/','poesia-contemporanea/','conto/']){
    const mortos=[];const ouve=r=>{if(r.status()>=400)mortos.push(r.status()+' '+r.url());};p.on('response',ouve);
    await p.goto(BASE+pg);await p.waitForLoadState('networkidle');p.off('response',ouve);
    ok(mortos.length===0,tag+' '+(pg||'entrada')+': todos os ficheiros carregam '+mortos.join(' | '));
    const d=await p.evaluate(()=>({lang:document.documentElement.lang,sitio:document.documentElement.getAttribute('data-appearance-site'),tema:document.documentElement.getAttribute('data-theme'),
      estilos:document.querySelectorAll('style:not(#epi-projection-launcher-style),[style]').length,embutidos:Array.from(document.scripts).filter(x=>!x.src&&x.type!=='application/json').length,
      txt:document.body.innerText,mig:Array.from(document.querySelectorAll('.migalhas ol a')).map(a=>a.getAttribute('href')),
      nav:Array.from(document.querySelectorAll('.site-head nav a')).map(a=>a.textContent+'>'+new URL(a.href).pathname),marca:new URL(document.querySelector('.wordmark').href).pathname,
      fundo:getComputedStyle(document.body).backgroundColor,tinta:getComputedStyle(document.body).color,letra:getComputedStyle(document.querySelector('h1')).fontFamily,
      tema1:!!document.querySelector('.epi-appearance-toggle'),projetar:!!document.querySelector('.epi-projection-launcher'),h1:document.querySelectorAll('h1').length}));
    ok(d.lang==='pt-PT'&&d.sitio==='pt'&&d.tema===cs,tag+' '+(pg||'entrada')+': língua, sítio e tema '+JSON.stringify([d.lang,d.sitio,d.tema]));
    ok(d.embutidos===0,tag+' '+(pg||'entrada')+': nenhum script embutido ('+d.embutidos+')');
    ok(!/pr[ée]via|piloto/i.test(d.txt)&&!/pr[ée]via|piloto/i.test(await p.content()),tag+' '+(pg||'entrada')+': nada de «prévia» nem de «piloto»');
    ok(d.marca==='/pt/exame/'&&d.nav.join(' ')==='Sessões>/pt/exame/ Laboratório de respostas>/pt/exame/laboratorio/ Provas em cartões>/pt/exame/provas/ Treinos>/pt/exame/treinos/',tag+' '+(pg||'entrada')+': navegação da preparação '+d.marca+' '+d.nav.join(' '));
    ok(d.mig.length===(pg?3:2)&&d.mig[0]===(pg?'../../../':'../../')&&d.mig[1]===(pg?'../../':'../'),tag+' '+(pg||'entrada')+': migalhas '+d.mig.join(' '));
    ok(d.h1===1&&/Fraunces Oficina/.test(d.letra)&&await p.evaluate(()=>document.fonts.ready.then(()=>document.fonts.check('600 20px "Fraunces Oficina"')&&document.fonts.check('16px "Plex Oficina"'))),tag+' '+(pg||'entrada')+': um só título e tipos de letra de assets/exame/fontes');
    ok(cs==='dark'?d.fundo==='rgb(28, 27, 24)'&&d.tinta==='rgb(237, 233, 222)':d.fundo==='rgb(243, 240, 231)'&&d.tinta==='rgb(36, 35, 31)',tag+' '+(pg||'entrada')+': cores do tema '+d.fundo+' '+d.tinta);
    ok(d.tema1,tag+' '+(pg||'entrada')+': controlo do tema presente');
    await semDeslize('página do sítio '+(pg||'entrada'));
  }
  // o controlo do tema troca as cores e a escolha fica para a página seguinte
  await p.goto(BASE+'gramatica/');await p.click('.epi-appearance-toggle');
  { const outro=cs==='dark'?'light':'dark';
    const d=await p.evaluate(()=>[document.documentElement.getAttribute('data-theme'),getComputedStyle(document.body).backgroundColor,getComputedStyle(document.querySelector('.caixa.nossa')).backgroundColor]);
    ok(d[0]===outro&&d[1]===(outro==='dark'?'rgb(28, 27, 24)':'rgb(243, 240, 231)')&&d[2]===(outro==='dark'?'rgb(58, 52, 32)':'rgb(246, 237, 201)'),tag+' o controlo do tema troca as cores '+d);
    await cap('0-tema-trocado');
    await p.goto(BASE);ok(await p.evaluate(()=>document.documentElement.getAttribute('data-theme'))===outro,tag+' a escolha do tema passa para a entrada');
    await p.click('.epi-appearance-toggle');ok(await p.evaluate(()=>document.documentElement.getAttribute('data-theme'))===cs,tag+' o tema volta ao do sistema'); }
  // ligações às sessões e aos aquecimentos, que continuam onde estavam
  // 12/11/2026: mais o treino da sessão 17
  // 12/11/2026: e o da sessão 18
  for(const [pg,s] of [['interpretacao/','s14'],['gramatica/','s21'],['escrita/','s24'],['poesia-contemporanea/','s17'],['conto/','s18']]){
    await p.goto(BASE+pg);
    const l=await p.evaluate(()=>Array.from(document.querySelectorAll('.lede a')).map(a=>new URL(a.href).pathname+new URL(a.href).hash));
    ok(l.join(' ')==='/pt/exame/#'+s+' /pt/exame/aquecimentos/'+s+'/'||l.join(' ')==='/pt/exame/aquecimentos/'+s+'/ /pt/exame/#'+s,tag+' '+pg+' liga à sessão e ao aquecimento '+l.join(' '));
    const r=await p.request.get(new URL('../../aquecimentos/'+s+'/',BASE+pg).href);ok(r.status()===200,tag+' '+pg+' aquecimento da sessão responde');
    ok(await p.locator('.cartoes').count()===0&&await p.locator('.tr-nav a[aria-current="page"]').count()===1,tag+' '+pg+' navegação dos treinos marca a página atual');
  }
  await p.goto(BASE+'escrita/');await p.click('.wordmark');await p.waitForLoadState('domcontentloaded');
  ok(new URL(p.url()).pathname==='/pt/exame/',tag+' a marca volta à entrada da preparação de exame '+p.url());
  await p.goto(BASE);
  { const l=await p.evaluate(()=>Array.from(document.querySelectorAll('.cartao-p')).map(c=>Array.from(c.querySelectorAll('a')).map(a=>new URL(a.href).pathname+new URL(a.href).hash).join(' ')));
    // 12/11/2026: quatro cartões, o último para o treino da sessão 17
    // 12/11/2026: cinco cartões, o último para o treino da sessão 18
    ok(l.join(' | ')==='/pt/exame/#s14 /pt/exame/treinos/interpretacao/ | /pt/exame/#s21 /pt/exame/treinos/gramatica/ | /pt/exame/#s24 /pt/exame/treinos/escrita/ | /pt/exame/#s17 /pt/exame/treinos/poesia-contemporanea/ | /pt/exame/#s18 /pt/exame/treinos/conto/',tag+' entrada liga aos cinco treinos e às cinco sessões '+l.join(' | '));
    const nv=await p.evaluate(()=>Array.from(document.querySelectorAll('.tr-nav a')).map(a=>a.textContent+'>'+new URL(a.href).pathname).join(' '));
    // 12/11/2026: a navegação e o título contam cinco treinos; nem «três» nem «quatro» ficam na entrada
    ok(nv==='Os cinco treinos>/pt/exame/treinos/ Interpretação>/pt/exame/treinos/interpretacao/ Gramática>/pt/exame/treinos/gramatica/ Escrita>/pt/exame/treinos/escrita/ Poesia contemporânea>/pt/exame/treinos/poesia-contemporanea/ Conto>/pt/exame/treinos/conto/'&&/Cinco treinos de exame/.test(await p.locator('h1').innerText())&&!/[Tt]rês treinos|[Qq]uatro treinos/.test(await p.locator('body').innerText()),tag+' navegação entre os cinco treinos '+nv); }
  ok(erros.length===0,tag+' página do sítio: erros de JavaScript: '+erros.join(' | '));erros.length=0;
  await p.evaluate(()=>localStorage.clear());

  /* ===== TREINO 1 ===== */
  await p.goto(BASE+'interpretacao/');await p.evaluate(()=>localStorage.clear());await p.goto(BASE+'interpretacao/');await p.reload();
  await semDeslize('p1 inicio');await cap('1-interpretacao-01-inicio',true);
  // teclado: Tab chega à ligação de salto e o foco vê-se
  await p.keyboard.press('Tab');
  let f=await ativo();
  ok(f.cls==='skip'&&f.os!=='none'&&parseFloat(f.ow)>=2,tag+' foco visível na ligação de salto '+JSON.stringify(f));
  await juntos('p1-pedido','p1 passo 1');
  await cap('1-interpretacao-02-texto-junto-da-pergunta');
  // 1.ª falha (teclado): pista ligada ao erro, restam duas tentativas
  await Q('p1-pedido').locator('.op').nth(0).focus();await p.keyboard.press('Enter');
  let r=await ret('p1-pedido');
  ok(/pista/.test(r.cls)&&/^PISTA/i.test(r.txt)&&/Relê os dois verbos/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p1 1.ª falha: pista da opção escolhida e duas tentativas '+r.txt);
  ok(await Q('p1-pedido').locator('.op').nth(0).getAttribute('aria-disabled')==='true',tag+' opção tentada fica indisponível (aria-disabled)');
  ok(await Q('p1-pedido').locator('.retorno').getAttribute('aria-live')==='polite'&&await Q('p1-pedido').locator('.retorno').getAttribute('role')==='status',tag+' pista anunciada (role=status, aria-live)');
  await aVista(Q('p1-pedido').locator('.retorno'),'p1 pista depois de errar');
  f=await ativo();ok(f.tag==='BUTTON'&&/^A/.test(f.t),tag+' o foco do teclado não se perde depois de errar '+JSON.stringify(f));
  await cap('1-interpretacao-03-pista');
  // repetir a opção já tentada não gasta tentativa
  await p.keyboard.press('Enter');r=await ret('p1-pedido');ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p1 repetir a opção tentada não gasta tentativa');
  // 2.ª falha: segunda pista, mais dirigida ao texto, resta uma tentativa
  await p.keyboard.press('Tab');
  f=await ativo();ok(f.fv&&f.os!=='none'&&parseFloat(f.ow)>=2&&/^B/.test(f.t),tag+' foco visível na opção B por teclado '+JSON.stringify(f));
  await p.keyboard.press('Enter');
  r=await ret('p1-pedido');
  ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/aos bocados/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/A opção adequada é/.test(r.txt),tag+' p1 2.ª falha: segunda pista sem a resposta '+r.txt);
  await aVista(Q('p1-pedido').locator('.retorno'),'p1 segunda pista');
  await cap('1-interpretacao-04-segunda-pista');
  await p.keyboard.press('Tab');await p.keyboard.press('Enter'); // C
  r=await ret('p1-pedido');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt),tag+' p1 certo à terceira '+r.txt.slice(0,60));
  await passo(2);
  f=await ativo();ok(f.tag==='H2',tag+' ao mudar de passo o foco vai para o título '+JSON.stringify(f));
  await juntos('p1-versos','p1 passo 2');
  // seleção por teclado
  await Q('p1-versos').locator('.tk').nth(estreito?5:2).focus();await p.keyboard.press('Space');
  ok(await Q('p1-versos').locator('.tk').nth(estreito?5:2).getAttribute('aria-pressed')==='true',tag+' seleção de verso por teclado');
  if(estreito){await tk('p1-versos',['Antes que Apolo','O seu curso']);}else{await tk('p1-versos',['Em esse dia']);}
  await verif('p1-versos');r=await ret('p1-versos');ok(/certo/.test(r.cls)&&/primeira/i.test(r.txt),tag+' p1 versos (seleção '+(estreito?'alternativa 6-8':'3-4')+') aceite '+r.txt.slice(0,50));
  // palavra: «Inscientes» só -> pista; verificar outra vez a mesma seleção não gasta tentativa
  await verif('p1-palavra');ok(/Ainda não escolheste/.test(await aviso('p1-palavra')),tag+' p1 verificar sem seleção avisa e não gasta tentativa');
  await tk('p1-palavra',['Inscientes,']);await verif('p1-palavra');r=await ret('p1-palavra');
  ok(/pista/.test(r.cls)&&/por querer/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p1 palavra pista do erro cometido '+r.txt.slice(0,80));
  await aVista(Q('p1-palavra').locator('.retorno'),'p1 pista da seleção');
  await verif('p1-palavra');await verif('p1-palavra');r=await ret('p1-palavra');
  ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt)&&/não gastaste outra tentativa/.test(await aviso('p1-palavra')),tag+' p1 verificar duas vezes a mesma seleção errada não gasta tentativa '+r.txt.slice(0,40));
  await cap('1-interpretacao-05-mesma-selecao');
  await tk('p1-palavra',['voluntariamente']);await verif('p1-palavra');r=await ret('p1-palavra');
  ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/Aceite com «Inscientes»/.test(r.txt),tag+' p1 fronteira equivalente aceite, à segunda '+r.txt.slice(0,80));
  await cap('1-interpretacao-06-fronteira-equivalente');
  await passo(3);await juntos('p1-distinguir','p1 passo 3');
  await op('p1-distinguir',0);r=await ret('p1-distinguir');ok(/pista/.test(r.cls)&&/segunda estrofe/.test(r.txt),tag+' p1 distinguir pista 1');
  await op('p1-distinguir',1);r=await ret('p1-distinguir');ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/versos 5 a 8/.test(r.txt),tag+' p1 distinguir segunda pista');
  ok(!/certa/.test(await Q('p1-distinguir').locator('.op').nth(3).getAttribute('class')),tag+' p1 a resposta não aparece antes da terceira falha');
  await op('p1-distinguir',2);r=await ret('p1-distinguir');ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&/não erra: omite/.test(r.txt),tag+' p1 explicação só à terceira falha '+r.txt.slice(0,60));
  ok(/certa/.test(await Q('p1-distinguir').locator('.op').nth(3).getAttribute('class')),tag+' p1 opção adequada marcada');
  await aVista(Q('p1-distinguir').locator('.retorno'),'p1 explicação');
  await cap('1-interpretacao-07-explicacao');
  await passo(4);
  ok(await p.locator('#passos li:nth-child(5) button').isDisabled(),tag+' p1 passo 5 trancado antes de guardar');
  ok(await p.locator('.retorno:visible').count()===0,tag+' p1 sem pistas à vista no passo de escrita');
  ok(/guarda-se automaticamente/.test(await p.locator('.antes-bt').innerText())&&await p.evaluate(()=>{const a=document.querySelector('.antes-bt'),b=[...document.querySelectorAll('button')].find(x=>x.textContent==='Guardar a primeira versão');return !!(a.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING);}),tag+' p1 aviso sobre o rascunho antes do botão de guardar');
  await p.fill('#t-p1-resposta',V1);
  await cap('1-interpretacao-08-escrever');
  await p.click('button:has-text("Guardar a primeira versão")');
  ok(await p.locator('.estado.ok').count()===1&&/Feita sem pistas à vista/.test(await p.locator('.estado.ok').innerText())&&/alterá-la em qualquer altura/.test(await p.locator('.estado.ok').innerText()),tag+' p1 primeira versão guardada');
  f=await ativo();ok(/estado ok/.test(f.cls),tag+' foco na confirmação depois de guardar '+JSON.stringify(f));
  await aVista(p.locator('.estado.ok'),'p1 confirmação de guardar');
  ok(await p.locator('#t-p1-resposta').isEditable()&&await p.locator('.alt:visible').count()===0,tag+' p1 primeira versão continua editável depois de guardada');
  // alterar antes de ver os critérios não deixa marca
  await p.fill('#t-p1-resposta',V1+' '+LONGA);await semDeslize('p1 passo 4 com palavra muito longa');
  ok(await p.locator('.alt:visible').count()===0,tag+' p1 alterar antes de ver os critérios não deixa aviso');
  await passo(5);
  ok(await p.evaluate(()=>location.hash)==='#passo-5',tag+' p1 o passo entra no endereço');
  ok((await p.locator('#v1-p1-resposta').innerText()).includes('Primeira versão do aluno')&&await p.locator('.alt:visible').count()===0,tag+' p1 primeira versão à vista na comparação, sem aviso');
  await semDeslize('p1 passo 5 com palavra muito longa');
  // alterar depois de ver os critérios: aviso junto da versão
  await p.click('text=Alterar a primeira versão');
  f=await ativo();ok(f.tag==='TEXTAREA',tag+' p1 foco na caixa ao abrir a alteração');
  await p.fill('#e-p1-resposta',V1+' Acrescento.');
  ok(/alterada depois de veres os critérios/.test(await p.locator('.alt:visible').innerText()),tag+' p1 aviso «alterada depois de veres os critérios» junto da versão');
  await aVista(p.locator('.alt'),'p1 aviso de alteração');
  await p.locator('.bloco',{has:p.locator('.alt')}).first().scrollIntoViewIfNeeded();await cap('1-interpretacao-09-primeira-versao-alterada');
  // repor o texto que estava quando os critérios foram abertos retira o aviso
  await p.fill('#e-p1-resposta',V1+' '+LONGA);ok(await p.locator('.alt:visible').count()===0,tag+' p1 repor o texto retira o aviso');
  await p.fill('#e-p1-resposta',V1F);
  await p.click('text=Fechar a alteração');
  ok((await p.locator('#v1-p1-resposta').innerText()).trim()===V1F,tag+' p1 primeira versão fica à vista depois de fechar a alteração');
  await p.locator('.marca-l input').nth(1).check();
  await cap('1-interpretacao-10-comparar',true);
  await passo(4);ok(await p.inputValue('#t-p1-resposta')===V1F&&(await p.locator('.alt:visible').count())===(estreito?1:0),tag+' p1 o aviso também aparece no passo de escrita (só quando há alteração)');
  ok(!/Feita sem pistas à vista/.test(await p.locator('.estado.ok').innerText()),tag+' p1 depois de vistos os critérios a página deixa de dizer «sem pistas à vista»');
  await passo(6);
  ok(await p.inputValue('#r-p1-resposta')===V1F,tag+' p1 versão revista começa pela primeira (como estava ao abrir este passo)');
  await semDeslize('p1 passo 6 com palavra muito longa na versão revista');
  // palavra muito longa na primeira versão não alarga a grelha
  await p.click('text=Alterar a primeira versão');await p.fill('#e-p1-resposta',V1+' '+LONGA);await p.click('text=Fechar a alteração');
  await semDeslize('p1 passo 6 com palavra muito longa na primeira versão');
  { const cw=await p.evaluate(()=>[...document.querySelectorAll('.duas>div')].map(d=>Math.round(d.getBoundingClientRect().width)));
    ok(cw.length===2&&cw[0]>0&&cw[1]>0&&Math.abs(cw[0]-cw[1])<=2,tag+' p1 as duas colunas mantêm a mesma largura '+cw); }
  await cap('1-interpretacao-11-palavra-longa');
  await p.click('text=Alterar a primeira versão');await p.fill('#e-p1-resposta',V1F);await p.click('text=Fechar a alteração');
  // versão revista: guardar sem mudar nada não conta
  await p.fill('#r-p1-resposta',await p.locator('#v1-p1-resposta').innerText());
  await p.click('text=Guardar a versão revista');
  ok(/Ainda não mudaste nada/.test(await p.locator('.duas .estado').last().innerText())&&/Versão revista da resposta\s+Por fazer/.test(await reg())&&!/feito/.test(await p.locator('#passos li:nth-child(6) button').getAttribute('class')||''),tag+' p1 versão revista igual à primeira não é aceite');
  await p.fill('#r-p1-resposta','');await p.click('text=Guardar a versão revista');
  ok(/Ainda não mudaste nada/.test(await p.locator('.duas .estado').last().innerText()),tag+' p1 versão revista vazia não é aceite');
  // «Revi no papel» atualiza logo o registo e o passo
  await p.locator('.duas .marca-l input').check();
  ok(/Versão revista da resposta\s+Depois de veres os critérios/.test(await reg())&&/feito/.test(await p.locator('#passos li:nth-child(6) button').getAttribute('class'))&&/feito/.test(await p.locator('#passos li:nth-child(6) button').innerText()),tag+' p1 «Revi no papel» atualiza logo o registo e o passo, com a palavra «feito»');
  await p.locator('.duas .marca-l input').uncheck();
  ok(/Versão revista da resposta\s+Por fazer/.test(await reg()),tag+' p1 desmarcar «Revi no papel» volta a «Por fazer»');
  await p.fill('#r-p1-resposta','Versão revista do aluno, com «voluntariamente» (v. 10).');
  await p.click('text=Guardar a versão revista');
  ok(/Versão revista guardada neste dispositivo/.test(await p.locator('.duas .estado.ok').innerText()),tag+' p1 versão revista guardada');
  await p.reload();await p.waitForTimeout(150);
  ok(/Passo 6 de 6/i.test(await p.locator('.passo-n').innerText()),tag+' p1 volta ao passo onde ficou');
  ok((await p.locator('#v1-p1-resposta').innerText()).includes(V1),tag+' p1 primeira versão guardada depois de recarregar');
  ok(await p.inputValue('#r-p1-resposta')==='Versão revista do aluno, com «voluntariamente» (v. 10).',tag+' p1 versão revista guardada depois de recarregar');
  { const g=await reg();
    ok(/manda fazer\s+Com pista, à terceira/.test(g)&&/no mesmo dia\s+Por ti, à primeira/.test(g)&&/é uma escolha\s+Com pista, à segunda/.test(g)&&/e porquê\s+Com explicação/.test(g),tag+' p1 registo distingue à primeira, à segunda, à terceira e com explicação: '+g.replace(/\s+/g,' '));
    ok(estreito?/a proposta\s+Alterada depois de veres os critérios/.test(g):/a proposta\s+Por ti, sem pistas à vista/.test(g),tag+' p1 registo diz se a primeira versão foi alterada depois dos critérios: '+g.replace(/\s+/g,' ').slice(-200));
    ok(/Versão revista da resposta\s+Depois de veres os critérios/.test(g)&&!/[Ss]ozinh/.test(await p.locator('body').innerText()),tag+' p1 registo da versão revista e sem formas com género'); }
  ok((await p.locator('.alt:visible').count())===(estreito?1:0),tag+' p1 aviso de alteração mantém-se depois de recarregar');
  await semDeslize('p1 fim');await cap('1-interpretacao-12-duas-versoes-e-registo',true);
  ok(await p.locator('#passos li button .fe:visible').count()===5,tag+' p1 os cinco passos com resposta feita trazem a palavra «feito»');
  await passo(5);ok(await p.locator('.marca-l input').nth(1).isChecked(),tag+' p1 conferência guardada');
  await passo(3);r=await ret('p1-distinguir');ok(/expl/.test(r.cls),tag+' p1 estado das perguntas reposto');
  // voltar atrás no navegador volta ao passo anterior
  await p.goBack();await p.waitForTimeout(120);
  ok(/Passo 5 de 6/i.test(await p.locator('.passo-n').innerText())&&/interpretacao/.test(p.url()),tag+' p1 voltar atrás no navegador volta ao passo anterior');
  await p.goForward();await p.waitForTimeout(120);ok(/Passo 3 de 6/i.test(await p.locator('.passo-n').innerText()),tag+' p1 avançar no navegador');
  // item oficial completo abre sem deslize
  await p.click('summary:has-text("Ver o item oficial completo")');await semDeslize('p1 item oficial aberto');
  ok(/Descalças!/.test(await p.locator('details.dobra .dentro').innerText()),tag+' p1 item oficial com o texto');
  await p.locator('details.dobra').scrollIntoViewIfNeeded();await cap('1-interpretacao-13-item-oficial',true);
  ok(/exceto quando tal é expressamente requerido no item/.test(await p.evaluate(()=>JSON.stringify(window.TREINO))),tag+' p1 regra da p. 2 citada com a ressalva');
  ok(erros.length===0,tag+' p1 erros de JavaScript: '+erros.join(' | '));erros.length=0;

  /* ===== TREINO 2 ===== */
  await p.goto(BASE+'gramatica/');await semDeslize('p2 inicio');await cap('2-gramatica-01-inicio',true);
  ok(/pp\. 10-11/.test(await p.locator('#apoio').innerText())&&!/pp\. 9-10/.test(await p.content()),tag+' p2 página do texto corrigida (pp. 10-11)');
  await juntos('p2-pedido','p2 passo 1');await cap('2-gramatica-02-texto-junto-da-pergunta');
  await op('p2-pedido',1);r=await ret('p2-pedido');ok(/certo/.test(r.cls)&&/primeira/i.test(r.txt),tag+' p2 certo à primeira');
  await passo(2);await juntos('p2-loc1','p2 passo 2');
  await tk('p2-loc1',['mesquitas']);await verif('p2-loc1');r=await ret('p2-loc1');ok(/pista/.test(r.cls)&&/o que é que lhes aconteceu/.test(r.txt),tag+' p2 pista do erro cometido');
  await aVista(Q('p2-loc1').locator('.retorno'),'p2 pista');
  await cap('2-gramatica-03-pista');
  await tk('p2-loc1',['mesquitas','várias']);await verif('p2-loc1');r=await ret('p2-loc1');
  ok(/^SEGUNDA PISTA/i.test(r.txt)&&/vem de um verbo/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/espalhadas/.test(r.txt),tag+' p2 segunda pista dirigida ao texto, sem a resposta '+r.txt);
  await cap('2-gramatica-04-segunda-pista');
  await tk('p2-loc1',['várias','espalhadas']);await verif('p2-loc1');r=await ret('p2-loc1');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt),tag+' p2 certo à terceira');
  if(estreito){await tk('p2-loc2',['ligeiramente','distorcido']);}else{await tk('p2-loc2',['distorcido']);}
  await verif('p2-loc2');r=await ret('p2-loc2');ok(/certo/.test(r.cls)&&(!estreito||/Aceite com «ligeiramente»/.test(r.txt)),tag+' p2 fronteira equivalente aceite');
  await cap('2-gramatica-05-fronteira-equivalente');
  await passo(3);await op('p2-teste',0);await op('p2-teste',1);r=await ret('p2-teste');ok(/^SEGUNDA PISTA/i.test(r.txt)&&/Justificação B/.test(r.txt),tag+' p2 teste segunda pista');
  await op('p2-teste',3);r=await ret('p2-teste');ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&/frase activa com o mesmo significado/.test(r.txt),tag+' p2 explicação à terceira falha');
  await cap('2-gramatica-06-explicacao');
  await passo(4);await juntos('p2-cortar','p2 passo 4');
  // 11/11/2026: a pergunta passou a ter quatro opções, para dar três tentativas e duas pistas como as outras; a explicação só vem à terceira falha
  ok(await Q('p2-cortar').locator('.op').count()===4,tag+' p2 cortar tem quatro opções');
  await op('p2-cortar',0);r=await ret('p2-cortar');ok(/pista/.test(r.cls)&&/^PISTA/i.test(r.txt)&&/pede o lugar/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p2 cortar pista do erro, restam duas tentativas');
  if(estreito){await op('p2-cortar',1);r=await ret('p2-cortar');ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/mesmo resultado nas duas/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/complemento oblíquo/.test(r.txt),tag+' p2 cortar segunda pista, sem a resposta, resta uma tentativa');
    await op('p2-cortar',3);r=await ret('p2-cortar');ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&!/duas tentativas/i.test(r.txt)&&/complemento oblíquo/.test(r.txt),tag+' p2 cortar: explicação só à terceira falha');}
  else{await op('p2-cortar',2);r=await ret('p2-cortar');ok(/certo/.test(r.cls)&&/complemento oblíquo/.test(r.txt),tag+' p2 cortar certo');}
  await juntos('p2-sujeito','p2 passo 4 item 2.ª fase');
  await op('p2-sujeito',1);r=await ret('p2-sujeito');ok(/pista/.test(r.cls)&&/isso/.test(r.txt),tag+' p2 sujeito pista');
  await op('p2-sujeito',0);r=await ret('p2-sujeito');ok(/certo/.test(r.cls)&&/Versão 2, \(A\)/.test(r.txt),tag+' p2 sujeito certo com chave');
  await cap('2-gramatica-07-limites-dos-testes',true);
  await passo(5);
  ok(await p.locator('#passos li:nth-child(6) button').isDisabled(),tag+' p2 passo 6 trancado');
  ok(!/Versão 2, <b>\(D\)/.test(await p.locator('#passo').innerHTML()),tag+' p2 chave escondida antes da resposta');
  await p.click('button:has-text("Guardar a primeira versão")');ok(/Escolhe primeiro uma opção/.test(await p.locator('#passo').innerText()),tag+' p2 exige opção');
  await p.locator('input[name="o-p2-resposta"]').nth(3).check();
  await p.fill('#t-p2-resposta','Em «que vemos pela Ásia» o verbo está na ativa.');
  await cap('2-gramatica-08-responder');
  await p.click('button:has-text("Guardar a primeira versão")');
  await passo(6);ok(/\(D\)/.test(await p.locator('.caixa.of').first().innerText())&&/\(D\) «pela Ásia»/.test(await p.locator('#passo').innerText()),tag+' p2 chave e opção escolhida');
  { const t=await p.locator('#passo').innerText();
    ok(/Cinco deles aparecem nos itens 7/.test(t)&&/é-o/.test(t)&&!/são os que aparecem nos itens 7/.test(t),tag+' p2 termos conferidos e limite do teste de troca corrigidos');
    ok(await p.locator('#passo i',{hasText:'Dicionário Terminológico'}).count()>=2&&await p.evaluate(()=>!/(^|[^>])Dicionário Terminológico/.test(JSON.stringify(window.TREINO))),tag+' p2 título do Dicionário Terminológico sempre em itálico'); }
  // mudar a opção depois de ver a chave fica assinalado
  await p.click('text=Alterar a primeira versão');await p.locator('input[name="e-o-p2-resposta"]').nth(0).check();
  ok(/alterada depois de veres a chave oficial/.test(await p.locator('.alt:visible').innerText()),tag+' p2 mudar a opção depois de ver a chave fica assinalado');
  await cap('2-gramatica-09-comparar',true);
  await p.locator('input[name="e-o-p2-resposta"]').nth(3).check();ok(await p.locator('.alt:visible').count()===0,tag+' p2 repor a opção retira o aviso');
  await p.click('text=Fechar a alteração');
  await passo(7);await p.fill('#r-p2-resposta','Versão revista: passei à ativa as três primeiras; em (D) não há passiva.');await p.click('text=Guardar a versão revista');
  await p.reload();await p.waitForTimeout(150);
  ok(/vemos pela Ásia/.test(await p.locator('#v1-p2-resposta').innerText())&&/Versão revista: passei/.test(await p.inputValue('#r-p2-resposta')),tag+' p2 duas versões depois de recarregar');
  { const g=await reg();ok(/Com pista, à terceira/.test(g)&&/Com explicação/.test(g)&&/Por ti, à primeira/.test(g)&&/Por ti, sem pistas à vista/.test(g)&&/Depois de veres a chave oficial/.test(g),tag+' p2 registo '+g.replace(/\s+/g,' ')); }
  await semDeslize('p2 fim');await cap('2-gramatica-10-duas-versoes-e-registo',true);
  ok(erros.length===0,tag+' p2 erros de JavaScript: '+erros.join(' | '));erros.length=0;

  /* ===== TREINO 3 ===== */
  await p.goto(BASE+'escrita/');await semDeslize('p3 inicio');await cap('3-escrita-01-inicio',true);
  await juntos('p3-pedido','p3 passo 1');await cap('3-escrita-02-texto-junto-da-pergunta');
  await op('p3-pedido',1);r=await ret('p3-pedido');ok(/certo/.test(r.cls),tag+' p3 pedido certo');
  await op('p3-limites',0);r=await ret('p3-limites');ok(/pista/.test(r.cls)&&/abaixo do qual/.test(r.txt),tag+' p3 limites pista');
  await aVista(Q('p3-limites').locator('.retorno'),'p3 pista');
  await op('p3-limites',1);r=await ret('p3-limites');ok(/^SEGUNDA PISTA/i.test(r.txt)&&/duas frases/.test(r.txt)&&!/4 pontos/.test(r.txt),tag+' p3 limites segunda pista sem a resposta');
  await op('p3-limites',2);r=await ret('p3-limites');ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&/descontam-se 4 pontos/.test(r.txt),tag+' p3 limites explicação à terceira falha');
  await cap('3-escrita-03-explicacao');
  await passo(2);await juntos('p3-tema','p3 passo 2');
  await tk('p3-tema',['visão']);await verif('p3-tema');r=await ret('p3-tema');ok(/pista/.test(r.cls)&&/para que as duas coisas contribuem/.test(r.txt),tag+' p3 tema pista do erro');
  await aVista(Q('p3-tema').locator('.retorno'),'p3 pista da seleção');
  await cap('3-escrita-04-pista');
  await tk('p3-tema',['visão']);
  if(estreito){await tk('p3-tema',['experiências','conhecimentos']);}else{await tk('p3-tema',['das','experiências','pessoais','dos','conhecimentos','adquiridos','na','escola']);}
  await verif('p3-tema');r=await ret('p3-tema');ok(/certo/.test(r.cls)&&/Leitura nossa/.test(r.txt)&&!/obriga-te/.test(r.txt),tag+' p3 tema fronteira '+(estreito?'curta':'longa')+' aceite; desvio do tema dito como leitura nossa');
  await p.fill('#c-p3-plano-pv','As duas completam-se.');await p.fill('#c-p3-plano-a1','A experiência aproxima. '+LONGA);
  await semDeslize('p3 plano com palavra muito longa');
  await cap('3-escrita-05-plano',true);
  await passo(3);await op('p3-distinguir',0);r=await ret('p3-distinguir');ok(/pista/.test(r.cls)&&/articulação interfrásica/.test(r.txt),tag+' p3 distinguir pista');
  await op('p3-distinguir',2);r=await ret('p3-distinguir');ok(/certo/.test(r.cls),tag+' p3 distinguir certo');
  await passo(4);
  await p.click('summary:has-text("Ver o meu plano")');ok(/As duas completam-se/.test(await p.locator('details.dobra .dentro').innerText()),tag+' p3 plano à vista');
  await semDeslize('p3 plano aberto com palavra muito longa');
  const semLeitura=async(onde)=>{const t=await p.locator('#passo').innerText();ok(!/desconta \d|Faltam \d|Passam \d|Dentro dos limites|célula realçada|a tabela indica/.test(t),tag+' sem leituras automáticas em '+onde);};
  await p.fill('#t-p3-texto','Uma');ok(/^1 palavra \(/.test(await p.locator('.conta').innerText()),tag+' p3 contagem no singular: '+await p.locator('.conta').innerText());
  await p.fill('#t-p3-texto',TXT196);ok(/^196 palavras \(contagem/.test(await p.locator('.conta').innerText()),tag+' p3 contagem ao vivo 196');await semLeitura('p3 passo 4 (196 palavras)');
  await p.fill('#t-p3-texto','Uma '+'palavra '.repeat(60));await semLeitura('p3 passo 4 (61 palavras)');
  await p.fill('#t-p3-texto','Uma');
  await cap('3-escrita-06-escrever');
  await p.click('button:has-text("Guardar a primeira versão")');
  await passo(5);
  ok(/1 palavra\./.test(await p.locator('.conta').first().innerText())&&!/1 palavras/.test(await p.locator('#passo').innerText()),tag+' p3 «1 palavra» na versão guardada');
  await passo(4);await p.fill('#t-p3-texto',TXT210);ok(/^210 palavras \(contagem/.test(await p.locator('.conta').innerText()),tag+' p3 contagem ao vivo 210');
  ok(/alterada depois de veres os critérios/.test(await p.locator('.alt:visible').innerText()),tag+' p3 aviso de alteração no passo de escrita');
  await passo(5);
  await semLeitura('p3 passo 5');
  { const t=await p.locator('#passo').innerText();
    ok(await p.locator('#passo input[type=number]').count()===0&&await p.locator('td.aqui,td[data-a]').count()===0&&await p.locator('#c-p3-cl-A').count()===0&&!/Erros do tipo A que encontraste/.test(t),tag+' p3 sem campo de contagem de erros nem realce de célula');
    ok(await p.locator('input[name^="c-p3-n"]').count()===0&&!/Onde situas/.test(t)&&!/Não sei: pergunto ao docente/.test(t),tag+' p3 sem autoavaliação por nível');
    ok(await p.locator('#passo table',{hasText:'Descritor de desempenho'}).count()===3&&/Nível/.test(t),tag+' p3 descritores oficiais de nível consultáveis (três tabelas)');
    ok(await p.locator('#passo table.cl').count()===1&&/Caso o número total de erros seja superior ao número máximo apresentado na tabela/.test(t)&&/contabiliza-se como uma única ocorrência quer a repetição de uma palavra com o mesmo erro ortográfico/.test(t)&&/critérios gerais, p\. 3/.test(t),tag+' p3 tabela e regras da correção linguística visíveis, com página');
    ok(/desconta-se um ponto por cada palavra/.test(t)&&/inferior a oitenta palavras/.test(t)&&/A página não calcula descontos/.test(t),tag+' p3 regra da extensão visível para o aluno aplicar');
    ok(await p.locator('#passo fieldset.radios').count()===14&&/por exemplo: fala das duas coisas/i.test(t),tag+' p3 marcação aspeto a aspeto (14 aspetos): '+await p.locator('#passo fieldset.radios').count()); }
  await p.locator('input[name="g-p3-gA-0"]').nth(0).check();
  await semDeslize('p3 grelha');await cap('3-escrita-07-grelha',true);
  await p.locator('input[name="g-p3-gC-0"]').nth(0).focus();await p.evaluate(()=>document.activeElement.scrollIntoView());await p.waitForTimeout(80);
  { const v=await p.evaluate(()=>{const a=document.getElementById('apoio').getBoundingClientRect(),e=document.activeElement.getBoundingClientRect();return {ab:a.bottom,et:e.top,estreito:window.innerWidth<980};});
    ok(!v.estreito||v.et>=v.ab-1,tag+' campo com foco não fica tapado pelo texto de apoio '+JSON.stringify(v)); }
  await p.evaluate(()=>{const c=document.querySelector('table.cl');c.scrollIntoView({block:'center'});const r=c.closest('.rolo');r.scrollLeft=r.scrollWidth;});await p.waitForTimeout(80);
  { const v=await p.evaluate(()=>{const r=document.querySelector('table.cl').closest('.rolo'),th=document.querySelector('table.cl tbody th').getBoundingClientRect(),rr=r.getBoundingClientRect();return {desliza:r.scrollWidth>r.clientWidth,dx:Math.round(th.left-rr.left)};});
    ok(!v.desliza||Math.abs(v.dx)<=2,tag+' tabela CL: a primeira coluna fica à vista quando a tabela desliza '+JSON.stringify(v)); }
  await cap('3-escrita-08-tabela-cl');
  await passo(6);await p.fill('#r-p3-texto',TXT210+' revista');await p.click('text=Guardar a versão revista');
  await semLeitura('p3 passo 6');
  await p.reload();await p.waitForTimeout(150);
  ok((await p.locator('#v1-p3-texto').innerText()).trim()===TXT210&&(await p.inputValue('#r-p3-texto'))===TXT210+' revista',tag+' p3 duas versões depois de recarregar');
  ok(/alterada depois de veres os critérios/.test(await p.locator('.alt:visible').innerText())&&/200 a 350 palavras\)\s+Alterada depois de veres os critérios/.test(await reg()),tag+' p3 alteração assinalada junto da versão e no registo');
  await passo(5);ok(await p.locator('input[name="g-p3-gA-0"]').nth(0).isChecked(),tag+' p3 grelha guardada');
  await passo(6);await semDeslize('p3 fim');await cap('3-escrita-09-duas-versoes-e-registo',true);
  // recolher o texto de apoio
  await p.click('#apoio-bt');ok(await p.locator('#apoio-corpo').isHidden()&&await p.getAttribute('#apoio-bt','aria-expanded')==='false',tag+' texto de apoio recolhe');await p.click('#apoio-bt');
  ok(erros.length===0,tag+' p3 erros de JavaScript: '+erros.join(' | '));erros.length=0;

  /* ===== TREINO 4 (12/11/2026): poesia contemporânea, sessão 17 ===== */
  await p.goto(BASE+'poesia-contemporanea/');await semDeslize('p4 inicio');await cap('5-poesia-01-inicio',true);
  // 12/11/2026: com o treino da sessão 18, este passa a ser o 4 de 5
  ok(/Treino 4 de 5/i.test(await p.locator('.sobre').innerText())&&/Comparar dois poemas a partir de um eixo/.test(await p.locator('dl.liga').innerText())&&/2\.ª fase, Grupo I, Parte A, item 2/.test(await p.locator('dl.liga').innerText()),tag+' p4 operação do exame e item oficial no cimo');
  // texto de apoio: só as duas citações curtas, a remissão para o manual e as ligações às lições do M8
  { const a=await p.evaluate(()=>{const d=document.querySelector('#apoio-corpo [data-apoio="cit"]');return {oculto:d.hidden||document.getElementById('apoio').hidden,rot:document.getElementById('apoio-rot').textContent,
      cit:Array.from(d.querySelectorAll('.cit')).map(e=>e.textContent),txt:d.innerText,lig:Array.from(d.querySelectorAll('a')).map(x=>new URL(x.href).pathname)};});
    ok(!a.oculto&&a.rot==='Citações e onde ler os poemas',tag+' p4 texto de apoio à vista com o seu rótulo '+a.rot);
    ok(a.cit.join(' | ')==='«Apenas como elas. / Mas brilha.» | «São como um cristal, / as palavras.»',tag+' p4 o texto de apoio traz só as duas citações curtas '+a.cit.join(' | '));
    ok(/Abre o manual/.test(a.txt)&&/Novo Sentidos 12/.test(a.txt)&&/direitos de autor/.test(a.txt)&&/Ou abre a lição/.test(a.txt),tag+' p4 o texto de apoio remete para o manual e para as lições');
    ok(a.lig.join(' ')==='/pt/m8/licao-m8-f03/ /pt/m8/licao-m8-f04/',tag+' p4 ligações às lições do M8 '+a.lig.join(' '));
    for(const u of a.lig){const r=await p.request.get(new URL(u,BASE).href);ok(r.status()===200,tag+' p4 a lição '+u+' responde');} }
  await juntos('p4-pedido','p4 passo 1');await cap('5-poesia-02-texto-junto-da-pergunta');
  ok(/perspetiva a escrita/.test(await p.locator('#passo').innerText())&&/Compare o ambiente do mercado do peixe/.test(await p.locator('#passo').innerText())&&await p.locator('#passo .etq.oficial').count()===2&&await p.locator('#passo .etq.treino').count()>=2,tag+' p4 passo 1: os dois itens oficiais e o pedido de treino, com etiqueta');
  // 1.ª falha: pista do erro; repetir a opção não gasta tentativa; 2.ª falha: segunda pista sem a resposta; certo à terceira
  await op('p4-pedido',0);r=await ret('p4-pedido');
  ok(/pista/.test(r.cls)&&/^PISTA/i.test(r.txt)&&/Relê o primeiro verbo/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p4 1.ª falha: pista da opção escolhida e duas tentativas '+r.txt);
  ok(await Q('p4-pedido').locator('.op').nth(0).getAttribute('aria-disabled')==='true',tag+' p4 opção tentada fica indisponível');
  await aVista(Q('p4-pedido').locator('.retorno'),'p4 pista depois de errar');
  await cap('5-poesia-03-pista');
  await Q('p4-pedido').locator('.op').nth(0).focus();await p.keyboard.press('Enter');r=await ret('p4-pedido');ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p4 repetir a opção tentada (teclado) não gasta tentativa');
  await op('p4-pedido',1);r=await ret('p4-pedido');
  ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/aos bocados/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/A opção adequada é/.test(r.txt),tag+' p4 2.ª falha: segunda pista sem a resposta '+r.txt);
  await aVista(Q('p4-pedido').locator('.retorno'),'p4 segunda pista');
  await cap('5-poesia-04-segunda-pista');
  await op('p4-pedido',2);r=await ret('p4-pedido');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt)&&/um verbo, um eixo e uma condição/.test(r.txt),tag+' p4 certo à terceira '+r.txt.slice(0,60));
  await passo(2);
  f=await ativo();ok(f.tag==='H2',tag+' p4 ao mudar de passo o foco vai para o título '+JSON.stringify(f));
  await juntos('p4-sena','p4 passo 2');
  ok((await Q('p4-sena').locator('.seg').innerText()).replace(/\s+/g,' ').trim()==='Apenas como elas. / Mas brilha.'&&(await Q('p4-eugenio').locator('.seg').innerText()).replace(/\s+/g,' ').trim()==='São como um cristal, / as palavras.',tag+' p4 as palavras em que se toca são as das duas citações');
  await verif('p4-sena');ok(/Ainda não escolheste/.test(await aviso('p4-sena')),tag+' p4 verificar sem seleção avisa e não gasta tentativa');
  // seleção por teclado
  await Q('p4-sena').locator('.tk',{hasText:'brilha.'}).focus();await p.keyboard.press('Space');
  ok(await Q('p4-sena').locator('.tk',{hasText:'brilha.'}).getAttribute('aria-pressed')==='true',tag+' p4 seleção de palavra por teclado');
  await verif('p4-sena');r=await ret('p4-sena');
  ok(/pista/.test(r.cls)&&/apesar de tudo/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p4 «brilha» só: pista do erro cometido '+r.txt.slice(0,80));
  await aVista(Q('p4-sena').locator('.retorno'),'p4 pista da seleção');
  await verif('p4-sena');r=await ret('p4-sena');
  ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt)&&/não gastaste outra tentativa/.test(await aviso('p4-sena')),tag+' p4 verificar duas vezes a mesma seleção errada não gasta tentativa');
  if(estreito){await tk('p4-sena',['Mas']);await verif('p4-sena');r=await ret('p4-sena');
    ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/Aceite com «brilha»/.test(r.txt)&&/adversativa/.test(r.txt),tag+' p4 fronteira equivalente aceite, à segunda '+r.txt.slice(0,80));}
  else{await tk('p4-sena',['brilha.','Apenas']);await verif('p4-sena');r=await ret('p4-sena');
    ok(/^SEGUNDA PISTA/i.test(r.txt)&&/é uma conjunção/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/«Mas»/.test(r.txt),tag+' p4 segunda pista dirigida à citação, sem a resposta '+r.txt);
    await tk('p4-sena',['Apenas','Mas']);await verif('p4-sena');r=await ret('p4-sena');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt)&&/adversativa/.test(r.txt),tag+' p4 certo à terceira');}
  await cap('5-poesia-05-localizar-sena');
  await juntos('p4-eugenio','p4 passo 2, segunda citação');
  await tk('p4-eugenio',['como']);await verif('p4-eugenio');r=await ret('p4-eugenio');ok(/pista/.test(r.cls)&&/faz a comparação/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p4 «como»: pista do erro cometido');
  if(estreito){await tk('p4-eugenio',['como','palavras.']);await verif('p4-eugenio');r=await ret('p4-eugenio');
    ok(/^SEGUNDA PISTA/i.test(r.txt)&&/dois termos/.test(r.txt)&&!/cristal/.test(r.txt),tag+' p4 segunda pista sem a resposta '+r.txt);
    await tk('p4-eugenio',['palavras.','cristal,']);await verif('p4-eugenio');r=await ret('p4-eugenio');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt),tag+' p4 certo à terceira (segunda citação)');}
  else{await tk('p4-eugenio',['como','um','cristal,']);await verif('p4-eugenio');r=await ret('p4-eugenio');
    ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/Aceite com «um»/.test(r.txt),tag+' p4 fronteira equivalente aceite (segunda citação) '+r.txt.slice(0,80));}
  ok(/lê os poemas inteiros no manual/.test(r.txt),tag+' p4 a explicação manda ler os poemas inteiros no manual');
  await cap('5-poesia-06-fronteira-equivalente');
  await passo(3);await juntos('p4-distinguir','p4 passo 3');
  await op('p4-distinguir',0);r=await ret('p4-distinguir');ok(/pista/.test(r.cls)&&/faz parte da maneira/.test(r.txt),tag+' p4 distinguir pista 1');
  await op('p4-distinguir',2);r=await ret('p4-distinguir');ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/mas só/.test(r.txt),tag+' p4 distinguir segunda pista');
  ok(!/certa/.test(await Q('p4-distinguir').locator('.op').nth(1).getAttribute('class')),tag+' p4 a resposta não aparece antes da terceira falha');
  await op('p4-distinguir',3);r=await ret('p4-distinguir');
  ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&/duas descrições lado a lado/.test(r.txt)&&/em ambos os casos/.test(r.txt)&&/um dos sujeitos poéticos/.test(r.txt)&&/leitura nossa/.test(r.txt),tag+' p4 explicação só à terceira falha, com os critérios oficiais '+r.txt.slice(0,60));
  ok(/certa/.test(await Q('p4-distinguir').locator('.op').nth(1).getAttribute('class')),tag+' p4 opção adequada marcada');
  await aVista(Q('p4-distinguir').locator('.retorno'),'p4 explicação');
  await cap('5-poesia-07-explicacao');
  await passo(4);
  ok(await p.locator('#passos li:nth-child(5) button').isDisabled(),tag+' p4 passo 5 trancado antes de guardar');
  ok(await p.locator('.retorno:visible').count()===0&&/Abre o manual e lê os dois poemas inteiros/.test(await p.locator('#passo').innerText()),tag+' p4 sem pistas à vista no passo de escrita, com a remissão para o manual');
  ok(/guarda-se automaticamente/.test(await p.locator('.antes-bt').innerText()),tag+' p4 aviso sobre o rascunho antes do botão de guardar');
  await p.fill('#t-p4-resposta',V1);
  await cap('5-poesia-08-escrever');
  await p.click('button:has-text("Guardar a primeira versão")');
  ok(await p.locator('.estado.ok').count()===1&&/Feita sem pistas à vista/.test(await p.locator('.estado.ok').innerText())&&/alterá-la em qualquer altura/.test(await p.locator('.estado.ok').innerText()),tag+' p4 primeira versão guardada');
  await aVista(p.locator('.estado.ok'),'p4 confirmação de guardar');
  await p.fill('#t-p4-resposta',V1+' '+LONGA);await semDeslize('p4 passo 4 com palavra muito longa');
  ok(await p.locator('.alt:visible').count()===0,tag+' p4 alterar antes de ver os critérios não deixa aviso');
  await passo(5);
  ok((await p.locator('#v1-p4-resposta').innerText()).includes('Primeira versão do aluno')&&await p.locator('.alt:visible').count()===0,tag+' p4 primeira versão à vista na conferência, sem aviso');
  await semDeslize('p4 passo 5 com palavra muito longa');
  { const t=await p.locator('#passo').innerText();
    ok(/Tópicos de resposta/.test(t)&&/O que se mantém e o que muda/.test(t)&&/se o texto te mostrar outra coisa, vale o texto/.test(t)&&/igualdade de circunstâncias/.test(t)&&/ou outros igualmente relevantes/.test(t),tag+' p4 tópicos nossos e regra oficial das outras formulações');
    ok(/Um exemplo comentado/.test(t)&&/Uma maneira de organizar \(é nossa, não é exigência do exame\)/.test(t)&&await p.locator('#passo .anot').count()===4,tag+' p4 exemplo comentado e «Uma maneira de organizar»');
    ok(await p.locator('#passo input[type=number]').count()===0&&await p.locator('#passo input[type=radio]').count()===0&&await p.locator('#passo .marca-l input[type=checkbox]').count()===9&&!/a tua classificação|pontos obtidos/i.test(t)&&/Não há classificação automática/.test(t),tag+' p4 sem classificação automática: só marcação aspeto a aspeto (9 aspetos)'); }
  await p.click('text=Alterar a primeira versão');
  await p.fill('#e-p4-resposta',V1+' Acrescento.');
  ok(/alterada depois de veres os critérios/.test(await p.locator('.alt:visible').innerText()),tag+' p4 aviso «alterada depois de veres os critérios» junto da versão');
  await aVista(p.locator('.alt'),'p4 aviso de alteração');
  await p.fill('#e-p4-resposta',V1+' '+LONGA);ok(await p.locator('.alt:visible').count()===0,tag+' p4 repor o texto retira o aviso');
  await p.fill('#e-p4-resposta',V1F);
  await p.click('text=Fechar a alteração');
  await p.locator('.marca-l input').nth(2).check();
  await cap('5-poesia-09-conferir',true);
  await passo(6);
  ok(await p.inputValue('#r-p4-resposta')===V1F,tag+' p4 versão revista começa pela primeira');
  await semDeslize('p4 passo 6');
  await p.click('text=Guardar a versão revista');
  ok(/Ainda não mudaste nada/.test(await p.locator('.duas .estado').last().innerText())&&/Versão revista da resposta\s+Por fazer/.test(await reg()),tag+' p4 versão revista igual à primeira não é aceite');
  await p.fill('#r-p4-resposta','Versão revista do aluno: os dois poemas, com «Mas brilha.»');
  await p.click('text=Guardar a versão revista');
  ok(/Versão revista guardada neste dispositivo/.test(await p.locator('.duas .estado.ok').innerText()),tag+' p4 versão revista guardada');
  await p.reload();await p.waitForTimeout(150);
  ok(/Passo 6 de 6/i.test(await p.locator('.passo-n').innerText()),tag+' p4 volta ao passo onde ficou');
  ok((await p.locator('#v1-p4-resposta').innerText()).includes(V1)&&await p.inputValue('#r-p4-resposta')==='Versão revista do aluno: os dois poemas, com «Mas brilha.»',tag+' p4 duas versões guardadas depois de recarregar');
  { const g=await reg();
    ok(/manda fazer\s+Com pista, à terceira/.test(g)&&(estreito?/a luz resiste\s+Com pista, à segunda/.test(g)&&/comparadas as palavras\s+Com pista, à terceira/.test(g):/a luz resiste\s+Com pista, à terceira/.test(g)&&/comparadas as palavras\s+Com pista, à segunda/.test(g))&&/e porquê\s+Com explicação/.test(g),tag+' p4 registo distingue à segunda, à terceira e com explicação: '+g.replace(/\s+/g,' '));
    ok((estreito?/dos dois poemas\s+Alterada depois de veres os critérios/.test(g):/dos dois poemas\s+Por ti, sem pistas à vista/.test(g))&&/Versão revista da resposta\s+Depois de veres os critérios/.test(g)&&!/[Ss]ozinh/.test(await p.locator('body').innerText()),tag+' p4 registo das duas versões: '+g.replace(/\s+/g,' ').slice(-200)); }
  ok((await p.locator('.alt:visible').count())===(estreito?1:0),tag+' p4 aviso de alteração mantém-se depois de recarregar (só quando há alteração)');
  { const t=await p.locator('#passo').innerText();const l=await p.evaluate(()=>Array.from(document.querySelectorAll('#passo .caixa.nossa a')).map(x=>new URL(x.href).pathname).join(' '));
    ok(/Outro par/.test(t)&&l==='/pt/m8/licao-m8-f05/'&&/a confirmar na Informação-Prova de 2027/.test(t),tag+' p4 outro par (lição M8-F05) e referência a 2027 '+l); }
  await semDeslize('p4 fim');await cap('5-poesia-10-duas-versoes-e-registo',true);
  ok(await p.locator('#passos li button .fe:visible').count()===5,tag+' p4 os cinco passos com resposta feita trazem a palavra «feito»');
  await passo(5);ok(await p.locator('.marca-l input').nth(2).isChecked(),tag+' p4 conferência guardada');
  await passo(3);r=await ret('p4-distinguir');ok(/expl/.test(r.cls),tag+' p4 estado das perguntas reposto');
  await p.goBack();await p.waitForTimeout(120);
  ok(/Passo 5 de 6/i.test(await p.locator('.passo-n').innerText())&&/poesia-contemporanea/.test(p.url()),tag+' p4 voltar atrás no navegador volta ao passo anterior');
  // item oficial: abre sem deslize, com o critério, e sem repetir os dois poemas da prova (ficam nas provas em cartões)
  await p.click('summary:has-text("Ver o item oficial")');await semDeslize('p4 item oficial aberto');
  { const t=await p.locator('details.dobra .dentro').innerText();
    ok(/perspetiva a escrita/.test(t)&&/mão rigorosa/.test(t)&&/Sou|fácil de definir/.test(t)&&/Descritor de desempenho/.test(t)&&/Erros do tipo B/.test(t),tag+' p4 item oficial com o item, o critério e as duas tabelas');
    ok(!/Obedecem-me agora muito menos/.test(await p.content())&&!/Um dia deu-me o sono/.test(await p.content()),tag+' p4 os poemas da prova não se repetem na página');
    const u=await p.evaluate(()=>new URL(document.querySelector('details.dobra .dentro a[href*="provas"]').href).href);const rr=await p.request.get(u);
    ok(rr.status()===200&&/\/pt\/exame\/provas\/2026-2f\/grupo-i\/$/.test(u)&&/Obedecem-me agora muito menos/.test(await rr.text()),tag+' p4 os poemas da prova leem-se nas provas em cartões '+u); }
  await p.locator('details.dobra').scrollIntoViewIfNeeded();await cap('5-poesia-11-item-oficial',true);
  await p.click('#apoio-bt');ok(await p.locator('#apoio-corpo').isHidden()&&await p.getAttribute('#apoio-bt','aria-expanded')==='false',tag+' p4 texto de apoio recolhe');await p.click('#apoio-bt');
  ok(erros.length===0,tag+' p4 erros de JavaScript: '+erros.join(' | '));erros.length=0;
  /* ===== TREINO 5 (12/11/2026): conto, sessão 18 ===== */
  { const RECORTE='À sua frente uma senhora de idade, primeiro esboçada, finalmente completa, olha-a atentamente. De idade não, George detesta eufemismos, mesmo só pensados, uma mulher velha.';
  const FRASE2='De idade não, George detesta eufemismos, mesmo só pensados, uma mulher velha.';
  // as palavras tocam-se pelo número de ordem: «De», «de» e «idade» repetem-se no recorte
  const tki=async(id,idxs)=>{for(const i of idxs){await Q(id).locator('.tk').nth(i).click();}};
  await p.goto(BASE+'conto/');await semDeslize('p5 inicio');await cap('6-conto-01-inicio',true);
  ok(/Treino 5 de 5/i.test(await p.locator('.sobre').innerText())&&/Fundamentar uma inferência sobre uma personagem/.test(await p.locator('dl.liga').innerText())&&/2\.ª fase, Grupo I, Parte B, item 4/.test(await p.locator('dl.liga').innerText()),tag+' p5 operação do exame e item oficial no cimo');
  // texto de apoio: só o recorte de duas frases, a referência, a remissão para o manual e as ligações às lições do M8
  { const a=await p.evaluate(()=>{const d=document.querySelector('#apoio-corpo [data-apoio="cit"]');return {oculto:d.hidden||document.getElementById('apoio').hidden,rot:document.getElementById('apoio-rot').textContent,
      cit:Array.from(d.querySelectorAll('.cit')).map(e=>e.textContent),txt:d.innerText,lig:Array.from(d.querySelectorAll('a')).map(x=>new URL(x.href).pathname)};});
    ok(!a.oculto&&a.rot==='O recorte e onde ler o conto',tag+' p5 texto de apoio à vista com o seu rótulo '+a.rot);
    ok(a.cit.length===1&&a.cit[0]==='«'+RECORTE+'»',tag+' p5 o texto de apoio traz só o recorte de duas frases '+a.cit.join(' | '));
    ok(/Abre o manual/.test(a.txt)&&/Novo Sentidos 12/.test(a.txt)&&/direitos de autor/.test(a.txt)&&/Ou abre a lição/.test(a.txt)&&/Seta Despedida, Mem Martins, Europa-América, 1995/.test(a.txt)&&/resumo, não são frases do conto/.test(a.txt),tag+' p5 o texto de apoio dá a referência e remete para o manual e para as lições');
    ok(a.lig.join(' ')==='/pt/m8/licao-m8-f16/ /pt/m8/licao-m8-f08/',tag+' p5 ligações às lições do M8 '+a.lig.join(' '));
    for(const u of a.lig){const rr=await p.request.get(new URL(u,BASE).href);ok(rr.status()===200,tag+' p5 a lição '+u+' responde');}
    const l16=await (await p.request.get(new URL('/pt/m8/licao-m8-f16/',BASE).href)).text();
    ok(l16.includes('«'+RECORTE+'»'),tag+' p5 o recorte é, letra a letra, o que a lição M8-F16 publica'); }
  await juntos('p5-pedido','p5 passo 1');await cap('6-conto-02-texto-junto-da-pergunta');
  ok(/Infira dois traços da personalidade de Manuel/.test(await p.locator('#passo').innerText())&&/Explicite o dilema com o qual Baltasar se debate/.test(await p.locator('#passo').innerText())&&await p.locator('#passo .etq.oficial').count()===2&&await p.locator('#passo .etq.treino').count()>=2,tag+' p5 passo 1: os dois itens oficiais e o pedido de treino, com etiqueta');
  // 1.ª falha: pista do erro; repetir a opção não gasta tentativa; 2.ª falha: segunda pista sem a resposta; certo à terceira
  await op('p5-pedido',0);r=await ret('p5-pedido');
  ok(/pista/.test(r.cls)&&/^PISTA/i.test(r.txt)&&/Relê o primeiro verbo/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 1.ª falha: pista da opção escolhida e duas tentativas '+r.txt);
  ok(await Q('p5-pedido').locator('.op').nth(0).getAttribute('aria-disabled')==='true',tag+' p5 opção tentada fica indisponível');
  await aVista(Q('p5-pedido').locator('.retorno'),'p5 pista depois de errar');
  await cap('6-conto-03-pista');
  await Q('p5-pedido').locator('.op').nth(0).focus();await p.keyboard.press('Enter');r=await ret('p5-pedido');ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 repetir a opção tentada (teclado) não gasta tentativa');
  await op('p5-pedido',2);r=await ret('p5-pedido');
  ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/aos bocados/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/A opção adequada é/.test(r.txt),tag+' p5 2.ª falha: segunda pista sem a resposta '+r.txt);
  await aVista(Q('p5-pedido').locator('.retorno'),'p5 segunda pista');
  await cap('6-conto-04-segunda-pista');
  await op('p5-pedido',1);r=await ret('p5-pedido');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt)&&/um verbo, uma condição e um limite/.test(r.txt)&&/Infere dois traços da personalidade de Manuel/.test(r.txt),tag+' p5 certo à terceira '+r.txt.slice(0,60));
  await passo(2);
  f=await ativo();ok(f.tag==='H2',tag+' p5 ao mudar de passo o foco vai para o título '+JSON.stringify(f));
  await juntos('p5-recusa','p5 passo 2');
  ok((await Q('p5-recusa').locator('.seg').innerText()).replace(/\s+/g,' ').trim()===RECORTE&&(await Q('p5-pensados').locator('.seg').innerText()).replace(/\s+/g,' ').trim()===FRASE2&&await Q('p5-recusa').locator('.tk').count()===25&&await Q('p5-pensados').locator('.tk').count()===12,tag+' p5 as palavras em que se toca são as do recorte');
  await verif('p5-recusa');ok(/Ainda não escolheste/.test(await aviso('p5-recusa')),tag+' p5 verificar sem seleção avisa e não gasta tentativa');
  // seleção por teclado
  await Q('p5-recusa').locator('.tk').nth(18).focus();await p.keyboard.press('Space');
  ok(await Q('p5-recusa').locator('.tk').nth(18).getAttribute('aria-pressed')==='true'&&(await Q('p5-recusa').locator('.tk').nth(18).innerText())==='eufemismos,',tag+' p5 seleção de palavra por teclado');
  await verif('p5-recusa');r=await ret('p5-recusa');
  ok(/pista/.test(r.cls)&&/dá a razão da troca/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 «eufemismos»: pista do erro cometido '+r.txt.slice(0,80));
  await aVista(Q('p5-recusa').locator('.retorno'),'p5 pista da seleção');
  await verif('p5-recusa');r=await ret('p5-recusa');
  ok(/^PISTA/i.test(r.txt)&&/mais duas tentativas/.test(r.txt)&&/não gastaste outra tentativa/.test(await aviso('p5-recusa')),tag+' p5 verificar duas vezes a mesma seleção errada não gasta tentativa');
  if(estreito){await tki('p5-recusa',[18,14,15]);await verif('p5-recusa');r=await ret('p5-recusa');
    ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/Aceite com «De idade»/.test(r.txt)&&/primeiro elemento textual/.test(r.txt),tag+' p5 fronteira equivalente aceite, à segunda '+r.txt.slice(0,80));}
  else{await tki('p5-recusa',[18,6]);await verif('p5-recusa');r=await ret('p5-recusa');
    ok(/^SEGUNDA PISTA/i.test(r.txt)&&/advérbio de negação/.test(r.txt)&&/mais uma tentativa/.test(r.txt)&&!/«não»/.test(r.txt),tag+' p5 segunda pista dirigida ao recorte, sem a resposta '+r.txt);
    await tki('p5-recusa',[6,15]);await verif('p5-recusa');r=await ret('p5-recusa');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt)&&/primeiro elemento textual/.test(r.txt),tag+' p5 certo à terceira');}
  await cap('6-conto-05-localizar-recusa');
  await juntos('p5-pensados','p5 passo 2, segunda busca');
  await tki('p5-pensados',[2]);await verif('p5-pensados');r=await ret('p5-pensados');ok(/pista/.test(r.cls)&&/não diz se ela é falada ou pensada/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 «não»: pista do erro cometido');
  if(estreito){await tki('p5-pensados',[2,6,7]);await verif('p5-pensados');r=await ret('p5-pensados');
    ok(/^SEGUNDA PISTA/i.test(r.txt)&&/particípio/.test(r.txt)&&!/pensados/.test(r.txt),tag+' p5 segunda pista sem a resposta '+r.txt);
    await tki('p5-pensados',[8]);await verif('p5-pensados');r=await ret('p5-pensados');ok(/certo/.test(r.cls)&&/terceira/i.test(r.txt)&&/Aceite com «mesmo só»/.test(r.txt),tag+' p5 certo à terceira (segunda busca)');}
  else{await tki('p5-pensados',[2,7,8]);await verif('p5-pensados');r=await ret('p5-pensados');
    ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/Aceite com «mesmo só»/.test(r.txt),tag+' p5 fronteira equivalente aceite (segunda busca) '+r.txt.slice(0,80));}
  ok(/segundo elemento textual/.test(r.txt)&&/lê o conto inteiro no manual/.test(r.txt),tag+' p5 a explicação manda ler o conto inteiro no manual');
  await cap('6-conto-06-fronteira-equivalente');
  // passo 3: o que o recorte diz, o que sugere e o que se lhe acrescenta; a explicação só aparece à terceira falha
  await passo(3);await juntos('p5-separar','p5 passo 3');
  await op('p5-separar',0);r=await ret('p5-separar');ok(/pista/.test(r.cls)&&/não precisas de inferir/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 separar pista 1 (o que o recorte já diz)');
  await op('p5-separar',1);r=await ret('p5-separar');ok(/pista/.test(r.cls)&&/^SEGUNDA PISTA/i.test(r.txt)&&/duas perguntas a cada afirmação/.test(r.txt)&&!/frontal/.test(r.txt),tag+' p5 separar segunda pista, sem a resposta');
  ok(!/certa/.test(await Q('p5-separar').locator('.op').nth(2).getAttribute('class')),tag+' p5 a resposta não aparece antes da terceira falha');
  await op('p5-separar',3);r=await ret('p5-separar');
  ok(/expl/.test(r.cls)&&/três tentativas/i.test(r.txt)&&/O recorte diz/.test(r.txt)&&/O recorte sugere/.test(r.txt)&&/Tu acrescentas/.test(r.txt)&&/O recorte contraria/.test(r.txt)&&/racionalidade, pois, apesar do intenso sofrimento/.test(r.txt),tag+' p5 explicação só à terceira falha: diz, sugere, acrescentas, contraria, com o tópico oficial '+r.txt.slice(0,60));
  ok(/certa/.test(await Q('p5-separar').locator('.op').nth(2).getAttribute('class')),tag+' p5 opção adequada marcada');
  await aVista(Q('p5-separar').locator('.retorno'),'p5 explicação');
  await cap('6-conto-07-diz-sugere-acrescentas');
  // passo 4: resposta insuficiente e resposta adequada; certo à segunda
  await passo(4);await juntos('p5-distinguir','p5 passo 4');
  ok(/Resposta A\./.test(await p.locator('#passo').innerText())&&/Resposta B\./.test(await p.locator('#passo').innerText()),tag+' p5 passo 4: as duas respostas à vista');
  await op('p5-distinguir',0);r=await ret('p5-distinguir');ok(/pista/.test(r.cls)&&/evidenciado no recorte/.test(r.txt)&&/mais duas tentativas/.test(r.txt),tag+' p5 distinguir pista 1');
  await op('p5-distinguir',1);r=await ret('p5-distinguir');
  ok(/certo/.test(r.cls)&&/segunda/i.test(r.txt)&&/começa por copiar/.test(r.txt)&&/dois dos tópicos seguintes, ou outros igualmente relevantes/.test(r.txt)&&/Infere um traço da personalidade de Manuel/.test(r.txt)&&/leitura nossa/.test(r.txt),tag+' p5 distinguir certo à segunda, com os critérios oficiais '+r.txt.slice(0,60));
  await aVista(Q('p5-distinguir').locator('.retorno'),'p5 explicação da resposta insuficiente');
  await cap('6-conto-08-insuficiente-ou-adequada');
  await passo(5);
  ok(await p.locator('#passos li:nth-child(6) button').isDisabled()&&await p.locator('#passos li:nth-child(7) button').isDisabled(),tag+' p5 passos 6 e 7 trancados antes de guardar');
  ok(await p.locator('.retorno:visible').count()===0&&/A tua resposta trata só do recorte/.test(await p.locator('#passo').innerText())&&!/Resposta B\./.test(await p.locator('#passo').innerText()),tag+' p5 sem pistas à vista no passo de escrita');
  ok(/guarda-se automaticamente/.test(await p.locator('.antes-bt').innerText()),tag+' p5 aviso sobre o rascunho antes do botão de guardar');
  await p.fill('#t-p5-resposta',V1);
  await cap('6-conto-09-escrever');
  await p.click('button:has-text("Guardar a primeira versão")');
  ok(await p.locator('.estado.ok').count()===1&&/Feita sem pistas à vista/.test(await p.locator('.estado.ok').innerText())&&/alterá-la em qualquer altura/.test(await p.locator('.estado.ok').innerText()),tag+' p5 primeira versão guardada');
  await aVista(p.locator('.estado.ok'),'p5 confirmação de guardar');
  await p.fill('#t-p5-resposta',V1+' '+LONGA);await semDeslize('p5 passo 5 com palavra muito longa');
  ok(await p.locator('.alt:visible').count()===0,tag+' p5 alterar antes de ver os critérios não deixa aviso');
  await passo(6);
  ok((await p.locator('#v1-p5-resposta').innerText()).includes('Primeira versão do aluno')&&await p.locator('.alt:visible').count()===0,tag+' p5 primeira versão à vista na conferência, sem aviso');
  await semDeslize('p5 passo 6 com palavra muito longa');
  { const t=await p.locator('#passo').innerText();
    ok(/Tópicos de resposta/.test(t)&&/O limite\./.test(t)&&/se o texto te mostrar outra coisa, vale o texto/.test(t)&&/igualdade de circunstâncias/.test(t)&&/ou outros igualmente relevantes/.test(t),tag+' p5 tópicos nossos e regra oficial das outras formulações');
    const l=await p.evaluate(()=>Array.from(document.querySelectorAll('#passo .caixa.nossa a')).map(x=>new URL(x.href).pathname).join(' '));
    ok(/Um exemplo comentado/.test(t)&&/Uma maneira de organizar \(é nossa, não é exigência do exame\)/.test(t)&&await p.locator('#passo .anot').count()===4&&l==='/pt/m8/m8-george-tres-idades/',tag+' p5 exemplo comentado e «Uma maneira de organizar» '+l);
    const rr=await p.request.get(new URL('/pt/m8/m8-george-tres-idades/',BASE).href);ok(rr.status()===200&&/Passagem, leitura, limite/.test(await rr.text()),tag+' p5 o exercício do M8 responde e tem o cartão citado');
    ok(await p.locator('#passo input[type=number]').count()===0&&await p.locator('#passo input[type=radio]').count()===0&&await p.locator('#passo .marca-l input[type=checkbox]').count()===9&&!/a tua classificação|pontos obtidos/i.test(t)&&/Não há classificação automática/.test(t),tag+' p5 sem classificação automática: só marcação aspeto a aspeto (9 aspetos)'); }
  await p.click('text=Alterar a primeira versão');
  await p.fill('#e-p5-resposta',V1+' Acrescento.');
  ok(/alterada depois de veres os critérios/.test(await p.locator('.alt:visible').innerText()),tag+' p5 aviso «alterada depois de veres os critérios» junto da versão');
  await aVista(p.locator('.alt'),'p5 aviso de alteração');
  await p.fill('#e-p5-resposta',V1+' '+LONGA);ok(await p.locator('.alt:visible').count()===0,tag+' p5 repor o texto retira o aviso');
  await p.fill('#e-p5-resposta',V1F);
  await p.click('text=Fechar a alteração');
  await p.locator('.marca-l input').nth(4).check();
  await cap('6-conto-10-conferir',true);
  await passo(7);
  ok(await p.inputValue('#r-p5-resposta')===V1F,tag+' p5 versão revista começa pela primeira');
  await semDeslize('p5 passo 7');
  await p.click('text=Guardar a versão revista');
  ok(/Ainda não mudaste nada/.test(await p.locator('.duas .estado').last().innerText())&&/Versão revista da resposta\s+Por fazer/.test(await reg()),tag+' p5 versão revista igual à primeira não é aceite');
  await p.fill('#r-p5-resposta','Versão revista do aluno: George é frontal, com «De idade não».');
  await p.click('text=Guardar a versão revista');
  ok(/Versão revista guardada neste dispositivo/.test(await p.locator('.duas .estado.ok').innerText()),tag+' p5 versão revista guardada');
  await p.reload();await p.waitForTimeout(150);
  ok(/Passo 7 de 7/i.test(await p.locator('.passo-n').innerText()),tag+' p5 volta ao passo onde ficou');
  ok((await p.locator('#v1-p5-resposta').innerText()).includes(V1)&&await p.inputValue('#r-p5-resposta')==='Versão revista do aluno: George é frontal, com «De idade não».',tag+' p5 duas versões guardadas depois de recarregar');
  { const g=await reg();
    ok(/manda fazer\s+Com pista, à terceira/.test(g)&&(estreito?/dizer a idade\s+Com pista, à segunda/.test(g)&&/não é dita\s+Com pista, à terceira/.test(g):/dizer a idade\s+Com pista, à terceira/.test(g)&&/não é dita\s+Com pista, à segunda/.test(g))&&/inferência com apoio\s+Com explicação/.test(g)&&/e porquê\s+Com pista, à segunda/.test(g),tag+' p5 registo distingue à segunda, à terceira e com explicação: '+g.replace(/\s+/g,' '));
    ok((estreito?/inferência sobre George\s+Alterada depois de veres os critérios/.test(g):/inferência sobre George\s+Por ti, sem pistas à vista/.test(g))&&/Versão revista da resposta\s+Depois de veres os critérios/.test(g)&&!/[Ss]ozinh/.test(await p.locator('body').innerText()),tag+' p5 registo das duas versões: '+g.replace(/\s+/g,' ').slice(-200)); }
  ok((await p.locator('.alt:visible').count())===(estreito?1:0),tag+' p5 aviso de alteração mantém-se depois de recarregar (só quando há alteração)');
  { const t=await p.locator('#passo').innerText();const l=await p.evaluate(()=>Array.from(document.querySelectorAll('#passo .caixa.nossa a')).map(x=>new URL(x.href).pathname).join(' '));
    ok(/Outra passagem/.test(t)&&l==='/pt/m8/licao-m8-f08/ /pt/m8/m8-george-tres-idades/'&&/a confirmar na Informação-Prova de 2027/.test(t),tag+' p5 outra passagem (lição M8-F08 e exercício do M8) e referência a 2027 '+l); }
  await semDeslize('p5 fim');await cap('6-conto-11-duas-versoes-e-registo',true);
  ok(await p.locator('#passos li button .fe:visible').count()===6,tag+' p5 os seis passos com resposta feita trazem a palavra «feito»');
  await passo(6);ok(await p.locator('.marca-l input').nth(4).isChecked(),tag+' p5 conferência guardada');
  await passo(3);r=await ret('p5-separar');ok(/expl/.test(r.cls),tag+' p5 estado das perguntas reposto');
  await p.goBack();await p.waitForTimeout(120);
  ok(/Passo 6 de 7/i.test(await p.locator('.passo-n').innerText())&&/\/conto\//.test(p.url()),tag+' p5 voltar atrás no navegador volta ao passo anterior');
  // item oficial: abre sem deslize, com o excerto da prova (36 linhas), o item, o critério e as duas tabelas
  await p.click('summary:has-text("Ver o item oficial")');await semDeslize('p5 item oficial aberto');
  { const t=await p.locator('details.dobra .dentro').innerText();
    ok(/Infira dois traços da personalidade de Manuel/.test(t)&&/Oh minha filha, minha filha!/.test(t)&&/imperscrutáveis – insondáveis/.test(t)&&/profunda religiosidade/.test(t)&&/abnegação\/altruísmo/.test(t)&&/Descritor de desempenho/.test(t)&&/Erros do tipo B/.test(t),tag+' p5 item oficial com o excerto, o item, o critério e as duas tabelas');
    ok(await p.locator('details.dobra .dentro ol.prosa li').count()===36&&await p.locator('details.dobra .dentro ol.prosa li b').count()===7,tag+' p5 o excerto da prova tem as 36 linhas, sete delas com o nome da personagem'); }
  // as únicas palavras de «George» na página são as do recorte: o resto do que se diz do conto vem como resumo das lições
  ok((await p.locator('#apoio-corpo').innerText()).split(RECORTE).length-1===1&&/resumo, não são frases do conto/.test(await p.locator('#apoio-corpo').innerText()),tag+' p5 o recorte e o resumo das lições, identificado como resumo');
  await p.locator('details.dobra').scrollIntoViewIfNeeded();await cap('6-conto-12-item-oficial',true);
  await p.click('#apoio-bt');ok(await p.locator('#apoio-corpo').isHidden()&&await p.getAttribute('#apoio-bt','aria-expanded')==='false',tag+' p5 texto de apoio recolhe');await p.click('#apoio-bt');
  ok(erros.length===0,tag+' p5 erros de JavaScript: '+erros.join(' | '));erros.length=0; }
  // 11/11/2026: nenhuma pergunta de escolha tem menos de quatro opções (três tentativas e duas pistas em todas, como diz a entrada)
  // 12/11/2026: também no treino da sessão 17
  // 12/11/2026: e no da sessão 18
  for(const pg of ['interpretacao','gramatica','escrita','poesia-contemporanea','conto']){
    await p.goto(BASE+pg+'/');
    const n=await p.evaluate(()=>{const d=JSON.parse(document.querySelector('script[type="application/json"]').textContent);const m=[];
      (function v(x){if(Array.isArray(x)){x.forEach(v);}else if(x&&typeof x==='object'){if(x.t==='escolha'){m.push([x.id,x.o.length,!!x.pista2]);}Object.keys(x).forEach(function(k){v(x[k]);});}})(d);return m;});
    ok(n.length>0&&n.every(x=>x[1]>=4&&x[2]),tag+' '+pg+': todas as escolhas com quatro opções ou mais e segunda pista '+JSON.stringify(n.filter(x=>!(x[1]>=4&&x[2]))));
  }
  // índice com estado
  await p.goto(BASE);ok(/primeira versão guardada; versão revista guardada/.test(await p.locator('[data-estado="escrita"]').innerText()),tag+' índice mostra o estado');
  // 12/11/2026: e o do treino da sessão 17
  ok(/primeira versão guardada; versão revista guardada/.test(await p.locator('[data-estado="poesia-contemporanea"]').innerText()),tag+' índice mostra o estado do treino 4: '+await p.locator('[data-estado="poesia-contemporanea"]').innerText());
  // 12/11/2026: e o do treino da sessão 18
  ok(/primeira versão guardada; versão revista guardada/.test(await p.locator('[data-estado="conto"]').innerText()),tag+' índice mostra o estado do treino 5: '+await p.locator('[data-estado="conto"]').innerText());
  await cap('0-indice-com-estado',true);
  // legenda coerente com as caixas
  ok(/os títulos e as frases de ligação são nossos/.test(await p.locator('.legenda').innerText())&&!/sem cortes/.test(await p.content()),tag+' legenda da etiqueta «Item oficial» ajustada');
  // 11/11/2026: depois de recomeçar, voltar atrás no navegador não deixa no endereço um passo que voltou a estar trancado
  await p.goto(BASE+'escrita/');await passo(6);
  ok(/#passo-6$/.test(p.url())&&/Passo 6 de 6/i.test(await p.locator('.passo-n').innerText()),tag+' p3 antes de recomeçar: passo 6 no endereço e na página');
  await p.click('#recomecar');await p.click('#recomecar');await p.waitForTimeout(120);
  ok(/Passo 1 de 6/i.test(await p.locator('.passo-n').innerText())&&/#passo-1$/.test(p.url())&&await p.locator('#passos li:nth-child(6) button').isDisabled(),tag+' p3 recomeçar volta ao passo 1 e tranca o passo 6');
  await p.goBack();await p.waitForTimeout(150);
  ok(/escrita\/#passo-1$/.test(p.url())&&/Passo 1 de 6/i.test(await p.locator('.passo-n').innerText()),tag+' p3 voltar atrás depois de recomeçar: endereço e página no passo 1 ('+p.url()+')');
  ok(await p.evaluate(()=>!!(history.state&&history.state.passo===0)),tag+' p3 voltar atrás depois de recomeçar: estado do histórico no passo 1');
  ok(erros.length===0,tag+' p3 recomeçar: erros de JavaScript: '+erros.join(' | '));erros.length=0;
  await c.close();

  /* ===== armazenamento indisponível ===== */
  const c2=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,colorScheme:cs});
  await c2.addInitScript(()=>{Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new Error('armazenamento bloqueado');}});});
  p=await c2.newPage();escuta(p);
  // 12/11/2026: também no treino da sessão 17
  // 12/11/2026: e no da sessão 18, que tem sete passos (escreve-se no 5.º e revê-se no 7.º)
  for(const [pil,npasso,cx,nrev] of [['interpretacao',4,'#t-p1-resposta',6],['escrita',4,'#t-p3-texto',6],['poesia-contemporanea',4,'#t-p4-resposta',6],['conto',5,'#t-p5-resposta',7]]){
    await p.goto(BASE+pil+'/');
    ok(await p.locator('#aviso-guarda').isVisible()&&/não deixa guardar/.test(await p.locator('#pe-guarda').innerText())&&!/localStorage/.test(await p.locator('#pe-guarda').innerText()),tag+' sem armazenamento ('+pil+'): aviso no cimo e rodapé verdadeiro');
    await passo(npasso);
    ok(/não deixa guardar/.test(await p.locator('.antes-bt').innerText()),tag+' sem armazenamento ('+pil+'): aviso repetido junto do botão');
    await p.fill(cx,'Texto escrito sem armazenamento.');
    await p.click('button:has-text("Guardar a primeira versão")');
    { const t=await p.locator('.estado.ok').innerText();
      ok(/só enquanto esta página estiver aberta/.test(t)&&/caderno/.test(t)&&!/guardada neste dispositivo/.test(t),tag+' sem armazenamento ('+pil+'): mensagem verdadeira ao guardar a primeira versão: '+t); }
    await aVista(p.locator('.estado.ok'),'sem armazenamento ('+pil+'): mensagem verdadeira');
    if(pil==='interpretacao')await cap('4-sem-armazenamento-primeira-versao');
    await passo(nrev);
    await p.fill('#r-'+cx.slice(3),'Texto revisto sem armazenamento.');await p.click('text=Guardar a versão revista');
    { const t=await p.locator('.duas .estado.ok').innerText();
      ok(/só enquanto esta página estiver aberta/.test(t)&&!/guardada neste dispositivo/.test(t),tag+' sem armazenamento ('+pil+'): mensagem verdadeira na versão revista: '+t); }
    ok(/não deixa guardar/.test(await p.locator('#passo').locator('p.ajuda').last().innerText())&&!/neste dispositivo/.test(await p.locator('#passo').innerText()),tag+' sem armazenamento ('+pil+'): nada na página diz «neste dispositivo»');
    await semDeslize('sem armazenamento '+pil);
  }
  await p.goto(BASE);
  ok(erros.length===0,tag+' sem armazenamento: erros de JavaScript: '+erros.join(' | '));
  await c2.close();
}
await b.close();server.close();
console.log('PASSARAM',passes,'FALHARAM',falhas.length);
if(falhas.length||!passes)process.exit(1);
})().catch(e=>{console.log('ERRO DO TESTE',e);process.exit(1);});
