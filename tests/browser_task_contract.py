"""Shared browser assertions for the authorised M1/M4/M7 closure-lesson model.

Imported by the existing CI entry points; this file never launches a browser.
"""
from urllib.parse import urljoin
TASK_MODULES = {1, 4, 7}
TASK_SLUGS = {1: ['m1-u1', 'm1-u2'],
              4: ['m4-u1', 'm4-u2', 'm4-u3-discurso'],
              7: ['m7-u1', 'm7-u2', 'm7-u3']}

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
    assert target.is_visible(), selector
    assert page.locator('[data-task-card]:visible').count() == 1
    return target


def assert_task_page(page, before):
    page.locator('[data-task-reader].task-reader-ready').wait_for()
    assert page.locator('[data-task-card]:visible').count() == 1
    assert page.locator('[data-task-reader]').count() == 1
    assert page.locator('[data-c-barra] rect').count() == page.locator('[data-task-card]').count()
    assert page.evaluate('(()=>{const ids=[...document.querySelectorAll("[id]")].map(e=>e.id);return ids.length===new Set(ids).size})()')
    assert page.locator('[data-task-question]').count() == 4
    assert page.locator('textarea, input[type="text"], [data-sintese-registar]').count() == 0
    assert page.locator('.task-clock b').all_text_contents() == ['10 min', '10 min', '60 min', '10 min']
    text = page.locator('main.task-page').text_content()
    assert 'durante toda a tarefa' in text and 'duas linhas' in text and 'síntese' in text.lower()
    assert 'Teams' in page.locator('#entregar').text_content()
    # Next/previous and the free index work without answering anything.
    page.locator('[data-task-reader-next]').focus(); page.locator('[data-task-reader-next]').press('Enter')
    assert page.locator('[data-task-card="1"]').is_visible()
    page.locator('[data-task-reader-prev]').focus(); page.locator('[data-task-reader-prev]').press('Enter')
    assert page.locator('[data-task-card="0"]').is_visible()
    open_task_card(page, '#entregar')
    assert learning_storage(page) == before
    for i in range(1, 5):
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
    assert '4 de 4' in page.locator('[data-task-status]').inner_text()
    # Consultation is close to the question and preserves the selected answer/listeners.
    question = open_task_card(page, '[data-task-question="1"]')
    selected = question.locator('button[aria-pressed="true"]').inner_text()
    page.locator('[data-task-reader-support]').focus(); page.locator('[data-task-reader-support]').press('Enter')
    assert page.locator('#apoios').is_visible()
    detail = page.locator('#apoios details').first
    detail.locator('summary').focus(); detail.locator('summary').press('Enter')
    assert detail.evaluate('e=>e.open')
    page.locator('[data-task-reader-return]').focus(); page.locator('[data-task-reader-return]').press('Enter')
    assert question.is_visible() and question.locator('button[aria-pressed="true"]').inner_text() == selected
    assert question.locator('[data-task-feedback]').is_visible()
    assert learning_storage(page) == before, 'Consultation must not evaluate or complete the task'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3')


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
    height=page.evaluate('innerHeight')
    if not body.evaluate('e=>e.scrollHeight>e.clientHeight+2'):
        page.set_viewport_size({'width':page.evaluate('innerWidth'),'height':500})
    assert body.evaluate('e=>e.scrollHeight>e.clientHeight+2')
    assert body.evaluate('e=>{e.scrollTop=e.scrollHeight;return e.scrollTop}') > 0
    assert page.locator('[data-task-reader]').bounding_box()['height'] <= page.evaluate('innerHeight') + 2
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3')
    page.set_viewport_size({'width':page.evaluate('innerWidth'),'height':height})
    page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
    page.emulate_media(media='print')
    assert page.locator('[data-task-card]:visible').count() == page.locator('[data-task-card]').count()
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
                    assert frame.locator('[data-task-question]').count() == 4
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
            assert page.locator('[data-task-question]:visible').count() == 4
            button=page.locator('[data-task-question="1"] button[data-response]').first
            button.focus();button.press('Enter')
            assert page.locator('[data-task-question="1"] [data-task-feedback]').inner_text()==button.get_attribute('data-response')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+3')
            print('PASS readable fallback with original feedback:',slug,flush=True)
            ctx.close()
