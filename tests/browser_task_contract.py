"""Shared browser assertions for the authorised M1/M4/M7 closure-lesson model.

Imported by the existing CI entry points; this file never launches a browser.
"""
from urllib.parse import urljoin
import re
# 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
TASK_MODULES = {1, 2, 4, 7}
TASK_SLUGS = {1: ['m1-u1', 'm1-u2'],
              2: ['m2-u1', 'm2-u2'],
              4: ['m4-u1', 'm4-u2', 'm4-u3-discurso'],
              7: ['m7-u1', 'm7-u2', 'm7-u3']}
# 28/10/2026 (decisão do docente, PR #122): o formato com aquecimento e tema à escolha cobre o M2 (piloto) e o M1.
# Estas páginas têm de o declarar; nenhuma passa pelo contrato compacto por omissão.
CHOICE_SLUGS = {'m1-u1', 'm1-u2', 'm2-u1', 'm2-u2'}

def learning_storage(page):
    return page.evaluate("""() => Object.fromEntries(Object.keys(localStorage)
      .filter(k=>/^(licao-|percurso-|desafio-|epi-pt-)/.test(k))
      .sort().map(k=>[k,localStorage.getItem(k)]))""")

def assert_task_route(page, module, units):
    assert module in TASK_MODULES
    assert page.locator('[data-task-lesson]').count() == len(units)
    assert page.locator('[data-sintese], [data-sintese-registar], #cartao, #copiar-cartao').count() == 0
    assert not page.locator('#arquivo-percurso').is_visible()
    assert page.locator('button[data-desafio]:visible').count() == 0
    assert page.locator('.module-links-support:visible, .extra-cidade:visible, .cz-linha').count() == 0
    assert page.locator('[data-cartaz]').count() == 0
    assert page.locator('.route-teacher-tools').count() == 1
    assert not page.locator('.route-teacher-tools').evaluate('e=>e.open')
    assert page.locator('a[href^="#sintese-unidade"], a[href^="#desafio-unidade"]').count() == 0
    assert 'TAREFA FINAL' not in page.locator('main').inner_text()
    hrefs = []
    for unit, slug in zip(units, TASK_SLUGS[module]):
        n = unit['number']
        section = page.locator(f'.unidade[data-u="{n}"]')
        assert section.locator('li[data-passo]').evaluate_all('(els)=>els.map(e=>e.dataset.passo)') == unit['steps']
        assert section.locator('[data-task-lesson]').count() == 1
        assert section.locator('button[data-desafio], fieldset[data-sintese]').count() == 0
        row = section.locator(f'ol.passos > li[data-task-lesson="{n}"]')
        assert row.is_visible()
        assert row.evaluate('(el)=>el===el.parentElement.lastElementChild')
        link = row.locator('a')
        assert link.get_attribute('href').endswith('/tarefas/' + slug + '/')
        assert '90 min' in row.inner_text()
        hrefs.append(link.get_attribute('href'))
    return hrefs

def visit_task_from_route(page, module, number, expected_href):
    route_url = page.url
    before = learning_storage(page)
    page.locator(f'[data-task-lesson="{number}"] > a').click()
    page.wait_for_url('**/tarefas/' + TASK_SLUGS[module][number - 1] + '/')
    assert page.url == urljoin(route_url, expected_href)
    assert_task_page(page, before)
    page.locator('.c-marca').focus(); page.locator('.c-marca').press('Enter')
    page.wait_for_url('**/m'+str(module)+'/#unidade-pedagogica-'+str(number))
    assert page.url.split('#',1)[0] == route_url.split('#',1)[0]


def open_task_card(page, selector):
    """Use the real free index, including for a node inside a hidden card."""
    target = page.locator(selector).first
    index = target.evaluate('e=>e.closest("[data-task-card]").dataset.taskCard')
    page.locator('[data-c-menu]').focus(); page.locator('[data-c-menu]').press('Enter')
    jump = page.locator(f'[data-task-reader-jump="{index}"]')
    jump.focus(); jump.press('Enter')
    for detail in target.locator('xpath=ancestor::details').all():
        if not detail.evaluate('e=>e.open'):
            detail.locator(':scope > summary').focus(); detail.locator(':scope > summary').press('Enter')
    assert target.is_visible(), selector
    assert page.locator('[data-task-card]:visible').count() == 1
    return target


