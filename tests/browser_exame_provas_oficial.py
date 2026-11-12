"""12/11/2026: as «Provas em cartões» do Exame com os documentos oficiais (camada exame_provas_oficial_20261112), no navegador, com
o CSS e os motores reais, a 360 e a 900 px, em tema claro e escuro:
* a secção exame/provas/: não desliza para o lado, nada passa do ecrã, as quatro ligações dos documentos (enunciado e critérios
  de cada prova) veem-se, com contraste de pelo menos 4,5:1, e levam a eduqa.pt; as referências presas não se partem; não há
  «IAVE» nem a cópia de examesnacionais.com.pt no que se lê;
* uma lição de cada grupo (Grupo I e Grupo III da 1.ª fase, Grupo II da 2.ª): o cartão «Abre» cabe no cartão e diz a EduQA; no
  menu, «Enunciado da prova (PDF)», «Critérios de classificação (PDF)» e as duas ligações do crédito veem-se, cabem no painel,
  têm contraste e levam a eduqa.pt (no Grupo III da 1.ª fase, também «A imagem do Grupo III», para a página 13 do enunciado); as
  referências da moldura não se partem; o cartão «Para levar» (a frase sobre as duas provas de 2026) e, nos Grupos I e III, o
  cartão com a formulação do critério cabem no cartão; no fim da lição, «Grupo II», «M4-F15» e «Sessão 22» não se partem;
* no Grupo III da 1.ª fase, o cartão «A prova» tem a ligação para a página 13 do enunciado, à vista, dentro do cartão.

Uso: python3 tests/browser_exame_provas_oficial.py [--url http://127.0.0.1:PORTA]
Sem --url, o teste abre o seu próprio servidor numa porta livre e fecha-o no fim. Com EXAME_PROVAS_OFICIAL_OUTPUT, guarda aí as
capturas (deviceScaleFactor 1). Não faz pedidos à rede (as ligações conferem-se pelo endereço, sem as abrir)."""
from functools import partial
from http.server import ThreadingHTTPServer
import argparse
import json
import os
import re
import sys
import threading
from playwright.sync_api import sync_playwright
from browser_m1_and_inventory import ROOT, QuietHandler

sys.path.insert(0, str(ROOT / 'tests'))
from browser_cuidado_m9 import confere_referencias  # noqa: E402
from browser_provas_cartoes import dentro_do_cartao, sem_desvio  # noqa: E402
from provas_casos import PROVAS, ROMANOS  # noqa: E402

LARGURAS = (360, 900)
SAIDA = os.environ.get('EXAME_PROVAS_OFICIAL_OUTPUT')
N, WJ = '\xa0', '⁠'
POR_PASTA = {P.pasta: P for P in PROVAS}
# Uma lição de cada grupo: (prova, grupo).
LICOES = [('2026-1f', 1), ('2026-2f', 2), ('2026-1f', 3)]
EDUQA = 'EduQA, Instituto de Educação, Qualidade e Avaliação'
# As ligações de um contentor: à vista, dentro do contentor e do ecrã, com o contraste do texto sobre o fundo que se vê por baixo.
LIGACOES = r'''([sel, dentro])=>{const c=document.querySelector(dentro),cx=c.getBoundingClientRect();
 const lum=s=>{const m=s.match(/[\d.]+/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};
  return {l:.2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]),alfa:m.length>3?m[3]:1}};
 return [...document.querySelectorAll(sel)].map(a=>{a.scrollIntoView({block:'center'});const r=a.getBoundingClientRect();
  let fundo=null;for(let e=a;e;e=e.parentElement){const b=getComputedStyle(e).backgroundColor;if(lum(b).alfa===1){fundo=b;break}}
  if(!fundo)fundo=getComputedStyle(document.documentElement).backgroundColor;
  const l1=lum(getComputedStyle(a).color).l,l2=lum(fundo).l;
  const meio=document.elementFromPoint(r.left+Math.min(r.width,40)/2,r.top+r.height/2);
  return {texto:a.textContent,href:a.getAttribute('href'),alvo:a.getAttribute('target'),rel:a.getAttribute('rel'),
   ve:a.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&r.width>20&&r.height>8,
   topo:meio===a||a.contains(meio)||(meio&&meio.contains(a)),
   dentro:r.left>=cx.left-1&&r.right<=cx.right+1&&r.left>=-1&&r.right<=innerWidth+1,
   contraste:(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05),caixa:[r.left,r.right,cx.left,cx.right,innerWidth]}})}'''
