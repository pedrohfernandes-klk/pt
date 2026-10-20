"""Regressão editorial para a tipologia trovador, jogral e segrel em M1 F01."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "m1/licao-m1-f01/index.html"


def cards():
    src = SOURCE.read_text(encoding="utf-8")
    return json.JSONDecoder().raw_decode(src.split("CARTOES=", 1)[1].lstrip())[0]


class HistoricalRoles(unittest.TestCase):
    def test_original_structure_and_answers(self):
        a = cards()
        self.assertEqual(22, len(a))
        self.assertEqual("vf", a[9]["t"])
        self.assertIs(a[9]["v"], False)
        self.assertEqual("ordenar", a[10]["t"])
        self.assertEqual(3, len(a[10]["passos"]))

    def test_classification_is_presented_as_a_model(self):
        a = cards()
        self.assertIn("simplificação tradicional", a[10]["f"])
        self.assertIn("segrel", a[10]["f"])
        self.assertIn("fronteiras", a[9]["f"])
        self.assertIn("Alguns jograis também compunham", a[9]["fe"])

    def test_historical_context_present_in_reading(self):
        a = cards()
        text = " ".join(c.get("html", "") for c in a if c["t"] == "ler")
        self.assertIn("categoria de contornos discutidos", text)
        self.assertIn("Alguns jograis também compunham", text)


if __name__ == "__main__":
    unittest.main()