def assert_task_page(page, before):
    page.locator('[data-task-reader].task-reader-ready').wait_for()
    slug = page.url.split('/tarefas/', 1)[1].split('/', 1)[0] if '/tarefas/' in page.url else ''
    if slug:
        assert (page.locator('main[data-task-choice]').count() == 1) == (slug in CHOICE_SLUGS), slug
    assert page.locator('[data-task-card]:visible').count() == 1
    assert page.locator('[data-task-reader]').count() == 1
    assert page.locator('[data-c-barra] rect').count() == page.locator('[data-task-card]').count()
    assert page.evaluate('(()=>{const ids=[...document.querySelectorAll("[id]")].map(e=>e.id);return ids.length===new Set(ids).size})()')
    compact = page.locator('main[data-task-compact]').count() == 1
    # 28/10/2026 (piloto M2, decisão do docente): o formato com escolha tem um cartão de aquecimento
    # primeiro e duas perguntas, a do aquecimento («aquecer») e uma opcional («1»).
    choice = page.locator('main[data-task-choice]').count() == 1
    count = 2 if compact else 4
    question_ids = ['aquecer', '1'] if choice else [str(i) for i in range(1, count + 1)]
    assert page.locator('[data-task-question]').count() == count
    if choice:
        assert page.locator('[data-task-card]').count() == 4
        assert page.locator('[data-task-card="0"] #aquecer').count() == 1
        assert page.locator('[data-task-card="1"] #produzir').count() == 1
        assert page.locator('[data-task-theme]').count() == 2
        # 28/10/2026 (revisão do PR #122): as letras ficam no nome acessível, porque as instruções mandam escrevê-las
        # no papel: cada opção do aquecimento começa pela letra e cada tema diz «Tema A» ou «Tema B».
        warm = page.locator('[data-task-question="aquecer"]')
        for letter in 'ABC':
            assert warm.get_by_role('button', name=re.compile('^' + letter + r'\s?: \S')).count() == 1, letter
        open_task_card(page, '#produzir')
        for letter in 'AB':
            assert page.get_by_role('heading', name=re.compile('^Tema ' + letter + ' ')).count() == 1, letter
        open_task_card(page, '[data-task-card="0"]')
    if compact:
        assert page.locator('[data-task-card]').count() == (4 if choice else 3)
        assert page.locator('.task-clock').count() == 0
        assert 'Tarefa individual' in page.locator('.task-kicker').first.text_content()
        assert not page.locator('[data-task-optional-preparation]').evaluate('e=>e.open')
    assert page.locator('textarea, input[type="text"], [data-sintese-registar]').count() == 0
    if not compact:
        assert page.locator('.task-clock b').all_text_contents() == ['10 min', '10 min', '60 min', '10 min']
    text = page.locator('main.task-page').text_content()
    assert ('consulta' if compact else 'durante toda a tarefa') in text.lower()
    assert 'duas linhas' in text and 'síntese' in text.lower()
    assert 'Teams' in page.locator('#entregar').text_content()
    # Next/previous and the free index work without answering anything.
    page.locator('[data-task-reader-next]').focus(); page.locator('[data-task-reader-next]').press('Enter')
    assert page.locator('[data-task-card="1"]').is_visible()
    page.locator('[data-task-reader-prev]').focus(); page.locator('[data-task-reader-prev]').press('Enter')
    assert page.locator('[data-task-card="0"]').is_visible()
    open_task_card(page, '#entregar')
    assert learning_storage(page) == before
    for i in question_ids:
        question = open_task_card(page, f'[data-task-question="{i}"]')
        options = question.locator('button[data-response]')
        assert options.count() == 3
        assert question.locator('button[data-correct="true"]').count() == 1
        assert not question.locator('[data-task-feedback]').is_visible()
        for button in options.all():
            button.focus(); button.press('Enter')
            assert button.get_attribute('aria-pressed') == 'true'
            assert question.locator('button[aria-pressed="true"]').count() == 1
            feedback = question.locator('[data-task-feedback]')
            assert feedback.is_visible()
            assert feedback.inner_text() == button.get_attribute('data-response')
            expected = 'supported' if button.get_attribute('data-correct') == 'true' else 'retry'
            assert feedback.get_attribute('data-answer') == expected
    assert f'{count} de {count}' in page.locator('[data-task-status]').inner_text()
    # Consultation is close to the question and preserves the selected answer/listeners.
    question = open_task_card(page, '[data-task-question="1"]')
    selected = question.locator('button[aria-pressed="true"]').inner_text()
    if compact:
        open_task_card(page, '#produzir')
        open_task_card(page, '[data-task-question="1"]')
    else:
        page.locator('[data-task-reader-support]').focus(); page.locator('[data-task-reader-support]').press('Enter')
        assert page.locator('#apoios').is_visible()
        details = page.locator('#apoios details')
        if details.count():
            detail = details.first
            detail.locator('summary').focus(); detail.locator('summary').press('Enter')
            assert detail.evaluate('e=>e.open')
        else:
            # M1-U1 keeps the short source texts open together for comparison.
            assert page.locator('#apoios article').count() >= 3
            assert page.locator('#apoios blockquote').count() >= 3
        page.locator('[data-task-reader-return]').focus(); page.locator('[data-task-reader-return]').press('Enter')
    assert question.is_visible() and question.locator('button[aria-pressed="true"]').inner_text() == selected
    assert question.locator('[data-task-feedback]').is_visible()
    assert learning_storage(page) == before, 'Consultation must not evaluate or complete the task'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3')
    # 28/10/2026 (revisão do PR #124): a barra de topo segue o relógio da produção, também quando o
    # aquecimento tem o primeiro relógio da página. Iniciar a produção mostra o mesmo tempo no topo.
    clock = '[data-relogio]:not([data-chave$=":aquecimento"])'
    if page.locator(clock).count():
        mini = page.locator('[data-task-reader] .relogio-mini')
        assert mini.count() == 1 and not mini.is_visible()
        start = open_task_card(page, clock + ' .relogio-principal')
        start.focus(); start.press('Enter')
        assert mini.is_visible() and mini.get_attribute('data-estado') == 'corre'
        shown = page.evaluate('s=>[document.querySelector(".relogio-mini").textContent,document.querySelector(s+" .relogio-mostrador").textContent]', clock)
        assert shown[0] == shown[1], shown
        warm = page.locator('[data-relogio][data-chave$=":aquecimento"] .relogio')
        if warm.count():
            assert warm.get_attribute('data-estado') == 'pronto'
            assert shown[0] != warm.locator('.relogio-mostrador').text_content(), shown
        page.locator('[data-task-reader-next]').focus(); page.locator('[data-task-reader-next]').press('Enter')
        assert mini.is_visible(), 'o tempo da produção acompanha os outros cartões'
        reset = open_task_card(page, clock + ' .relogio-recomecar')
        reset.focus(); reset.press('Enter')
        assert not mini.is_visible()
        open_task_card(page, '[data-task-card="0"]')