# O que passa do ecrã ou do seu contentor, na secção.
FORA_DO_ECRA = r'''()=>[...document.querySelectorAll('main *, header *, footer *, nav *')].filter(e=>{const r=e.getBoundingClientRect();
 return r.width>0&&e.checkVisibility()&&!e.closest('.skip')&&(r.right>innerWidth+1||r.left<-1)}).slice(0,5)
 .map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().left)+'..'+Math.round(e.getBoundingClientRect().right))'''


def captura(page, nome, **kw):
    if SAIDA:
        os.makedirs(SAIDA, exist_ok=True)
        page.screenshot(path=os.path.join(SAIDA, nome + '.png'), **kw)


def confere_ligacoes(page, sel, dentro, esperadas, onde):
    """esperadas: [(texto, href)], pela ordem. Cada uma à vista, dentro do contentor e do ecrã, com contraste, a abrir noutro separador."""
    ls = page.evaluate(LIGACOES, [sel, dentro])
    assert [(x['texto'], x['href']) for x in ls] == esperadas, (onde, [(x['texto'], x['href']) for x in ls])
    for x in ls:
        assert x['href'].startswith('https://eduqa.pt/wp-content/uploads/'), (onde, x['href'])
        assert x['ve'] and x['topo'], (onde, x['texto'], 'não se vê')
        assert x['dentro'], (onde, x['texto'], x['caixa'])
        assert x['contraste'] >= 4.5, (onde, x['texto'], x['contraste'])
        assert x['alvo'] == '_blank' and x['rel'] == 'noopener', (onde, x)
    return len(ls)


def cartoes(texto):
    i = texto.index('CARTOES=') + len('CARTOES=')
    return json.JSONDecoder().raw_decode(texto[i:].replace('<\\/', '</'))[0]


def montar(page, card):
    """Mostra um cartão da lição sozinho, com o motor da página (como tests/browser_cuidado_exame.py)."""
    page.evaluate('''card=>{
      document.querySelectorAll('.casca').forEach(e=>e.remove());
      EPIJogo.montar({itens:[card,{t:'ler',rot:'QA',html:'<p>Voltar.</p>'}],chave:'qa-provas-oficial',variar:false});
      document.querySelector('.jogo-alvo').id='baralho';
      document.querySelectorAll('#baralho details').forEach(d=>d.open=true);
    }''', card)
    page.locator('#baralho .cartao').first.wait_for()


def nova(browser, largura, esquema):
    ctx = browser.new_context(viewport={'width': largura, 'height': 900}, device_scale_factor=1, color_scheme=esquema,
                              reduced_motion='reduce')
    page = ctx.new_page()
    # Sem rede: as fontes externas ficam de fora (como em tests/browser_provas_cartoes.py).
    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
    erros = []
    page.on('pageerror', lambda e: erros.append(str(e)))
    page.on('response', lambda r: erros.append(f'{r.status}: {r.url}') if r.url.startswith('http://127.0.0.1') and r.status >= 400 else None)
    return ctx, page, erros


