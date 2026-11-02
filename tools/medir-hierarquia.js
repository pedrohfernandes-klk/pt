// Medição da hierarquia dos títulos nos dois sítios (01/11/2026, decisão 61).
// Serve /tmp/sites/pt em /pt/ e /tmp/sites/lente em /lente/, abre cada página a 390 e a 1366 px e regista:
//  R1 inversão: um título mais pequeno do que um título de nível inferior que agrupa;
//  R2 antetítulo a competir: texto curto em maiúsculas ou espaçado logo antes de um título, com letra acima de 65 % da do título;
//  R3 antetítulos com a mesma classe e letra diferente na mesma página (família, tamanho ou peso);
//  R4 o mesmo papel com tamanhos diferentes em páginas do mesmo molde;
//  R5 título mais pequeno do que o texto corrido que o segue.
// Elementos decorativos (aria-hidden, como as palavras de marca de água) ficam fora de R2 e R3.
// Uso: node medir-hierarquia.js [saida.json] [--sitio pt|lente] [--max N]
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const args=process.argv.slice(2);const OUT=args.find(a=>a.endsWith('.json'))||'/home/user/bordo/design/hierarquia/medidas.json';
const only=(()=>{const i=args.indexOf('--sitio');return i>=0?args[i+1]:null})();const max=(()=>{const i=args.indexOf('--max');return i>=0?+args[i+1]:1e9})();
const ROOTS={pt:process.env.ROOT_PT||'/tmp/sites/pt',lente:process.env.ROOT_LENTE||'/tmp/sites/lente'};
const TYPES={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.woff2':'font/woff2','.woff':'font/woff','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.gif':'image/gif','.ico':'image/x-icon','.vtt':'text/vtt','.txt':'text/plain','.pdf':'application/pdf'};
function listPages(site){const root=ROOTS[site];const out=[];(function walk(d){for(const n of fs.readdirSync(d)){if(['.git','tests','docs','_qa','node_modules','assets'].includes(n))continue;const f=path.join(d,n);const st=fs.statSync(f);if(st.isDirectory())walk(f);else if(n.endsWith('.html')){const s=fs.readFileSync(f,'utf8');if(/<\/head\s*>/i.test(s)&&!/http-equiv=["']?refresh/i.test(s))out.push(path.relative(root,f));}}})(root);return out.sort();}
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0].split('#')[0]);const m=u.match(/^\/(pt|lente)(\/.*)?$/);if(!m){r.writeHead(404);return r.end();}let f=path.join(ROOTS[m[1]],m[2]||'/');try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');}catch(e){r.writeHead(404);return r.end();}if(!fs.existsSync(f)){r.writeHead(404);return r.end();}r.writeHead(200,{'content-type':TYPES[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r);});
function template(p){return p.replace(/\/index\.html$/,'/').replace(/\d+/g,'N');}
const MEASURE=()=>{
  const vis=e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;for(let x=e;x&&x!==document.documentElement;x=x.parentElement){if(x.hidden)return false;const c=getComputedStyle(x);if(c.display==='none'||c.visibility==='hidden'||+c.opacity<.05)return false;if(x.matches&&x.matches('.sr-only,.c-sr,.p-sr,.visually-hidden,dialog:not([open]),details:not([open])>:not(summary)'))return false;}return true;};
  const fs=e=>parseFloat(getComputedStyle(e).fontSize);
  const txt=e=>e.textContent.replace(/\s+/g,' ').trim().slice(0,80);
  const desc=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).slice(0,3).join('.'):'');
  const sig=e=>{const parent=e.parentElement;const pc=parent&&typeof parent.className==='string'&&parent.className.trim()?'.'+parent.className.trim().split(/\s+/)[0]:'';return (parent?parent.tagName.toLowerCase()+pc+'>':'')+desc(e).replace(/#[^.]+/,'');};
  const level=e=>{const m=e.tagName.match(/^H([1-6])$/);if(m)return +m[1];const a=e.getAttribute('aria-level');return a?+a:2;};
  const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')].filter(e=>vis(e)&&txt(e));
  const out={r1:[],r2:[],r3:[],r5:[],roles:[]};
  heads.forEach((h,i)=>{const L=level(h),F=fs(h);out.roles.push({sig:sig(h),lvl:L,fs:F,txt:txt(h)});
    for(let j=i+1;j<heads.length;j++){const k=heads[j],Lk=level(k);if(Lk<=L)break;const Fk=fs(k);if(Fk>F+.5){out.r1.push({pai:desc(h),paiTxt:txt(h),paiFs:F,filho:desc(k),filhoTxt:txt(k),filhoFs:Fk});break;}}
    // R2 antetítulo
    const prev=h.previousElementSibling;if(prev&&vis(prev)&&!/^H[1-6]$/.test(prev.tagName)&&!prev.closest('[aria-hidden="true"]')){const t=txt(prev);const c=getComputedStyle(prev);const ls=parseFloat(c.letterSpacing)||0;if(t&&t.length<=60&&(c.textTransform==='uppercase'||ls>=.05*parseFloat(c.fontSize))){const Fp=fs(prev);out.r3.push({cls:desc(prev).replace(/#[^.]+/,''),desc:desc(prev),txt:t,fs:Fp,fam:c.fontFamily.split(',')[0].replace(/["']/g,''),w:c.fontWeight});if(Fp>.65*F)out.r2.push({ante:desc(prev),anteTxt:t,anteFs:Fp,titulo:desc(h),tituloTxt:txt(h),tituloFs:F});}}
    // R5 texto corrido a seguir
    const c=getComputedStyle(h);if(c.textTransform!=='uppercase'){let n=h.nextElementSibling;while(n&&!vis(n))n=n.nextElementSibling;if(n&&n.tagName==='P'&&txt(n).length>60){const Fn=fs(n);if(F<Fn-.5)out.r5.push({titulo:desc(h),tituloTxt:txt(h),tituloFs:F,texto:desc(n),textoFs:Fn});}}
  });
  const byCls={};for(const k of out.r3)(byCls[k.cls]=byCls[k.cls]||new Set()).add(k.fam+'|'+Math.round(k.fs)+'|'+k.w);out.r3=out.r3.filter(k=>byCls[k.cls].size>1);
  return out;};
srv.listen(0,async()=>{const port=srv.address().port;const browser=await chromium.launch();const results=[];const t0=Date.now();
  const sites=only?[only]:['pt','lente'];const jobs=[];for(const s of sites)for(const p of listPages(s).slice(0,max))for(const w of [390,1366])jobs.push({s,p,w});
  console.log('páginas×larguras:',jobs.length);let done=0;
  async function worker(){const ctx=await browser.newContext({reducedMotion:'reduce'});await ctx.route('**/*',route=>{const u=route.request().url();if(u.startsWith('http://127.0.0.1:'+port))return route.continue();return route.abort();});
    const page=await ctx.newPage();
    while(jobs.length){const j=jobs.shift();try{await page.setViewportSize({width:j.w,height:900});await page.goto(`http://127.0.0.1:${port}/${j.s}/${j.p}`,{waitUntil:'load',timeout:20000});await page.waitForTimeout(250);const m=await page.evaluate(MEASURE);results.push({site:j.s,page:j.p,tpl:template(j.p),w:j.w,...m});}catch(e){results.push({site:j.s,page:j.p,w:j.w,erro:String(e).slice(0,160)});}
      if(++done%200===0)console.log(done,'feitas',Math.round((Date.now()-t0)/1000)+'s');}
    await ctx.close();}
  await Promise.all(Array.from({length:6},worker));await browser.close();srv.close();
  fs.writeFileSync(OUT,JSON.stringify(results));console.log('escrito',OUT,results.length,'medições em',Math.round((Date.now()-t0)/1000)+'s');});
