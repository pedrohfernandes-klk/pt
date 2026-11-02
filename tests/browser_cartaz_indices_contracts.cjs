// 01/11/2026: sem JavaScript, teclado, âncoras, impressão e eventos reais de conclusão.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright'),root=path.resolve(__dirname,'..'),out=process.env.CARTAZ_INDICES_OUTPUT;
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://local').pathname.replace(/^\/pt\//,'')),f=path.resolve(root,rel);if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
const action=()=>{const a=document.querySelector('[data-module-next]'),r=a.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);let visible=true;for(let p=a;p;p=p.parentElement){const c=getComputedStyle(p);if(c.display==='none'||c.visibility==='hidden'||+c.opacity!==1)visible=false}return {visible,hit:a===hit||a.contains(hit),height:r.height}};
const quiet=()=>{const main=document.querySelector('main'),bad=[];for(const e of main.querySelectorAll('*'))for(const pseudo of [null,'::before','::after']){const c=getComputedStyle(e,pseudo);if(c.animationName!=='none'||c.transitionDuration.split(',').some(t=>parseFloat(t)>0))bad.push([e.className,pseudo,c.animationName,c.transitionDuration])}return {active:main.getAnimations({subtree:true}).length,bad}};
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,b=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let scenarios=0;try{
async function context(options){const ctx=await b.newContext(options);await ctx.route('**/*',async r=>{const u=new URL(r.request().url());if(u.origin===origin)return r.continue();if(u.hostname==='pedrohfernandes-klk.github.io'&&u.pathname.startsWith('/pt/')){const response=await ctx.request.get(origin+u.pathname+u.search);return r.fulfill({response})}return r.abort()});return ctx}
for(let n=1;n<=9;n++){
 // 01/11/2026: a ação inteira cabe no primeiro ecrã pequeno, nos três estados.
 for(const [width,height] of [[320,568],[360,560],[375,548]])for(const theme of ['light','dark'])for(const progress of ['none','half','all']){
  const ctx=await context({viewport:{width,height},colorScheme:theme,reducedMotion:'reduce'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
  const html=fs.readFileSync(path.join(root,`m${n}/index.html`),'utf8'),steps=JSON.parse(html.match(/<script type="application\/json" id="cz-index-route">([\s\S]*?)<\/script>/)[1]).flatMap(u=>u.passos);
  await p.addInitScript(({steps,progress})=>{const count=progress==='all'?steps.length:progress==='half'?Math.floor(steps.length/2):0,longos={feitas:{}};for(const s of steps.slice(0,count)){if(s.licao)localStorage.setItem('licao-'+s.licao,JSON.stringify({lida:true,t:Date.UTC(2026,10,1,12)}));else for(const id of s.exs||[])longos.feitas[id]=Date.UTC(2026,10,1,12)}localStorage.setItem('epi-pt-longos',JSON.stringify(longos))},{steps,progress});
  await p.goto(`${origin}/pt/m${n}/`,{waitUntil:'load'});
  const box=await p.locator('[data-module-next]').boundingBox();assert(box.y<600);assert(box.y+box.height<=height,`M${n} ${width} ${theme} ${progress}: ${JSON.stringify(box)}`);assert((await p.evaluate(action)).hit,'ação sem sobreposição');assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);
  await ctx.close();scenarios++;
 }
 for(const width of [390,1366])for(const theme of ['light','dark'])for(const js of [false,true]){
  const ctx=await context({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce',javaScriptEnabled:js}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));await p.goto(`${origin}/pt/m${n}/`,{waitUntil:'load'});
  assert.deepEqual(await p.evaluate(quiet),{active:0,bad:[]},'movimento reduzido e sem JS');
  const folds=p.locator('details.cz-fold'),count=await folds.count();assert(count>=2);
  if(!js)assert(await folds.evaluateAll(es=>es.every(e=>e.open)),'sem JS: todas as unidades abertas');
  if(js&&width===390){const last=folds.last();await last.locator(':scope > summary').focus();const was=await last.getAttribute('open');await p.keyboard.press('Enter');assert.notEqual(await last.getAttribute('open'),was,'dobra pelo teclado');
   const id=await last.locator('h2').getAttribute('id');await p.goto(`${origin}/pt/m${n}/#${id}`,{waitUntil:'load'});assert(await last.evaluate(e=>e.open),'âncora abre a unidade');assert(await last.locator('h2').isVisible(),'título da âncora visível');
  }
  await p.emulateMedia({media:'print'});if(js)await p.evaluate(()=>dispatchEvent(new Event('beforeprint')));
  assert.equal(await p.locator('.passos>li').evaluateAll(es=>es.filter(e=>e.checkVisibility()).length),await p.locator('.passos>li').count(),'impressão inclui todas as linhas');
  assert.equal(await p.locator('.prova-esperada').evaluateAll(es=>es.filter(e=>e.checkVisibility()).length),count,'impressão inclui todas as provas');
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'impressão sem corte horizontal');
  if(out&&js&&width===1366&&theme==='light')await p.pdf({path:path.join(out,`m${n}-indice-impressao.pdf`),format:'A4',printBackground:true});
  assert.deepEqual(errors,[]);await ctx.close();scenarios++;
 }
 // Mapa independente: não é reescrito, mas a impressão também é conferida.
 const ctx=await context({viewport:{width:1024,height:900},reducedMotion:'reduce'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
 await p.goto(`${origin}/pt/m${n}/mapa-do-modulo-m${n}/`,{waitUntil:'load'});await p.emulateMedia({media:'print'});assert(await p.locator('h1').isVisible());assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'mapa impresso sem corte');if(out)await p.pdf({path:path.join(out,`m${n}-mapa-impressao.pdf`),format:'A4',printBackground:true});assert.deepEqual(errors,[]);await ctx.close();scenarios++;
 // Movimento normal: ação disponível no primeiro fotograma e só conclusão nova acende.
 const move=await context({viewport:{width:390,height:900},reducedMotion:'no-preference'}),page=await move.newPage();await page.addInitScript(source=>{const old=DOMTokenList.prototype.add;DOMTokenList.prototype.add=function(...t){if(t.includes('cz-motion-active')&&!window.__czFirst)window.__czFirst=(0,eval)('('+source+')')();return old.apply(this,t)}},action.toString());
 await page.goto(`${origin}/pt/m${n}/`,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);const first=await page.evaluate(()=>window.__czFirst);assert(first?.visible&&first.hit&&first.height>=48,'primeira ação a 0 ms');await page.waitForTimeout(850);
 const result=await page.evaluate(()=>{const step=JSON.parse(document.getElementById('cz-index-route').textContent)[0].passos.find(s=>s.licao),row=document.getElementById(step.id);localStorage.setItem('licao-'+step.licao,JSON.stringify({lida:true,t:Date.UTC(2026,10,1,12)}));dispatchEvent(new Event('focus'));return {text:row.querySelector('[data-chip]').textContent,animations:row.getAnimations({subtree:true}).length}});assert(result.text.includes('Feita 01/11'));assert.equal(result.animations,1,'uma conclusão acende uma vez');
 await page.waitForTimeout(300);await page.evaluate(()=>dispatchEvent(new Event('focus')));assert.equal(await page.locator('.cz-next').evaluate(e=>e.getAnimations({subtree:true}).length),0);assert.equal(await page.locator('.cz-motion-point').evaluateAll(es=>es.reduce((n,e)=>n+e.getAnimations({subtree:true}).length,0)),0,'visita não repete');await move.close();scenarios++;
 console.log(`PASS M${n}: sem JS, teclado, âncora, impressão, ação imediata e conclusão única`);
}
console.log(`PASS ${scenarios} cenários de contratos e impressão`);
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
