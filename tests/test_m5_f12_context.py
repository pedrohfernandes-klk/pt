"""Protect context-sensitive reported speech and its isolated module copy."""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards, validate_cards


class ReportedSpeech(unittest.TestCase):
    def test_context_is_available_in_both_prompts(self):
        cards = lesson_cards(ROOT / 'm5/licao-m5-f12/index.html')
        self.assertEqual(validate_cards(cards), [])
        self.assertEqual(len(cards), 23)
        for prompt in ('p', 'p2'):
            self.assertIn('Carlos', cards[6][prompt])
            self.assertIn('aqui', cards[17][prompt])
            self.assertIn('mesmo', cards[17][prompt])
        self.assertTrue(cards[6]['v'])
        self.assertIn('Para que?', cards[6]['cita'])
        self.assertTrue(cards[17]['v'])
        self.assertIn('Exemplos inventados', cards[12]['html'])

    def test_module_copies_do_not_restore_automatic_rules(self):
        cards = lesson_cards(ROOT / 'm5/licao-m5-f12/index.html')
        text = (ROOT / 'm5/index.html').read_text(encoding='utf-8')
        units, _ = json.JSONDecoder().raw_decode(re.split(r'var U\s*=', text, 1)[1])
        pool = [c for u in units for c in u['pool']]
        for card in (cards[16],):
            matches = [c for c in pool if c.get('p') == card['p']]
            self.assertEqual(len(matches), 1)
            for key, value in card.items():
                self.assertEqual(matches[0][key], value)
        self.assertNotIn('Passar ao indireto obriga a mudar', text)


if __name__ == '__main__':
    unittest.main()
