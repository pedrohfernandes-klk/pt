"""A remotely launched card must have the question shown to its teacher."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from sync_teacher_labels import synchronize


class TeacherLabels(unittest.TestCase):
    def test_m5_m6_remote_selectors_and_banks_match_lessons(self):
        report = synchronize(ROOT)
        self.assertEqual(len(report['checked']), 20)
        self.assertEqual(report['different'], [])
        self.assertEqual(report['notes'], [
            'm6/painel-m6-f12/index.html', 'm6/painel-m6-f13/index.html'])
        # 01/11/2026: mantém os 20 painéis e verifica também os quatro bancos de projeção direta.
        self.assertEqual(report['direct_projection'], [
            'm5/licao-m5-f16/index.html', 'm5/licao-m5-f17/index.html',
            'm6/licao-m6-f14/index.html', 'm6/licao-m6-f15/index.html'])


if __name__ == '__main__':
    unittest.main()
