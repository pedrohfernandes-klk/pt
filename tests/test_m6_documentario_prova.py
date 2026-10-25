import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards, validate_cards
from sync_teacher_labels import expected_cards


class DocumentarioProva(unittest.TestCase):
    def test_choice_and_inference_are_separated_without_claiming_inner_access(self):
        c = lesson_cards(ROOT / 'm6/licao-m6-f11/index.html')
        self.assertEqual(validate_cards(c), [])
        self.assertEqual(len(c), 22)
        self.assertEqual([x['t'] for x in c[16:18]], ['completar', 'emparelhar'])
        self.assertEqual([x['c'] for x in c[16]['lacunas']], [0, 0])
        self.assertIn('00:05', c[16]['p'])
        self.assertIn('00:05', c[16]['p2'])
        self.assertIn('pode criar distância', c[16]['lacunas'][1]['o'][0])
        self.assertIn('não prova', c[17]['pares'][2][1])
        self.assertIn('duas escolhas', c[3]['html'])
        self.assertIn('a5FVxpP0Pfk', c[3]['html'])
        self.assertIn('ou anota no caderno', c[21]['html'])
        self.assertIn('minuto e o segundo', c[21]['html'])

    def test_teacher_controls_use_current_questions_and_indices(self):
        lesson = ROOT / 'm6/licao-m6-f11/index.html'
        s = (ROOT / 'm6/painel-m6-f11/index.html').read_text('utf-8')
        panel = json.JSONDecoder().raw_decode(s.split('CARTOES=', 1)[1])[0]
        self.assertEqual(panel, expected_cards(lesson))
        self.assertNotIn('Quantas escolhas comenta a apreciação', s)


if __name__ == '__main__':
    unittest.main()
