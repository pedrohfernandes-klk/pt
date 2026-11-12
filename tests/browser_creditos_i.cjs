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
// 05/11/2026: pedido pt-2, fatia 2: amostras de P10 (Pessoa em M7-F01, «linha») e P11 (dupla exposição em M7-F34, «canto»)
// no primeiro cartão; e, montados no cartão aberto ou abertos na página, os retratos do «Em paralelo» (P12, «linha», o «i» por
// baixo do retrato e o crédito com a largura da coluna), a imagem do campo ver de uma lição (P13: o «i» fora da figura que
// amplia, e a imagem continua a ampliar), o material de um painel (P13, «linha») e a galeria do mapa M7 (P10, «linha»).
// 05/11/2026: pedido pt-2, fatia 3: amostra da P14 («Pensar devagar», «canto») no primeiro cartão; e, preparados na página, a
// imagem de dois exercícios «Olhar» (P15: «canto» em M4, «linha» no retrato de Pessoa em M7; o «i» liga ao creditoUrl) e a
// galeria «Para ver» do mapa M8 (P16, «linha»; a ligação «Lição Mx-Fyy» fica à vista, fora do «i»). Na galeria do mapa M7 há agora
// um «i» por figura: o caso da P10 olha só para a figura de Pessoa (a primeira); as outras são da P16, que o teste estático conta.
// 06/11/2026: confirmação final do pedido pt-2: nas lições de Pessoa (P10, M7-F01 e M7-F05), a legenda à vista nunca passa por
// baixo do «i» fechado (secção 9).
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
 {url:'/pt/m7/licao-m7-f01/',variante:'linha',familia:'P10'},
 {url:'/pt/m7/licao-m7-f34/',variante:'canto',familia:'P11'},
 {url:'/pt/m1/m1-promessa-do-cronista/',variante:'canto',familia:'P14'},
];
const LARGURAS=[320,390,852,1366];
function lum(c){const m=c.match(/[\d.]+/g).map(Number),f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])}
function contraste(a,b){const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
// 05/11/2026: os dados JSON de um script da página (CARTOES=[…], MATERIAL={…}), a partir do primeiro [ ou { em i.
function jsonEm(t,i){let n=0,s=false,e=false;for(let k=i;k<t.length;k++){const c=t[k];if(s){if(e)e=false;else if(c==='\\')e=true;else if(c==='"')s=false;continue}
 if(c==='"')s=true;else if(c==='['||c==='{')n++;else if(c===']'||c==='}'){n--;if(!n)return JSON.parse(t.slice(i,k+1))}}throw new Error('JSON sem fim')}
// Os casos da fatia 2 que não estão no primeiro cartão: monta-se o cartão (como nos outros testes das lições), abre-se a galeria
// ou lança-se o material do painel; devolve o seletor onde ficam os «i».
const CASOS=[
 {nome:'P12 M4-F01',url:'/pt/m4/licao-m4-f01/',rel:'m4/licao-m4-f01/index.html',cartao:c=>/class="rosto"/.test(c.html||''),variante:'linha',n:2,nomes:['Créditos da imagem: Santo António','Créditos da imagem: António Vieira']},
 {nome:'P12 M1-F19',url:'/pt/m1/licao-m1-f19/',rel:'m1/licao-m1-f19/index.html',cartao:c=>/class="rosto"/.test(c.html||''),variante:'linha',n:2,nomes:['Créditos da imagem: ilha de San Simón','Créditos da imagem: Pergaminho Vindel']},
 {nome:'P13 M4-F11',url:'/pt/m4/licao-m4-f11/',rel:'m4/licao-m4-f11/index.html',cartao:c=>/info-i/.test(c.ver||''),variante:'canto',n:1,nomes:['Créditos da imagem']},
 {nome:'P13 painel M4-F01',url:'/pt/m4/painel-m4-f01/',rel:'m4/painel-m4-f01/index.html',painel:true,variante:'linha',n:1,nomes:['Créditos da imagem']},
 // 05/11/2026: fatia 3. A galeria do mapa M7 tem agora 19 «i» (P16): este caso olha só para a figura de Pessoa, a primeira.
 {nome:'P10 mapa M7',url:'/pt/m7/mapa-do-modulo-m7/',galeria:true,raiz:'#galeria .galeria>figure:first-child',variante:'linha',n:1,nomes:['Créditos da imagem: Fernando Pessoa']},
 {nome:'P15 Olhar M4',url:'/pt/m4/olhar-lupi/',olhar:'https://commons.wikimedia.org/w/index.php?curid=39076717',variante:'canto',n:1,nomes:['Créditos da imagem']},
 {nome:'P15 Olhar M7',url:'/pt/m7/olhar-pessoa/',olhar:'https://commons.wikimedia.org/w/index.php?curid=56775462',variante:'linha',n:1,nomes:['Créditos da imagem']},
 {nome:'P16 mapa M8',url:'/pt/m8/mapa-do-modulo-m8/',galeria:true,variante:'linha',n:4,licoes:4,nomes:['Créditos da imagem: Os fuzilamentos de 3 de maio de 1808','Créditos da imagem: Rua do Alecrim, Lisboa','Créditos da imagem: Estação do Rossio, Lisboa','Créditos da imagem: Relógio de bolso']},
];
async function preparar(p,caso){
 if(caso.cartao){const t=fs.readFileSync(path.join(root,caso.rel),'utf8'),card=jsonEm(t,t.indexOf('[',t.search(/CARTOES\s*=/))).find(caso.cartao);
  await p.evaluate(x=>{window.qaCasca=EPICasca.abrir({semVoltar:true});EPIJogo.montar({casca:qaCasca,itens:[x],chave:'qa-creditos-i'})},card);return '.casca.sobreposta'}
 if(caso.painel){const t=fs.readFileSync(path.join(root,caso.rel),'utf8'),M=jsonEm(t,t.indexOf('{',t.indexOf('MATERIAL='))),k=Object.keys(M).find(k=>/info-i/.test(M[k].ver||''));
  await p.locator('[data-r-k]').selectOption(k);await p.locator('[data-relampago]').click();return '[data-extra]'}
 // 05/11/2026: fatia 3. O «Olhar»: «Começar» e «Ver a imagem» (o passo de memória); o relógio para, para a imagem não sumir.
 if(caso.olhar){await p.locator('#seguir').click();await p.locator('#mostrar').click();await p.locator('#palco .olhar-com-i img').waitFor();
  await p.clock.pauseAt(await p.evaluate(()=>Date.now()+1000));return '#palco'}
 await p.locator('#galeria > summary').click();return caso.raiz||'#galeria'}
// O «i», a imagem que ele acompanha e as caixas de cada um.
// 05/11/2026: sel é o índice do «i» na página, ou {raiz, i} para o i-ésimo «i» dentro de um seletor (cartão montado, galeria).
const MEDIR=(sel)=>{const d=(typeof sel==='number'?document.querySelectorAll('details.info-i'):document.querySelectorAll(sel.raiz+' details.info-i'))[typeof sel==='number'?sel:sel.i];if(!d)return null;const s=d.querySelector(':scope>summary'),t=d.querySelector(':scope>.info-i-texto');
 const casa=d.closest('.com-i')||d.parentElement,img=casa.querySelector('img')||(d.closest('figure')&&d.closest('figure').querySelector('img'));
 const caixa=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}};
 const sp=getComputedStyle(s.querySelector('span')),tt=getComputedStyle(t);
 return {open:d.open,linha:d.classList.contains('info-i--linha'),s:caixa(s),img:caixa(img),t:caixa(t),tVisivel:t.checkVisibility(),sVisivel:s.checkVisibility(),
  borda:sp.borderTopColor,halo:(sp.boxShadow.match(/rgba?\([^)]*\)/)||[sp.backgroundColor])[0],fundoCirculo:sp.backgroundColor,cor:tt.color,fundo:tt.backgroundColor,
  rolagem:document.documentElement.scrollWidth>innerWidth+1,vw:innerWidth,
  justificado:[t,...t.querySelectorAll('*')].filter(e=>{const c=getComputedStyle(e);return c.textAlign==='justify'||c.hyphens==='auto'}).map(e=>e.tagName)}};
