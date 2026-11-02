// 01/11/2026: decisão 83. Estados antigos, continuação, dobras, projeção e impressão.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http'),cp=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.CARTAZ_INDICES_OUTPUT;
// 01/11/2026: o antes desfaz a própria camada, com contagens, mesmo após squash.
const manifest=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/cartaz-indices-edits-20261101.json'),'utf8'));
const before=new Map(Object.entries(manifest.files).map(([f,rec])=>{let text=fs.readFileSync(path.join(root,f),'utf8').replace(/\r\n/g,'\n');for(const e of [...rec.edits].reverse()){assert.equal(text.split(e.new).length-1,e.occurrences,f+' '+e.location);text=text.split(e.new).join(e.old)}return [f,text]}));
const config=n=>JSON.parse(fs.readFileSync(path.join(root,`m${n}/index.html`),'utf8').match(/<script type="application\/json" id="cz-index-route">([\s\S]*?)<\/script>/)[1]);
const server=http.createServer((q,r)=>{let url=new URL(q.url,'http://local'),isBefore=url.pathname.startsWith('/before/'),rel=decodeURIComponent(url.pathname.replace(/^\/(?:before\/)?pt\//,''));if(rel.endsWith('/'))rel+='index.html';let f=path.resolve(root,rel);if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');r.end(isBefore&&before.has(rel)?before.get(rel):fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
function measure(){
 const main=document.querySelector('main'),vis=e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&e.getBoundingClientRect().width>1&&e.getBoundingClientRect().height>1&&!e.closest('[hidden],[aria-hidden="true"],.vh,.sr-only');
 const targets=[...main.querySelectorAll('a,button,summary,[role=button]')].filter(vis),small=targets.filter(e=>{const r=e.getBoundingClientRect();const pseudo=e.matches('.cz-credit a')?getComputedStyle(e,'::before'):null;return pseudo?(parseFloat(pseudo.width)<43.9||parseFloat(pseudo.height)<43.9):(r.width<43.9||r.height<43.9)}).map(e=>({text:e.textContent.trim().slice(0,70),class:e.className,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}));
 const leaves=[...main.querySelectorAll('*')].filter(e=>vis(e)&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
 const tiny=leaves.filter(e=>parseFloat(getComputedStyle(e).fontSize)<12.99).map(e=>({text:e.textContent.trim().slice(0,70),class:e.className,size:getComputedStyle(e).fontSize}));
 const rgb=s=>{const a=s.match(/[\d.]+/g);return a?a.map(Number):[0,0,0,0]},lum=c=>c.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0),contrast=[];
 for(const e of leaves){const c=getComputedStyle(e),fg=rgb(c.color);let bg=[255,255,255];for(let p=e;p;p=p.parentElement){const b=rgb(getComputedStyle(p).backgroundColor);if(b.length===3||b[3]===1){bg=b;break}}const a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05),large=parseFloat(c.fontSize)>=24||(parseFloat(c.fontSize)>=18.66&&+c.fontWeight>=700);if(ratio<(large?3:4.5)-.02)contrast.push({text:e.textContent.trim().slice(0,70),class:e.className,ratio:+ratio.toFixed(2),color:c.color,bg});}
 const next=main.querySelector('[data-module-next]'),r=next.getBoundingClientRect();
 return {rootSize:parseFloat(getComputedStyle(document.documentElement).fontSize),height:document.documentElement.scrollHeight,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),small,tiny,contrast,next:{href:next.getAttribute('href'),text:next.textContent.trim(),height:r.height,y:r.y,visible:vis(next)},counts:[...main.querySelectorAll('[data-prog]')].map(e=>e.textContent.replace(/ · /g,', ')),groups:[...main.querySelectorAll('.grupo-topo h2')].map(e=>parseFloat(getComputedStyle(e).fontSize)),folds:[...main.querySelectorAll('details.cz-fold')].map(e=>({open:e.open,height:e.querySelector('summary').getBoundingClientRect().height})),states:[...main.querySelectorAll('[data-chip]')].map(e=>e.textContent.trim().replace(/^✓/,'')),images:[...main.querySelectorAll('img')].filter(vis).every(e=>e.complete&&e.naturalWidth>0)};
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})}),rows=[],quality=[];if(out)fs.mkdirSync(out,{recursive:true});let cases=0;
try{
for(const n of [1,2,3,4,5,6,7,8,9])for(const width of [320,390,1024,1366])for(const theme of ['light','dark'])for(const mode of ['normal','projection'])for(const state of ['none','half','all']){
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
   assert.deepEqual(pair.after.groups,config(n).map(()=>31*(mode==='projection'?pair.after.rootSize/16:1)),'topos de grupo iguais');
   assert.equal(pair.after.states.filter(s=>s==='A seguir').length,mode==='projection'||state==='all'?0:1);
   assert.equal(pair.after.states.filter(s=>s.startsWith('Feita')).length,mode==='projection'?0:count);
   assert.equal(pair.after.states.filter(s=>s==='por fazer').length,0);
   assert.deepEqual(pair.after.counts,pair.before.counts,'contadores mantidos');assert.equal(pair.after.next.href,pair.before.next.href,'continuação mantida');
   if(mode==='projection'){assert.equal(await p.locator('.cz-index-status').count(),0,'a linha de estado saiu com a caixa (decisão 134, 02/11/2026)');assert(await p.locator('.cz-fold>summary').evaluateAll(es=>es.every(e=>!e.checkVisibility())));assert(await p.locator('.cz-index-fold-state').evaluateAll(es=>es.every(e=>!e.textContent)));}
   if(mode==='normal'&&count){for(const step of steps.slice(0,count).filter(s=>!s.licao))assert.equal(await p.locator('#'+step.id+' [data-cz-state-text]').textContent(),'Feita 01/11');}
   if(state==='none')assert(pair.after.next.text.startsWith('Começar:'));else if(state==='half')assert(pair.after.next.text.startsWith('Continuar:'));
   if(mode==='projection')assert.equal(await p.evaluate(()=>document.querySelector('main').getAnimations({subtree:true}).length),0,'projeção parada');
   if(width<640&&mode==='normal')assert(pair.after.folds.every(f=>f.height===(width<360?72:88)),'bandas de 72 ou 88 px');
   for(const key of ['small','tiny','contrast'])if(pair.after[key].length)quality.push({n,width,theme,mode,state,key,problems:pair.after[key]});
  }
  await ctx.close();
 }
 rows.push(pair);cases++;console.log(`PASS M${n} ${width} ${theme} ${mode} ${state}`);
}
if(out)fs.writeFileSync(path.join(out,'medidas.json'),JSON.stringify(rows,null,2));
assert.deepEqual(quality,[],JSON.stringify(quality));
console.log(`PASS ${cases} pares antes/depois; progresso e continuação preservados.`);
}finally{await browser.close();server.closeAllConnections();server.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
