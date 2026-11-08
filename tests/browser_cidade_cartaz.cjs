// 08/11/2026: cartaz «Ler a cidade» na entrada do Português (camada cidade_cartaz_20261108; pedido do utilizador: «quero que [Ler a
// cidade] tenha um banner em português»). O cartaz vem logo a seguir ao do Atlas e logo antes do portal do Lente.
// 08/11/2026 (revisão): o utilizador achou a primeira versão «visualmente igual ao do Atlas... estranho e mau»; o cartaz passa a ter
// cara própria (a fotografia de Lisboa vista do Tejo em 1907, a do cartão «Ler a cidade.» da entrada do Lente, e o título em
// Georgia itálico), e a conferência «o mesmo aspeto do Atlas» passa a ser a contrária: o cartaz não usa a família de letra do
// título do Atlas nem a cor de fundo do Atlas, nem as suas classes ou a grelha de números.
// A 320, 390, 768 e 1280 px (tema claro), a 390 e 1280 px no tema escuro, a 1280 px na projeção (/pt/projetar/?pagina=/pt/, a
// entrada dentro do quadro da projeção) e a 390 px em cores forçadas: a página não rola para o lado e nada sai do cartaz; o título
// cabe numa só linha e não transborda; as duas ligações têm 44 px de altura ou mais; a fotografia carrega (naturalWidth > 0) e
// mostra-se em 3:2 (tolerância de 2 %), sem recorte, com a etiqueta pousada no canto de baixo; o «i» do crédito está fechado ao
// carregar, tem alvo de 44 px, não fica tapado, abre por clique e por Enter com o crédito inteiro e a ligação da Biblioteca do
// Congresso, sem transbordar, e fecha por clique e por Escape. No claro e no escuro, o texto tem 4,5:1 contra o cartão; no escuro,
// o cartão é escuro e o texto claro. Sem erros na página.
// Corre com: node tests/browser_cidade_cartaz.cjs (CIDADE_CARTAZ_OUTPUT=<pasta> guarda capturas: os cartazes do Atlas, de Ler a
// cidade e do Lente seguidos, como aparecem na página, a 390 e a 1280 px, claro e escuro, e a projeção).
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.CIDADE_CARTAZ_OUTPUT;if(out)fs.mkdirSync(out,{recursive:true});
const LENTE='https://pedrohfernandes-klk.github.io/lente/cidade/';
const ALT='Barco à vela no Tejo; atrás, o cais e a cidade.';
const CREDITO='Metade de um estereograma de 1907, com direitos de J. J. Killelea & Co. e publicado por H. C. White Co. Domínio público. Library of Congress.';
const tipos={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://local').pathname.replace(/^\/pt\//,'/')),f=path.resolve(root,'.'+rel);if(!f.startsWith(root)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',tipos[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
// Só a origem local; o resto (o Lente publicado, tipos de letra de fora) não se carrega, para o teste não depender da rede.
async function contexto(b,origem,opcoes){const ctx=await b.newContext({deviceScaleFactor:1,...opcoes});await ctx.route('**/*',r=>new URL(r.request().url()).origin===origem?r.continue():r.abort());return ctx}
// A fotografia vem com loading="lazy": chega-se a ela e espera-se que carregue e se descodifique.
async function verFoto(alvo){const c=alvo.locator('section.cidade-cartaz');await c.evaluate(e=>e.scrollIntoView({block:'center'}));
 await alvo.locator('section.cidade-cartaz img').evaluate(async i=>{if(!(i.complete&&i.naturalWidth))await new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true})});await i.decode().catch(()=>{})})}