def seccao(browser, host, largura, esquema):
    onde = ('secção', largura, esquema)
    ctx, page, erros = nova(browser, largura, esquema)
    page.goto(f'{host}/exame/provas/', wait_until='networkidle')
    assert page.evaluate("matchMedia('(prefers-color-scheme: dark)').matches") == (esquema == 'dark'), onde
    sem_desvio(page, onde)
    assert page.evaluate(FORA_DO_ECRA) == [], (onde, page.evaluate(FORA_DO_ECRA))
    esperadas = []
    for P in PROVAS:   # a mais recente primeiro
        esperadas += [(f'enunciado da versão{N}{P.versao} (PDF)', P.url_enunciado), ('critérios de classificação (PDF)', P.url_criterios)]
    n = confere_ligacoes(page, '.pv-fonte a', 'main', esperadas, onde)
    assert page.locator('main a[href^="http"]').count() == n, (onde, 'há outra ligação para fora na secção')
    texto = page.locator('body').inner_text()
    for proibido in ('IAVE', 'examesnacionais', 'Cópias públicas', 'VERSÃO DE TRABALHO'):
        assert proibido not in texto, (onde, proibido)
    assert texto.count(EDUQA) == len(PROVAS), onde
    # Cada referência presa (a palavra e o número, sem espaços normais pelo meio) fica numa só linha, onde quer que apareça.
    confere_referencias(page, 'main', [f'Prova{N}639', f'12.º{N}ano', f'200{N}a{N}350{N}palavras', f'120{N}minutos', f'200{N}pontos', f'Versão{N}2',
                                       f'2.ª{N}fases', f'2.ª{N}fase', f'1.ª{N}fase', f'Grupo{N}III', f'Grupo{N}II', f'Grupo{N}I', f'versão{N}2',
                                       f'(p.{N}1)'], onde)
    page.evaluate('scrollTo(0,0)')
    captura(page, f'provas-oficial-seccao-{largura}-{esquema}', full_page=True)
    assert erros == [], (onde, erros)
    ctx.close()
    return n