def assert_reader_navigation(page):
    # Original anchors keep their targets and open the owning card.
    anchors = page.locator('.task-actions a[href^="#"]').all()
    for anchor in anchors:
        open_task_card(page, '.task-actions')
        fragment = anchor.get_attribute('href')
        anchor.focus(); anchor.press('Enter')
        page.wait_for_function('hash=>location.hash===hash', arg=fragment)
        assert page.locator(fragment).is_visible()
    # A fresh deep link also opens the correct card. Details containing the target open.
    page.goto(page.url.split('#', 1)[0] + '#apoios', wait_until='networkidle')
    page.reload(wait_until='networkidle')
    page.locator('[data-task-reader].task-reader-ready').wait_for()
    assert page.locator('#apoios').is_visible()
    nested = page.locator('#apoios details [id]').first
    if nested.count():
        page.goto(page.url.split('#', 1)[0] + '#' + nested.get_attribute('id'), wait_until='networkidle')
        assert nested.is_visible() and nested.evaluate('e=>e.closest("details").open')
    page.goto(page.url.split('#', 1)[0] + '#criterios', wait_until='networkidle')
    page.locator('#criterios').wait_for(state='visible')
    # There is one viewport-sized shell; long reading scrolls within its body.
    body = page.locator('.task-reader .casca-corpo')
    assert body.evaluate('e=>["auto","scroll"].includes(getComputedStyle(e).overflowY)')
    if body.evaluate('e=>e.scrollHeight>e.clientHeight+2'):
        assert body.evaluate('e=>{e.scrollTop=e.scrollHeight;return e.scrollTop}') > 0
    assert page.locator('[data-task-reader]').bounding_box()['height'] <= page.evaluate('innerHeight') + 2
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3')
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    page.emulate_media(media='print')
    assert page.locator('[data-task-card]:visible').count() == page.locator('[data-task-card]').count()
    # 28/10/2026 (revisão do PR #122): o aquecimento faz-se em papel; impressa, a máquina 02 mostra a pergunta e as
    # três passagens. Não saem a explicação da escolha nem o estado das respostas exploradas.
    if page.locator('main[data-task-choice]').count():
        question = page.locator('#aquecer [data-task-question="aquecer"]')
        assert question.is_visible() and question.locator('.task-question-title').is_visible()
        assert question.locator('button[data-response]:visible').count() == 3
        assert not page.locator('[data-task-feedback]:visible').count()
        assert not page.locator('[data-task-status]:visible').count()
    page.emulate_media(media='screen')
    page.evaluate('window.dispatchEvent(new Event("afterprint"))')
    assert page.locator('[data-task-card]:visible').count() == 1