// Medidas dentro da página (ou do quadro da projeção).
function medir(){
 const c=document.querySelector('section.cidade-cartaz'),a=document.querySelector('section.atlas-poster');
 const R=e=>{const r=e.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}};
 const cs=getComputedStyle,h2=c.querySelector('h2'),img=c.querySelector('.cidade-cartaz-imagem img'),et=c.querySelector('.cidade-cartaz-etiqueta');
 const d=c.querySelector('details.info-i'),s=d.querySelector(':scope>summary'),t=d.querySelector(':scope>.info-i-texto');
 const visivel=e=>e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,opacityProperty:true});
 const cor=x=>x.match(/[\d.]+/g).slice(0,4).map(Number),lum=k=>{const f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(k[0])+.7152*f(k[1])+.0722*f(k[2])},contraste=(p,q)=>{const x=lum(p),y=lum(q);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const fundo=cor(cs(c).backgroundColor);
 // linhas do título: as caixas do texto do h2 com topos diferentes
 const rg=document.createRange();rg.selectNodeContents(h2);const linhas=new Set([...rg.getClientRects()].filter(q=>q.width>1).map(q=>Math.round(q.top))).size;
 // tudo o que está à vista dentro do cartaz cabe nele (a largura)
 const fora=[...c.querySelectorAll('*')].filter(e=>visivel(e)&&!d.contains(e)).filter(e=>{const r=e.getBoundingClientRect(),k=c.getBoundingClientRect();return r.left<k.left-.5||r.right>k.right+.5}).map(e=>e.tagName.toLowerCase()+'.'+[...e.classList].join('.'));
 const meio=x=>({x:x.left+x.width/2,y:x.top+x.height/2}),sm=meio(s.getBoundingClientRect()),topo=document.elementFromPoint(sm.x,sm.y);
 return {
  lado:document.documentElement.scrollWidth-document.documentElement.clientWidth,
  ordem:[...document.querySelectorAll('section.atlas-poster, section.cidade-cartaz, nav.site-portal-wrap')].map(e=>e.matches('.atlas-poster')?'atlas':e.matches('.cidade-cartaz')?'cidade':'lente'),
  anterior:(()=>{let e=c.previousElementSibling;while(e&&e.tagName==='STYLE')e=e.previousElementSibling;return e?e.tagName.toLowerCase()+'.'+[...e.classList].join('.'):null})(),
  seguinte:(()=>{let e=c.nextElementSibling;return e?e.tagName.toLowerCase()+'.'+[...e.classList].join('.'):null})(),
  classes:[...c.classList],grelha:c.querySelectorAll('.atlas-poster-art,.atlas-poster-copy,[class*="atlas"]').length,
  cartaz:R(c),atlas:R(a),fora,
  titulo:{sw:h2.scrollWidth,cw:h2.clientWidth,caixa:R(h2),linhas,texto:h2.textContent.replace(/\s+/g,' ').trim(),familia:cs(h2).fontFamily,estilo:cs(h2).fontStyle,peso:cs(h2).fontWeight,tamanho:parseFloat(cs(h2).fontSize)},
  tituloAtlas:{familia:cs(a.querySelector('h2')).fontFamily},fundo:cs(c).backgroundColor,fundoAtlas:cs(a).backgroundColor,borda:[cs(c).borderTopWidth,cs(c).borderTopStyle].join(' '),
  ligacoes:[...c.querySelectorAll('nav a')].map(e=>({t:e.textContent.replace(/\s+/g,' ').trim(),href:e.getAttribute('href'),...R(e),contraste:contraste(cor(cs(e).color),fundo)})),
  // (textContent: o pré-título vai em maiúsculas pela folha, mas o texto é o do HTML)
  texto:[...c.querySelectorAll('.cidade-cartaz-texto>p')].map(p=>({t:p.textContent.replace(/\s+/g,' ').trim(),contraste:contraste(cor(cs(p).color),fundo)})),
  tituloContraste:contraste(cor(cs(h2).color),fundo),luzFundo:lum(fundo),
  foto:{src:img.getAttribute('src'),alt:img.getAttribute('alt'),nw:img.naturalWidth,nh:img.naturalHeight,completa:img.complete,caixa:R(img),ajuste:cs(img).objectFit,visivel:visivel(img)},
  etiqueta:{t:et.textContent,caixa:R(et),visivel:visivel(et)},
  i:{open:d.open,nome:s.getAttribute('aria-label'),alvo:R(s),visivel:visivel(s),tapado:!(topo&&(s===topo||s.contains(topo))),texto:t.textContent.replace(/\s+/g,' ').trim(),
   ligacoes:[...t.querySelectorAll('a[href]')].map(x=>x.getAttribute('href')),textoVisivel:visivel(t),textoCaixa:R(t),textoSw:t.scrollWidth,textoCw:t.clientWidth,
   // as linhas do crédito aberto: a margem que lhes sobra até ao filete do cartão, de cada lado
   margens:(()=>{const q=document.createRange();q.selectNodeContents(t);const rs=[...q.getClientRects()].filter(x=>x.width>1),k=c.getBoundingClientRect();return rs.length?[Math.min(...rs.map(x=>x.left))-k.left,k.right-Math.max(...rs.map(x=>x.right))]:null})()},
 };
}
function conferir(m,rot,{forcadas=false,escuro=false}={}){
 assert.ok(m.lado<=0,rot+': a página não rola para o lado ('+m.lado+' px)');
 assert.deepEqual(m.ordem,['atlas','cidade','lente'],rot+': Atlas, Ler a cidade e Lente, por esta ordem');
 assert.equal(m.anterior,'section.atlas-poster',rot+': o cartaz vem logo a seguir ao do Atlas');assert.equal(m.seguinte,'nav.site-portal-wrap',rot+': e logo antes do portal do Lente');
 assert.ok(m.cartaz.x>=-.5&&m.cartaz.r<=m.atlas.r+.5,rot+': o cartaz cabe na coluna');assert.equal(Math.round(m.cartaz.w),Math.round(m.atlas.w),rot+': a largura da coluna, como o do Atlas');
 assert.deepEqual(m.fora,[],rot+': nada sai do cartaz para os lados');
 // Distinto do Atlas: nem as classes, nem a grelha de números, nem a letra do título, nem a cor de fundo.
 assert.deepEqual(m.classes,['cidade-cartaz'],rot+': só a classe própria');assert.equal(m.grelha,0,rot+': sem peças do cartaz do Atlas');
 assert.notEqual(m.titulo.familia,m.tituloAtlas.familia,rot+': o título não usa a letra do título do Atlas');
 assert.match(m.titulo.familia,/^Georgia\b/,rot+': o título em Georgia');assert.equal(m.titulo.estilo,'italic',rot+': em itálico');assert.equal(m.titulo.peso,'400',rot+': de peso normal');
 if(!forcadas)assert.notEqual(m.fundo,m.fundoAtlas,rot+': o fundo não é o do Atlas');
 assert.equal(m.borda,'1px solid',rot+': um filete fino à volta');
 assert.deepEqual(m.texto.map(x=>x.t),['Português × Cidadania','Uma rua pode ser lida como um texto e discutida como um espaço de todos. São 14 missões, no bairro ou a partir das fotografias.'],rot+': o texto');
 assert.equal(m.titulo.texto,'Ler a cidade',rot+': o título');assert.equal(m.titulo.linhas,1,rot+': o título numa só linha');
 assert.ok(m.titulo.sw<=m.titulo.cw,rot+': o título não transborda do h2 ('+m.titulo.sw+' > '+m.titulo.cw+')');assert.ok(m.titulo.caixa.r<=m.cartaz.r+.5,rot+': o título dentro do cartaz');
 assert.deepEqual(m.ligacoes.map(l=>[l.t,l.href]),[['Entrar na cidade →',LENTE],['Ver as missões →',LENTE+'#m01']],rot+': as ligações');
 for(const l of m.ligacoes){assert.ok(l.h>=44,rot+': «'+l.t+'» com 44 px de altura ou mais ('+l.h+')');assert.ok(l.x>=m.cartaz.x-.5&&l.r<=m.cartaz.r+.5,rot+': «'+l.t+'» dentro do cartaz');}
 // A fotografia: carregada, 3:2 sem recorte (a proporção do ficheiro), dentro do cartaz; a etiqueta no canto de baixo dela.
 assert.equal(m.foto.src,'img/arquivo/tejo-1907-vela-e-cidade.jpg',rot);assert.equal(m.foto.alt,ALT,rot+': o alt');
 assert.ok(m.foto.completa&&m.foto.nw>0,rot+': a fotografia carrega');assert.deepEqual([m.foto.nw,m.foto.nh],[1160,773],rot+': o ficheiro inteiro');
 assert.ok(Math.abs(m.foto.caixa.w/m.foto.caixa.h/1.5-1)<=.02,rot+': a fotografia em 3:2 ('+(m.foto.caixa.w/m.foto.caixa.h).toFixed(3)+')');
 assert.ok(Math.abs(m.foto.caixa.w/m.foto.caixa.h-m.foto.nw/m.foto.nh)<.01,rot+': sem recorte (a proporção do ficheiro)');
 assert.ok(m.foto.visivel&&m.foto.caixa.x>=m.cartaz.x-.5&&m.foto.caixa.r<=m.cartaz.r+.5,rot+': a fotografia dentro do cartaz');
 assert.equal(m.etiqueta.t,'Lisboa vista do Tejo, 1907',rot+': a etiqueta');assert.ok(m.etiqueta.visivel,rot+': a etiqueta à vista');
 assert.ok(Math.abs(m.etiqueta.caixa.b-m.foto.caixa.b)<=1&&Math.abs(m.etiqueta.caixa.x-m.foto.caixa.x)<=1&&m.etiqueta.caixa.r<=m.foto.caixa.r+.5,rot+': a etiqueta pousada no canto de baixo da fotografia');
 // O «i» fechado: à vista, com alvo de 44 px, sem nada por cima, dentro do cartaz.
 assert.equal(m.i.open,false,rot+': o «i» fechado ao carregar');assert.ok(m.i.visivel,rot+': o «i» à vista');assert.equal(m.i.nome,'Créditos da fotografia: Lisboa vista do Tejo',rot);
 assert.ok(m.i.alvo.w>=44&&m.i.alvo.h>=44,rot+': alvo de 44 px');assert.equal(m.i.tapado,false,rot+': nada tapa o «i»');
 assert.ok(m.i.alvo.x>=m.cartaz.x-.5&&m.i.alvo.r<=m.cartaz.r+.5&&m.i.alvo.b<=m.cartaz.b+.5,rot+': o «i» dentro do cartaz');
 assert.equal(m.i.texto,CREDITO,rot+': o crédito inteiro');assert.deepEqual(m.i.ligacoes,['https://www.loc.gov/item/2021640928/'],rot+': a ligação da Biblioteca do Congresso');
 if(forcadas)return;
 for(const x of [...m.texto,{t:'título',contraste:m.tituloContraste},...m.ligacoes])assert.ok(x.contraste>=4.5,rot+': 4,5:1 de «'+x.t.slice(0,24)+'» contra o cartão ('+x.contraste.toFixed(2)+')');
 if(escuro)assert.ok(m.luzFundo<.05,rot+': no escuro, o cartão é escuro');else assert.ok(m.luzFundo>.8,rot+': no claro, o cartão é claro');
}
// O «i» abre e fecha (clique e teclado), com o crédito inteiro, sem transbordar e sem pôr a página a rolar para o lado.
async function abrirFechar(alvo,teclado,rot){
 const s=alvo.locator('section.cidade-cartaz details.info-i>summary'),d=alvo.locator('section.cidade-cartaz details.info-i');
 await s.click();await alvo.waitForTimeout(250);let m=await alvo.evaluate(medir);
 assert.ok(m.i.open&&m.i.textoVisivel,rot+': o clique abre o «i»');assert.ok(m.i.textoSw<=m.i.textoCw+1,rot+': o crédito aberto não transborda');
 assert.ok(m.i.textoCaixa.x>=m.cartaz.x-.5&&m.i.textoCaixa.r<=m.cartaz.r+.5&&m.i.textoCaixa.b<=m.cartaz.b+.5,rot+': o crédito aberto dentro do cartaz');assert.ok(m.lado<=0,rot+': aberto, sem deslize');
 assert.ok(m.i.margens&&m.i.margens.every(x=>x>=12),rot+': o crédito aberto não encosta ao filete do cartão ('+JSON.stringify(m.i.margens)+')');
 assert.equal(m.i.tapado,false,rot+': aberto, o «i» continua livre');
 await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': o clique fecha o «i»');
 if(teclado){await s.focus();await teclado.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
  await teclado.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');}
}
// Captura dos três cartazes seguidos, como aparecem na página: do cartaz do Atlas ao «i» da fotografia do portal do Lente.
async function tresCartazes(page,ficheiro){
 const clip=await page.evaluate(()=>{const a=document.querySelector('section.atlas-poster').getBoundingClientRect(),l=document.querySelector('nav.site-portal-wrap').getBoundingClientRect();const y=a.top+scrollY-16;return {x:0,y,width:document.documentElement.clientWidth,height:l.bottom+scrollY+16-y}});
 await page.screenshot({path:path.join(out,ficheiro),clip,fullPage:true});
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});const feitos=[];
 try{
  const CENARIOS=[...[320,390,768,1280].map(width=>({width,tema:'light'})),{width:390,tema:'dark'},{width:1280,tema:'dark'}];
  for(const {width,tema} of CENARIOS){
   const ctx=await contexto(browser,origin,{viewport:{width,height:900},colorScheme:tema,reducedMotion:'reduce',hasTouch:width<800}),page=await ctx.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/pt/',{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.evaluate(()=>document.documentElement.getAttribute('data-theme')),tema,width+': o tema '+tema+' ligado (assets/appearance.js)');
   await verFoto(page);const rot=`${width} px, ${tema}`;conferir(await page.evaluate(medir),rot,{escuro:tema==='dark'});
   if(out&&(width===390||width===1280))await tresCartazes(page,`atlas-cidade-lente-${width}-${tema}.png`);
   await abrirFechar(page,page.keyboard,rot);
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
   await frame.evaluate(()=>document.fonts.ready);await verFoto(frame);
   const rot=`${width} px, projeção`;conferir(await frame.evaluate(medir),rot);
   if(out)await page.locator('#lesson-frame').screenshot({path:path.join(out,'projecao-1280.png')});
   await abrirFechar(frame,null,rot);
   assert.deepEqual(errors,[],rot+': sem erros na página');await ctx.close();feitos.push(rot);}
  // Cores forçadas, a 390 px.
  {const width=390,ctx=await contexto(browser,origin,{viewport:{width,height:900},forcedColors:'active',reducedMotion:'reduce'}),page=await ctx.newPage();
   await page.goto(origin+'/pt/',{waitUntil:'load'});await verFoto(page);const rot=`${width} px, cores forçadas`;conferir(await page.evaluate(medir),rot,{forcadas:true});
   await abrirFechar(page,page.keyboard,rot);
   if(out)await page.locator('section.cidade-cartaz').screenshot({path:path.join(out,'cores-forcadas-390.png')});await ctx.close();feitos.push(rot);}
  console.log(`Cartaz «Ler a cidade»: ${feitos.length} cenários (${feitos.join('; ')}), distinto do Atlas, sem deslize horizontal, título numa linha, fotografia em 3:2 com etiqueta, «i» que abre e fecha, ligações com 44 px.`);
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
