const {chromium}=require('playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{let file=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',({'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.woff2':'font/woff2'})[path.extname(file)]||'text/plain');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});

/* 27/10/2026 (redesenho «Oficina da palavra»): garantias novas, sem enfraquecer as anteriores.
   Relógio como estado do exercício, texto e foco conservados, teclado, contraste medido nos dois temas e papel. */
async function contrast(page){
 return page.evaluate(()=>{
  const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:((x+.055)/1.055)**2.4});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
  const bg=el=>{for(let e=el;e;e=e.parentElement){const c=getComputedStyle(e).backgroundColor;const a=c.match(/[\d.]+/g);if(a&&(a.length<4||Number(a[3])>.9))return c}return 'rgb(255,255,255)'};
  const sel=['.of-instrucao .writing-task','.of-linha-texto','.of-ref','.of-nome','.of-verbo','.of-operacao','.of-estatuto','.of-pergunta','.of-escolhas .choice','#verify','.of-discreto','.of-colofao-texto p'];
  return sel.map(s=>{const el=document.querySelector(s);if(!el)return [s,null];const a=lum(getComputedStyle(el).color),b=lum(bg(el));return [s,Math.round(((Math.max(a,b)+.05)/(Math.min(a,b)+.05))*100)/100]});
 });
}
async function oficina(browser,host){
 for(const scheme of ['light','dark']){
  const ctx=await browser.newContext({viewport:{width:1366,height:900},colorScheme:scheme});const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(host+'/exame/laboratorio/');await page.evaluate(()=>window.print=()=>{});
  for(const machine of ['0','1','2','3']){
   await page.locator(`[data-machine="${machine}"]`).click();
   if(machine!=='2'){await page.locator('[data-answer="1"]').click();}
   for(const [s,ratio] of await contrast(page))if(ratio!==null)assert(ratio>=4.5,`${scheme} ${machine} contraste ${s}: ${ratio}`);
  }
  assert.deepEqual(errors,[]);await ctx.close();
 }
 console.log('PASS contrast >= 4.5 for reading, instruction, choices, actions and notes, light and dark');
 const ctx=await browser.newContext({viewport:{width:1366,height:900}});const page=await ctx.newPage();
 await page.goto(host+'/exame/laboratorio/');await page.evaluate(()=>window.print=()=>{});
 // relógio e rascunho conservados ao revelar apoios; pausa ao mudar de máquina
 // 27/10/2026: o relógio passa a ser o relógio do aluno (assets/relogio.js): #timer, #clock e #reset dão lugar às classes do componente.
 await page.locator('[data-machine="2"]').click();
 assert.equal(await page.evaluate(()=>document.activeElement.tagName),'H2');
 await page.locator('#answer').fill('Rascunho a conservar');
 await page.locator('#exercise .relogio-principal').click();await page.waitForTimeout(1300);
 await page.locator('#reveal').click();
 assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Pista');
 assert.equal(await page.locator('#answer').inputValue(),'Rascunho a conservar');
 assert.notEqual(await page.locator('#exercise .relogio-mostrador').innerText(),'02:00');
 assert.equal(await page.locator('#exercise .relogio-principal').innerText(),'Pausar');
 await page.locator('[data-machine="0"]').click();await page.waitForTimeout(1300);
 await page.locator('[data-machine="2"]').click();
 const paused=await page.locator('#exercise .relogio-mostrador').innerText();await page.waitForTimeout(1300);
 assert.equal(await page.locator('#exercise .relogio-mostrador').innerText(),paused);
 assert.equal(await page.locator('#exercise .relogio-principal').innerText(),'Continuar');
 assert.equal(await page.locator('#answer').inputValue(),'Rascunho a conservar');
 assert(await page.locator('[data-apoio="1"]').isVisible());
 assert.match(await page.locator('#of-aviso').innerText(),/Relógio em pausa: \d\d:\d\d \(pausa 1 de 2\)/);
 // teclado: a escolha faz-se com Espaço e o foco fica na escolha
 await page.locator('[data-machine="1"]').click();
 await page.locator('[data-answer="3"]').focus();await page.keyboard.press('Space');
 assert.equal(await page.locator('[data-answer="3"]').getAttribute('aria-pressed'),'true');
 assert.equal(await page.evaluate(()=>document.activeElement.dataset.answer),'3');
 // 02: «Verificar escolha» vem logo a seguir à última linha
 await page.keyboard.press('Tab');
 assert.equal(await page.evaluate(()=>document.activeElement.id),'verify');
 // 01: a instrução só aparece anotada depois de verificar
 await page.locator('[data-machine="0"]').click();
 assert.equal(await page.locator('.of-parte').count(),0);
 await page.locator('[data-answer="0"]').click();await page.locator('#verify').click();
 assert.equal(await page.locator('.of-parte').count(),3);
 // 04: marcas de revisão só depois de verificar, com conteúdo e língua separados
 await page.locator('[data-machine="3"]').click();
 assert.equal(await page.locator('mark.of-marca').count(),0);
 await page.locator('[data-answer="1"]').click();await page.locator('#verify').click();
 assert(await page.locator('mark.of-marca').count()>=2);
 assert.match(await page.locator('#feedback').innerText(),/C-ED[\s\S]*CL/);
 // papel: só a folha impressa, com linhas que saem sem a opção de imprimir fundos
 await page.locator('#papel').click();await page.emulateMedia({media:'print'});
 assert(await page.locator('main').isHidden());assert(await page.locator('#print-sheet').isVisible());
 assert.equal(await page.locator('#print-sheet .answer-lines').evaluate(e=>getComputedStyle(e).printColorAdjust||getComputedStyle(e).webkitPrintColorAdjust),'exact');
 assert(!(await page.locator('#print-sheet').innerText()).includes('Rascunho a conservar'));
 await page.emulateMedia({media:'screen'});
 // projeção: a tarefa curta cabe no primeiro ecrã de sala (1366×768)
 await page.setViewportSize({width:1366,height:768});await page.goto(host+'/exame/laboratorio/?projetar=1');
 const bottom=await page.locator('#verify').evaluate(e=>e.getBoundingClientRect().bottom);
 assert(bottom<=768,`verificar fora do primeiro ecrã: ${bottom}`);
 await ctx.close();
 console.log('PASS timer and draft kept on reveal, pause on switch, focus, keyboard, annotations after checking, paper, projection first screen');
}
async function run(){await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{browser=await chromium.launch({headless:true,...(process.env.PT_BROWSER_CHANNEL?{channel:process.env.PT_BROWSER_CHANNEL}:{})});const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));const host=`http://127.0.0.1:${server.address().port}`;
for(const width of [390,1366]){await page.setViewportSize({width,height:900});await page.goto(host+'/exame/laboratorio/');await page.evaluate(()=>window.print=()=>{});
for(const text of ['0','1']){await page.locator('#texto').selectOption(text);
for(let machine=0;machine<4;machine++){await page.locator(`[data-machine="${machine}"]`).click();assert(await page.getByRole('heading',{name:'Uma resposta possível',exact:true}).isHidden());
if(machine!==2){assert(await page.locator('#verify').isDisabled());const wrong=machine===0?2:0,right=machine===0?0:machine===1?(text==='0'?1:3):1;await page.locator(`[data-answer="${wrong}"]`).click();await page.locator('#verify').click();assert.match(await page.locator('#feedback').innerText(),/Revê a escolha/);await page.locator(`[data-answer="${right}"]`).click();await page.locator('#verify').click();assert.match(await page.locator('#feedback').innerText(),/Escolha adequada/);}
if(machine>=2)await page.locator('#answer').fill('<script>texto privado</script>');await page.locator('#papel').click();const printed=await page.locator('#print-sheet').textContent();assert(!printed.includes('Uma resposta possível'));assert(!printed.includes('texto privado'));
for(let i=0;i<3;i++)await page.locator('#reveal').click();assert(await page.getByRole('heading',{name:'Uma resposta possível',exact:true}).isVisible());await page.locator('[data-check="0"]').check();await page.locator('#solucoes').click();assert((await page.locator('#print-sheet').textContent()).includes('Uma resposta possível'));
await page.locator('#projetar').click();if(machine>=2)assert(await page.locator('#answer').isHidden());assert(await page.locator('#fontes').isHidden());await page.locator('#projetar').click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('#restart').click();assert(await page.getByRole('heading',{name:'Uma resposta possível',exact:true}).isHidden());
}}console.log(`PASS 8 exercises at ${width}px: choices, reveal, self-review, print privacy, projection, reset`);
}
await page.goto(host+'/exame/laboratorio/?projetar=1');assert.equal(await page.locator('#projetar').getAttribute('aria-pressed'),'true');await page.locator('[data-machine="2"]').click();await page.locator('#exercise .relogio-principal').click();await page.waitForTimeout(1250);assert.notEqual(await page.locator('#exercise .relogio-mostrador').innerText(),'02:00');await page.locator('#exercise .relogio-recomecar').click();assert.equal(await page.locator('#exercise .relogio-mostrador').innerText(),'02:00');assert(await page.getByRole('heading',{name:'Uma resposta possível',exact:true}).isHidden());
if(process.env.PT_SCREENSHOT){await page.screenshot({path:process.env.PT_SCREENSHOT,fullPage:true});}
await oficina(browser,host);
await page.goto(host+'/exame/');await page.locator('.session-card').first().waitFor();assert.equal(await page.locator('.session-card').count(),27);assert.equal(await page.locator('a[href="laboratorio/"]').count(),1);
assert.deepEqual(errors,[]);console.log('PASS timer, direct projection link, preserved 27-session catalogue, no browser errors');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}}
run().catch(e=>{console.error(e);process.exitCode=1;});
