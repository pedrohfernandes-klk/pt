"""M4 F11: provas explicadas e objeção pertinente na comparação Vieira/Garrett."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "m4/licao-m4-f11/index.html"

class M4F11Comparison(unittest.TestCase):
    def test_comparison_explains_evidence_and_limits_claim(self):
        text = SOURCE.read_text(encoding="utf-8")
        items = json.JSONDecoder().raw_decode(text.split("CARTOES=", 1)[1].lstrip())[0]
        self.assertEqual(23, len(items))
        plan, objection = items[15], items[16]
        self.assertEqual("ordenar", plan["t"])
        self.assertEqual(4, len(plan["passos"]))
        self.assertIn("passagem e explicação", plan["passos"][1])
        self.assertIn("sustenta a tese", plan["f"])
        self.assertEqual("escolha", objection["t"])
        self.assertEqual(0, objection["c"])
        self.assertEqual(4, len(objection["o"]))
        self.assertIn("gesto", objection["o"][0])
        self.assertIn("limita a tese", objection["f"])

if __name__ == "__main__":
    unittest.main()
