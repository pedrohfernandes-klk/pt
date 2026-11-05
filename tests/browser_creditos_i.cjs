// 05/11/2026: decisões 153 e 162. Créditos atrás de um botão «i», no navegador (plano-creditos-i-20261105.md, secção 3.3).
// O papel na árvore é DisclosureTriangle (DisclosureTriangleGrouped no Chromium 141, por causa do name="info-i").
// Sobre a página de ensaio tests/fixtures/info-i.html (canto, linha, imagem pequena, imagem dentro de ligação, dentro de um
// cartão, documento visual com tabela de identificação e a linha de um fundo animado) e uma amostra real por família feita: lição M1 (canto e
// linha), lição M4 e um documento visual (pedido pt-2, fatia 1: P7 e P9). Confere, a 320, 390, 852 e 1366 px e nos dois
// temas: fechado ao carregar; alvo de 44 × 44 px ou mais, no canto da imagem («canto») ou logo por baixo dela («linha");
// aberto, sem deslocamento horizontal e com o crédito dentro do ecrã; teclado (Tab chega ao «i», contorno de 2 px ou mais,
// Enter abre, Escape fecha e devolve o foco); a árvore de acessibilidade (DisclosureTriangle, nome, expanded); 3:1 do círculo e
// 4,5:1 do texto aberto; projeção; impressão (o crédito por extenso, sem o «i», com o endereço da licença); sem JavaScript; e
// «Parar o desenho» sempre fora do «i». Corre com: node tests/browser_creditos_i.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright'),root=path.resolve(__dirname,'..');
const tipos={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://local').pathname.replace(/^\/pt\//,'/')),f=path.resolve(root,'.'+rel);if(!f.startsWith(root)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',tipos[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
const ENSAIO='/pt/tests/fixtures/info-i.html';
// Amostras reais: o «i» do primeiro cartão (o «Abre») de cada lição.
const AMOSTRAS=[
 {url:'/pt/m1/licao-m1-f01/',variante:'canto',familia:'P7'},
 {url:'/pt/m1/licao-m1-f05/',variante:'linha',familia:'P7'},
 {url:'/pt/m4/licao-m4-f01/',variante:'canto',familia:'P7'},
 {url:'/pt/m3/licao-m3-f19/',variante:'linha',familia:'P9'},
];
const LARGURAS=[320,390,852,1366];
function lum(c){const m=c.match(/[\d.]+/g).map(Number),f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])}
function contraste(a,b){const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
// O «i», a imagem que ele acompanha e as caixas de cada um.
const MEDIR=(sel)=>{const d=document.querySelectorAll('details.info-i')[sel];if(!d)return null;const s=d.querySelector(':scope>summary'),t=d.querySelector(':scope>.info-i-texto');
 const casa=d.closest('.com-i')||d.parentElement,img=casa.querySelector('img')||(d.closest('figure')&&d.closest('figure').querySelector('img'));
 const caixa=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}};
 const sp=getComputedStyle(s.querySelector('span')),tt=getComputedStyle(t);
 return {open:d.open,linha:d.classList.contains('info-i--linha'),s:caixa(s),img:caixa(img),t:caixa(t),tVisivel:t.checkVisibility(),sVisivel:s.checkVisibility(),
  borda:sp.borderTopColor,halo:(sp.boxShadow.match(/rgba?\([^)]*\)/)||[sp.backgroundColor])[0],fundoCirculo:sp.backgroundColor,cor:tt.color,fundo:tt.backgroundColor,
  rolagem:document.documentElement.scrollWidth>innerWidth+1,vw:innerWidth,
  justificado:[t,...t.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return c.textAlign==='justify'||c.hyphens==='auto'}).map(e=>e.tagName)}};
async function contexto(b,origem,opcoes){const ctx=await b.newContext({reducedMotion:'reduce',...opcoes});await ctx.route('**/*',r=>{const u=new URL(r.request().url());return u.origin===origem?r.continue():r.abort()});return ctx}
async function arvore(p){const s=await p.context().newCDPSession(p);const {nodes}=await s.send('Accessibility.getFullAXTree');await s.detach();
 return nodes.filter(n=>n.name&&/^(Créditos|Fonte)/.test(n.name.value||'')).map(n=>({papel:n.role&&n.role.value,nome:n.name.value,expanded:((n.properties||[]).find(x=>x.name==='expanded')||{value:{}}).value.value}))}
