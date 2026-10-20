"""Editorial regression checks for M2 Unit 2; not an outcomes or browser test.

Run: python -m unittest discover -s tests -p test_m2_u2_learning.py
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ORDER = [
    'm2-f06', 'm2-ines-escolhe-duas-vezes', 'm2-f10',
    'm2-maquina-de-rir', 'm2-f08', 'm2-f09',
    'm2-f11', 'm2-f12', 'm2-f13',
]
EXPECTED_LENGTHS = {'06': 34, '10': 22, '08': 22, '09': 20,
                    '11': 24, '12': 15, '13': 15}


def cards(id_):
    text = (ROOT / f'm2/licao-m2-f{id_}/index.html').read_text(encoding='utf-8')
    return json.JSONDecoder().raw_decode(text.split('CARTOES=', 1)[1].lstrip())[0]


class M2U2Learning(unittest.TestCase):
    def test_unit_route_and_existing_pages(self):
        route = json.loads(
            (ROOT / 'docs/pedagogia/m2-u2-progressao.json').read_text(encoding='utf-8')
        )
        self.assertEqual('m2-u2', route['unit'])
        self.assertEqual(EXPECTED_ORDER, [step['id'] for step in route['steps']])
        self.assertEqual(7, sum(s['type'] == 'lesson' for s in route['steps']))
        self.assertEqual(2, sum(s['type'] == 'extended' for s in route['steps']))
        for step in route['steps']:
            self.assertTrue((ROOT / step['path']).is_file(), step['path'])
            for field in ('goal', 'evidence', 'misconception', 'next_step'):
                self.assertTrue(step[field].strip(), (step['id'], field))

    def test_bank_counts_and_feedback(self):
        for id_, expected in EXPECTED_LENGTHS.items():
            bank = cards(id_)
            self.assertEqual(expected, len(bank), id_)
            for i, card in enumerate(bank):
                with self.subTest(lesson=id_, card=i):
                    if card['t'] != 'ler':
                        self.assertTrue(card.get('f', '').strip())
                    if card['t'] == 'escolha':
                        self.assertGreaterEqual(len(card['o']), 3)
                        self.assertIsInstance(card['c'], int)
                        self.assertTrue(0 <= card['c'] < len(card['o']))

    def test_error_specific_feedback_matches_selected_option(self):
        for id_, indices in {'06': [25], '10': [18],
                             '08': [16], '11': [15]}.items():
            bank = cards(id_)
            for i in indices:
                x = bank[i]
                with self.subTest(lesson=id_, index=i):
                    self.assertEqual('escolha', x['t'])
                    self.assertEqual(len(x['o']), len(x['fe']))
                    self.assertEqual('', x['fe'][x['c']])
                    self.assertTrue(all(
                        f.strip() for j, f in enumerate(x['fe']) if j != x['c']
                    ))

    def test_reportage_rules_are_not_universalized(self):
        bank = cards('10')
        self.assertIn('Uma reportagem também pode investigar', bank[4]['html'])
        self.assertIn('Não são regras universais', bank[4]['html'])
        for index in (9, 12):
            self.assertEqual('vf', bank[index]['t'])
            self.assertIs(bank[index]['v'], False)
            self.assertIn('tarefa', bank[index]['p'])
        self.assertIn('Nesta tarefa', bank[14]['p'])
        self.assertIn('fala ou de um conflito', bank[18]['o'][0])

    def test_critical_reading_uses_two_independent_indicia(self):
        writing = cards('08')
        self.assertIn('propomos cinco movimentos', writing[1]['html'])
        self.assertIn('Coitada', writing[16]['p'])
        self.assertIn('Quero asno', writing[16]['p'])
        self.assertIn('mudança', writing[16]['f'])
        satire = cards('11')
        self.assertIn('discute esta hipótese', satire[1]['html'])
        self.assertIn('incluindo Inês', satire[1]['html'])
        self.assertIn('sem justificar um pelo outro', satire[15]['o'][1])
        self.assertIn('não desculpa', satire[15]['f'])

    def test_unchanged_number_of_activities(self):
        expected = {'06': 17, '10': 17, '08': 17, '09': 16,
                    '11': 18, '12': 8, '13': 8}
        for id_, count in expected.items():
            self.assertEqual(count, sum(x['t'] != 'ler' for x in cards(id_)))


if __name__ == '__main__':
    unittest.main()