// 05/11/2026: fatia 3. As imagens dos «Pensar devagar» vêm pelo endereço publicado (https://pedrohfernandes-klk.github.io/pt/…):
// servem-se da árvore local, como as outras; o resto de fora continua cortado.
const PUBLICADO='https://pedrohfernandes-klk.github.io';
async function contexto(b,origem,opcoes){const ctx=await b.newContext({reducedMotion:'reduce',...opcoes});await ctx.route('**/*',r=>{const u=new URL(r.request().url());
 if(u.origin===PUBLICADO&&u.pathname.startsWith('/pt/')){const f=path.resolve(root,'.'+decodeURIComponent(u.pathname.slice(3)));return f.startsWith(root)&&fs.existsSync(f)&&fs.statSync(f).isFile()?r.fulfill({path:f}):r.abort()}
 return u.origin===origem?r.continue():r.abort()});return ctx}
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
  }else if(alvo.familia==='P7'||alvo.familia==='P10'||alvo.familia==='P14'){
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
  // 06/11/2026: na projeção, o «i» canto guarda o fundo e o halo; o contraste mede-se contra o halo.
  if(!m.linha)assert(m.fundoCirculo!=='rgba(0, 0, 0, 0)'&&contraste(m.borda,m.halo)>=3,`${alvo.url}: projeção, o «i» canto com fundo e halo (${m.fundoCirculo} / ${m.borda} / ${m.halo})`);
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
  // 07/11/2026: decisão 177 (pedido pt-1). O motor comum (assets/fundos.js, igual no Lente) escreve agora «Parar a animação» (era
  // «Parar o desenho»); o resto da exigência fica igual.
  assert.equal(await botao.innerText(),'Parar a animação');assert(await p.evaluate(()=>document.querySelector('[data-fundo]').classList.contains('ii-anda')),'o desenho anda');
  const r=await botao.boundingBox();assert(r.height>=44-1/64,'alvo do botão');
  await p.locator('[data-caso="fundo"] details.info-i>summary').click();assert(await botao.isVisible(),'com o «i» aberto, o botão continua à vista');
  await botao.click();assert(!(await p.evaluate(()=>document.querySelector('[data-fundo]').classList.contains('ii-anda'))),'o botão para o desenho');
  await ctx.close();cenarios++;}
 // 7. Fatia 2: os casos montados (P12, P13) e abertos na página (P10 na galeria, P13 no painel), nas quatro larguras e nos dois
 // temas: fechado; alvo de 44 px no sítio da variante; aberto, o crédito no ecrã, legível, e o «i» no mesmo sítio; Escape fecha.
 for(const caso of CASOS)for(const width of LARGURAS)for(const tema of ['light','dark']){
  const ctx=await contexto(b,origem,{viewport:{width,height:width>800?800:860},colorScheme:tema}),p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(String(e)));
  if(caso.olhar)await p.clock.install();
  await p.goto(origem+caso.url,{waitUntil:'networkidle'});const raiz=await preparar(p,caso),sel=raiz+' details.info-i',onde=`${caso.nome} ${width} ${tema}`;
  await p.locator(sel+'>summary').first().waitFor();assert.equal(await p.locator(sel).count(),caso.n,`${onde}: ${caso.n} «i»`);
  assert.deepEqual(await p.locator(sel+'>summary').evaluateAll(s=>s.map(x=>x.getAttribute('aria-label'))),caso.nomes,`${onde}: nomes`);
  const fundoPagina=await p.evaluate(s=>{for(let e=document.querySelector(s);e;e=e.parentElement){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)')return c}return getComputedStyle(document.body).backgroundColor},sel);
  for(let i=0;i<caso.n;i++){
   await p.locator(sel+'>summary').nth(i).scrollIntoViewIfNeeded();const m0=await p.evaluate(MEDIR,{raiz,i});
   assert(!m0.open,`${onde} «i» ${i}: fechado ao carregar`);conferirCaixas(m0,`${onde} «i» ${i}`);assert.equal(m0.linha,caso.variante==='linha',`${onde}: variante ${caso.variante}`);
   assert(contraste(m0.borda,m0.halo)>=3,`${onde} «i» ${i}: 3:1 do círculo contra o halo`);
   await p.locator(sel+'>summary').nth(i).click();const m1={...(await p.evaluate(MEDIR,{raiz,i})),fundoPagina};conferirAberto(m1,`${onde} «i» ${i}`);
   // Em relação à imagem (a página pode rolar quando o crédito abre no fluxo, por baixo).
   assert(Math.abs((m1.s.x-m1.img.x)-(m0.s.x-m0.img.x))<=.5&&Math.abs((m1.s.y-m1.img.y)-(m0.s.y-m0.img.y))<=.5,`${onde} «i» ${i}: aberto, o «i» fica no mesmo sítio`);
   if(caso.nome.startsWith('P12'))assert(m1.t.w>m1.img.w+40,`${onde} «i» ${i}: o crédito do retrato abre com a largura da coluna (${m1.t.w} / ${m1.img.w})`);
   assert.equal(await p.locator('.amp-ov').count(),0,`${onde} «i» ${i}: abrir o «i» não amplia a imagem`);
   await p.keyboard.press('Escape');assert(!(await p.evaluate(([s,k])=>document.querySelectorAll(s)[k].open,[sel,i])),`${onde} «i» ${i}: Escape fecha`);
  }
  if(width===390&&tema==='light'){const ax=await arvore(p);for(const nome of caso.nomes)assert(ax.some(n=>n.nome===nome&&/^DisclosureTriangle/.test(n.papel)&&n.expanded===false),`${onde}: «${nome}» na árvore, fechado`)}
  if(width===1366&&tema==='light'){await p.emulateMedia({media:'print'});
   for(let i=0;i<caso.n;i++){const m=await p.evaluate(MEDIR,{raiz,i});if(!m.img||m.img.w===0)continue;
    assert(!m.sVisivel&&m.tVisivel&&m.t.y>=m.img.b-1,`${onde} «i» ${i}: na impressão, o crédito por baixo da imagem e sem o «i»`)}
   // 06/11/2026: as ligações do crédito são texto corrido, mesmo onde a página dá outra caixa às suas ligações (as galerias
   // «Para ver» põem-nas em inline-block, e o ponto final depois da licença ficava sozinho numa linha na impressão).
   assert.deepEqual(await p.evaluate(r=>[...document.querySelectorAll(r+' .info-i-texto a')].map(a=>getComputedStyle(a).display).filter(d=>d!=='inline'),raiz),[],`${onde}: na impressão, as ligações do crédito seguem a linha do texto`);
   await p.emulateMedia({media:'screen'})}
  if(caso.cartao&&caso.variante==='canto'){
   // P13: o «i» fica fora da figura que amplia (um botão); tocar na imagem continua a ampliar.
   assert(await p.evaluate(s=>!document.querySelector(s).closest('[role="button"],button,a,figure'),sel),`${onde}: o «i» fora da figura que amplia`);
   await p.locator(raiz+' .ver-fig').click({position:{x:20,y:20}});assert.equal(await p.locator('.amp-ov').count(),1,`${onde}: a imagem continua a ampliar`);
   await p.keyboard.press('Escape');assert.equal(await p.locator('.amp-ov').count(),0,`${onde}: Escape fecha o ampliador`);
  }
  if(caso.olhar){
   // P15: o crédito já não fica por baixo da imagem (p.credito); dentro do «i», a ligação para a imagem de origem (creditoUrl).
   assert.equal(await p.locator('#palco p.credito').count(),0,`${onde}: sem p.credito`);
   assert.deepEqual(await p.locator(sel+' .info-i-texto a').evaluateAll(as=>as.map(a=>[a.getAttribute('href'),a.textContent])),[[caso.olhar,'Wikimedia Commons']],`${onde}: a ligação creditoUrl no «i»`);
   assert.equal(await p.locator(sel+' .info-i-texto').evaluate(t=>/·/.test(t.textContent)),false,`${onde}: sem pontos médios no crédito`);
  }
  if(caso.licoes){
   // P16: a ligação «Lição Mx-Fyy» fica à vista, na legenda, fora do «i».
   // 12/11/2026: decisão 152 no M8 (achado 36): no mapa do M8 (o único caso com esta contagem), a sigla leva a junção (U+2060) depois do
   // hífen, para não se partir entre linhas; a mesma exigência, com a sigla como está agora na página.
   const licoes=await p.locator(raiz+' figcaption a').evaluateAll(as=>as.filter(a=>/^Lição M\d-\u2060F\d+$/.test(a.textContent)&&a.checkVisibility()&&!a.closest('details.info-i')).length);
   assert.equal(licoes,caso.licoes,`${onde}: as ligações «Lição Mx-Fyy» à vista`);
   assert.equal(await p.locator(raiz+' figcaption').evaluateAll(fs=>fs.filter(f=>/Domínio público|CC BY|CC0/.test(f.textContent)).length),0,`${onde}: a licença já não está na legenda`);
  }
  assert.deepEqual(erros,[],`${onde}: sem erros`);await ctx.close();cenarios++;
 }
 // 8. 06/11/2026: revisão do pedido pt-2 (proximidade). Com o «i» «linha» fechado entre a imagem e a legenda, a legenda fica junto da
 // sua imagem (figcaption.top − img.bottom ≤ 8 px) e a caixa do «i» não toca no texto da legenda; o toque no centro do «i» chega ao
 // «i». Nas quatro larguras: P9 (M3-F19), P10 (M7-F01) e as galerias «Para ver» de M1 e M8 (P16).
 // A legenda do «i»: logo a seguir a ele, ou a seguir à moldura .com-i onde ele vive (P10 nas lições).
 const CAP="(d=>{const n=d.nextElementSibling,m=d.parentElement.classList.contains('com-i')&&d.parentElement.nextElementSibling;return n&&n.tagName==='FIGCAPTION'?n:m&&m.tagName==='FIGCAPTION'?m:null})";
 for(const alvo of [{url:'/pt/m3/licao-m3-f19/'},{url:'/pt/m7/licao-m7-f01/'},{url:'/pt/m1/mapa-do-modulo-m1/',galeria:true},{url:'/pt/m8/mapa-do-modulo-m8/',galeria:true}])for(const width of LARGURAS){
  const ctx=await contexto(b,origem,{viewport:{width,height:860}}),p=await ctx.newPage();await p.goto(origem+alvo.url,{waitUntil:'networkidle'});
  if(alvo.galeria)await p.locator('#galeria > summary').click();await p.locator('details.info-i--linha>summary').first().waitFor();
  const n=await p.evaluate(c=>{const capDe=eval(c);return [...document.querySelectorAll('details.info-i--linha')].filter(d=>capDe(d)&&d.checkVisibility()).length},CAP);
  assert(n>=1,`${alvo.url} ${width}: há «i» «linha» seguidos de legenda`);
  for(let i=0;i<Math.min(n,4);i++){
   const r=await p.evaluate(([k,fc])=>{const capDe=eval(fc),d=[...document.querySelectorAll('details.info-i--linha')].filter(d=>capDe(d)&&d.checkVisibility())[k];d.scrollIntoView({block:'center'});
    const s=d.querySelector(':scope>summary').getBoundingClientRect(),cap=capDe(d),img=d.closest('figure').querySelector('img').getBoundingClientRect(),rg=document.createRange();rg.selectNodeContents(cap);
    const toca=[...rg.getClientRects()].filter(t=>t.width>0&&t.height>0&&!(t.right<=s.left||t.left>=s.right||t.bottom<=s.top||t.top>=s.bottom)).length,c=document.elementFromPoint(s.left+s.width/2,s.top+s.height/2);
    const cr=cap.getBoundingClientRect(),lado=cr.left>=img.right-1;
    return {open:d.open,lado,folga:lado?cr.left-img.right:cr.top-img.bottom,toca,alvo:!!c&&!!c.closest('details.info-i>summary')&&c.closest('details')===d}},[i,CAP]);
   // Com a legenda ao lado da imagem (a casca das lições, a partir de 1024 × 560 px), a folga mede-se na horizontal (22 px).
   assert(!r.open&&r.folga<=(r.lado?24:8)&&r.toca===0&&r.alvo,`${alvo.url} ${width} «i» ${i}: proximidade ${JSON.stringify(r)}`);
  }
  await ctx.close();cenarios++;
 }
 // 9. 06/11/2026: confirmação final do pedido pt-2 (P10). Nas lições de Pessoa, o «i» fica no canto direito da moldura da imagem,
 // mais estreita do que a coluna: com o «i» fechado, nenhuma caixa de linha da legenda («Fernando Pessoa, cerca de 1914.») toca no
 // círculo do «i» nem no seu alvo de 44 px, e a legenda fica inteira, dentro do ecrã e junto da imagem. Em telemóvel de pé (320 × 568,
 // 375 × 667, 390 × 800) e deitado (844 × 390).
 for(const url of ['/pt/m7/licao-m7-f01/','/pt/m7/licao-m7-f05/'])for(const [width,height] of [[320,568],[375,667],[390,800],[844,390]]){
  const ctx=await contexto(b,origem,{viewport:{width,height}}),p=await ctx.newPage(),onde=`${url} ${width}×${height}`;await p.goto(origem+url,{waitUntil:'networkidle'});
  await p.locator('.jogo .ler .fig details.info-i--linha>summary').first().waitFor();
  const r=await p.evaluate(()=>{const d=document.querySelector('.jogo .ler .fig details.info-i--linha');d.scrollIntoView({block:'center'});
   const s=d.querySelector(':scope>summary'),c=s.querySelector(':scope>span').getBoundingClientRect(),a=s.getBoundingClientRect(),cap=d.parentElement.nextElementSibling,img=d.parentElement.querySelector('img').getBoundingClientRect();
   const rg=document.createRange();rg.selectNodeContents(cap);const linhas=[...rg.getClientRects()].filter(t=>t.width>0&&t.height>0);
   const toca=z=>linhas.filter(t=>!(t.right<=z.left||t.left>=z.right||t.bottom<=z.top||t.top>=z.bottom)).length;
   return {open:d.open,tag:cap.tagName,texto:cap.textContent,linhas:linhas.length,circulo:toca(c),alvo:toca(a),dentro:linhas.every(t=>t.left>=-.5&&t.right<=innerWidth+.5),
    folga:cap.getBoundingClientRect().top-img.bottom,rolagem:document.documentElement.scrollWidth>innerWidth+1}});
  assert(!r.open&&r.tag==='FIGCAPTION'&&r.texto==='Fernando Pessoa, cerca de 1914.'&&r.linhas>=1,`${onde}: a legenda inteira, com o «i» fechado ${JSON.stringify(r)}`);
  assert.equal(r.circulo,0,`${onde}: nenhuma linha da legenda toca no círculo do «i» ${JSON.stringify(r)}`);
  assert.equal(r.alvo,0,`${onde}: nenhuma linha da legenda toca no alvo de 44 px do «i» ${JSON.stringify(r)}`);
  assert(r.dentro&&!r.rolagem&&r.folga<=8,`${onde}: a legenda dentro do ecrã e junto da imagem ${JSON.stringify(r)}`);
  await ctx.close();cenarios++;
 }
 console.log(`PASS ${cenarios} cenários da peça «i» (ensaio, P7, P9 a P16)`);
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