function conferirCaixas(m,onde){
 assert(m.s.w>=44-1/64&&m.s.h>=44-1/64,`${onde}: alvo de 44 × 44 px (${m.s.w} × ${m.s.h})`);
 if(!m.img)return; // a linha de um fundo animado não tem imagem ao lado
 if(m.linha){assert(m.s.y>=m.img.b-1,`${onde}: «linha» por baixo da imagem`);assert(Math.abs(m.s.r-m.img.r)<=1.5||m.s.r<=m.img.r+1,`${onde}: «linha» alinhado à direita da imagem (${m.s.r} / ${m.img.r})`)}
 else{assert(m.s.x>=m.img.x-.5&&m.s.r<=m.img.r+.5&&m.s.y>=m.img.y-.5&&m.s.b<=m.img.b+.5,`${onde}: «canto» dentro da caixa da imagem`);assert(m.img.r-m.s.r<=8.5&&m.img.b-m.s.b<=8.5,`${onde}: a 8 px do canto`)}
}
function conferirAberto(m,onde){
 assert(m.open&&m.tVisivel,`${onde}: aberto, o crédito vê-se`);assert(!m.rolagem,`${onde}: sem deslocamento horizontal`);
 assert(m.t.x>=-.5&&m.t.r<=m.vw+.5,`${onde}: o crédito dentro do ecrã (${m.t.x}..${m.t.r} / ${m.vw})`);
 if(!m.linha&&m.img)assert(m.t.x>=m.img.x-.5&&m.t.r<=m.img.r+.5&&m.t.y>=m.img.y-.5&&m.t.b<=m.img.b+.5,`${onde}: «canto», o crédito por cima da imagem`);
 assert.deepEqual(m.justificado,[],`${onde}: o crédito nunca se justifica nem se hifeniza (decisão 140)`);
 assert(contraste(m.cor,m.fundo==='rgba(0, 0, 0, 0)'?m.fundoPagina:m.fundo)>=4.5,`${onde}: 4,5:1 do texto aberto (${m.cor} / ${m.fundo})`);
}
async function abrirPorTeclado(p,indice,onde){
 // Tab chega ao «i» (sem saltar nada à frente dele que seja do próprio «i»).
 for(let k=0;k<60;k++){await p.keyboard.press('Tab');if(await p.evaluate(i=>document.activeElement===document.querySelectorAll('details.info-i>summary')[i],indice))break}
 assert(await p.evaluate(i=>document.activeElement===document.querySelectorAll('details.info-i>summary')[i],indice),`${onde}: Tab chega ao «i»`);
 const foco=await p.evaluate(()=>{const c=getComputedStyle(document.activeElement);return {estilo:c.outlineStyle,largura:parseFloat(c.outlineWidth)}});
 assert(foco.estilo!=='none'&&foco.largura>=2,`${onde}: contorno de foco de 2 px ou mais (${JSON.stringify(foco)})`);
 await p.keyboard.press('Enter');assert(await p.evaluate(i=>document.querySelectorAll('details.info-i')[i].open,indice),`${onde}: Enter abre`);
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origem='http://127.0.0.1:'+server.address().port;
const b=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let cenarios=0;
try{
 // 1. Larguras e temas, na página de ensaio e nas amostras reais.
 for(const alvo of [{url:ENSAIO,variante:'ensaio'},...AMOSTRAS])for(const width of LARGURAS)for(const tema of ['light','dark']){
  const ctx=await contexto(b,origem,{viewport:{width,height:width>800?800:860},colorScheme:tema}),p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(String(e)));
  await p.goto(origem+alvo.url,{waitUntil:'networkidle'});await p.locator('details.info-i>summary').first().waitFor();
  const n=await p.locator('details.info-i').count(),onde=`${alvo.url} ${width} ${tema}`;
  assert(n>=1,`${onde}: há um «i»`);
  assert.deepEqual(await p.locator('details.info-i').evaluateAll(es=>es.filter(e=>e.open).length),0,`${onde}: tudo fechado ao carregar`);
  const fundoPagina=await p.evaluate(()=>{for(let e=document.querySelector('details.info-i');e;e=e.parentElement){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)')return c}return getComputedStyle(document.body).backgroundColor});
  for(let i=0;i<n;i++){
   const fechado=await p.evaluate(MEDIR,i);if(!fechado.sVisivel)continue;
   await p.locator('details.info-i>summary').nth(i).scrollIntoViewIfNeeded();const m0=await p.evaluate(MEDIR,i);
   conferirCaixas(m0,`${onde} «i» ${i}`);
   if(alvo.variante!=='ensaio')assert.equal(m0.linha,alvo.variante==='linha',`${onde}: variante ${alvo.variante}`);
   assert(contraste(m0.borda,m0.halo)>=3,`${onde} «i» ${i}: 3:1 do círculo contra o halo (${m0.borda} / ${m0.halo})`);
   await p.locator('details.info-i>summary').nth(i).click();const m1={...(await p.evaluate(MEDIR,i)),fundoPagina};conferirAberto(m1,`${onde} «i» ${i}`);
   assert(contraste(m1.fundoCirculo,m1.halo)>=3,`${onde} «i» ${i}: aberto, o círculo cheio contra o halo`);
   // Um clique fora fecha (no texto da página, fora de qualquer «i»).
   await p.locator('#fora, .jogo .tit').first().click();assert(!(await p.evaluate(i=>document.querySelectorAll('details.info-i')[i].open,i)),`${onde} «i» ${i}: um clique fora fecha`);
  }
  assert.deepEqual(erros,[],`${onde}: sem erros`);await ctx.close();cenarios++;
 }
 // 2. Teclado, árvore de acessibilidade e «um aberto de cada vez», na página de ensaio e nas amostras.
 for(const alvo of [{url:ENSAIO},...AMOSTRAS]){
  const ctx=await contexto(b,origem,{viewport:{width:390,height:860}}),p=await ctx.newPage();await p.goto(origem+alvo.url,{waitUntil:'networkidle'});await p.locator('details.info-i>summary').first().waitFor();
  const antes=await arvore(p);assert(antes.length>=1&&antes.every(n=>/^DisclosureTriangle/.test(n.papel)&&n.expanded===false),`${alvo.url}: árvore fechada ${JSON.stringify(antes)}`);
  const nome=await p.locator('details.info-i>summary').first().getAttribute('aria-label');
  if(alvo.url!==ENSAIO)assert.equal(nome,'Créditos da imagem');
  assert.equal(antes.filter(n=>n.nome===nome).length,1,`${alvo.url}: o nome «${nome}» na árvore`);
  await abrirPorTeclado(p,0,alvo.url);
  const depois=await arvore(p);assert.equal(depois.find(n=>n.nome===nome).expanded,true,`${alvo.url}: expanded depois de abrir`);
  await p.keyboard.press('Escape');
  assert(!(await p.evaluate(()=>document.querySelector('details.info-i').open)),`${alvo.url}: Escape fecha`);
  assert(await p.evaluate(()=>document.activeElement===document.querySelector('details.info-i>summary')),`${alvo.url}: Escape devolve o foco ao «i»`);
  if(alvo.url===ENSAIO){
   const nomes=antes.map(n=>n.nome);assert.equal(new Set(nomes).size,nomes.length,'com vários «i» no ecrã, cada nome é único');
   await p.locator('details.info-i>summary').nth(0).click();await p.locator('details.info-i>summary').nth(3).click();
   assert.deepEqual(await p.locator('details.info-i').evaluateAll(es=>es.map(e=>e.open)),[false,false,false,true,false,false,false],'abrir outro fecha o primeiro');
   // A imagem dentro de uma ligação: o «i» fica fora da ligação e a ligação continua a funcionar.
   assert.equal(await p.locator('[data-caso="ligacao"] a details').count(),0);
  }else if(alvo.familia==='P7'){
   // O ampliador das lições continua a abrir a imagem; a legenda dele já não traz o crédito.
   await p.locator('.jogo .ler figure img').first().click({position:{x:20,y:20}});
   const leg=await p.locator('.amp-ov .amp-leg').innerText();assert(!/Domínio público|CC BY/.test(leg),`${alvo.url}: legenda do ampliador sem crédito (${leg})`);
   await p.keyboard.press('Escape');assert.equal(await p.locator('.amp-ov').count(),0,'Escape fecha o ampliador');
  }
  await ctx.close();cenarios++;
 }
 // 3. Projeção: fechado, sem transbordo, alvo de 44 px; «Parar o desenho» escondido.
 for(const alvo of [{url:ENSAIO},...AMOSTRAS]){
  const ctx=await contexto(b,origem,{viewport:{width:1366,height:768}}),p=await ctx.newPage();await p.goto(origem+alvo.url+'?projetar=1',{waitUntil:'networkidle'});await p.locator('details.info-i>summary').first().waitFor();
  const m=await p.evaluate(MEDIR,0);assert(!m.open&&m.s.w>=44-1/64&&m.s.h>=44-1/64&&!m.rolagem,`${alvo.url}: projeção ${JSON.stringify(m.s)}`);
  assert.equal(await p.evaluate(()=>document.documentElement.hasAttribute('data-ii-projecao')),true,'a marca da projeção');
  if(alvo.url===ENSAIO)assert.equal(await p.locator('[data-fundo-botao]').isVisible(),false,'projeção: «Parar o desenho» escondido');
  await ctx.close();cenarios++;
 }
 // 4. Impressão: o crédito sai por extenso por baixo de cada imagem, sem o «i»; a licença leva o endereço; a linha do fundo não sai.
 for(const alvo of [{url:ENSAIO},...AMOSTRAS]){
  const ctx=await contexto(b,origem,{viewport:{width:1024,height:900}}),p=await ctx.newPage();await p.goto(origem+alvo.url,{waitUntil:'networkidle'});await p.locator('details.info-i>summary').first().waitFor();
  await p.emulateMedia({media:'print'});const n=await p.locator('details.info-i').count();
  for(let i=0;i<n;i++){const m=await p.evaluate(MEDIR,i);if(!m.img||m.img.w===0)continue;
   assert(!m.sVisivel,`${alvo.url} «i» ${i}: na impressão o «i» não sai`);assert(m.tVisivel,`${alvo.url} «i» ${i}: na impressão o crédito sai`);
   assert(m.t.y>=m.img.b-1,`${alvo.url} «i» ${i}: o crédito por baixo da imagem`);}
  const licencas=await p.locator('details.info-i a[rel~="license"]').evaluateAll(as=>as.map(a=>[a.getAttribute('href'),getComputedStyle(a,'::after').content]));
  for(const [href,depois] of licencas)assert(/attr\(href\)|creativecommons/.test(depois),`${alvo.url}: a licença leva o endereço (${href}: ${depois})`);
  if(alvo.url===ENSAIO){assert(licencas.length>=2,'o ensaio tem licenças CC');assert.equal(await p.locator('.fundo-acoes').isVisible(),false,'a linha do fundo não sai na impressão')}
  await ctx.close();cenarios++;
 }
 // 5. Sem JavaScript: o «i» abre com clique e com Enter; o botão do fundo fica escondido.
 for(const alvo of [{url:ENSAIO}]){
  const ctx=await contexto(b,origem,{viewport:{width:390,height:860},javaScriptEnabled:false}),p=await ctx.newPage();await p.goto(origem+alvo.url,{waitUntil:'load'});
  const s=p.locator('details.info-i>summary');await s.nth(0).click();assert(await p.evaluate(()=>document.querySelectorAll('details.info-i')[0].open),'sem JS, o clique abre');
  await s.nth(1).focus();await p.keyboard.press('Enter');assert(await p.evaluate(()=>document.querySelectorAll('details.info-i')[1].open),'sem JS, Enter abre');
  assert.equal(await p.locator('[data-fundo-botao]').isVisible(),false,'sem JS, «Parar o desenho» escondido');
  await ctx.close();cenarios++;
 }
 // 6. Com o desenho a andar: «Parar o desenho» à vista, fora do «i», e para o desenho.
 {const ctx=await contexto(b,origem,{viewport:{width:390,height:860},reducedMotion:'no-preference'}),p=await ctx.newPage();await p.goto(origem+ENSAIO,{waitUntil:'networkidle'});
  const botao=p.locator('[data-fundo-botao="ii"]');await botao.waitFor({state:'visible'});
  assert.equal(await botao.evaluate(e=>!!e.closest('details.info-i')),false,'«Parar o desenho» fora do «i»');
  assert.equal(await botao.innerText(),'Parar o desenho');assert(await p.evaluate(()=>document.querySelector('[data-fundo]').classList.contains('ii-anda')),'o desenho anda');
  const r=await botao.boundingBox();assert(r.height>=44-1/64,'alvo do botão');
  await p.locator('[data-caso="fundo"] details.info-i>summary').click();assert(await botao.isVisible(),'com o «i» aberto, o botão continua à vista');
  await botao.click();assert(!(await p.evaluate(()=>document.querySelector('[data-fundo]').classList.contains('ii-anda'))),'o botão para o desenho');
  await ctx.close();cenarios++;}
 console.log(`PASS ${cenarios} cenários da peça «i» (ensaio, P7 e P9)`);
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
