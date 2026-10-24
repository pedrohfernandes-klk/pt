"""Prevent the teacher panel and module challenge from serving stale F08 tasks."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards, validate_cards


class LetterIntegration(unittest.TestCase):
    def setUp(self):
        self.cards = lesson_cards(ROOT / 'm5/licao-m5-f08/index.html')

    def test_card_bank_and_indices_remain_valid(self):
        self.assertEqual(validate_cards(self.cards), [])
        self.assertEqual(len(self.cards), 20)
        self.assertEqual([self.cards[i]['t'] for i in (9, 13, 17)],
                         ['escolha', 'completar', 'escolha'])

    def test_teacher_labels_match_the_actual_remote_activity(self):
        text = (ROOT / 'm5/painel-m5-f08/index.html').read_text(encoding='utf-8')
        panel, _ = json.JSONDecoder().raw_decode(text.split('CARTOES=', 1)[1])
        expected = [{'k': i, 't': c['t'], 'p': c['p']}
                    for i, c in enumerate(self.cards) if c['t'] != 'ler']
        self.assertEqual(panel, expected)
        options = re.findall(r'<option value="(\d+)">(.*?)</option>',
                             re.search(r'<select data-r-k>(.*?)</select>', text)[1])
        self.assertEqual([(int(k), p) for k, p in options],
                         [(c['k'], c['p']) for c in expected])

    def test_module_copy_preserves_the_same_answers_and_feedback(self):
        text = (ROOT / 'm5/index.html').read_text(encoding='utf-8')
        units, _ = json.JSONDecoder().raw_decode(re.split(r'var U\s*=', text, 1)[1])
        copies = [c for u in units for c in u['pool'] if c.get('p') == self.cards[9]['p']]
        self.assertEqual(len(copies), 1)
        for key, value in self.cards[9].items():
            self.assertEqual(copies[0][key], value, key)


if __name__ == '__main__':
    unittest.main()
