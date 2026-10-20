"""Verificações estruturais dos pré-requisitos de M1-F11 para M2-F01."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def cards(module, lesson):
    raw = (ROOT / module / f"licao-{module}-f{lesson}" / "index.html").read_text(encoding="utf-8")
    return json.JSONDecoder().raw_decode(raw.split("CARTOES=", 1)[1].lstrip())[0]

class ModuleTransition(unittest.TestCase):
    def test_last_lesson_keeps_distinct_voices_and_textual_proof(self):
        a = cards("m1", "11")
        self.assertEqual(24, len(a))
        self.assertEqual("emparelhar", a[16]["t"])
        self.assertIn("cantiga", a[16]["f"].lower())
        self.assertIn("crónica", a[16]["f"].lower())
        self.assertEqual("ordenar", a[21]["t"])
        self.assertIn("provas", a[21]["f"])

    def test_first_theatre_lesson_distinguishes_voice_and_stage_direction(self):
        a = cards("m2", "01")
        self.assertEqual(24, len(a))
        self.assertEqual("completar", a[16]["t"])
        self.assertIn("rubrica", a[16]["f"].lower())
        self.assertEqual("completar", a[19]["t"])
        self.assertIn("falas", a[19]["f"].lower())
        self.assertIn("didascálias", a[19]["f"].lower())
        self.assertEqual("escolha", a[20]["t"])
        self.assertIn("aparte", a[20]["f"].lower())

if __name__ == "__main__":
    unittest.main()
