"""Regressão da transição da última ficha lírica para a entrada na epopeia."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class M3LyricEpicNavigation(unittest.TestCase):
    def test_lyric_lesson_points_to_epic_introduction(self):
        source = (ROOT / "m3/licao-m3-f09/index.html").read_text(encoding="utf-8")
        self.assertIn('seguinte:"https://pedrohfernandes-klk.github.io/pt/m3/licao-m3-f18/"', source)
        self.assertNotIn('seguinte:"https://pedrohfernandes-klk.github.io/pt/m3/licao-m3-f13/"', source)

    def test_epic_introduction_exists_and_leads_to_next_lesson(self):
        entry = ROOT / "m3/licao-m3-f18/index.html"
        engine = ROOT / "assets/pt-lessons/m3-f18.js"
        self.assertTrue(entry.is_file())
        src = engine.read_text(encoding="utf-8")
        self.assertIn('seguinte:"../licao-m3-f13/"', src)
        self.assertIn("Gama fala ao rei de Melinde", src)

if __name__ == "__main__":
    unittest.main()
