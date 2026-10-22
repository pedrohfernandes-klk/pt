"""Inventory coverage and broken-answer regressions, including dedicated engines."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_cards', ROOT / 'scripts/audit_cards.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CardAudit(unittest.TestCase):
    def test_current_inventory_and_answers(self):
        result = audit.audit()
        self.assertEqual([], result['errors'])
        self.assertEqual(109, result['lessons'])
        self.assertEqual(5, len(result['external_banks']))

    def test_external_banks_have_actual_validated_activities(self):
        for rel in audit.EXTERNAL_BANKS:
            bank = audit.lesson_cards(ROOT / rel)
            self.assertGreater(len(bank), 10)
            self.assertEqual([], audit.validate_cards(bank))
            self.assertTrue(any(c['t'] == 'escolha' for c in bank))

    def test_unexpected_missing_bank_is_never_silently_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'm1/licao-m1-f99/index.html'
            path.parent.mkdir(parents=True)
            path.write_text('<html></html>', encoding='utf-8')
            result = audit.audit(root)
            self.assertTrue(any('m1/licao-m1-f99' in e for e in result['errors']))

    def test_invalid_answers_and_feedback_are_reported(self):
        invalid = [
            {'t': 'escolha', 'o': ['igual', 'igual'], 'c': 0, 'f': 'explica'},
            {'t': 'escolha', 'o': ['a', 'b'], 'c': 2, 'f': 'explica'},
            {'t': 'escolha', 'o': ['a', 'b'], 'c': 0, 'fe': ['a'], 'f': 'explica'},
            {'t': 'sublinhar', 'frase': 'duas palavras', 'certas': [2], 'f': 'explica'},
            {'t': 'completar', 'frase': 'Falta [2]', 'lacunas': [{'o': ['a'], 'c': 0}], 'f': 'explica'},
        ]
        for card in invalid:
            with self.subTest(card=card):
                self.assertTrue(audit.validate_cards([card]))


if __name__ == '__main__':
    unittest.main()
