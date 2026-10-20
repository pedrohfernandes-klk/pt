"""Regression checks for three evidenced curriculum issues, not learning-outcome measurements."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def cards(module, index):
    source = (ROOT / f'{module}/licao-{module}-f{index}/index.html').read_text('utf-8')
    return json.JSONDecoder().raw_decode(source.split('CARTOES=', 1)[1].lstrip())[0]


class EvidenceBasedReview(unittest.TestCase):
    def test_existing_bank_sizes(self):
        self.assertEqual([21, 23, 24],
                         [len(cards(m, n)) for m, n in [('m3', '17'), ('m5', '12'), ('m7', '11')]])

    def test_m3_voice_question_is_hypothesis_not_certainty(self):
        c = cards('m3', '17')[11]
        self.assertEqual('emparelhar', c['t'])
        self.assertIn('investigar', c['p'])
        self.assertEqual(4, len(c['pares']))
        self.assertEqual(4, len(set(p[1] for p in c['pares'])))
        self.assertIn('perguntas de leitura', c['f'])
        self.assertIn('passagem', c['f'])

    def test_m5_only_classifies_quoted_example(self):
        c = cards('m5', '12')[20]
        self.assertEqual('completar', c['t'])
        self.assertIn('Paris era', c['p'])
        self.assertIn('Neste exemplo', c['frase'])
        self.assertIn('não exige sempre', c['f'])
        self.assertEqual([0, 0], [item['c'] for item in c['lacunas']])

    def test_m7_biography_does_not_replace_poem(self):
        c = cards('m7', '11')
        self.assertIn('não explicam, por si sós', c[9]['f'])
        self.assertIn('poemas', c[9]['f'])
        self.assertIn('serenidade', c[5]['f'])
        self.assertIn('Forma e pensamento', c[20]['html'])
        self.assertIn('fundamento', c[21]['f'])
        self.assertEqual('escolha', c[5]['t'])

    def test_data_types_and_explanatory_feedback(self):
        for module, index in [('m3', '17'), ('m5', '12'), ('m7', '11')]:
            for pos, c in enumerate(cards(module, index)):
                with self.subTest(module=module, card=pos):
                    if c['t'] != 'ler':
                        self.assertTrue(c.get('f', '').strip())
                    if c['t'] == 'escolha':
                        self.assertTrue(0 <= c['c'] < len(c['o']))


if __name__ == '__main__':
    unittest.main()
