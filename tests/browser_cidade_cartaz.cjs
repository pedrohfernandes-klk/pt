// 2026-11-08: cartaz «Ler a cidade» na entrada do Português (camada cidade_cartaz_20261108; pedido do utilizador: «quero que [Ler a
// cidade] tenha um banner em português»). O cartaz vem logo a seguir ao do Atlas, com as classes dele. A 320, 390, 768 e 1280 px
// (tema claro), a 390 e 1280 px no tema escuro e a 1280 px na projeção (/pt/projetar/?pagina=/pt/, a entrada dentro do quadro da
// projeção): a página não rola para o lado; cada número cabe no seu quadrado (scrollWidth ≤ clientWidth, e também na altura); o
// título não transborda (nem do h2 nem do cartaz) e a seta fica dentro do cartaz; as duas ligações têm 44 px de altura ou mais e
// cabem no cartaz; o cartaz tem o mesmo fundo, a mesma letra, a mesma margem e a mesma moldura que o do Atlas. Em cores forçadas, a
// 390 px, os números (decorativos) saem, como os do Atlas, e nada transborda. Sem erros na página.
// Corre com: node tests/browser_cidade_cartaz.cjs (CIDADE_CARTAZ_OUTPUT=<pasta> guarda capturas: os dois cartazes lado a lado).
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.CIDADE_CARTAZ_OUTPUT;if(out)fs.mkdirSync(out,{recursive:true});
const NUMEROS=['01','02','03','04','05','06','08','10','11','12','15','16','17','18'];
const LENTE='https://pedrohfernandes-klk.github.io/lente/cidade/';
const tipos={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://local').pathname.replace(/^\/pt\//,'/')),f=path.resolve(root,'.'+rel);if(!f.startsWith(root)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',tipos[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
// Só a origem local; o resto (o Lente publicado, tipos de letra de fora) não se carrega, para o teste não depender da rede.
async function contexto(b,origem,opcoes){const ctx=await b.newContext({deviceScaleFactor:1,...opcoes});await ctx.route('**/*',r=>new URL(r.request().url()).origin===origem?r.continue():r.abort());return ctx}
// Medidas dentro da página (ou do quadro da projeção).
function medir(){
 const c=document.querySelector('section.cidade-poster'),a=document.querySelector('section.atlas-poster:not(.cidade-poster)');
 const R=e=>{const r=e.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}};
 const cs=getComputedStyle,h2=c.querySelector('h2'),seta=h2.querySelector('span'),arte=c.querySelector('.cidade-poster-art');
 const estilo=e=>{const s=cs(e);return {fundo:s.backgroundColor,cor:s.color,borda:[s.borderTopWidth,s.borderTopColor,s.borderLeftWidth,s.borderLeftColor].join(' '),sombra:s.boxShadow,padding:s.padding,margem:[s.marginTop,s.marginBottom].join(' ')}};
 const letra=e=>{const s=cs(e);return [s.fontFamily,s.fontWeight,s.fontSize,s.lineHeight,s.letterSpacing].join(' ')};
 return {
  lado:document.documentElement.scrollWidth-document.documentElement.clientWidth,
  ordem:!!(a&&a.nextElementSibling&&a.compareDocumentPosition(c)&Node.DOCUMENT_POSITION_FOLLOWING)&&[...document.querySelectorAll('section.atlas-poster')].indexOf(c)===1,
  seguinte:(()=>{let e=c.nextElementSibling;return e?e.tagName.toLowerCase()+'.'+[...e.classList].join('.'):null})(),
  cartaz:R(c),atlas:a?R(a):null,
  numeros:[...arte.querySelectorAll('span')].map(s=>({t:s.textContent,sw:s.scrollWidth,cw:s.clientWidth,sh:s.scrollHeight,ch:s.clientHeight,visivel:s.getClientRects().length>0})),
  arteVisivel:arte.getClientRects().length>0,arte:arte.getClientRects().length?R(arte):null,colunas:cs(arte).gridTemplateColumns.split(' ').length,
  titulo:{sw:h2.scrollWidth,cw:h2.clientWidth,caixa:R(h2),seta:R(seta),texto:h2.innerText.replace(/\s+/g,' ').trim()},
  ligacoes:[...c.querySelectorAll('nav a')].map(e=>({t:e.textContent.replace(/\s+/g,' ').trim(),href:e.getAttribute('href'),...R(e)})),
  // (textContent: o pré-título vai em maiúsculas pela folha, mas o texto é o do HTML)
  texto:[...c.querySelectorAll('.atlas-poster-copy p')].map(p=>p.textContent.replace(/\s+/g,' ').trim()),
  estilo:estilo(c),estiloAtlas:a?estilo(a):null,
  letras:{h2:letra(h2),p:letra(c.querySelector('.atlas-poster-copy p:not(.portal-kicker)')),a:letra(c.querySelector('nav a')),kicker:letra(c.querySelector('.portal-kicker'))},
  letrasAtlas:a?{h2:letra(a.querySelector('h2')),p:letra(a.querySelector('.atlas-poster-copy p:not(.portal-kicker)')),a:letra(a.querySelector('nav a')),kicker:letra(a.querySelector('.portal-kicker'))}:null,
  setaCor:cs(seta).color,setaCorAtlas:a?cs(a.querySelector('h2 span')).color:null,
 };
}
function conferir(m,rot,{forcadas=false}={}){
 assert.ok(m.lado<=0,rot+': a página não rola para o lado ('+m.lado+' px)');
 assert.ok(m.ordem,rot+': o cartaz vem logo a seguir ao do Atlas');assert.equal(m.seguinte,'nav.site-portal-wrap',rot+': e logo antes do portal do Lente');
 assert.ok(m.cartaz.x>=-.5&&m.cartaz.r<=m.atlas.r+.5,rot+': o cartaz cabe na coluna, como o do Atlas');
 assert.equal(Math.round(m.cartaz.w),Math.round(m.atlas.w),rot+': a mesma largura do cartaz do Atlas');
 assert.deepEqual(m.texto,['Português × Cidadania','Uma rua pode ser lida como um texto e discutida como um espaço de todos. São 14 missões, no bairro ou a partir das fotografias.'],rot+': o texto');
 assert.match(m.titulo.texto,/^Ler a cidade ?↗$/,rot+': o título');
 assert.ok(m.titulo.sw<=m.titulo.cw,rot+': o título não transborda do h2 ('+m.titulo.sw+' > '+m.titulo.cw+')');
 assert.ok(m.titulo.caixa.r<=m.cartaz.r+.5&&m.titulo.seta.r<=m.cartaz.r+.5&&m.titulo.seta.x>=m.cartaz.x-.5,rot+': o título e a seta dentro do cartaz');
 assert.deepEqual(m.ligacoes.map(l=>[l.t,l.href]),[['Entrar na cidade →',LENTE],['Ver as missões →',LENTE+'#m01']],rot+': as ligações');
 for(const l of m.ligacoes){assert.ok(l.h>=44,rot+': «'+l.t+'» com 44 px de altura ou mais ('+l.h+')');assert.ok(l.x>=m.cartaz.x-.5&&l.r<=m.cartaz.r+.5,rot+': «'+l.t+'» dentro do cartaz');}
 assert.deepEqual(m.numeros.map(n=>n.t),NUMEROS,rot+': os 14 números, pela ordem');
 if(forcadas){assert.equal(m.arteVisivel,false,rot+': em cores forçadas, os números (decorativos) saem, como os do Atlas');return}
 assert.ok(m.arteVisivel,rot+': os números à vista');
 assert.ok(m.arte.x>=m.cartaz.x-.5&&m.arte.r<=m.cartaz.r+.5,rot+': os números dentro do cartaz');
 for(const n of m.numeros){assert.ok(n.visivel,rot+': '+n.t+' à vista');assert.ok(n.sw<=n.cw,rot+': '+n.t+' cabe na largura do quadrado ('+n.sw+' > '+n.cw+')');assert.ok(n.sh<=n.ch,rot+': '+n.t+' cabe na altura do quadrado ('+n.sh+' > '+n.ch+')');}
 // Igual ao cartaz do Atlas: o fundo, a cor, a moldura, a sombra, o espaço por dentro e por fora, e a letra de cada parte.
 assert.deepEqual(m.estilo,m.estiloAtlas,rot+': o mesmo aspeto do cartaz do Atlas');
 assert.deepEqual(m.letras,m.letrasAtlas,rot+': a mesma letra do cartaz do Atlas');assert.equal(m.setaCor,m.setaCorAtlas,rot+': a seta da mesma cor');
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});const feitos=[];
 const capturas=[];
 try{
  const CENARIOS=[...[320,390,768,1280].map(width=>({width,tema:'light'})),{width:390,tema:'dark'},{width:1280,tema:'dark'}];
  for(const {width,tema} of CENARIOS){
   const ctx=await contexto(browser,origin,{viewport:{width,height:900},colorScheme:tema,reducedMotion:'reduce'}),page=await ctx.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/pt/',{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.evaluate(()=>document.documentElement.getAttribute('data-theme')),tema,width+': o tema '+tema+' ligado (assets/appearance.js)');
   const rot=`${width} px, ${tema}`;conferir(await page.evaluate(medir),rot);
   // (cada cartaz ao centro do ecrã, longe dos botões flutuantes da ajuda e do modo noturno, que ficam nos cantos de baixo)
   if(out&&(width===390||width===1280)){
    for(const sel of ['section.atlas-poster:not(.cidade-poster)','section.cidade-poster']){const el=page.locator(sel);await el.evaluate(e=>e.scrollIntoView({block:'center'}));capturas.push({width,tema,sel,png:(await el.screenshot()).toString('base64')});}
   }
   assert.deepEqual(errors,[],rot+': sem erros na página');await ctx.close();feitos.push(rot);
  }
  // Projeção: a entrada no quadro da projeção, a 1280 px.
  {const width=1280,ctx=await contexto(browser,origin,{viewport:{width,height:900},reducedMotion:'reduce'}),page=await ctx.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/pt/projetar/?pagina=/pt/',{waitUntil:'load'});
   await page.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
   if(await page.locator('#qr-toggle').getAttribute('aria-expanded')==='true')await page.locator('#qr-toggle').click();
   const frame=await (await page.locator('#lesson-frame').elementHandle()).contentFrame();
   await frame.waitForFunction(()=>[...document.styleSheets].some(s=>s.href&&s.href.includes('projection-frame.css')));
   await frame.evaluate(()=>document.fonts.ready);await frame.locator('section.cidade-poster').scrollIntoViewIfNeeded();
   const rot=`${width} px, projeção`;conferir(await frame.evaluate(medir),rot);
   if(out)await page.locator('#lesson-frame').screenshot({path:path.join(out,'projecao-1280.png')});
   assert.deepEqual(errors,[],rot+': sem erros na página');await ctx.close();feitos.push(rot);}
  // Cores forçadas, a 390 px.
  {const width=390,ctx=await contexto(browser,origin,{viewport:{width,height:900},forcedColors:'active',reducedMotion:'reduce'}),page=await ctx.newPage();
   await page.goto(origin+'/pt/',{waitUntil:'load'});const rot=`${width} px, cores forçadas`;conferir(await page.evaluate(medir),rot,{forcadas:true});await ctx.close();feitos.push(rot);}
  // Capturas: o cartaz do Atlas e o novo lado a lado, a 390 e a 1280 px, no tema claro e no escuro.
  if(out)for(const width of [390,1280])for(const tema of ['light','dark']){
   const [atlas,cidade]=['section.atlas-poster:not(.cidade-poster)','section.cidade-poster'].map(sel=>capturas.find(c=>c.width===width&&c.tema===tema&&c.sel===sel).png);
   const ctx=await browser.newContext({viewport:{width:width*2+72,height:400},deviceScaleFactor:1}),page=await ctx.newPage();
   await page.setContent(`<body style="margin:0;padding:24px;background:${tema==='dark'?'#111':'#fff'};display:flex;gap:24px;align-items:flex-start"><img src="data:image/png;base64,${atlas}"><img src="data:image/png;base64,${cidade}"></body>`);
   await page.screenshot({path:path.join(out,`atlas-e-cidade-${width}-${tema}.png`),fullPage:true});await ctx.close();
  }
  console.log(`Cartaz «Ler a cidade»: ${feitos.length} cenários (${feitos.join('; ')}), sem deslize horizontal, números nos quadrados, título sem transbordo, ligações com 44 px.`);
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