def responsive_task_matrix(browser, host):
    """CI-only 8 tasks x 2 real viewports x 2 media schemes; no CSS-regex proxy."""
    from urllib.parse import urlsplit, parse_qs
    for width in (390, 1366):
        for scheme in ('light', 'dark'):
            for module, slugs in TASK_SLUGS.items():
                for slug in slugs:
                    ctx = browser.new_context(viewport={'width': width, 'height': 900},
                                              color_scheme=scheme, reduced_motion='reduce')
                    page = ctx.new_page()
                    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                    # Keep /pt/ in the visible URL so the real projection launcher mounts.
                    # The fixture server serves the checkout root; strip only this URL prefix.
                    def local(route):
                        u = urlsplit(route.request.url)
                        response = route.fetch(url=host + u.path.removeprefix('/pt') +
                                               ('?' + u.query if u.query else ''))
                        route.fulfill(response=response)
                    page.route(host + '/pt/**', local)
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    target = '/pt/tarefas/' + slug + '/'
                    page.goto(host + target, wait_until='networkidle')
                    assert page.evaluate('innerWidth') == width, (slug, width, page.evaluate('innerWidth'))
                    assert page.evaluate('matchMedia("(prefers-color-scheme: dark)").matches') == (scheme == 'dark')
                    before = learning_storage(page)
                    assert_task_page(page, before)
                    assert_reader_navigation(page)
                    buoy = page.locator('.teacher-access')
                    assert buoy.count() == 1 and buoy.is_visible()
                    buoy.focus()
                    assert buoy.evaluate('e=>e===document.activeElement')
                    assert 'lente/docente/' in buoy.get_attribute('href')
                    launcher = page.locator('.epi-projection-launcher')
                    if not launcher.is_visible():
                        page.locator('[data-c-menu]').focus(); page.locator('[data-c-menu]').press('Enter')
                        launcher = page.locator('.epi-projection-menu-link').last
                    assert launcher.is_visible()
                    projection_url = launcher.get_attribute('href')
                    projected = parse_qs(urlsplit(projection_url).query)['pagina'][0]
                    assert projected.split('#', 1)[0] == target
                    launcher.click(); page.wait_for_url('**/projetar/**')
                    frame = page.frame_locator('#lesson-frame')
                    frame.locator('[data-task-reader].task-reader-ready').wait_for()
                    expected = 2 if frame.locator('[data-task-compact]').count() else 4
                    assert frame.locator('[data-task-question]').count() == expected
                    assert not errors, (slug, width, scheme, errors)
                    print('PASS responsive task:', slug, 'actual width', width, scheme,
                          'feedback/anchors/buoy/projection', flush=True)
                    ctx.close()


def fallback_task_pages(browser, host):
    """If the adapter cannot load, all original content and formative listeners remain."""
    for slugs in TASK_SLUGS.values():
        for slug in slugs:
            ctx = browser.new_context(viewport={'width':390,'height':900}, reduced_motion='reduce')
            page = ctx.new_page()
            page.route('**/fonts.googleapis.com/**', lambda r:r.abort())
            page.route('**/fonts.gstatic.com/**', lambda r:r.abort())
            page.route('**/assets/task-reader.js*', lambda r:r.abort())
            page.goto(host+'/tarefas/'+slug+'/', wait_until='networkidle')
            assert page.locator('[data-task-reader]').count() == 0
            assert not page.locator('html').evaluate('e=>e.classList.contains("com-casca")')
            assert page.locator('main.task-page').is_visible()
            for target in ('#preparacao','#apoios','#produzir','#entregar'):
                assert page.locator(target).is_visible()
            compact = page.locator('main[data-task-compact]').count() == 1
            choice = page.locator('main[data-task-choice]').count() == 1
            if compact:
                # 28/10/2026: no formato com escolha, a pergunta do aquecimento está sempre à vista.
                assert page.locator('[data-task-question]:visible').count() == (1 if choice else 0)
                optional=page.locator('[data-task-optional-preparation] > summary')
                optional.focus();optional.press('Enter')
            assert page.locator('[data-task-question]:visible').count() == (2 if compact else 4)
            button=page.locator('[data-task-question="1"] button[data-response]').first
            button.focus();button.press('Enter')
            assert page.locator('[data-task-question="1"] [data-task-feedback]').inner_text()==button.get_attribute('data-response')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+3')
            print('PASS readable fallback with original feedback:',slug,flush=True)
            ctx.close()


