"""Regressão editorial: contraste de perspetivas em M3-F03."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "m3/licao-m3-f03/index.html"

class M3F03Perspective(unittest.TestCase):
    def test_contrast_is_evidential_and_original_choice_is_unchanged(self):
        source = SOURCE.read_text(encoding="utf-8")
        cards = json.JSONDecoder().raw_decode(source.split("CARTOES=", 1)[1].lstrip())[0]
        self.assertEqual(25, len(cards))
        card = cards[19]
        self.assertEqual("escolha", card["t"])
        self.assertEqual(0, card["c"])
        self.assertEqual(4, len(card["o"]))
        self.assertIn("perspetivas diferentes", card["f"])
        self.assertIn("glória de mandar", card["f"])
        self.assertIn("indícios", card["f"])

if __name__ == "__main__":
    unittest.main()
