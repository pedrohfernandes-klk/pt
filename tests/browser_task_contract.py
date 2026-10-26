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
    page.go_back(wait_until='networkidle')
    assert page.url == route_url
