"""Focused editorial contract for the M2-U1 pilot.

Run: python -m unittest discover -s tests -p 'test_m2_u1_learning.py'
These are structure/content checks, not browser or learning-outcome tests.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def lesson(f):
    source = (ROOT / f'm2/licao-m2-f{f}/index.html').read_text(encoding='utf-8')
    return json.JSONDecoder().raw_decode(source.split('CARTOES=', 1)[1].lstrip())[0]


class M2LearningContinuity(unittest.TestCase):
    def test_sequence_and_scope(self):
        route = json.loads((ROOT / 'docs/pedagogia/m2-u1-progressao.json').read_text(encoding='utf-8'))
        self.assertEqual(['m2-f01', 'm2-f02', 'm2-f07'], [l['id'] for l in route['lessons']])
        self.assertEqual([24, 28, 25], [len(lesson(f)) for f in ('01', '02', '07')])
        for f in ('01', '02', '07'):
            self.assertTrue(all(x['t'] == 'ler' or x.get('f') for x in lesson(f)))

    def test_specific_feedback_per_wrong_option(self):
        for f, positions in {'01': [10, 20], '02': [25], '07': [8, 15, 23]}.items():
            for index in positions:
                card = lesson(f)[index]
                with self.subTest(f=f, index=index):
                    self.assertEqual('escolha', card['t'])
                    self.assertIsInstance(card['fe'], list)
                    self.assertEqual(len(card['o']), len(card['fe']))
                    self.assertEqual('', card['fe'][card['c']])
                    self.assertTrue(all(text.strip() for i, text in enumerate(card['fe']) if i != card['c']))
        for f, index in [('02', 17), ('07', 9)]:
            card = lesson(f)[index]
            self.assertEqual('vf', card['t'])
            self.assertIsInstance(card['fe'], str)
            self.assertTrue(card['fe'].strip())

    def test_contextual_recall(self):
        self.assertIn('Na próxima cena', lesson('01')[-1]['html'])
        self.assertIn('Para a próxima lição', lesson('02')[-1]['html'])
        self.assertIn('Da cena à frase', lesson('07')[1]['html'])

    def test_transfer_is_distinct_and_in_all_variable_trials(self):
        cards = lesson('07')
        transfer = [x for x in cards if x.get('g') == 'transfer']
        self.assertEqual(1, len(transfer), 'one transfer objective, not a quota of extra questions')
        x = transfer[0]
        self.assertEqual('escolha', x['t'])
        self.assertIn('diálogo criado', x['p'])
        self.assertIn('substantiva completiva', x['f'])
        self.assertEqual(4, len(x['o']))
        self.assertIn('Frases inventadas', cards[-1]['html'])
        # The current engine includes one item per group when >12 questions.
        # An exclusive group with one item cannot be missed in that selection.
        groups = {str(c.get('g', 'fim')) for c in cards if c['t'] != 'ler'}
        self.assertIn('transfer', groups)
        self.assertGreater(len([c for c in cards if c['t'] != 'ler']), 12)

    def test_no_duplicate_questions(self):
        for f in ('01', '02', '07'):
            ps = [x['p'] for x in lesson(f) if x.get('p')]
            self.assertEqual(len(ps), len(set(ps)), f'duplicate prompts in F{f}')


if __name__ == '__main__':
    unittest.main()
