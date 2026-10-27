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
    page.go_back(wait_until='networkidle')
    assert page.url == route_url


def assert_task_page(page, before):
    assert page.locator('.task-question').count() == 4
    assert page.locator('textarea, input[type="text"], [data-sintese-registar]').count() == 0
    assert page.locator('.task-clock b').all_text_contents() == ['10 min', '10 min', '60 min', '10 min']
    assert 'durante toda a tarefa' in page.locator('main').inner_text()
    production = page.locator('#produzir')
    assert 'duas linhas' in page.locator('main').inner_text()
    assert 'síntese' in page.locator('main').inner_text().lower()
    assert 'Teams' in page.locator('#entregar').inner_text()
    for i in range(1, 5):
        question = page.locator(f'[data-task-question="{i}"]')
        options = question.locator('button[data-response]')
        assert options.count() == 3
        assert question.locator('button[data-correct="true"]').count() == 1
        assert not question.locator('[data-task-feedback]').is_visible()
        for button in options.all():
            button.focus()
            button.press('Enter')
            assert button.get_attribute('aria-pressed') == 'true'
            assert question.locator('button[aria-pressed="true"]').count() == 1
            feedback = question.locator('[data-task-feedback]')
            assert feedback.is_visible()
            assert feedback.inner_text() == button.get_attribute('data-response')
            expected = 'supported' if button.get_attribute('data-correct') == 'true' else 'retry'
            assert feedback.get_attribute('data-answer') == expected
    assert '4 de 4' in page.locator('[data-task-status]').inner_text()
    assert learning_storage(page) == before, 'Formative preparation must not evaluate or complete the task'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3')


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
                    for anchor in page.locator('.task-actions a[href^="#"]').all():
                        fragment = anchor.get_attribute('href')
                        anchor.focus(); anchor.press('Enter')
                        page.wait_for_function('hash=>location.hash===hash', arg=fragment)
                        assert page.locator(fragment).count() == 1
                    buoy = page.locator('.teacher-access')
                    assert buoy.count() == 1 and buoy.is_visible()
                    buoy.focus()
                    assert buoy.evaluate('e=>e===document.activeElement')
                    assert 'lente/docente/' in buoy.get_attribute('href')
                    launcher = page.locator('.epi-projection-launcher')
                    assert launcher.is_visible()
                    projection_url = launcher.get_attribute('href')
                    projected = parse_qs(urlsplit(projection_url).query)['pagina'][0]
                    assert projected.split('#', 1)[0] == target
                    launcher.click(); page.wait_for_url('**/projetar/**')
                    frame = page.frame_locator('#lesson-frame')
                    frame.locator('.task-page').wait_for()
                    assert frame.locator('[data-task-question]').count() == 4
                    assert not errors, (slug, width, scheme, errors)
                    print('PASS responsive task:', slug, 'actual width', width, scheme,
                          'feedback/anchors/buoy/projection', flush=True)
                    ctx.close()
