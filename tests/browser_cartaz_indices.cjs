// 01/11/2026: decisão 83. Estados antigos, continuação, dobras, projeção e impressão.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http'),cp=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.CARTAZ_INDICES_OUTPUT;
// 01/11/2026: o antes desfaz a própria camada, com contagens, mesmo após squash.
const manifest=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cartaz-indices-edits-20261101.json'),'utf8'));
// 02/11/2026: a camada das tarefas individuais (por cima desta) desfaz-se primeiro, também com contagens.
const individuais=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/tarefas-individuais-edits-20261102.json'),'utf8')).files;
// 02/11/2026: retirar o lote 2 com contagens antes da comparação histórica.
const lote2=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/conteudos-lote2-edits-20261101.json'),'utf8')).files;
// 02/11/2026: retirar a camada piloto antes da comparação histórica, com contagem estrita.
const piloto=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cartaz-m4-piloto-edits-20261102.json'),'utf8')).files;
// 05/11/2026: a revisão de 5/11 (a camada mais recente) desfaz-se antes de todas, com contagem estrita.
const revisao=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/revisao-edits-20261105.json'),'utf8')).files;
// 05/11/2026: a decisão 154 (camada autonomia_154_20261105) passa a ser a mais recente e muda os índices do M2, M3, M4, M5, M8 e
// M9; desfaz-se antes da revisão de 5/11, com contagem estrita, e as conferências ficam iguais.
const autonomia=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/autonomia-154-edits-20261105.json'),'utf8')).files;
// 06/11/2026: o desenho comum dos nove índices (decisão 148) é a camada mais recente; desfaz-se antes de todas, com contagem estrita.
const comum148=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cartaz-indices-148-edits-20261106.json'),'utf8')).files;
// 07/11/2026: os três acertos dos índices deixados pela decisão 173 são a camada mais recente; desfazem-se antes de todas, com contagem estrita.
const acertos=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/indices-acertos-edits-20261107.json'),'utf8')).files;
// 06/11/2026: a decisão 152 no M1 (camada cuidado_m1_20261106: a tabela dos pesos e os espaços que não quebram no índice do
// M1). 07/11/2026 (fusão do main 29441e6b no pedido #182): passa a ser a mais recente, por cima dos acertos da decisão 173;
// desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidado=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m1-edits-20261106.json'),'utf8')).files;
// 07/11/2026: os créditos atrás de um «i» na entrada, nos índices e no Atlas (camada creditos_i_pt1_20261107, pedido pt-1) passam a
// ser a camada mais recente, por cima da decisão 152 no M1; desfazem-se antes de todas, com contagem estrita, e as conferências
// ficam iguais.
const creditosPt1=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/creditos-i-pt1-edits-20261107.json'),'utf8')).files;
// 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção (camada cidade_cartaz_20261108, que muda a frase da sugestão
// «continua» dos nove índices) passam a ser a camada mais recente, por cima dos créditos do pedido pt-1; desfazem-se antes de todas,
// com contagem estrita, e as conferências ficam iguais.
const cidadeCartaz=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cidade-cartaz-edits-20261108.json'),'utf8')).files;
// 08/11/2026: a decisão 152 no M2 (camada cuidado_m2_20261108: espaços que não quebram no índice do M2) passa a ser a camada mais
// recente, por cima do cartaz «Ler a cidade»; desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidadoM2=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m2-edits-20261108.json'),'utf8')).files;
// 08/11/2026: a decisão 152 no M3 (camada cuidado_m3_20261108: a tabela dos pesos e os espaços que não quebram no índice do M3) passa
// a ser a camada mais recente, por cima da decisão 152 no M2; desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidadoM3=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m3-edits-20261108.json'),'utf8')).files;
// 08/11/2026: a decisão 152 no M4 (camada cuidado_m4_20261108: os espaços que não quebram no índice do M4) passa a ser a camada mais
// recente, por cima da decisão 152 no M3; desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidadoM4=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m4-edits-20261108.json'),'utf8')).files;
// 08/11/2026: a decisão 152 no M5 (camada cuidado_m5_20261108: a tabela dos pesos e os espaços que não quebram no índice do M5)
// passa a ser a camada mais recente, por cima da decisão 152 no M4; desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidadoM5=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m5-edits-20261108.json'),'utf8')).files;
// 08/11/2026: a decisão 152 no M6 (camada cuidado_m6_20261108: os espaços que não quebram no índice do M6) passa a ser a camada
// mais recente, por cima da decisão 152 no M5; desfaz-se antes de todas, com contagem estrita, e as conferências ficam iguais.
const cuidadoM6=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m6-edits-20261108.json'),'utf8')).files;
// 11/11/2026: a decisão 152 no M7 (camada cuidado_m7_20261111: a tabela dos pesos e os espaços que não quebram no índice do M7) passa a ser a camada
// mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com contagem estrita.
const cuidadoM7=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m7-edits-20261111.json'),'utf8')).files;
// 12/11/2026: a decisão 152 no M8 (camada cuidado_m8_20261112: a tabela dos pesos e os espaços que não quebram no índice do M8) passa a ser a camada
// mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com contagem estrita.
const cuidadoM8=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m8-edits-20261112.json'),'utf8')).files;
// 12/11/2026: a decisão 152 no M9 (camada cuidado_m9_20261112: a tabela dos pesos e os espaços que não quebram no índice do M9) passa a ser a camada
// mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com contagem estrita.
const cuidadoM9=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cuidado-m9-edits-20261112.json'),'utf8')).files;
// 07/11/2026: primeiro a decisão 152 no M1, depois os acertos da decisão 173, depois o desenho comum (decisão 148).
// 07/11/2026: e, antes de tudo, os créditos atrás de um «i» do pedido pt-1.
// 08/11/2026: e, antes ainda, o cartaz «Ler a cidade» e o nome novo da secção.
// 08/11/2026: e, antes de tudo, a decisão 152 no M2.
// 08/11/2026: e, antes ainda, a decisão 152 no M3.
// 08/11/2026: e, antes ainda, a decisão 152 no M4.
// 08/11/2026: e, antes ainda, a decisão 152 no M5.
// 08/11/2026: e, antes ainda, a decisão 152 no M6.
// 11/11/2026: e, antes ainda, a decisão 152 no M7.
// 12/11/2026: e, antes de todas, a decisão 152 no M8.
// 12/11/2026: e, antes de todas, a decisão 152 no M9.
const before=new Map(Object.entries(manifest.files).map(([f,rec])=>{let text=fs.readFileSync(path.join(root,f),'utf8').replace(/\r\n/g,'\n');for(const e of [...((cuidadoM9[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M9 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM8[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M8 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM7[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M7 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM6[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M6 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM5[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M5 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM4[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M4 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM3[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M3 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidadoM2[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 no M2 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cidadeCartaz[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' cartaz «Ler a cidade» '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((creditosPt1[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' créditos atrás de um «i» (pt-1) '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((cuidado[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 152 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((acertos[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' acertos da decisão 173 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((comum148[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 148 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((autonomia[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' decisão 154 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((revisao[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' revisão '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((piloto[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' piloto '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((lote2[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' lote2 '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...((individuais[f]||{}).edits||[])].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' individuais '+e.location);text=text.split(e.new).join(e.old)}for(const e of [...rec.edits].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' '+e.location);text=text.split(e.new).join(e.old)}return [f,text]}));
const config=n=>JSON.parse(fs.readFileSync(path.join(root,`m${n}/index.html`),'utf8').match(/<script type="application\/json" id="cz-index-route">([\s\S]*?)<\/script>/)[1]);
const server=http.createServer((q,r)=>{let url=new URL(q.url,'http://local'),isBefore=url.pathname.startsWith('/before/'),rel=decodeURIComponent(url.pathname.replace(/^\/(?:before\/)?pt\//,''));if(rel.endsWith('/'))rel+='index.html';let f=path.resolve(root,rel);if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');r.end(isBefore&&before.has(rel)?before.get(rel):fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
// 06/11/2026: decisão 148, a medida das bandas também lê a altura do título (o <h2> da unidade passou para a banda nos nove).
// 06/11/2026: decisão 173, cada banda conta as linhas do próprio título de duas maneiras independentes (as caixas de linha do
// texto, agrupadas pelo topo, e a altura do <h2> a dividir pela altura de linha calculada) e diz se o título está cortado:
// conteúdo maior do que a caixa (scrollHeight/scrollWidth), reticências, line-clamp, título escondido ou fora da banda.
function measure(){
 // 06/11/2026: decisão 173, dentro de measure() para correr na página (page.evaluate só leva esta função).
 function bandTitle(e){
  const s=e.querySelector('summary'),t=s.querySelector('h2.cz-fold-t'),sr=s.getBoundingClientRect(),band={open:e.open,height:sr.height,title:null,lines:null,linesByHeight:null,lineHeight:null,clip:['sem título']};if(!t)return band;
  const c=getComputedStyle(t),tr=t.getBoundingClientRect(),lineHeight=parseFloat(c.lineHeight),tops=[],walk=document.createTreeWalker(t,NodeFilter.SHOW_TEXT);let n;
  while(n=walk.nextNode()){if(!n.textContent.trim())continue;const range=document.createRange();range.selectNodeContents(n);for(const r of range.getClientRects())if(r.width>0&&r.height>0)tops.push(r.top)}
  tops.sort((a,b)=>a-b);const lines=[];for(const top of tops)if(!lines.length||top-lines[lines.length-1]>lineHeight/2)lines.push(top);
  const clip=[];if(!t.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))clip.push('escondido');if(t.scrollHeight>t.clientHeight+1)clip.push('scrollHeight '+t.scrollHeight+'>'+t.clientHeight);if(t.scrollWidth>t.clientWidth+1)clip.push('scrollWidth '+t.scrollWidth+'>'+t.clientWidth);if(c.textOverflow==='ellipsis')clip.push('reticências');if(c.webkitLineClamp&&c.webkitLineClamp!=='none')clip.push('line-clamp '+c.webkitLineClamp);if(s.scrollHeight>s.clientHeight+1)clip.push('banda: scrollHeight '+s.scrollHeight+'>'+s.clientHeight);if(tr.top<sr.top-1||tr.bottom>sr.bottom+1||tr.left<sr.left-1||tr.right>sr.right+1)clip.push('título fora da banda');
  // 06/11/2026: decisão 173, revisão de 6/11: cada linha do título tem de se ver no seu centro (elementFromPoint dá o próprio
  // título ou uma parte dele), com o título a meio do ecrã; apanha também um corte ou uma cobertura que venham de um antepassado
  // (overflow, clip-path, max-height no details ou no main) ou de outro elemento. O deslize volta a ficar onde estava.
  const x0=scrollX,y0=scrollY;scrollTo({left:x0,top:y0+tr.top+tr.height/2-innerHeight/2,behavior:'instant'});const seen=document.createTreeWalker(t,NodeFilter.SHOW_TEXT);let m;
  while(m=seen.nextNode()){if(!m.textContent.trim())continue;const range=document.createRange();range.selectNodeContents(m);for(const r of range.getClientRects()){if(!(r.width>0&&r.height>0))continue;const hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);if(!hit||!t.contains(hit))clip.push('linha tapada ou cortada: '+m.textContent.trim().slice(0,40))}}
  scrollTo({left:x0,top:y0,behavior:'instant'});
  return {...band,title:tr.height,lines:lines.length,linesByHeight:Math.round(tr.height/lineHeight),lineHeight,clip};
 }
 const main=document.querySelector('main'),vis=e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&e.getBoundingClientRect().width>1&&e.getBoundingClientRect().height>1&&!e.closest('[hidden],[aria-hidden="true"],.vh,.sr-only');
 const targets=[...main.querySelectorAll('a,button,summary,[role=button]')].filter(vis),small=targets.filter(e=>{const r=e.getBoundingClientRect();const pseudo=e.matches('.cz-credit a')?getComputedStyle(e,'::before'):null;return pseudo?(parseFloat(pseudo.width)<43.9||parseFloat(pseudo.height)<43.9):(r.width<43.9||r.height<43.9)}).map(e=>({text:e.textContent.trim().slice(0,70),class:e.className,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}));
 const leaves=[...main.querySelectorAll('*')].filter(e=>vis(e)&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const tiny=leaves.filter(e=>parseFloat(getComputedStyle(e).fontSize)<12.99).map(e=>({text:e.textContent.trim().slice(0,70),class:e.className,size:getComputedStyle(e).fontSize}));
 const rgb=s=>{const a=s.match(/[\d.]+/g);return a?a.map(Number):[0,0,0,0]},lum=c=>c.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0),contrast=[];
 // 03/11/2026: texto recortado num gradiente usa as cores pintadas; avaliar todas, sem excluir o glifo.
 for(const e of leaves){const c=getComputedStyle(e);let bg=[255,255,255];for(let p=e;p;p=p.parentElement){const b=rgb(getComputedStyle(p).backgroundColor);if(b.length===3||b[3]===1){bg=b;break}}let colors=[c.color];if(c.backgroundClip==='text'&&rgb(c.color)[3]===0&&c.backgroundImage!=='none'){colors=c.backgroundImage.match(/rgba?\([^)]+\)/g)||[];if(!c.backgroundImage.startsWith('linear-gradient(')||!colors.length)throw Error('Pintura de texto sem medição suportada: '+c.backgroundImage)}const large=parseFloat(c.fontSize)>=24||(parseFloat(c.fontSize)>=18.66&&+c.fontWeight>=700);for(const color of colors){const raw=rgb(color),alpha=raw[3]??1,fg=raw.slice(0,3).map((v,i)=>v*alpha+bg[i]*(1-alpha)),a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);if(ratio<(large?3:4.5)-.02)contrast.push({text:e.textContent.trim().slice(0,70),class:e.className,ratio:+ratio.toFixed(2),color,bg});}}

 // 06/11/2026: revisão da decisão 148. A palavra do módulo está aria-hidden (vis() deixa-a de fora), mas vê-se: o contraste dela
 // mede-se à parte, sobre o primeiro fundo opaco, com 4,5:1 abaixo de 24 px e 3:1 a partir daí, e junta-se a contrast.
 const agua=main.querySelector('.cabm>.agua');if(agua&&agua.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&agua.getBoundingClientRect().width>1&&agua.getBoundingClientRect().height>1){const c=getComputedStyle(agua);let bg=[255,255,255];for(let p=agua;p;p=p.parentElement){const b=rgb(getComputedStyle(p).backgroundColor);if(b.length===3||b[3]===1){bg=b;break}}const raw=rgb(c.color),alpha=raw[3]??1,fg=raw.slice(0,3).map((v,i)=>v*alpha+bg[i]*(1-alpha)),a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);if(ratio<(parseFloat(c.fontSize)>=24?3:4.5)-.02)contrast.push({text:agua.textContent.trim().slice(0,70),class:agua.className,ratio:+ratio.toFixed(2),color:c.color,bg});}

 const next=main.querySelector('[data-module-next]'),r=next.getBoundingClientRect();
 // 06/11/2026: decisão 148, cada banda devolve também a altura do seu título (para a medida exata das bandas no telemóvel).
 // 06/11/2026: decisão 173, e também as linhas do título contadas nas duas maneiras e o que o corta (bandTitle, acima).
 return {rootSize:parseFloat(getComputedStyle(document.documentElement).fontSize),height:document.documentElement.scrollHeight,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),small,tiny,contrast,next:{href:next.getAttribute('href'),text:next.textContent.trim(),height:r.height,y:r.y,visible:vis(next)},counts:[...main.querySelectorAll('[data-prog]')].map(e=>e.textContent.replace(/ · /g,', ')),groups:[...main.querySelectorAll('.grupo-topo h2,summary h2.cz-fold-t')].map(e=>parseFloat(getComputedStyle(e).fontSize)),folds:[...main.querySelectorAll('details.cz-fold')].map(bandTitle),states:[...main.querySelectorAll('[data-chip]')].map(e=>e.textContent.trim().replace(/^✓/,'')),images:[...main.querySelectorAll('img')].filter(vis).every(e=>e.complete&&e.naturalWidth>0)};
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})}),rows=[],quality=[];if(out)fs.mkdirSync(out,{recursive:true});let cases=0;
try{
// 03/11/2026: a medição rejeita cada paragem de contraste baixo e texto transparente sem pintura.
{const p=await browser.newPage();await p.setContent('<main style="background:rgb(37,39,34)"><h1><span class="contrast-probe" style="font:39px Arial;color:transparent;background-clip:text">Â</span></h1><a data-module-next href="#">Continuar</a></main>');for(const [paint,bad] of [['linear-gradient(rgb(228,85,92) 20%,rgb(245,241,231) 20%)',false],['linear-gradient(rgb(40,40,40) 20%,rgb(245,241,231) 20%)',true],['linear-gradient(rgb(228,85,92) 20%,rgb(40,40,40) 20%)',true],['none',true]]){await p.locator('.contrast-probe').evaluate((e,v)=>e.style.backgroundImage=v,paint);assert.equal((await p.evaluate(measure)).contrast.some(x=>x.class==='contrast-probe'),bad,paint)}await p.close();console.log('PASS contraste: duas cores medidas, cada falha detetada')}
// 06/11/2026: revisão da decisão 148, a sonda da palavra do módulo: o vermelho do escuro (#e4555c, 4,13:1 sobre #252722) com 20 px
// falha, com 24 px passa (texto grande); #f07075 com 20 px passa.
{const p=await browser.newPage();for(const [style,bad] of [['font:20px Arial;color:rgb(228,85,92)',true],['font:24px Arial;color:rgb(228,85,92)',false],['font:20px Arial;color:rgb(240,112,117)',false]]){await p.setContent(`<body style="background:rgb(37,39,34)"><main><header class="cabm"><span class="agua" aria-hidden="true" style="${style}">voz</span><h1>Título</h1></header><a data-module-next href="#">Continuar</a></main></body>`);assert.equal((await p.evaluate(measure)).contrast.some(x=>x.class==='agua'),bad,style)}await p.close();console.log('PASS contraste: a palavra do módulo também se mede')}
// 06/11/2026: decisão 173, revisão de 6/11, a sonda do corte vindo de fora do título: um clip-path ou um overflow com max-height
// no details da banda escondem a segunda linha sem mexer no título nem na banda, e a medição tem de o apanhar; sem eles, não.
{const p=await browser.newPage();await p.setViewportSize({width:320,height:600});for(const [style,bad] of [['clip-path:inset(0 0 50% 0)',true],['overflow:hidden;max-height:60px',true],['',false]]){await p.setContent(`<main><details class="cz-fold" style="${style}"><summary style="display:block;padding:16px 0"><h2 class="cz-fold-t" style="margin:0;font:31px/34px Arial">Um título que se parte em mais linhas</h2></summary></details><a data-module-next href="#">Continuar</a></main>`);const f=(await p.evaluate(measure)).folds[0];assert(f.lines>=2,JSON.stringify(f));assert.equal(f.clip.some(c=>c.startsWith('linha tapada ou cortada')),bad,style+' '+JSON.stringify(f))}await p.close();console.log('PASS título: o corte vindo de um antepassado também se apanha')}
// 06/11/2026: revisão da decisão 148, também a 768 px (entre 640 e 876 px a terceira coluna de «Neste módulo» chegou a sair do ecrã).
for(const n of [1,2,3,4,5,6,7,8,9])for(const width of [320,390,768,1024,1366])for(const theme of ['light','dark'])for(const mode of ['normal','projection'])for(const state of ['none','half','all']){
 const steps=config(n).flatMap(u=>u.passos),count=state==='all'?steps.length:state==='half'?Math.floor(steps.length/2):0,seed={};
 steps.slice(0,count).forEach((s,i)=>{const value=i%2?{lida:true,fim:true,n:10,i:10}:{lida:true,fim:true,n:10,i:10,t:Date.UTC(2026,10,1,12)};if(s.licao)seed['licao-'+s.licao]=JSON.stringify(value);else{const longos=JSON.parse(seed['epi-pt-longos']||'{"feitas":{}}');for(const id of s.exs||[])longos.feitas[id]=Date.UTC(2026,10,1,12);seed['epi-pt-longos']=JSON.stringify(longos)}});
 seed[`percurso-M${n}-antes-unidades`]=JSON.stringify({legado:true,feito:1});
 const pair={n,width,theme,mode,state};
 for(const variant of ['before','after']){
  const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'no-preference'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
  await ctx.route('**/*',async route=>{const u=new URL(route.request().url());if(u.origin===origin)return route.continue();if(u.hostname==='pedrohfernandes-klk.github.io'&&u.pathname.startsWith('/pt/')){const response=await ctx.request.get(origin+u.pathname+u.search);return route.fulfill({response})}return route.abort()});
  await p.addInitScript(seed=>{for(const [k,v] of Object.entries(seed))localStorage.setItem(k,v)},seed);
  await p.goto(origin+(variant==='before'?'/before':'')+`/pt/m${n}/`+(mode==='projection'?'?projetar=1':''),{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.EPICartaz?.motion?.stop());
  assert.equal(await p.locator('main [data-module-next]').count(),1,`${variant} M${n}: ${p.url()} ${String(await p.locator('main').innerHTML()).slice(0,300)}`);pair[variant]=await p.evaluate(measure);assert.deepEqual(errors,[],`M${n} ${variant} JS`);
  assert.equal(pair[variant].overflow,0,`M${n} ${width} ${variant} deslize`);
  for(const [k,v] of Object.entries(seed))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,'progresso antigo intacto');
  if(out&&state==='none'&&mode==='normal'&&[390,1366].includes(width))await p.screenshot({path:path.join(out,`m${n}-${width}-${theme}-${variant}.png`),fullPage:true});
  if(variant==='after'){
   assert(pair.after.next.height>=48,'ação de 48 px');assert(pair.after.next.visible,'ação visível');assert.equal(await p.locator('.module-entry a').count(),1,'ação única');assert.equal(await p.locator('.cz-next').count(),0,'sem a caixa «A seguir» (decisão 134, 02/11/2026)');
   // 01/11/2026: conserva também o limite UX-06 da primeira ação no telemóvel.
   if(width===320&&mode==='normal'&&state==='none')assert(pair.after.next.y<600,'primeira ação antes de 600 px');
   // 02/11/2026: o molde piloto tem h2 no summary, 31/39 px; mesmas três unidades e escala da raiz.
   // 06/11/2026: decisão 148, o mesmo para os nove (sem exceção para o M4): o <h2> da banda tem 31 px abaixo de 640 px e 39 px a partir daí.
   assert.deepEqual(pair.after.groups,config(n).map(()=>(width>=640?39:31)*(mode==='projection'?pair.after.rootSize/16:1)),'topos de grupo iguais');
   assert.equal(pair.after.states.filter(s=>s==='A seguir').length,mode==='projection'||state==='all'?0:1);
   assert.equal(pair.after.states.filter(s=>s.startsWith('Feita')).length,mode==='projection'?0:count);
   assert.equal(pair.after.states.filter(s=>s==='por fazer').length,0);
   assert.deepEqual(pair.after.counts,pair.before.counts,'contadores mantidos');assert.equal(pair.after.next.href,pair.before.next.href,'continuação mantida');
   if(mode==='projection'){assert.equal(await p.locator('.cz-index-status').count(),0,'a linha de estado saiu com a caixa (decisão 134, 02/11/2026)');/* 06/11/2026: decisão 148, o mesmo para os nove: a banda leva o título da unidade e vê-se também na projeção. */assert(await p.locator('.cz-fold>summary').evaluateAll(es=>es.length>0&&es.every(e=>e.checkVisibility()&&e.querySelector('h2.cz-fold-t').checkVisibility())));assert(await p.locator('.cz-index-fold-state').evaluateAll(es=>es.every(e=>!e.textContent)));}
   if(mode==='normal'&&count){for(const step of steps.slice(0,count).filter(s=>!s.licao))assert.equal(await p.locator('#'+step.id+' [data-cz-state-text]').textContent(),'Feita 01/11');}
   if(state==='none')assert(pair.after.next.text.startsWith('Começar:'));else if(state==='half')assert(pair.after.next.text.startsWith('Continuar:'));
   if(mode==='projection')assert.equal(await p.evaluate(()=>document.querySelector('main').getAnimations({subtree:true}).length),0,'projeção parada');
   // 06/11/2026: decisão 148, exato nos nove (sem «+34 px por linha»): sai o «>= 88» do M4 e a banda tem 72 px abaixo de 360 px e
   // 88 px a partir daí, em todos os índices, como antes do #166.
   // 06/11/2026: decisão 173, a banda cresce para mostrar o título inteiro, como o M4 publicado: 72 px abaixo de 360 px ou 88 px,
   // mais exatamente 34 px (a altura de linha do título) por cada linha a mais do título, contada no próprio título.
   if(width<640&&mode==='normal')assert(pair.after.folds.every(f=>f.lines>=1&&f.lines===f.linesByHeight&&f.lineHeight===34&&f.height===(width<360?72:88)+34*(f.lines-1)),'bandas de 72 ou 88 px, mais 34 px por linha a mais do título: '+JSON.stringify(pair.after.folds));
   // 06/11/2026: decisão 173, o título da banda nunca é cortado, encurtado com reticências nem escondido, em nenhuma largura nem modo.
   assert(pair.after.folds.length>0&&pair.after.folds.every(f=>f.title>0&&f.lines>=1&&f.lines===f.linesByHeight&&f.clip.length===0),'título inteiro na banda: '+JSON.stringify(pair.after.folds));
   for(const key of ['small','tiny','contrast'])if(pair.after[key].length)quality.push({n,width,theme,mode,state,key,problems:pair.after[key]});
  }
  await ctx.close();
 }
 rows.push(pair);cases++;console.log(`PASS M${n} ${width} ${theme} ${mode} ${state}`);
}
// 06/11/2026: decisão 173, revisão de 6/11: as bandas também em larguras fracionárias, com o zoom nativo do Chromium completo (o
// «headless shell» ignora o zoom do perfil): uma janela de 539 px a 150 % dá 359,33 px CSS (abaixo de 360 px: 72 px mais 34 px por
// linha a mais) e uma de 799 px a 125 % dá 639,2 px (88 px mais 34 px por linha a mais). Com (max-width:359px) e (max-width:639px),
// estas larguras ficavam sem regra (no M3, a 359,33 px, as bandas davam 88 e 122 px).
const os=require('node:os');
for(const [factor,janela,base,top] of [[1.5,539,72,360],[1.25,799,88,640]]){const profile=fs.mkdtempSync(path.join(os.tmpdir(),'cartaz-indices-zoom-'));fs.mkdirSync(path.join(profile,'Default'));fs.writeFileSync(path.join(profile,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(factor)/Math.log(1.2)}}}));const z=await chromium.launchPersistentContext(profile,{headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{channel:'chromium'}),viewport:null,args:[`--window-size=${janela},900`]});
 try{await z.route('**/*',async route=>{const u=new URL(route.request().url());if(u.origin===origin)return route.continue();if(u.hostname==='pedrohfernandes-klk.github.io'&&u.pathname.startsWith('/pt/')){const response=await z.request.get(origin+u.pathname+u.search);return route.fulfill({response})}return route.abort()});const p=await z.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
  for(const n of [1,2,3,4,5,6,7,8,9]){await p.goto(origin+`/pt/m${n}/`,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.EPICartaz?.motion?.stop());const w=await p.evaluate(()=>visualViewport.width),m=await p.evaluate(measure),at=`M${n} zoom ${factor*100} % ${w} px`;
   assert(w>top-1&&w<top,at+': largura fracionária');assert.equal(m.overflow,0,at+' deslize');
   assert(m.folds.length>0&&m.folds.every(f=>f.lines>=1&&f.lines===f.linesByHeight&&f.lineHeight===34&&f.height===base+34*(f.lines-1)),at+': bandas de '+base+' px, mais 34 px por linha a mais do título: '+JSON.stringify(m.folds));
   assert(m.folds.every(f=>f.title>0&&f.clip.length===0),at+': título inteiro na banda: '+JSON.stringify(m.folds));console.log('PASS bandas',at)}
  assert.deepEqual(errors,[])}finally{await z.close();assert(path.resolve(profile).startsWith(path.resolve(os.tmpdir())+path.sep)&&path.basename(profile).startsWith('cartaz-indices-zoom-'));fs.rmSync(profile,{recursive:true,force:true})}}
if(out)fs.writeFileSync(path.join(out,'medidas.json'),JSON.stringify(rows,null,2));
assert.deepEqual(quality,[],JSON.stringify(quality));
console.log(`PASS ${cases} pares antes/depois; progresso e continuação preservados.`);
}finally{await browser.close();server.closeAllConnections();server.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
