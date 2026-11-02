"""01/11/2026: decisão 61. Os títulos do exame não voltam a ficar fora de ordem (pt #147), no navegador.

O docente viu na entrada do exame um título mais pequeno do que devia. O #147 pôs na ordem certa o antetítulo da porta
das provas, o título da porta e os títulos de cada ano; a decisão 61 pede um teste que impeça a regressão. Este teste abre
exame/index.html, exame/provas/index.html e exame/laboratorio/index.html a 390 e a 1366 px e corre as regras R1, R2, R3 e
R5 da medição da hierarquia com a mesma função (MEASURE, copiada letra a letra de medir-hierarquia.js; não se muda aqui
sem mudar lá):

* R1, um título mais pequeno do que um título de nível inferior que ele agrupa;
* R2, um antetítulo (texto curto em maiúsculas ou espaçado, logo antes do título) com letra acima de 65 % da do título;
* R3, antetítulos com a mesma classe e letra diferente na mesma página (família, tamanho ou peso);
* R5, um título mais pequeno do que o texto corrido que o segue.

Exige zero casos nas três páginas e nas duas larguras; não há lista de pendentes. O sítio é servido em /pt/ (como no
GitHub Pages) e os pedidos para fora do servidor local são cortados, como na medição.
Corre com: python tests/browser_exame_hierarquia.py
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGINAS = ('exame/index.html', 'exame/provas/index.html', 'exame/laboratorio/index.html')
LARGURAS = (390, 1366)

# Copiado letra a letra de medir-hierarquia.js (01/11/2026, decisão 61): a mesma função mede no relatório e aqui.
MEASURE = r'''()=>{
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
  return out;}'''


class Quiet(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.js': 'text/javascript', '.mjs': 'text/javascript',
                      '.webp': 'image/webp', '.vtt': 'text/vtt', '.woff2': 'font/woff2', '.svg': 'image/svg+xml'}

    def log_message(self, *args):
        pass


class Servidor(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # um pedido cortado a meio pelo navegador (ao mudar de página) não é uma falha da página
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError)):
            return
        super().handle_error(request, client_address)


def casos(pagina, largura, m):
    """Uma linha legível por caso R1, R2, R3 ou R5 de uma medição."""
    saida = []
    for x in m['r1']:
        saida.append(f"R1 em {pagina} a {largura} px: «{x['paiTxt'][:40]}» ({x['pai']}) {x['paiFs']:.1f} px < "
                     f"«{x['filhoTxt'][:40]}» ({x['filho']}) {x['filhoFs']:.1f} px")
    for x in m['r2']:
        saida.append(f"R2 em {pagina} a {largura} px: «{x['anteTxt'][:30]}» ({x['ante']}) {x['anteFs']:.1f} px antes de "
                     f"«{x['tituloTxt'][:40]}» ({x['titulo']}) {x['tituloFs']:.1f} px")
    for cls in sorted({x['cls'] for x in m['r3']}):
        estilos = sorted({f"{x['fam']} {x['fs']:.1f} px {x['w']}" for x in m['r3'] if x['cls'] == cls})
        saida.append(f"R3 em {pagina} a {largura} px: {cls} com {'; '.join(estilos)}")
    for x in m['r5']:
        saida.append(f"R5 em {pagina} a {largura} px: «{x['tituloTxt'][:40]}» ({x['titulo']}) {x['tituloFs']:.1f} px, "
                     f"texto ({x['texto']}) {x['textoFs']:.1f} px")
    return saida


def main():
    raiz = tempfile.mkdtemp(prefix='exame-hierarquia-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = Servidor(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    falhas, medidas = [], 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(reduced_motion='reduce')
            ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith(host) else route.abort())
            page = ctx.new_page()
            erros = []
            page.on('pageerror', lambda e: erros.append(str(e)))
            for pagina in PAGINAS:
                for largura in LARGURAS:
                    page.set_viewport_size({'width': largura, 'height': 900})
                    page.goto(f'{host}/{pagina}', wait_until='load', timeout=20000)
                    page.wait_for_timeout(250)
                    m = page.evaluate(MEASURE)
                    medidas += 1
                    # a página tem de ter títulos medidos: uma página vazia não pode passar por boa
                    if not m['roles']:
                        falhas.append(f'{pagina} a {largura} px: nenhum título visível medido')
                    falhas.extend(casos(pagina, largura, m))
            falhas.extend(f'erro de JavaScript: {e}' for e in erros)
            ctx.close()
            browser.close()
    finally:
        server.shutdown()
        os.unlink(os.path.join(raiz, 'pt'))
        os.rmdir(raiz)
    if falhas:
        print('\n'.join(falhas))
        sys.exit(1)
    print(f'exame, hierarquia dos títulos: {len(PAGINAS)} páginas a {LARGURAS[0]} e {LARGURAS[1]} px ({medidas} medições), '
          'R1, R2, R3 e R5 a zero')


if __name__ == '__main__':
    main()
