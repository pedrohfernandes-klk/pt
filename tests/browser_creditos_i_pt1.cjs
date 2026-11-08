// 07/11/2026: decisões 153, 176 e 177 (pedido pt-1 do plano plano-creditos-i-20261105.md, famílias P1 a P4). Cada «i» novo da
// entrada (fundo da calçada e fotografia de Muybridge no portal do Lente), da imagem documental dos nove índices e do mapa do Atlas
// abre por teclado (Tab chega lá, Enter e Espaço abrem, Escape fecha e devolve o foco) e por toque, a 390 e a 1366 px, no tema claro
// e no escuro; o crédito aberto é o de antes, palavra a palavra e com as mesmas ligações (no M8, mais a ligação da licença); nada
// tapa o crédito nem o crédito tapa texto, a página não rola para o lado, e o texto aberto tem 4,5:1 contra o fundo. Na projeção
// (?projetar=1) fica tudo fechado, com alvo de 44 px e sem transbordo, e o botão do fundo escondido. Na impressão, o «i» não sai e o
// crédito sai por extenso sempre que sai a imagem a que pertence (a ligação da licença com o endereço). Com o desenho a andar, o
// botão do fundo está à vista, fora do «i», diz «Parar a animação», para o desenho e passa a «Retomar a animação», e retoma-o
// (decisão 177). O «antes» de cada crédito sai da própria página com a camada creditos_i_pt1_20261107 desfeita pelo manifesto.
// Corre com: node tests/browser_creditos_i_pt1.cjs (CREDITOS_I_PT1_OUTPUT=<pasta> guarda capturas).
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.CREDITOS_I_PT1_OUTPUT;if(out)fs.mkdirSync(out,{recursive:true});
const manifesto=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/creditos-i-pt1-edits-20261107.json'),'utf8')).files;
// A página sem esta camada (desfeita da última troca para a primeira, com contagem estrita).
function antes(rel){let t=fs.readFileSync(path.join(root,rel),'utf8');for(const e of [...manifesto[rel].edits].reverse()){assert.equal(t.split(e.new).length-1,e.occurrences,rel+' '+e.location);t=t.split(e.new).join(e.old)}return t}
const um=(s,re)=>{const m=s.match(re);assert.ok(m,String(re));return m[1]};
const LICENCA_M8='https://creativecommons.org/licenses/by-sa/2.0/deed.pt';
// Para cada página: os «i» novos, pela ordem da página, com o crédito antigo (HTML), o nome, as ligações a mais e a imagem.
const PAGINAS=[
 {p:'',rel:'index.html',is:(()=>{const s=antes('index.html');return [
  {html:um(s,/<p class="cf-credito">(.*?) <button /),nome:'Créditos do desenho',visual:'.cf-mar'},
  // O crédito do portal: os «·» passam a pontos finais (nunca «·» dentro de frases); as palavras e a ligação são as mesmas.
  // 08/11/2026: decisão 162: o nome de Muybridge sai do rótulo e entra no crédito, antes das palavras de antes.
  {html:'Eadweard Muybridge · '+um(s,/<p class="sp-credit">(Estudo do movimento.*?)<\/p>/),nome:'Créditos da fotografia',visual:'.sp-image img',soPalavras:true}]})()},
 ...[1,2,3,4,5,6,7,8,9].map(n=>({p:`m${n}/`,rel:`m${n}/index.html`,is:[{html:um(antes(`m${n}/index.html`),/<figcaption class="cz-credit">(.*?)<\/figcaption><\/figure>/),
  nome:'Créditos da imagem',visual:'main>figure.doc img',mais:n===8?[LICENCA_M8]:[]}]})),
 {p:'atlas/',rel:'atlas/index.html',is:[{html:um(antes('atlas/index.html'),/<p class="credito">(.*?)<\/p>/),nome:'Créditos do mapa',visual:'svg.mundo-c'}]},
];
const tipos={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://local').pathname.replace(/^\/pt\//,'/')),f=path.resolve(root,'.'+rel);if(!f.startsWith(root)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',tipos[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
const PUBLICADO='https://pedrohfernandes-klk.github.io';
async function contexto(b,origem,opcoes){const ctx=await b.newContext(opcoes);await ctx.route('**/*',r=>{const u=new URL(r.request().url());
 if(u.origin===PUBLICADO&&u.pathname.startsWith('/pt/')){const f=path.resolve(root,'.'+decodeURIComponent(u.pathname.slice(3)));return f.startsWith(root)&&fs.existsSync(f)&&fs.statSync(f).isFile()?r.fulfill({path:f}):r.abort()}
 return u.origin===origem?r.continue():r.abort()});return ctx}
// Medidas dentro da página: o «i» n, aberto ou fechado.
function medir([n,htmlAntigo]){
 const d=document.querySelectorAll('details.info-i[name="info-i"]')[n],s=d.querySelector(':scope>summary'),t=d.querySelector(':scope>.info-i-texto');
 const norm=x=>x.replace(/\s+/g,' ').trim(),palavras=x=>x.toLowerCase().replace(/[^\p{L}\p{N}©↗]+/gu,' ').trim(),tpl=document.createElement('template');tpl.innerHTML=htmlAntigo;
 // (checkVisibility: o conteúdo de um «i» fechado não se vê)
 const visivel=e=>e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true,opacityProperty:true});
 // texto à vista fora deste «i» (sem o que é decorativo)
 const fora=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const el=no.parentElement;if(!el||!no.data.trim()||d.contains(el)||el.closest('[aria-hidden="true"],script,style,.vh,.sr-only,.salta')||!visivel(el))continue;const r=document.createRange();r.selectNodeContents(no);for(const q of r.getClientRects())if(q.width>1&&q.height>1)fora.push({x:q.left,y:q.top,r:q.right,b:q.bottom,t:no.data.trim().slice(0,40)});}
 const cruza=(a,b)=>a.left<b.r-1&&a.right>b.x+1&&a.top<b.b-1&&a.bottom>b.y+1;
 const circ=s.querySelector('span').getBoundingClientRect(),sp=getComputedStyle(s.querySelector('span'));
 const cor=c=>c.match(/[\d.]+/g).slice(0,4).map(Number),lum=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])},contraste=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const fundo=e=>{for(let x=e;x;x=x.parentElement){const c=cor(getComputedStyle(x).backgroundColor);if(c.length<4||c[3]>0)return c}return [255,255,255]};
 const out={open:d.open,summary:visivel(s),alvo:[s.getBoundingClientRect().width,s.getBoundingClientRect().height],nome:s.getAttribute('aria-label'),tabIndex:s.tabIndex,
  dentroLigacao:!!d.parentElement.closest('a,button,label,figcaption,[aria-hidden="true"]'),
  texto:norm(t.textContent),esperado:norm(tpl.content.textContent),palavras:palavras(t.textContent),palavrasAntes:palavras(tpl.content.textContent),
  ligacoes:[...t.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),ligacoesAntes:[...tpl.content.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),
  lado:document.documentElement.scrollWidth-innerWidth,circuloTapa:s.getClientRects().length?fora.filter(b=>cruza(circ,b)).map(b=>b.t):[],
  circulo:contraste(cor(sp.borderTopColor),cor((sp.boxShadow.match(/rgba?\([^)]*\)/)||[sp.backgroundColor])[0])),
  foco:document.activeElement===s?Math.max(parseFloat(getComputedStyle(s).outlineWidth)||0,/inset/.test(getComputedStyle(s).boxShadow)?2:0):null};
 if(d.open){out.textoVisivel=visivel(t);const r=t.getBoundingClientRect();
  const linhas=[];const w2=document.createTreeWalker(t,NodeFilter.SHOW_TEXT);let m;while(m=w2.nextNode()){if(!m.data.trim())continue;const rr=document.createRange();rr.selectNodeContents(m);for(const q of rr.getClientRects())if(q.width>2)linhas.push(q);}
  // nenhuma linha do crédito aberto cruza texto de fora do «i», e nada fica por cima dele
  out.textoTapa=[...new Set(linhas.flatMap(q=>fora.filter(b=>cruza(q,b)).map(b=>b.t)))];
  out.tapado=linhas.filter(q=>{const x=q.left+Math.min(q.width/2,8),y=q.top+q.height/2;if(y<r.top||y>r.bottom||y<0||y>innerHeight)return false;const e=document.elementFromPoint(x,y);return !e||!(t.contains(e)||e===t);}).length;
  // (o alvo de 44 px das ligações da casa «Cartaz», um ::before que sai 15 px acima e abaixo, conta no scrollHeight; com overflow
  // visible nada se corta, e o que pudesse sair por cima de outro texto conta em textoTapa)
  out.foraDoEcra=r.left<-1||r.right>innerWidth+1;out.rola=t.scrollHeight>t.clientHeight+1?getComputedStyle(t).overflowY:'nao';
  out.contrasteTexto=contraste(cor(getComputedStyle(t).color),fundo(t));out.linhas=linhas.length;}
 return out;}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0,cenarios=0;
 try{for(const width of [390,1366])for(const tema of ['light','dark']){
  const ctx=await contexto(browser,origin,{viewport:{width,height:900},hasTouch:true,colorScheme:tema,reducedMotion:'reduce'});
  for(const pg of PAGINAS){
   const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/pt/'+pg.p,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
   const sel='details.info-i[name="info-i"]',todos=page.locator(sel);
   assert.equal(await todos.count(),pg.is.length,pg.p+': número de «i»');
   for(const [k,info] of pg.is.entries()){
    const rot=`${width} px, ${tema}, /pt/${pg.p} «i» ${k+1}`,d=todos.nth(k),s=d.locator(':scope>summary');
    await s.scrollIntoViewIfNeeded();
    let m=await page.evaluate(medir,[k,info.html]);
    assert.equal(m.open,false,rot+': fechado ao carregar');assert.ok(m.summary,rot+': «i» à vista');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');
    assert.equal(m.nome,info.nome,rot+': nome do «i»');assert.equal(m.tabIndex,0,rot);assert.equal(m.dentroLigacao,false,rot+': fora de ligação, legenda ou parte decorativa');
    if(info.soPalavras)assert.equal(m.palavras,m.palavrasAntes,rot+': crédito completo, palavra a palavra');else assert.equal(m.texto,m.esperado,rot+': crédito completo, letra a letra');
    assert.deepEqual(m.ligacoes,[...m.ligacoesAntes,...(info.mais||[])],rot+': as mesmas ligações');
    assert.deepEqual(m.circuloTapa,[],rot+': o «i» fechado não tapa texto');assert.ok(m.lado<=0,rot+': sem deslocamento para o lado');assert.ok(m.circulo>=3,rot+': 3:1 do círculo ('+m.circulo.toFixed(2)+')');
    // teclado: Tab chega ao «i» (vindo do elemento anterior), com contorno de foco; Enter abre, Escape fecha e devolve o foco, Espaço abre
    await s.focus();await page.keyboard.press('Shift+Tab');await page.keyboard.press('Tab');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': Tab chega ao «i»');
    m=await page.evaluate(medir,[k,info.html]);assert.ok(m.foco>=2,rot+': contorno de foco de 2 px ou mais');
    await page.keyboard.press('Enter');m=await page.evaluate(medir,[k,info.html]);
    assert.ok(m.open&&m.textoVisivel,rot+': Enter abre');assert.deepEqual(m.textoTapa,[],rot+': o crédito aberto não tapa texto');assert.equal(m.tapado,0,rot+': nada tapa o crédito');
    assert.equal(m.foraDoEcra,false,rot+': crédito dentro do ecrã');assert.ok(['nao','auto','visible'].includes(m.rola),rot+': crédito inteiro (sem nada cortado) ou a rolar por dentro');assert.ok(m.lado<=0,rot+': aberto, sem deslocamento para o lado');
    assert.ok(m.contrasteTexto>=4.5,rot+': 4,5:1 do texto aberto ('+m.contrasteTexto.toFixed(2)+')');
    if(out&&k===0)await page.screenshot({path:path.join(out,`${(pg.p||'entrada').replace(/\//g,'')}-${width}-${tema}-aberto.png`)});
    await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
    await page.keyboard.press(' ');assert.equal(await d.evaluate(e=>e.open),true,rot+': Espaço abre');await page.keyboard.press('Escape');
    // toque: abre e fecha
    await s.tap();m=await page.evaluate(medir,[k,info.html]);assert.ok(m.open&&m.textoVisivel,rot+': toque abre');assert.deepEqual(m.textoTapa,[],rot+': aberto ao toque, não tapa texto');assert.equal(m.tapado,0,rot);assert.ok(m.lado<=0,rot);
    await s.tap();assert.equal(await d.evaluate(e=>e.open),false,rot+': toque fecha');n++;
   }
   if(pg.rel==='index.html'){
    // um só aberto de cada vez; um clique fora fecha; o botão de parar fica fora do «i»
    await todos.nth(0).locator('summary').click();await todos.nth(1).locator('summary').click();
    assert.equal((await todos.evaluateAll(es=>es.map(e=>e.open))).filter(Boolean).length,1,width+': um só «i» aberto');
    await page.mouse.click(2,2);assert.equal(await page.locator('details.info-i[open]').count(),0,width+': clique fora fecha');
    assert.equal(await page.locator('[data-fundo-botao="cf"]').evaluate(e=>!!e.closest('details')),false,'botão fora do «i»');
   }
   // impressão: o «i» não sai; o crédito sai por extenso sempre que sai a imagem a que pertence; a licença leva o endereço
   await page.emulateMedia({media:'print'});
   const imp=await page.evaluate(vis=>{const ds=[...document.querySelectorAll('details.info-i[name="info-i"]')];const v=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
    return {lado:document.documentElement.scrollWidth-innerWidth,is:ds.map((d,i)=>({texto:v(d.querySelector('.info-i-texto')),inteiro:getComputedStyle(d.querySelector('.info-i-texto')).overflowY==='visible'||d.querySelector('.info-i-texto').scrollHeight<=d.querySelector('.info-i-texto').clientHeight+1,i:v(d.querySelector('summary')),imagem:v(document.querySelector(vis[i])),
     licenca:[...d.querySelectorAll('a[rel~=license]')].map(a=>getComputedStyle(a,'::after').content)}))};},pg.is.map(x=>x.visual));
   imp.is.forEach((x,i)=>{const rot=`${width} px, ${tema}, /pt/${pg.p} «i» ${i+1}, impressão`;assert.equal(x.i,false,rot+': sem o botão «i»');assert.equal(x.texto,x.imagem,rot+': o crédito acompanha a imagem');
    if(x.texto)assert.ok(x.inteiro,rot+': por extenso');for(const c of x.licenca)assert.ok(c.includes('creativecommons.org/licenses/'),rot+': a licença com o endereço');});
   if(pg.rel==='m8/index.html')assert.equal(imp.is[0].licenca.length,1,'M8: a ligação da licença na impressão');
   if(pg.rel!=='index.html')assert.ok(imp.is.every(x=>x.texto),pg.p+': na impressão, o crédito sai com a imagem');
   assert.ok(imp.lado<=0,pg.p+': impressão sem corte horizontal');
   if(out&&tema==='light'&&width===1366)await page.pdf({path:path.join(out,`${(pg.p||'entrada').replace(/\//g,'')}-impressao.pdf`),format:'A4',printBackground:true});
   await page.emulateMedia({media:'screen'});assert.deepEqual(errors,[]);await page.close();cenarios++;
  }
  await ctx.close();
 }
 // Projeção (?projetar=1): tudo fechado, alvo de 44 px, sem transbordo; o botão do fundo escondido; abre e cabe no ecrã.
 for(const width of [390,1366]){
  const ctx=await contexto(browser,origin,{viewport:{width,height:900},hasTouch:true,reducedMotion:'no-preference'});
  for(const pg of PAGINAS){
   const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/pt/'+pg.p+'?projetar=1',{waitUntil:'load'});
   const ds=page.locator('details.info-i[name="info-i"]');
   for(let k=0;k<pg.is.length;k++){const rot=`projeção ${width} px, /pt/${pg.p} «i» ${k+1}`,s=ds.nth(k).locator(':scope>summary');await s.scrollIntoViewIfNeeded();
    let m=await page.evaluate(medir,[k,pg.is[k].html]);assert.equal(m.open,false,rot+': fechado');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');assert.ok(m.lado<=0,rot+': sem transbordo');
    // (com movimento, o crédito aparece em 160 ms, a partir da opacidade 0: mede-se depois)
    await s.click();await page.waitForTimeout(300);m=await page.evaluate(medir,[k,pg.is[k].html]);assert.ok(m.open&&m.textoVisivel,rot+': abre');assert.equal(m.foraDoEcra,false,rot);assert.ok(m.lado<=0,rot);assert.equal(m.tapado,0,rot);await s.click();}
   if(pg.rel==='index.html')assert.equal(await page.locator('[data-fundo-botao="cf"]').isVisible(),false,'projeção: o botão do fundo escondido');
   assert.deepEqual(errors,[]);await page.close();cenarios++;
  }
  await ctx.close();
 }
 // Decisão 177: com o desenho a andar, o botão do fundo à vista, fora do «i», com o texto novo; para e retoma o desenho; com o «i»
 // aberto, continua à vista e livre.
 for(const width of [390,1366]){
  const ctx=await contexto(browser,origin,{viewport:{width,height:900},reducedMotion:'no-preference'}),page=await ctx.newPage();
  await page.goto(origin+'/pt/',{waitUntil:'load'});const b=page.locator('[data-fundo-botao="cf"]'),fundo=page.locator('[data-fundo="cf"]');
  await b.waitFor({state:'visible'});assert.equal(await b.evaluate(e=>!!e.closest('details.info-i')),false,'botão fora do «i»');
  assert.equal(await b.innerText(),'Parar a animação');assert.ok(await fundo.evaluate(e=>e.classList.contains('cf-anda')),width+': o desenho anda');
  await b.click();assert.equal(await b.innerText(),'Retomar a animação',width+': parado, «Retomar a animação»');assert.equal(await fundo.evaluate(e=>e.classList.contains('cf-anda')),false,width+': o desenho para');
  await b.click();assert.equal(await b.innerText(),'Parar a animação',width+': retoma');assert.ok(await fundo.evaluate(e=>e.classList.contains('cf-anda')),width+': o desenho retoma');
  await page.locator('details.info-i').first().locator('summary').click();
  assert.ok(await b.evaluate(e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2));}),width+': botão à vista e livre com o «i» aberto');
  const altura=await page.locator('.fundo-acoes').evaluate(e=>{e.querySelector('details').open=false;return e.getBoundingClientRect().height});assert.ok(altura<=48.5,width+': a linha fechada do fundo tem 48 px ou menos ('+altura+')');
  if(out)await page.screenshot({path:path.join(out,`entrada-botao-${width}.png`)});
  await ctx.close();cenarios++;
 }
 // 08/11/2026 (revisão do pt-1): no Atlas, a 320 e a 390 px, o nome de um país comprido não tapa o «© OpenStreetMap», que fica
 // sempre à vista (ODbL); o nome é posto como o mapa o põe (no p.mapa-nome) e mede-se a sobreposição das duas caixas.
 for(const width of [320,390]){const ctx=await browser.newContext({viewport:{width,height:800}});const page=await ctx.newPage();
  await page.goto(origin+'/pt/atlas/',{waitUntil:'load'});
  for(const nome of ['São Tomé e Príncipe','Guiné-Bissau']){
   const sobre=await page.evaluate(n=>{const e=document.querySelector('.mapa-nome');e.textContent=n;const a=e.getBoundingClientRect(),b=document.querySelector('.mapa-osm').getBoundingClientRect();return a.width>0&&b.width>0&&!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top)},nome);
   assert.equal(sobre,false,width+': «'+nome+'» não tapa o «© OpenStreetMap»');}
  await ctx.close();cenarios++;}
 console.log(`Créditos atrás do «i» (pt-1): ${n} «i» abertos por teclado e por toque, a 390 e 1366 px, nos dois temas, sem tapar texto, sem deslocamento, com impressão; ${cenarios} cenários com projeção e o botão do fundo.`);
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
