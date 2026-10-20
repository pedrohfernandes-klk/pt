"""M3-F09: distinguir leitura de dois sonetos de regra de escola literária."""
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "m3/licao-m3-f09/index.html"

class M3Lyric(unittest.TestCase):
    def test_claim_is_limited_to_read_poems(self):
        cards = json.JSONDecoder().raw_decode(SOURCE.read_text(encoding="utf-8").split("CARTOES=", 1)[1].lstrip())[0]
        self.assertEqual(29, len(cards))
        item = cards[23]
        self.assertEqual("vf", item["t"])
        self.assertIs(item["v"], True)
        self.assertIn("Nestes sonetos", item["p"])
        self.assertIn("não uma regra para toda", item["f"])

if __name__ == "__main__":
    unittest.main()
