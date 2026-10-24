"""Editorial tests: M8 inference/revision and M4 evidence-sensitive distractors.

Run: python -m unittest discover -s tests -p 'test_inferencia_m8_m4.py' -v
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    ('m8', '08'): {'count': 22, 'choices': (8, 13), 'read': (1, 21)},
    ('m8', '09'): {'count': 19, 'choices': (10,), 'vf': (15,)},
    ('m8', '12'): {'count': 22, 'choices': (6,), 'read': (0, 2)},
    # 24/10/2026, aulas claras do M4: a lição M4-F27 foi refeita (18 cartões); os três cartões verificados aqui são os mesmos
    # (c, f, fe iguais; opções encurtadas ao limite de 15 palavras) e passaram dos índices 3, 6 e 12 para 2, 3 e 8
    ('m4', '27'): {'count': 18, 'choices': (2, 3, 8)},
}

def cards(module, lesson):
    source = (ROOT / module / f'licao-{module}-f{lesson}' / 'index.html').read_text('utf-8')
    return json.JSONDecoder().raw_decode(source.split('CARTOES=', 1)[1].lstrip())[0]

class EvidenceBasedLearning(unittest.TestCase):
    def test_card_counts_and_feedback_in_all_four_banks(self):
        for key, cfg in CASES.items():
            bank = cards(*key)
            self.assertEqual(cfg['count'], len(bank), key)
            for index, item in enumerate(bank):
                with self.subTest(lesson=key, card=index):
                    if item['t'] != 'ler':
                        self.assertTrue(item.get('f', '').strip())
                    if item['t'] == 'escolha':
                        self.assertLess(item['c'], len(item['o']))
                        self.assertGreaterEqual(item['c'], 0)

    def test_specific_feedback_matches_original_option_indices(self):
        for key, cfg in CASES.items():
            bank = cards(*key)
            for index in cfg['choices']:
                with self.subTest(lesson=key, card=index):
                    item = bank[index]
                    self.assertEqual('escolha', item['t'])
                    self.assertEqual(len(item['o']), len(item['fe']))
                    self.assertEqual('', item['fe'][item['c']])
                    self.assertTrue(all(
                        s.strip() for j,s in enumerate(item['fe']) if j != item['c']
                    ))

    def test_m8_two_pass_inference_and_revision_not_passages_from_george(self):
        bank = cards('m8', '08')
        self.assertIn('Exemplo inventado', bank[8]['p'])
        self.assertIn('exemplo inventado', bank[13]['p'])
        self.assertIn('desconhecida', bank[8]['o'][0])
        self.assertIn('não demonstra', bank[13]['o'][0])
        self.assertIn('conto', bank[21]['html'])
        self.assertIn('«George»', bank[1]['html'])
        self.assertNotIn('1995', bank[8]['p'])

    def test_m8_creation_keeps_open_intentions_and_task_specific_rules(self):
        bank = cards('m8', '09')
        self.assertIn('inventada', bank[10]['p'])
        self.assertIn('sem afirmar o motivo', bank[10]['p'])
        self.assertEqual(0, bank[10]['c'])
        self.assertIs(bank[15]['v'], False)
        self.assertIn('nesta tarefa', bank[15]['f'])
        self.assertIn('estruturas diferentes', bank[15]['f'])

    def test_m8_comparison_is_text_specific_not_a_universal_slogan(self):
        bank = cards('m8', '12')
        self.assertIn('que deixam os textos por explicar', bank[0]['html'])
        self.assertIn('os silêncios não têm necessariamente', bank[2]['html'])
        self.assertEqual(0, bank[6]['c'])
        self.assertIn('função do que fica', bank[6]['o'][0])
        self.assertIn('critério comum', bank[6]['f'])

    def test_m4_all_distractors_require_contextual_evidence(self):
        bank = cards('m4', '27')
        for index in (2, 3, 8):  # 24/10/2026: os índices 3, 6 e 12 da lição antiga (ver CASES)
            item = bank[index]
            self.assertEqual(0, item['c'])
            self.assertEqual(3, len(item['o']))
            self.assertFalse(any(
                'porque sim' in option.lower() or
                'velhas mentem sempre' in option.lower() or
                'personagem de teatro' in option.lower()
                for option in item['o']
            ))
        self.assertIn('exploração', bank[2]['f'])
        self.assertIn('cidade', bank[3]['f'])
        self.assertIn('evasão', bank[8]['f'])

if __name__ == '__main__':
    unittest.main()