def licao(browser, host, pasta, g, largura, esquema):
    P = POR_PASTA[pasta]
    slug, nome = P.grupos[g], ROMANOS[g - 1]
    onde = (pasta, slug, largura, esquema)
    rel = f'exame/provas/{pasta}/{slug}/'
    baralho = cartoes((ROOT / rel / 'index.html').read_text('utf-8'))
    ctx, page, erros = nova(browser, largura, esquema)
    page.goto(f'{host}/{rel}', wait_until='networkidle')
    page.locator('#baralho .cartao').first.wait_for()
    assert page.title() == f'{P.nome}: Grupo {nome}', (onde, page.title())   # o <title> com espaços normais
    # O cartão «Abre».
    sem_desvio(page, onde)
    dentro_do_cartao(page, onde)
    abre = page.locator('#baralho .cartao').inner_text()
    assert f'(os PDF trazem o logótipo da {EDUQA})' in abre and 'IAVE' not in abre, onde
    confere_referencias(page, '#baralho .cartao', [f'Grupo{N}{nome}:'], onde)
    captura(page, f'provas-oficial-{pasta}-{slug}-{largura}-{esquema}-abre')
    # O menu: as ligações dos documentos e as referências da moldura.
    page.locator('[data-c-menu]').click()
    painel = page.locator('[data-c-painel]')
    painel.wait_for(state='visible')
    esperadas = []
    img = P.imagem()
    if img and img['grupo'] == g:
        esperadas.append((f'A imagem do Grupo{N}{nome} (enunciado, p.{N}{img["pagina_pdf"]}, PDF)', f'{P.url_enunciado}#page={img["pagina_pdf"]}'))
    esperadas += [('Enunciado da prova (PDF)', P.url_enunciado), ('Critérios de classificação (PDF)', P.url_criterios),
                  (f'enunciado da versão{N}{P.versao} (PDF)', P.url_enunciado), ('critérios de classificação (PDF)', P.url_criterios)]
    n = confere_ligacoes(page, '[data-c-painel] a[href^="http"]', '[data-c-painel] .c-menu-in', esperadas, onde)
    assert painel.evaluate('p=>{const m=p.querySelector(".c-menu-in");return m.scrollWidth<=m.clientWidth+1}'), (onde, 'o menu desliza para o lado')
    texto = painel.inner_text()
    for proibido in ('IAVE', 'examesnacionais', 'Cópias públicas', 'VERSÃO DE TRABALHO', 'marca de água'):
        assert proibido not in texto, (onde, proibido)
    assert P.cfg['autoria']['texto'] in painel.text_content(), onde
    for frase in (f'Estás em: Grupo{N}{nome}', f'{P.nome_preso}, versão{N}{P.versao}.', f'Grupo{N}{nome} de{N}III'):
        assert frase in painel.text_content(), (onde, frase)
    agulhas = [f'Grupo{N}{nome}', f'de{N}III', f'Prova{N}{P.codigo}', f'{P.fase}.ª{N}fase', f'versão{N}{P.versao}', f'p.{N}1,']
    agulhas += [f'Grupo{N}{ROMANOS[g - 2]}'] if g > 1 else []
    agulhas += [f'Grupo{N}{ROMANOS[g]}'] if g < len(P.grupos) else []
    agulhas += [f'p.{N}{img["pagina_pdf"]},'] if img and img['grupo'] == g else []
    confere_referencias(page, '[data-c-painel]', agulhas, onde)
    page.locator('[data-c-painel] a[href^="http"]').first.scroll_into_view_if_needed()
    captura(page, f'provas-oficial-{pasta}-{slug}-{largura}-{esquema}-menu')
    page.locator('[data-c-painel] .c-menu-extra').last.scroll_into_view_if_needed()
    captura(page, f'provas-oficial-{pasta}-{slug}-{largura}-{esquema}-credito')
    page.locator('[data-c-fecha-menu]').click()
    # Os cartões que a camada mudou, um a um, com o motor da página.
    vistos = 0
    alvos = [c for c in baralho if c.get('rot') == 'Para levar']
    assert len(alvos) == 1 and '<p>Nas duas provas de 2026' in alvos[0]['html'], onde
    if g == 1:
        alvos += [c for c in baralho if c.get('rot') == 'Confere com os critérios'][:1]
        assert '«ou outros igualmente relevantes»' in alvos[-1]['html'], onde
    if g == 3:
        alvos += [c for c in baralho if c.get('rot') == 'Revê com a grelha']
        assert '«mecanismos de articulação interfrásica»' in alvos[-1]['html'], onde
        if img:
            alvos += [c for c in baralho if c.get('rot') == 'A prova']
    for c in alvos:
        montar(page, c)
        sem_desvio(page, onde + (c['rot'],))
        dentro_do_cartao(page, onde + (c['rot'],))
        visto = page.locator('#baralho .cartao').first.inner_text()
        assert 'IAVE' not in visto and 'oito provas' not in visto and 'conectores' not in visto.replace('conectores interfrásicos', ''), (onde, c['rot'])
        if c['rot'] == 'Para levar':
            assert 'Nas duas provas de 2026' in visto, onde
            confere_referencias(page, '#baralho .cartao', [f'Grupo{N}{nome}'], onde + (c['rot'],))
        if c['rot'] == 'A prova':
            n += confere_ligacoes(page, '#baralho .cartao .prova-imagem a', '#baralho .cartao',
                                  [('abre o enunciado (PDF) nessa página', f'{P.url_enunciado}#page={img["pagina_pdf"]}')], onde)
            confere_referencias(page, '#baralho .cartao', [f'p.{N}{img["pagina_pdf"]}', f'Grupo{N}{nome}'], onde + (c['rot'],))
        page.evaluate('scrollTo(0,0)')
        captura(page, f'provas-oficial-{pasta}-{slug}-{largura}-{esquema}-{re.sub(r"[^a-z]+", "-", c["rot"].lower())}', full_page=True)
        vistos += 1
    # O fim da lição («Já feita»): as ligações para os grupos vizinhos, as lições dos módulos e as sessões, sem se partirem.
    fazer = len([c for c in baralho if c['t'] != 'ler'])
    page.evaluate(f'localStorage.setItem("{P.chave(g)}",JSON.stringify({{versao:"{P.versao_licao(g)}",lida:true,melhor:{fazer},totalMelhor:{fazer},total:{fazer},tentativas:1}}))')
    page.goto(f'{host}/{rel}', wait_until='networkidle')
    page.locator('#baralho .portas-ext').first.wait_for()
    sem_desvio(page, onde + ('fim',))
    cfg = P.cfg['grupos'][g - 1]
    sigla = next(x.split('/')[-1].replace('licao-', '').upper() for x in cfg['licoes'] if '/licao-' in x)
    agulhas = [sigla.replace('-', '-' + WJ) + ':', f'Sessão{N}{int(cfg["sessoes"][0][1:])}:']
    agulhas += [f'Grupo{N}{ROMANOS[g - 2]}'] if g > 1 else []
    agulhas += [f'Grupo{N}{ROMANOS[g]}'] if g < len(P.grupos) else []
    confere_referencias(page, '#baralho', agulhas, onde + ('fim',))
    prox = page.locator('#baralho .prox').text_content()
    assert (g == 1 or f'← Grupo{N}{ROMANOS[g - 2]}' in prox) and (g == len(P.grupos) or f'Grupo{N}{ROMANOS[g]} →' in prox), (onde, prox)
    fora = page.evaluate('''()=>[...document.querySelectorAll('#baralho .portas-ext a, #baralho .prox a')].filter(a=>{const r=a.getBoundingClientRect();
      return r.right>innerWidth+1||r.left<-1}).map(a=>a.textContent)''')
    assert fora == [], (onde, fora)
    if g < len(P.grupos):
        acoes = page.evaluate('[...document.querySelectorAll("[data-c-acoes] a,[data-c-acoes] button")].map(a=>a.textContent.trim())')
        assert f'Grupo{N}{ROMANOS[g]}' in acoes, (onde, acoes)
    page.locator('#baralho .portas-ext').first.scroll_into_view_if_needed()
    captura(page, f'provas-oficial-{pasta}-{slug}-{largura}-{esquema}-fim')
    assert erros == [], (onde, erros)
    ctx.close()
    return n, vistos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='servidor já aberto (por omissão, um próprio numa porta livre)')
    args = ap.parse_args()
    server = None
    if args.url:
        host = args.url.rstrip('/')
    else:
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        host = f'http://127.0.0.1:{server.server_port}'
    ligacoes = cartoes_vistos = vistas = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for largura in LARGURAS:
                for esquema in ('light', 'dark'):
                    ligacoes += seccao(browser, host, largura, esquema)
                    vistas += 1
                    for pasta, g in LICOES:
                        n, vistos = licao(browser, host, pasta, g, largura, esquema)
                        ligacoes, cartoes_vistos, vistas = ligacoes + n, cartoes_vistos + vistos, vistas + 1
            browser.close()
    finally:
        if server:
            server.shutdown()
    # Por largura e tema: 4 ligações na secção; 4 no menu de cada lição, mais a da imagem no menu e a do cartão «A prova» no Grupo III
    # da 1.ª fase; 2 cartões no Grupo I, 1 no Grupo II e 3 no Grupo III.
    assert (vistas, ligacoes, cartoes_vistos) == (16, 4 * (4 + 4 + 4 + 6), 4 * 6), (vistas, ligacoes, cartoes_vistos)
    print(f'{vistas} vistas das provas em cartões (a secção e uma lição de cada grupo, a 360 e a 900 px, em tema claro e escuro): nada '
          f'transborda, {ligacoes} ligações dos documentos à vista e para eduqa.pt, {cartoes_vistos} cartões mudados dentro do cartão, '
          'as referências presas não se partem: OK')


if __name__ == '__main__':
    main()
