"""Prevent firsthand-witness and all-speech-uses-que generalizations."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def cards(module, lesson):
    path = ROOT / f'{module}/licao-{module}-f{lesson}/index.html'
    return json.JSONDecoder().raw_decode(path.read_text('utf-8').split('CARTOES=', 1)[1].lstrip())[0]


class ContextualInterpretation(unittest.TestCase):
    def test_witness_is_mediated_by_painting_not_firsthand_1808_report(self):
        bank = cards('m8', '03')
        self.assertEqual(26, len(bank))
        self.assertEqual('completar', bank[14]['t'])
        self.assertEqual(0, bank[14]['lacunas'][0]['c'])
        for index in (14, 15, 20):
            self.assertIn('Goya', bank[index]['f'])
        self.assertIn('1808', bank[22]['f'])
        self.assertIs(True, bank[22]['v'])
        self.assertIn('sem os ter presenciado', bank[22]['p'])
        self.assertIn('por que meio', bank[23]['passos'][0])
        self.assertEqual(3, len(bank[23]['passos']))
        self.assertIn('caderno', bank[23]['f'])

    def test_indirect_statement_rule_does_not_overwrite_indirect_question(self):
        bank = cards('m9', '03')
        self.assertIn('afirmação', bank[12]['p'])
        self.assertEqual(3, len(bank[12]['passos']))
        self.assertIn('perguntou dentro de quê', bank[12]['f'])
        self.assertEqual(1, bank[11]['lacunas'][1]['c'])
        self.assertEqual('dentro de quê', bank[11]['lacunas'][1]['o'][1])

    def test_coordination_feedback_requires_context(self):
        # 24/10/2026 (aulas claras M1, decisão do docente de 23/10): a lição foi refeita no molde do M4; os cartões verificados ficam iguais, mudam de propósito a contagem e os índices. O vf do «mas» e do «e» passa do cartão 19 para o 15.
        card = cards('m1', '11')[15]
        self.assertIs(True, card['v'])
        self.assertIn('contexto', card['f'])
        self.assertNotIn('Quem dá o nome à oração é a conjunção', card['f'])


if __name__ == '__main__':
    unittest.main()
