"""One meaningful checkpoint per unit; explicit M2 core/complement split."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'docs/pedagogia/percursos-unidades-20261020.json'


class Controls(HTMLParser):
    def __init__(self):
        super().__init__()
        self.challenges = []
        self.responses = []
        self.tasks = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-task-lesson' in attrs:
            self.tasks.append(attrs['data-task-lesson'])
        if tag == 'button' and 'data-desafio' in attrs:
            self.challenges.append(attrs['data-desafio'])
        # 23/10/2026 (plano de melhoria, fase 0): a síntese da unidade deixou de ter caixa de escrita
        # (textarea data-resp, «Notas no ecrã»); o ponto de fecho de cada unidade é agora o registo
        # oral / no caderno (fieldset data-sintese). Conta-se esse registo em vez da caixa.
        if tag == 'fieldset' and 'data-sintese' in attrs:
            self.responses.append(attrs['data-sintese'])


class UnitRoutes(unittest.TestCase):
    def test_all_modules_have_one_challenge_and_response_per_unit(self):
        for plan in json.loads(PLAN.read_text('utf-8')):
            module = plan['module']
            src = (ROOT / f'm{module}/index.html').read_text('utf-8')
            match = re.search(r'\bU\s*=\s*(\[)', src)
            data = json.JSONDecoder().raw_decode(src[match.start(1):])[0]
            ui = Controls()
            ui.feed(src)
            numbers = [str(i + 1) for i in range(len(plan['units']))]
            with self.subTest(module=module):
                self.assertEqual(numbers, ui.challenges)
                # 26/10: M1/M4/M7 end in a task lesson; old pools remain optional archive.
                if module in (1, 4, 7):
                    self.assertEqual(numbers, ui.tasks)
                    self.assertEqual([], ui.responses)
                    self.assertIn('id="arquivo-percurso" hidden', src)
                    self.assertIn('unit-task-route.js', src)
                else:
                    self.assertEqual(numbers, ui.responses)
                    self.assertEqual([], ui.tasks)
                self.assertEqual(len(numbers), len(data))
                for unit, config in zip(plan['units'], data):
                    self.assertEqual(unit['lessons'], config['licoes'])
                    self.assertEqual(unit['steps'], [p['id'] for p in config['passos']])
                    self.assertGreater(len(config['licoes']), 1)
                    self.assertTrue(set(c['_l'] for c in config['pool']).issubset(unit['lessons']))
                    self.assertEqual(set(unit['lessons']), set(c['_l'] for c in config['pool']))

    def test_m2_is_two_complete_core_sequences_with_purposeful_complements(self):
        plan = json.loads(PLAN.read_text('utf-8'))[1]
        first, second = plan['units']
        self.assertEqual(['m2-f01', 'm2-f02', 'm2-f07', 'm2-f06'], first['lessons'])
        self.assertEqual(['m2-f11', 'm2-f10', 'm2-f08', 'm2-f09'], second['lessons'])
        self.assertEqual(['m2-f10', 'm2-f10', 'm2-f11'], [x['after'] for x in second['complements']])
        self.assertEqual(4, sum(len(u['complements']) for u in plan['units']))
        self.assertTrue(all(c['purpose'] for u in plan['units'] for c in u['complements']))
        src = (ROOT / 'm2/index.html').read_text('utf-8')
        for unit in plan['units']:
            for complement in unit['complements']:
                self.assertIn('id="' + complement['id'] + '"', src)

    def test_changed_unit_assessments_do_not_inherit_old_stage_badges(self):
        for m in (1, 2, 3, 7):
            text = (ROOT / f'm{m}/index.html').read_text('utf-8')
            if m in (1, 7):
                self.assertIn('unit-task-route.js', text)
                adapter = (ROOT / 'assets/unit-task-route.js').read_text('utf-8')
                self.assertIn('desafio-unidade-v2-', adapter)
                self.assertIn('percurso-v2-', adapter)
            else:
                self.assertIn('K0="desafio-unidade-v2-"', text)
            if m not in (1, 7):
                self.assertIn('"percurso-v2-"+M+"-u"', text)
                self.assertIn('unit-history.js', text)
        history = (ROOT / 'assets/unit-history.js').read_text('utf-8')
        self.assertIn('localStorage.getItem("percurso-"', history)
        self.assertNotIn('removeItem', history)

    def test_maps_guides_and_portfolios_use_the_same_units(self):
        for plan in json.loads(PLAN.read_text('utf-8')):
            m = plan['module']
            for role in ('mapa-do-modulo', 'guia-da-tarefa', 'portefolio-do-modulo'):
                path = ROOT / f'm{m}/{role}-m{m}/index.html'
                text = unescape(path.read_text('utf-8'))
                with self.subTest(module=m, role=role):
                    for unit in plan['units']:
                        self.assertIn(unit['title'], text)
                    self.assertNotIn('as etapas mantêm os seus desafios', text)
                    if role == 'portefolio-do-modulo':
                        numbers = set(re.findall(r'M' + str(m) + r'_U(\d+)_', text))
                        self.assertEqual({str(u['number']) for u in plan['units']}, numbers)


if __name__ == '__main__':
    unittest.main()