def grelha_pages(browser, host):
    """28/10/2026: grelhas /20 (aluno e correção) de 320 a 1440 px sem a página deslizar na horizontal.

    Cada tabela fica num contentor que desliza sozinho; a página nunca desliza. Num ecrã largo, nenhuma tabela desliza.
    28/10/2026 (PR #122): também em modo escuro (texto e fundo seguem a aparência, com contraste) e na impressão
    (a navegação e os botões não saem no papel e as tabelas cabem na largura da página).
    """
    import json
    from pathlib import Path
    dados = json.loads((Path(__file__).resolve().parents[1] / 'docs/pedagogia/grelhas-tarefas-20261027.json').read_text('utf-8'))
    for slug in dados['tarefas']:
        # 28/10/2026 (revisão do PR #122): da tarefa à grelha e de volta, o leitor abre o cartão «Verificar» de onde
        # se partiu, e não o aquecimento. O mesmo a partir da versão de correção.
        for pasta, texto in (('grelha', 'Voltar à tarefa'), ('correcao', 'Tarefa')):
            ctx = browser.new_context(viewport={'width': 390, 'height': 900}, reduced_motion='reduce')
            page = ctx.new_page()
            page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
            page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
            page.goto(host + '/tarefas/' + slug + '/', wait_until='networkidle')
            page.locator('[data-task-reader].task-reader-ready').wait_for()
            link = open_task_card(page, 'a[href="grelha/"]')
            link.click(); page.wait_for_url('**/tarefas/' + slug + '/grelha/')
            if pasta == 'correcao':
                page.locator('footer a[href="../correcao/"]').click(); page.wait_for_url('**/tarefas/' + slug + '/correcao/')
            page.locator('.g-nav a', has_text=texto).click()
            page.wait_for_url(re.compile('/tarefas/' + slug + '/#entregar$'))
            page.locator('[data-task-reader].task-reader-ready').wait_for()
            assert page.locator('#entregar').is_visible(), (slug, pasta)
            card = page.locator('#entregar').evaluate('e=>+e.closest("[data-task-card]").dataset.taskCard')
            assert page.evaluate('EPITaskReader.current()') == card, (slug, pasta)
            assert page.locator('[data-task-card]:visible').count() == 1
            ctx.close()
        for pasta in ('grelha', 'correcao'):
            for scheme in ('light', 'dark'):
                for width in (320, 390, 768, 1440):
                    ctx = browser.new_context(viewport={'width': width, 'height': 900}, color_scheme=scheme)
                    page = ctx.new_page()
                    page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
                    page.route('**/fonts.gstatic.com/**', lambda r: r.abort())
                    page.goto(host + '/tarefas/' + slug + '/' + pasta + '/', wait_until='networkidle')
                    assert page.evaluate('innerWidth') == width
                    assert page.locator('table').count() == page.locator('.g-tab[role="region"][tabindex="0"] > table').count() > 0, (slug, pasta)
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (slug, pasta, width, page.evaluate('document.documentElement.scrollWidth'))
                    if width >= 768:
                        assert page.locator('.g-tab').evaluate_all('(els)=>els.every(e=>e.scrollWidth<=e.clientWidth)'), (slug, pasta, width)
                    colours = page.evaluate('()=>[getComputedStyle(document.body).color,getComputedStyle(document.body).backgroundColor]')
                    assert colours[0] != colours[1], (slug, pasta, scheme, colours)
                    if width == 768:
                        page.emulate_media(media='print')
                        assert page.locator('.g-nav').evaluate('e=>getComputedStyle(e).display') == 'none', (slug, pasta)
                        assert page.locator('table').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().right<=document.documentElement.clientWidth+1)'), (slug, pasta, scheme)
                        page.emulate_media(media='screen')
                    ctx.close()
        print('PASS grelha /20 sem deslizar na horizontal, claro e escuro, impressão:', slug, flush=True)
