"""Regressão: não confundir hipérbole épica com facto histórico em M3-F02."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "m3/licao-m3-f02/index.html"

class M3F02Voice(unittest.TestCase):
    def test_poetic_perspective_and_original_answer(self):
        cards = json.JSONDecoder().raw_decode(SOURCE.read_text(encoding="utf-8").split("CARTOES=", 1)[1].lstrip())[0]
        self.assertEqual(27, len(cards))
        card = cards[5]
        self.assertEqual("escolha", card["t"])
        self.assertEqual(0, card["c"])
        self.assertEqual(4, len(card["o"]))
        self.assertIn("como apresenta o Poeta", card["p"])
        self.assertIn("não prova que ninguém", card["f"])
        self.assertIn("não dá voz", cards[17]["f"])

if __name__ == "__main__":
    unittest.main()
