"""M3 F17 — dois versos como prova, não mera enumeração."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "m3/licao-m3-f17/index.html"

class M3F17Synthesis(unittest.TestCase):
    def test_synthesis_requires_evidence_and_explanation(self):
        src = SOURCE.read_text(encoding="utf-8")
        cards = json.JSONDecoder().raw_decode(src.split("CARTOES=", 1)[1].lstrip())[0]
        self.assertEqual(21, len(cards))
        c14, c15 = cards[14], cards[15]
        self.assertEqual("escolha", c14["t"])
        self.assertEqual(0, c14["c"])
        self.assertEqual(4, len(c14["o"]))
        self.assertIn("interpretando", c14["o"][0])
        self.assertIn("género não decide sozinho", c14["f"])
        self.assertEqual("ordenar", c15["t"])
        self.assertEqual(3, len(c15["passos"]))
        self.assertIn("explica o sentido", c15["passos"][1])
        self.assertIn("que palavras sustentam", c15["f"])

if __name__ == "__main__":
    unittest.main()
