from pathlib import Path
import json,re,threading,argparse
from functools import partial
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT,QuietHandler,new_page
from browser_m2_complete import respond
parser=argparse.ArgumentParser();parser.add_argument('--live-media',action='store_true');args=parser.parse_args();OUT=ROOT.parents[1]/'outputs/m8-palavras-escuta';OUT.mkdir(parents=True,exist_ok=True)
cards=json.JSONDecoder().raw_decode((ROOT/'m8/licao-m8-f04/index.html').read_text('utf-8').split('CARTOES=',1)[1])[0];results=[]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)));threading.Thread(target=server.serve_forever,daemon=True).start();host=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  for width in [320,1440]:
   ctx,page=new_page(browser,width);errors=[];media=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:media.append(r.url) if 'cdn-ondemand.rtp.pt' in r.url else None)
   if not args.live_media:page.route('https://cdn-ondemand.rtp.pt/**',lambda r:r.abort())
   page.goto(host+'/pt/m8/licao-m8-f04/',wait_until='networkidle')
   def finish():
    for action in range(170):
     if page.locator('#baralho .cartao.fim').count():return
     assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');respond(page)
    raise AssertionError('Lesson stalled')
   def mount(items):page.evaluate("items=>{document.querySelectorAll('.casca').forEach(n=>n.remove());EPIJogo.montar({itens:items,chave:'qa-palavras-escuta',variar:false,mostrarAnterior:false});document.querySelector('.jogo-alvo').id='baralho'}",items)
   finish();page.reload(wait_until='networkidle');page.locator('#baralho .cartao.fim').wait_for();mount(cards);finish();assert not media
   mount([cards[3]]);load=page.locator('[data-rtp-load]');assert page.locator('video').count()==0;assert not media;assert load.bounding_box()['height']>=44;assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');load.focus();load.press('Enter');v=page.locator('[data-rtp-leitura] video');assert v.count()==1;assert v.evaluate('v=>v.controls&&!v.autoplay&&v.preload==="none"');assert v.get_attribute('aria-label');assert page.locator('[data-rtp-close]').evaluate('e=>e===document.activeElement')
   playback=None
   if args.live_media and width==320:
    v.evaluate('v=>v.play()');page.wait_for_function("document.querySelector('[data-rtp-leitura] video').currentTime>2",timeout=45000);playback=v.evaluate('(v)=>({time:v.currentTime,duration:v.duration,audioDecodedBytes:v.webkitAudioDecodedByteCount,videoWidth:v.videoWidth,error:v.error&&v.error.message})');v.evaluate('v=>v.pause()')
   # Controlled error event checks the fallback independently of CDN availability.
   v.evaluate('v=>{window.previousVideo=v;v.dispatchEvent(new Event("error"))}');assert 'Não foi possível' in page.locator('[data-rtp-error]').inner_text();page.locator('[data-rtp-close]').focus();page.locator('[data-rtp-close]').press('Enter');assert page.locator('video').count()==0;assert page.evaluate('previousVideo.paused&&!previousVideo.getAttribute("src")');assert page.locator('[data-rtp-load]').evaluate('e=>e===document.activeElement')
   summary=page.locator('#baralho summary');summary.focus();summary.press('Enter');assert summary.evaluate('e=>e.parentElement.open');assert 'não depende de imitar' in page.locator('#baralho').inner_text();summary.press('Enter');page.screenshot(path=str(OUT/f'escuta-{width}.png'));page.locator('[data-rtp-load]').click();page.locator('video').evaluate('v=>window.departingVideo=v');respond(page);page.wait_for_function('!departingVideo.getAttribute("src")&&departingVideo.paused')
   mount([cards[6]]);page.locator('.corte-modelo h3').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'cortes-{width}.png'));assert page.locator('.corte-modelo dd').count()==4;assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');assert not errors
   results.append({'width':width,'normal_attempt':True,'full_bank':25,'progress_after_reload':True,'lazy_video':True,'keyboard_close_and_alternative':True,'simulated_error_fallback':True,'live_playback':playback,'errors':errors});ctx.close()
  browser.close()
finally:server.shutdown()
(OUT/'qa.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('PASS full lesson, optional RTP player, keyboard, fallback and cut model at 320/1440')
