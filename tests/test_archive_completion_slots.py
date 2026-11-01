"""01/11/2026: todas as lacunas do arquivo têm dados antes de abrir a sobreposição."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ArchiveCompletionSlots(unittest.TestCase):
    def test_every_completion_placeholder_has_exactly_one_definition(self):
        checked = 0
        for module in range(1, 10):
            source = (ROOT / f'm{module}/index.html').read_text('utf-8')
            start = re.search(r'\bU\s*=\s*(\[)', source).start(1)
            units = json.JSONDecoder().raw_decode(source[start:])[0]
            for unit in units:
                for index, card in enumerate(unit['pool']):
                    if card['t'] != 'completar':
                        continue
                    with self.subTest(module=module, card=index, lesson=card.get('_l')):
                        slots = [int(n) for n in re.findall(r'\[(\d+)\]', card['frase'])]
                        self.assertEqual(sorted(slots), list(range(1, len(card['lacunas']) + 1)))
                        for slot in card['lacunas']:
                            self.assertTrue(slot['o'])
                            self.assertIn(slot['c'], range(len(slot['o'])))
                    checked += 1
        self.assertGreater(checked, 0)


if __name__ == '__main__':
    unittest.main()
