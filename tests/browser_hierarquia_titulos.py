"""01/11/2026: hierarquia dos títulos em todas as páginas do Português (decisão 61), no navegador.

O docente viu na entrada do exame um título mais pequeno do que devia («tudo tem de funcionar na perfeição»). A medição
de 01/11/2026 (medir-hierarquia.js, 1114 páginas dos dois sítios) passa a teste permanente: este teste abre todas as
páginas do repositório a 390 e a 1366 px e corre as regras R1, R2, R3 e R5 com a mesma função de medição (MEASURE,
copiada letra a letra do script; não se muda aqui sem mudar lá):

* R1, um título mais pequeno do que um título de nível inferior que ele agrupa;
* R2, um antetítulo (texto curto em maiúsculas ou espaçado, logo antes do título) com letra acima de 65 % da do título;
* R3, antetítulos com a mesma classe e letra diferente na mesma página (família, tamanho ou peso);
* R5, um título mais pequeno do que o texto corrido que o segue.

Os elementos decorativos com aria-hidden="true" (as palavras de marca de água) ficam fora de R2 e de R3. A regra R4 (o
mesmo papel com tamanhos diferentes em páginas do mesmo molde) não faz falhar: imprime-se no fim, como relatório.

Falha com qualquer caso novo. Os casos ainda por corrigir estão em PENDENTES_20261101, com o número de vezes que
aparecem a 390 e a 1366 px, a data e o motivo. O teste falha se um caso aparecer mais vezes do que as listadas (um caso
novo, mesmo numa página que já está na lista e com os mesmos seletores) e também se aparecer menos vezes: corrigido um
caso, baixa-se o número ou tira-se da lista, que só pode diminuir.

Páginas: todos os .html com </head> e sem redirecionamento (meta refresh), fora de .git, tests, docs, _qa, node_modules e
assets, como no script. O sítio é servido em /pt/ (como no GitHub Pages) e os pedidos para fora do servidor local são
cortados. Corre com: python tests/browser_hierarquia_titulos.py [--json medidas.json]
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import asyncio
import collections
import json
import os
import re
import sys
import tempfile
import threading

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
LARGURAS = (390, 1366)
FORA = {'.git', 'tests', 'docs', '_qa', 'node_modules', 'assets'}
TRABALHADORES = 6

# 01/11/2026: casos medidos que ainda não se podem corrigir. Cada um é (regra, página, vezes, primeiro, segundo, motivo):
# vezes é o número de ocorrências a 390 e a 1366 px (como no teste do Lente); em R1, primeiro e segundo são o título que
# agrupa e o título maior; em R2, o antetítulo e o título; em R3, a classe dos antetítulos (uma ocorrência por antetítulo
# dessa classe); em R5, o título e o texto. Os seletores são os da medição (etiqueta, #id e até três classes).
CONGELADA = ('página congelada (gerada fora do repositório): corrige-se numa camada nova de trocas literais '
             '(scripts/aplicar_trocas.py), depois do #144 e do #145, que ocupam a camada mais recente')
EXAME_147 = 'corrige-se no #147 (exame: títulos na ordem certa); quando o #147 entrar, sai daqui'
OBRAS = CONGELADA + ('; troca prevista em cada uma das 15 páginas das obras: «.ob h2{font:700 .78rem/1.2» passa a '
                     '«.ob h2{font:700 1.25rem/1.2» (20 px, acima dos h3 de 17,3 px)')
AGUA = CONGELADA + ('; troca prevista: «<span class="agua">escolha</span>» passa a '
                    '«<span class="agua" aria-hidden="true">escolha</span>», como nas outras páginas do M2')
UMA = (1, 1)
PENDENTES_20261101 = (
    # «Ouvir o texto» e «Ver em cena» (h2 de 12,5 px) sobre h3 de 17,3 px nas páginas das obras
    ('R1', 'obras/amor-perdicao/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/cantigas/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/cesario/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/frei-luis/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/frei-luis/index.html', UMA, 'h2#ver', 'h3', OBRAS),
    ('R1', 'obras/ines/index.html', UMA, 'h2#ver', 'h3', OBRAS),
    ('R1', 'obras/lirica-camoes/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/lusiadas/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/maias/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/memorial/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/pessoa/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/poesia-m8/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    ('R1', 'obras/sermao/index.html', UMA, 'h2#ouvir', 'h3', OBRAS),
    # a palavra de marca de água «escolha» é decorativa, mas sem aria-hidden="true" conta como antetítulo
    ('R2', 'm2/gram-subordinadas/index.html', UMA, 'span.agua', 'h1', AGUA),
    # entrada do exame
    ('R1', 'exame/index.html', (4, 4), 'h2', 'h3', EXAME_147),
    ('R2', 'exame/index.html', UMA, 'p.eyebrow', 'h2#provas-porta-t', EXAME_147),
    ('R3', 'exame/index.html', (2, 2), 'p.eyebrow', '', EXAME_147),
)

# Copiada letra a letra de medir-hierarquia.js (01/11/2026, decisão 61): a mesma função mede no relatório e aqui.
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


def paginas():
    """As páginas medidas, pela mesma regra do script."""
    saida = []
    for pasta, subpastas, ficheiros in os.walk(ROOT):
        subpastas[:] = sorted(n for n in subpastas if n not in FORA)
        for nome in sorted(ficheiros):
            if not nome.endswith('.html'):
                continue
            caminho = Path(pasta) / nome
            texto = caminho.read_text('utf-8', errors='replace')
            if re.search(r'</head\s*>', texto, re.I) and not re.search(r'http-equiv=["\']?refresh', texto, re.I):
                saida.append(caminho.relative_to(ROOT).as_posix())
    return sorted(saida)


def casos(medicao):
    """Chaves (regra, página, largura, primeiro, segundo) de uma medição, com o número de vezes que cada uma aparece.

    01/11/2026: conta-se cada ocorrência (collections.Counter, como no teste do Lente), em vez de um conjunto: numa página
    que já está na lista, um caso novo com os mesmos seletores também faz falhar."""
    pagina, largura = medicao['page'], medicao['w']
    chaves = collections.Counter()
    for x in medicao['r1']:
        chaves[('R1', pagina, largura, x['pai'], x['filho'])] += 1
    for x in medicao['r2']:
        chaves[('R2', pagina, largura, x['ante'], x['titulo'])] += 1
    for x in medicao['r3']:
        chaves[('R3', pagina, largura, x['cls'], '')] += 1
    for x in medicao['r5']:
        chaves[('R5', pagina, largura, x['titulo'], x['texto'])] += 1
    return chaves


def pendentes():
    """Chaves da lista, com o número de vezes listado a cada largura (as que ficam a 0 não entram)."""
    chaves = collections.Counter()
    for regra, pagina, vezes, primeiro, segundo, motivo in PENDENTES_20261101:
        for largura, n in zip(LARGURAS, vezes):
            chaves[(regra, pagina, largura, primeiro, segundo)] += n
    return +chaves


def descrever(medicao, chave):
    """Uma linha legível para um caso: textos e tamanhos."""
    regra, pagina, largura, primeiro, segundo = chave
    if regra == 'R1':
        x = next(x for x in medicao['r1'] if (x['pai'], x['filho']) == (primeiro, segundo))
        return f"«{x['paiTxt'][:40]}» {x['paiFs']:.1f} px < «{x['filhoTxt'][:40]}» {x['filhoFs']:.1f} px"
    if regra == 'R2':
        x = next(x for x in medicao['r2'] if (x['ante'], x['titulo']) == (primeiro, segundo))
        return f"«{x['anteTxt'][:30]}» {x['anteFs']:.1f} px antes de «{x['tituloTxt'][:40]}» {x['tituloFs']:.1f} px"
    if regra == 'R3':
        estilos = sorted({f"{x['fam']} {x['fs']:.1f} px {x['w']}" for x in medicao['r3'] if x['cls'] == primeiro})
        return '; '.join(estilos)
    x = next(x for x in medicao['r5'] if (x['titulo'], x['texto']) == (primeiro, segundo))
    return f"«{x['tituloTxt'][:40]}» {x['tituloFs']:.1f} px, texto {x['textoFs']:.1f} px"


def relatorio_r4(medicoes):
    """R4 fica como relatório: o mesmo papel (assinatura e nível) com tamanhos diferentes no mesmo molde e largura."""
    por = collections.defaultdict(lambda: collections.defaultdict(set))
    for m in medicoes:
        molde = re.sub(r'\d+', 'N', re.sub(r'/index\.html$', '/', m['page']))
        for x in m['roles']:
            por[(molde, m['w'], x['sig'], x['lvl'])][round(x['fs'], 1)].add(m['page'])
    linhas = []
    for (molde, largura, assinatura, nivel), tamanhos in sorted(por.items()):
        if len(tamanhos) > 1 and max(tamanhos) - min(tamanhos) >= 1.5:
            detalhe = '; '.join(f'{fs} px em {len(p)} ({sorted(p)[0]})' for fs, p in sorted(tamanhos.items()))
            linhas.append(f'  R4 (relatório) {molde} a {largura} px, {assinatura} (h{nivel}): {detalhe}')
    return linhas


async def medir(host, lista):
    trabalhos = [(p, w) for p in lista for w in LARGURAS]
    medicoes, erros = [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()

        async def trabalhador():
            ctx = await browser.new_context(reduced_motion='reduce')

            async def rota(route):
                if route.request.url.startswith(host):
                    await route.continue_()
                else:
                    await route.abort()

            await ctx.route('**/*', rota)
            page = await ctx.new_page()
            while trabalhos:
                pagina, largura = trabalhos.pop(0)
                try:
                    await page.set_viewport_size({'width': largura, 'height': 900})
                    await page.goto(f'{host}/{pagina}', wait_until='load', timeout=20000)
                    await page.wait_for_timeout(250)
                    medicoes.append({'page': pagina, 'w': largura, **await page.evaluate(MEASURE)})
                except Exception as erro:  # uma página que não abre é uma falha, não um caso a menos
                    erros.append(f'{pagina} a {largura} px não abriu: {str(erro)[:160]}')
            await ctx.close()

        await asyncio.gather(*(trabalhador() for _ in range(TRABALHADORES)))
        await browser.close()
    return sorted(medicoes, key=lambda m: (m['page'], m['w'])), erros


def main():
    lista = paginas()
    raiz = tempfile.mkdtemp(prefix='hierarquia-pt-')
    os.symlink(ROOT, os.path.join(raiz, 'pt'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=raiz))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    host = f'http://127.0.0.1:{server.server_port}/pt'
    try:
        medicoes, erros = asyncio.run(medir(host, lista))
    finally:
        server.shutdown()
        os.unlink(os.path.join(raiz, 'pt'))
        os.rmdir(raiz)
    if '--json' in sys.argv:
        Path(sys.argv[sys.argv.index('--json') + 1]).write_text(json.dumps(medicoes, ensure_ascii=False), 'utf-8')

    lista_pendente = pendentes()
    encontrados, medicao_de = collections.Counter(), {}
    for m in medicoes:
        for chave, n in casos(m).items():
            encontrados[chave] += n
            medicao_de[chave] = m
    falhas = list(erros)
    # 01/11/2026: compara-se o número de vezes a cada largura: mais do que na lista é um caso novo; menos é um caso
    # corrigido, que se tira da lista (ou se baixa o número) no mesmo pedido.
    for chave in sorted(encontrados):
        n, listado = encontrados[chave], lista_pendente.get(chave, 0)
        if n > listado:
            regra, pagina, largura, primeiro, segundo = chave
            falhas.append(f'caso novo {regra} em {pagina} a {largura} px ({primeiro}' + (f' / {segundo}' if segundo else '')
                          + f'), {n} vez(es) para {listado} na lista: {descrever(medicao_de[chave], chave)}')
    for chave in sorted(lista_pendente):
        n, listado = encontrados.get(chave, 0), lista_pendente[chave]
        if n < listado:
            regra, pagina, largura, primeiro, segundo = chave
            falhas.append(f'{regra} em {pagina} a {largura} px ({primeiro}' + (f' / {segundo}' if segundo else '')
                          + f'): agora {n} vez(es) para {listado} na lista; baixa o número ou tira-o de PENDENTES_20261101 '
                          '(a lista só diminui)')
    for linha in relatorio_r4(medicoes):
        print(linha)
    if falhas:
        print('\n'.join(falhas))
        sys.exit(1)
    print(f'Hierarquia dos títulos: {len(lista)} páginas a {LARGURAS[0]} e a {LARGURAS[1]} px ({len(medicoes)} medições); '
          f'R1, R2, R3 e R5 sem casos novos; {len(lista_pendente)} casos por corrigir, todos ainda presentes')


if __name__ == '__main__':
    main()
