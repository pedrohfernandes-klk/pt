"""M3 F16: qualidade das perguntas do torneio, fundamentação e prova."""
import json
from pathlib import Path
import unittest
SOURCE=Path(__file__).resolve().parents[1]/"m3/licao-m3-f16/index.html"
class TournamentQuestions(unittest.TestCase):
    def test_difficult_question_requires_interpretation_and_evidence(self):
        cards=json.JSONDecoder().raw_decode(SOURCE.read_text(encoding="utf-8").split("CARTOES=",1)[1].lstrip())[0]
        self.assertEqual(19,len(cards))
        item=cards[16]
        self.assertEqual("escolha",item["t"])
        self.assertEqual(0,item["c"])
        self.assertEqual(4,len(item["o"]))
        self.assertIn("apoiada num verso",item["o"][0])
        self.assertIn("explicar a ligação",item["f"])
        self.assertEqual(False,cards[7]["v"])
if __name__=="__main__":
    unittest.main()
