// 01/11/2026: contratos de movimento, geometria, gesto, teclado e contraparte parada.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http'),cp=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),site=cp.execFileSync('git',['config','--get','remote.origin.url'],{cwd:root,encoding:'utf8'}).trim().split('/').pop().replace(/\.git$/,'');
const server=http.createServer((q,r)=>{let p=new URL(q.url,'http://local').pathname.replace(new RegExp('^/'+site+'/'),'/'),f=path.resolve(root,'.'+p);if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f));}catch{r.writeHead(404);r.end();}});
const zero=()=>{const problems=[];for(const el of document.querySelectorAll('[data-cz-motion-region],[data-cz-motion-region] *,.epi-ampliar,.epi-ampliar *'))for(const pseudo of [null,'::before','::after']){const c=getComputedStyle(el,pseudo);if(c.animationName!=='none'||c.transitionDuration.split(',').some(t=>parseFloat(t)>0))problems.push([el.className,pseudo,c.animationName,c.transitionDuration]);}return {active:document.getAnimations().length,problems};};
const action=()=>{const a=document.getElementById('primeira-acao'),r=a.getBoundingClientRect(),top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);let visible=true;for(let e=a;e;e=e.parentElement){const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden'||+c.opacity!==1||c.pointerEvents==='none')visible=false;}return {visible,hit:top===a||a.contains(top),width:r.width,height:r.height};};
// 02/11/2026: revisão curta do pt #151 (achado 5). Limite de cada animação por peça, em ms: título e cartaz, 200 por parte;
// linha, número e restantes, 350 (respostas a gestos até 350 ms, decisão 112). timing() lê o fim e os ciclos de cada animação.
const LIMIT={title:200,poster:200,line:350,number:350},REST=350;
const timing=(e,limit)=>{const all=e.getAnimations({subtree:true}).map(a=>{const t=a.effect.getComputedTiming();return {name:a.animationName,end:t.endTime,iterations:t.iterations};});return {count:all.length,bad:all.filter(t=>!(t.end<=limit&&t.iterations===1))};};
const geometry=()=>[...document.querySelectorAll('h1,h2,h3,p,button,a,summary,.demo-example,.epi-ampliar')].filter(e=>!e.closest('[aria-hidden="true"]')&&e.getBoundingClientRect().height).map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(n=>Math.round(n*100)/100)});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,url=origin+'/'+site+'/demonstracoes/cartaz-animacoes/';const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let scenarios=0,gestures=0;
try{
for(const width of [320,390,1366])for(const theme of ['light','dark'])for(const mode of ['normal','reduce','projection','simulation-reduce','simulation-projection','no-js']){
const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:mode==='reduce'?'reduce':'no-preference',javaScriptEnabled:mode!=='no-js'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(String(e)));
await ctx.route('**/*',route=>route.request().url().startsWith(origin)?route.continue():route.abort());
if(mode!=='no-js')await p.addInitScript(({theme,mode,source})=>{const setup=()=>{if(!document.documentElement)return false;document.documentElement.dataset.theme=theme;if(mode==='simulation-reduce')document.documentElement.setAttribute('data-cz-reduce','');if(mode==='simulation-projection')document.documentElement.setAttribute('data-cz-projection','');return true;};if(!setup()){const o=new MutationObserver(()=>{if(setup())o.disconnect()});o.observe(document,{childList:true});}const old=DOMTokenList.prototype.add;DOMTokenList.prototype.add=function(...tokens){if(tokens.includes('cz-motion-active')&&!window.__firstAction)window.__firstAction=(0,eval)('('+source+')')();return old.apply(this,tokens);};},{theme,mode,source:action.toString()});
await p.goto(url+(mode==='projection'?'?projetar=1':''),{waitUntil:'load'});
await p.evaluate(()=>{window.__viewerEvents=[];for(const type of ['epi-ampliar-aberto','epi-ampliar-fechado'])document.addEventListener(type,e=>window.__viewerEvents.push({type,image:e.detail instanceof HTMLImageElement&&e.detail.classList.contains('epi-ampliar__img'),time:performance.now()}));});
const first=await p.evaluate(action);assert(first.visible&&first.hit&&first.height>=48,JSON.stringify({width,mode,first}));
assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'largura');
assert.equal(await p.locator('meta[name=robots]').getAttribute('content'),'noindex,nofollow');
assert.equal(await p.locator('img').evaluateAll(es=>es.every(e=>e.complete&&e.naturalWidth>0)),true,'imagens locais');
if(mode!=='normal'){
 assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]},mode);
 if(mode!=='no-js'){
  for(const k of ['title','poster','line','correct','error','number']){await p.locator(`[data-play="${k}"]`).click();assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]},mode+' '+k);gestures++;}
  await p.locator('[data-play=point]').click();assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]});
  await p.locator('[data-viewer]').click();await p.waitForFunction(()=>window.__viewerEvents.length===1);assert.equal(await p.locator('.epi-ampliar').evaluate(e=>e.getAttribute('aria-modal')==='true'),true);assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]});await p.keyboard.press('Escape');assert.equal(await p.locator('.epi-ampliar').count(),0,'fecho imediato sem movimento');assert.equal(await p.locator('[data-viewer]').evaluate(e=>e===document.activeElement),true);assert.deepEqual(await p.evaluate(()=>window.__viewerEvents.map(e=>[e.type,e.image])),[['epi-ampliar-aberto',true],['epi-ampliar-fechado',true]]);
 }else assert.equal(await p.locator('details').evaluateAll(es=>es.every(e=>e.open)),true,'sem JS: conteúdo aberto');
}else{
 const atZero=await p.evaluate(()=>window.__firstAction);assert(atZero?.visible&&atZero.hit,'primeira ação no instante em que começa o movimento');
 await p.waitForFunction(()=>document.getAnimations().length===0);
 if(process.env.CARTAZ_CAPTURE_DIR&&[390,1366].includes(width)){fs.mkdirSync(process.env.CARTAZ_CAPTURE_DIR,{recursive:true});await p.screenshot({path:path.join(process.env.CARTAZ_CAPTURE_DIR,`${site}-${width}-${theme}.png`),fullPage:true});}
 // Não basta confirmar o resultado: mede o que acontece durante cada transição.
 for(const kind of ['title','poster','line','correct','error','number','point']){
  const button=p.locator(`[data-play="${kind}"]`);await button.scrollIntoViewIfNeeded();const before=await p.evaluate(geometry);await button.click();
  assert((await p.locator(`[data-example="${kind}"]`).first().evaluate(e=>e.getAnimations({subtree:true}).length))>0,kind+' anima');
  // 02/11/2026: revisão curta do pt #151 (achado 5). Cada animação da peça acaba dentro do limite e corre uma só vez.
  assert.deepEqual((await p.locator(`[data-example="${kind}"]`).first().evaluate(timing,LIMIT[kind]||REST)).bad,[],kind+' tempo e ciclos');
  for(const fraction of [.1,.5,.9]){await p.locator(`[data-example="${kind}"]`).first().evaluate((e,f)=>{for(const a of e.getAnimations({subtree:true})){a.pause();a.currentTime=Number(a.effect.getTiming().duration)*f;}},fraction);assert.deepEqual(await p.evaluate(geometry),before,kind+' geometria');}
  // 02/11/2026: revisão curta do pt #151 (achado 10). As animações que o teste pausou ficavam vivas depois de stop() no
  // Chromium 1194; cancelam-se aqui, antes de stop().
  await p.evaluate(()=>document.getAnimations().forEach(a=>{if(a.playState==='paused')a.cancel()}));
  await p.evaluate(()=>EPICartaz.motion.stop());assert.deepEqual(await p.evaluate(geometry),before,kind+' fim');gestures++;
 }
 // 02/11/2026: revisão curta do pt #151 (achado 5). Nada se esconde enquanto anima: em cada parte do título e do cartaz, a
 // 10 % do tempo, a opacidade calculada é pelo menos 0,5; cada parte acaba dentro de 200 ms e corre uma só vez.
 for(const kind of ['title','poster'])assert.deepEqual(await p.locator(`[data-example="${kind}"]:not([data-cz-static])`).evaluate((region,limit)=>region.querySelectorAll('.cz-motion-part').length>0&&[...region.querySelectorAll('.cz-motion-part')].map(part=>{part.classList.add('cz-motion-active');const all=part.getAnimations(),out=all.length?all.map(a=>{const t=a.effect.getComputedTiming();a.pause();a.currentTime=t.endTime*.1;const opacity=+getComputedStyle(part).opacity;a.cancel();return {part:part.textContent,opacity,end:t.endTime,iterations:t.iterations};}).filter(t=>!(t.opacity>=.5&&t.end<=limit&&t.iterations===1)):[{part:part.textContent,animations:0}];part.classList.remove('cz-motion-active');return out;}).flat(),LIMIT[kind]),[],kind+' partes visíveis a 10 %');
 // A conclusão é uma transição fornecida pelo adaptador, nunca uma visita.
 await p.locator('[data-play=point]').click();assert.equal(await p.locator('[data-example=point]').first().evaluate(e=>e.getAnimations({subtree:true}).length),0,'não repete conclusão');
 const state=await p.evaluate(()=>{const e=document.querySelector('.cz-motion-point');return EPICartaz.motion.complete(e,{before:true,after:true,event:'visita'})});assert.equal(state,false);
 assert.equal((await p.locator('[data-example=number]').first().ariaSnapshot()).includes('7 de 14 concluídos'),true,'estado final acessível');
 assert.equal(await p.locator('[aria-live]').count(),0,'sem anúncios repetidos');
 // Concorrência rejeitada, inclusive em regiões encaixadas; não há fila atrasada.
 assert.deepEqual(await p.evaluate(()=>{const a=document.querySelector('.cz-motion-title'),r=a.closest('[data-cz-motion-region]');const b=document.createElement('div');b.dataset.czMotionRegion='';b.innerHTML='<p class="cz-motion-correct">Outra resposta</p>';r.append(b);const one=EPICartaz.motion.play(a),two=EPICartaz.motion.play(b.firstChild),count=r.getAnimations({subtree:true}).length;EPICartaz.motion.stop();b.remove();return [one,two,count]}),[true,false,1]);
 // 02/11/2026: revisão curta do pt #151 (achados 2 e 4). Duas regiões irmãs animam ao mesmo tempo: play(título) e play(linha
 // na outra região) devolvem [true,true] e as duas regiões têm animações ativas.
 assert.deepEqual(await p.evaluate(()=>{const t=document.querySelector('[data-example="title"]:not([data-cz-static]) .cz-motion-title'),l=document.querySelector('[data-example="line"]:not([data-cz-static]) .cz-motion-line');const played=[EPICartaz.motion.play(t),EPICartaz.motion.play(l)],animating=[t,l].map(e=>e.closest('[data-cz-motion-region]').getAnimations({subtree:true}).length>0);EPICartaz.motion.stop();return {played,animating};}),{played:[true,true],animating:[true,true]});
 // Mesmo uma marcação indevida na região proibida não pode fazê-la animar.
 assert.deepEqual(await p.evaluate(()=>{const e=document.querySelector('.cz-next');e.classList.add('cz-motion-correct');const accepted=EPICartaz.motion.play(e);e.classList.add('cz-motion-active');const n=e.getAnimations({subtree:true}).length;e.classList.remove('cz-motion-active','cz-motion-correct');return [accepted,n]}),[false,0]);
 const fold=p.locator('[data-example=fold]:not([data-cz-static]) details');await fold.locator('summary').click();await fold.locator('summary').click();await p.waitForTimeout(20);
 // 02/11/2026: revisão curta do pt #151 (achado 5). A dobra anima, acaba dentro de 350 ms e corre uma só vez.
 {const t=await p.locator('[data-example=fold]:not([data-cz-static])').evaluate(timing,REST);assert(t.count>0&&!t.bad.length,'dobra tempo e ciclos '+JSON.stringify(t));}
 const opened=await p.evaluate(geometry);await p.waitForTimeout(220);assert.deepEqual(await p.evaluate(geometry),opened,'dobra sem altura animada');
 // 02/11/2026: revisão curta do pt #151 (achado 11). Sem a classe ativa, o visor repousa opaco: nunca fica translúcido.
 assert.equal(await p.evaluate(()=>{const v=document.createElement('div');v.className='epi-ampliar cz-motion-viewer';document.body.append(v);const o=getComputedStyle(v).opacity;v.remove();return o;}),'1','visor em repouso opaco');
 await p.locator('[data-viewer]').click();await p.waitForFunction(()=>window.__viewerEvents.length===1);assert.equal(await p.locator('.epi-ampliar').evaluate(e=>e.getAttribute('aria-modal')==='true'),true);
 // 02/11/2026: revisão curta do pt #151 (achados 5 e 11). O visor entra por @keyframes: anima, acaba dentro de 350 ms e corre
 // uma só vez.
 {const t=await p.locator('.epi-ampliar').evaluate(timing,REST);assert(t.count>0&&!t.bad.length,'visor tempo e ciclos '+JSON.stringify(t));}
 const viewer=await p.evaluate(geometry);await p.waitForTimeout(220);assert.deepEqual(await p.evaluate(geometry),viewer,'visor sem deslocação');await p.keyboard.press('Tab');assert.equal(await p.locator('.epi-ampliar button').evaluate(e=>e===document.activeElement),true,'teclado no visor');const closeTime=await p.evaluate(()=>performance.now());await p.keyboard.press('Escape');await p.waitForFunction(()=>!document.querySelector('.epi-ampliar'));assert.equal(await p.locator('[data-viewer]').evaluate(e=>e===document.activeElement),true,'foco regressa');const events=await p.evaluate(()=>window.__viewerEvents);assert.deepEqual(events.map(e=>[e.type,e.image]),[['epi-ampliar-aberto',true],['epi-ampliar-fechado',true]]);assert(events[1].time-closeTime<=350,'fecho dentro do contrato de 350 ms');
 // Preferência ou projeção ligada durante uma animação termina no estado final.
 await p.evaluate(()=>{EPICartaz.motion.play(document.querySelector('.cz-motion-title'));document.documentElement.setAttribute('data-cz-reduce','');EPICartaz.motion.sync();});assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]});
 await p.evaluate(()=>{document.documentElement.removeAttribute('data-cz-reduce');EPICartaz.motion.sync();EPICartaz.motion.play(document.querySelector('.cz-motion-title'));document.documentElement.setAttribute('data-cz-projection','');EPICartaz.motion.sync();});assert.deepEqual(await p.evaluate(zero),{active:0,problems:[]});
}
assert.deepEqual(errors,[],`${width} ${theme} ${mode}`);await ctx.close();scenarios++;console.log(`PASS ${width} ${theme} ${mode}`);
}
console.log(`PASS Cartaz: ${scenarios} cenários, ${gestures} gestos, zero deslocação durante movimento, primeira ação a 0 ms, sem JS, teclado, foco e estados finais.`);
}finally{await browser.close();server.closeAllConnections();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
