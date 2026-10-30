from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import html
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards
from task_source_contract import historical_task_source


class TaskPage(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.links, self.questions = [], set(), [], []
        self.current = None
        self.errors = []
        self.feed(text)
        if self.stack:
            self.errors.append(('unclosed', self.stack))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append(('duplicate id', a['id']))
            self.ids.add(a['id'])
        if tag in ('a', 'link', 'script'):
            href = a.get('href', a.get('src'))
            if href:
                self.links.append(href)
        if 'data-task-question' in a:
            self.current = {'key': a['data-task-question'], 'options': [], 'feedback': False}
            self.questions.append(self.current)
        if self.current is not None:
            if tag == 'button':
                self.current['options'].append(a)
            if 'data-task-feedback' in a:
                self.current['feedback'] = a.get('role') == 'status' and 'hidden' in a
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(('mismatched tag', tag))
        if tag == 'article':
            self.current = None


class M1UnitTasks(unittest.TestCase):
    def pages(self):
        for unit in (1, 2):
            path = ROOT / f'tarefas/m1-u{unit}/index.html'
            yield unit, path, historical_task_source(path)

    def test_html_links_and_shared_quiz_contract(self):
        for unit, path, text in self.pages():
            with self.subTest(unit=unit):
                page = TaskPage(text)
                self.assertEqual(page.errors, [])
                self.assertEqual([q['key'] for q in page.questions], ['1', '2', '3', '4'])
                for q in page.questions:
                    self.assertTrue(q['feedback'])
                    self.assertEqual(len(q['options']), 3)
                    self.assertEqual(sum(o['data-correct'] == 'true' for o in q['options']), 1)
                    self.assertEqual(len({o['data-response'] for o in q['options']}), 3)
                    for o in q['options']:
                        self.assertEqual(o['type'], 'button')
                        self.assertEqual(o['aria-pressed'], 'false')
                        self.assertGreater(len(o['data-response']), 30)
                for href in page.links:
                    parsed = urlsplit(href)
                    if parsed.scheme:
                        continue
                    target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), href)
                    if parsed.fragment:
                        ids = page.ids if target == path else TaskPage(target.read_text('utf-8')).ids
                        self.assertIn(unquote(parsed.fragment), ids, href)
                self.assertIn('../../assets/task-90.js?v=20261026.1', text)
                self.assertIn('../../assets/task-90.css?v=20261027-tarefas-1', text)
                self.assertIn('data-task-status', text)
                self.assertNotIn('localStorage', text)
                self.assertNotIn('onclick=', text)

    def test_lesson_timing_consultation_and_integrated_submission(self):
        for unit, _, text in self.pages():
            clock = re.search(r'<ol class="task-clock".*?</ol>', text, re.S)[0]
            self.assertEqual(re.findall(r'<b>(\d+) min</b>', clock), ['10', '10', '60', '10'])
            self.assertIn(f'Aula de tarefa · Unidade {unit} · 90 min', text)
            self.assertIn('durante toda a tarefa', text)
            self.assertIn('folhas próprias', text)
            self.assertIn('Teams no início desta aula', text)
            self.assertIn('fotografias legíveis', text)
            self.assertIn('duas linhas', text)
            self.assertNotIn('Tarefa Final', text)
            self.assertNotIn('data-desafio', text)
            self.assertNotIn('data-sintese', text)
            self.assertNotIn('<textarea', text)

    def test_u1_is_written_comparison_and_transfer_without_old_products(self):
        text = historical_task_source(ROOT / 'tarefas/m1-u1/index.html')
        for phrase in ['Como se faz ouvir uma espera?', 'Quando deixa a promessa',
                       'Como podes transferir', 'Chega já', '180 a 250 palavras',
                       'passagem de A', 'uma de C']:
            self.assertIn(phrase, text)
        self.assertNotIn('M1_Tarefa1_Cantiga', text)
        self.assertNotIn('M1_Tarefa2_Escarnio', text)
        self.assertNotIn('.m4a', text)
        self.assertIn('não é pedido desenho, iluminura ou áudio', text)

    def test_u2_preserves_guide_criteria_and_preconditions(self):
        text = historical_task_source(ROOT / 'tarefas/m1-u2/index.html')
        guide = (ROOT / 'm1/guia-da-tarefa-m1/index.html').read_text('utf-8')
        task = re.search(r'<section[^>]*id="tarefa-3".*?</section>', guide, re.S)[0]
        criteria = re.search(r'<h3>O que conta</h3><ul>(.*?)</ul>', task, re.S)[1]
        for criterion in re.findall(r'<li>(.*?)</li>', criteria):
            self.assertIn(criterion, text)
        for phrase in ['250 a 300 palavras', 'duas fontes', 'antes desta oficina',
                       'outro lugar de Lisboa', 'documentada', 'imaginada',
                       'fora dessa contagem', 'M1_Tarefa3_Cronica', 'DOCX ou PDF']:
            self.assertIn(phrase, text)

    def test_support_quotations_are_in_the_identified_lesson_cards(self):
        expected = {
            1: [('m1/licao-m1-f19/index.html', 2), ('m1/licao-m1-f19/index.html', 7),
                ('m1/licao-m1-f19/index.html', 7)],
            2: [('m1/licao-m1-f06/index.html', 8), ('m1/licao-m1-f06/index.html', 2),
                ('m1/licao-m1-f10/index.html', 8)]}
        for unit, _, text in self.pages():
            support = re.search(r'<section[^>]*id="apoios".*?</section>', text, re.S)[0]
            quotes = re.findall(r'<blockquote>(.*?)</blockquote>', support, re.S)
            self.assertEqual(len(quotes), len(expected[unit]))
            for quote, (source, number) in zip(quotes, expected[unit]):
                card = lesson_cards(ROOT / source)[number - 1]
                original = html.unescape(re.sub(r'<[^>]+>', '', card['html']))
                for line in re.split(r'<br\s*/?>', quote):
                    if line.strip():
                        self.assertIn(html.unescape(line), original, (unit, source, number))



# 30/10/2026: aquecimento em cartões (decisão do docente)
class AquecimentoAtualM1(unittest.TestCase):
    """As asserções anteriores preservam as tarefas históricas; estas verificam as atuais."""
    def test_aquecimento_atual_substitui_maquinas_e_totaliza_90(self):
        import json
        from pathlib import Path
        raiz = Path(__file__).resolve().parents[1]
        for unidade in (1, 2):
            slug = f'm1-u{unidade}'
            with self.subTest(slug=slug):
                d = json.loads((raiz / 'docs/pedagogia/tarefas-escolha' / f'{slug}.json').read_text('utf-8'))
                s = (raiz / 'tarefas' / slug / 'index.html').read_text('utf-8')
                self.assertEqual(d['aquecer']['cartoes'], 'aquecimento/')
                self.assertEqual(d['aquecer']['minutos'], 10)
                self.assertIn('data-task-warm="cartoes"', s)
                self.assertNotIn('data-task-machine', s)
                self.assertNotIn('data-task-question="aquecer"', s)
                self.assertIn('data-max="10"', s)
                self.assertIn('data-max="60"', s)
                self.assertIn('Total: 90 minutos', s)
                self.assertEqual(10 + 5 + 60 + 15, 90)

if __name__ == '__main__':
    unittest.main()
