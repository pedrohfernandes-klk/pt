"""03/11/2026: F2-03, lançador real e caixas internas, sem confundir corte com ausência de scroll."""
import argparse,json,mimetypes
from pathlib import Path
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
from browser_tipos_mais import CARDS,pagina,ROOT

def route_for(card):
 def route(r):
  path=unquote(urlsplit(r.request.url).path)
  if path=='/pt/ensaio/':
   r.fulfill(body=pagina(card),content_type='text/html; charset=utf-8');return
  rel=path[4:] if path.startswith('/pt/') else path.lstrip('/')
  if rel.endswith('/'):rel+='index.html'
  f=(ROOT/rel).resolve()
  if f.is_relative_to(ROOT) and f.is_file():r.fulfill(path=str(f),content_type=mimetypes.guess_type(f)[0] or 'application/octet-stream')
  else:r.fulfill(status=404,body='')
 return route

def measure(frame):
 return frame.evaluate('''()=>{
 const bad=[], boxes=[];
 const visible=e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';
 const nodes=document.querySelectorAll('.casca-topo,.casca-corpo,.casca-acoes,.cartao,.q,.dica,[data-tipo-ext],.casca button,.casca label,.casca legend,.casca select');
 for(const e of nodes){
  if(!visible(e))continue;
  const r=e.getBoundingClientRect();let left=0,right=innerWidth;
  for(let p=e.parentElement;p;p=p.parentElement){
   if(['hidden','clip','auto','scroll'].includes(getComputedStyle(p).overflowX)){
    const pr=p.getBoundingClientRect();left=Math.max(left,pr.left+p.clientLeft);right=Math.min(right,pr.left+p.clientLeft+p.clientWidth);
   }
  }
  const info={tag:e.tagName,cls:e.className,text:(e.textContent||'').trim().slice(0,90),x:r.x,right:r.right,width:r.width,y:r.y,bottom:r.bottom,height:r.height,limit:[left,right]};
  boxes.push(info);
  if(r.left<left-1||r.right>right+1)bad.push(info);
  if(e.matches('.casca-acoes button,.casca-topo button')&&(r.height<44||r.top< -1||r.bottom>innerHeight+1))bad.push({...info,actionOutside:true});
  // Os retângulos do texto também denunciam palavras cortadas dentro de caixas aparentemente ajustadas.
  const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);
  while(walker.nextNode()){
   const n=walker.currentNode;if(!n.textContent.trim()||!visible(n.parentElement)||n.parentElement.closest('.c-sr,[hidden],.tm-impressao'))continue;
   const range=document.createRange();range.selectNodeContents(n);
   for(const tr of range.getClientRects())if(tr.left<left-1||tr.right>right+1)bad.push({...info,text:n.textContent.trim(),textRect:[tr.left,tr.right]});
  }
 }
 return {width:innerWidth,scroll:document.documentElement.scrollWidth,bad,boxes};
}''')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--saida');args=parser.parse_args()
 out=Path(args.saida) if args.saida else None
 if out:out.mkdir(parents=True,exist_ok=True)
 results=[]
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for card in [*CARDS,None]:
   for width in (320,390,1366):
    for theme in ('light','dark'):
     context=browser.new_context(viewport={'width':width,'height':900},color_scheme=theme)
     context.route('**/*',route_for(card));page=context.new_page();errors=[]
     page.on('pageerror',lambda e:errors.append(str(e)))
     path='/pt/ensaio/' if card else '/pt/m1/licao-m1-f01/'
     page.goto('https://f2.test/pt/projetar/?pagina='+path)
     frame=page.locator('#lesson-frame').element_handle().content_frame()
     frame.wait_for_selector('html.epi-projection');frame.locator('.cartao').wait_for()
     before=frame.evaluate('JSON.stringify(localStorage)')
     if not card:
      for _ in range(30):
       if frame.locator('[data-mostrar]').is_visible():break
       frame.locator('[data-seguinte]:visible').first.click()
      assert frame.locator('[data-mostrar]').is_visible()
     name=f'{card["t"] if card else "m1-f01"}-{width}-{theme}'
     for state in ('inicio','resposta'):
      if state=='resposta':
       frame.locator('[data-mostrar]').click();frame.locator('[data-c-folha]').wait_for()
      page.wait_for_timeout(300)
      result=measure(frame);results.append({'caso':name,'estado':state,**result})
      if out:
       page.screenshot(path=str(out/f'{name}-{state}.png'))
       (out/'medidas.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
      assert result['scroll']<=result['width']+1,(name,state,result)
      assert not result['bad'],(name,state,result['bad'])
     assert frame.evaluate('JSON.stringify(localStorage)')==before,(name,'progresso alterado')
     assert not errors,(name,errors)
     print('PASS projeção real',name,flush=True);context.close()
  browser.close()
 print('PASS 42 contextos, início e resposta, seis tipos e lição anterior',flush=True)
if __name__=='__main__':main()
