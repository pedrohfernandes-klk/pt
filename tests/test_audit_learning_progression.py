"""Regression checks for structural audit; no browser or site rewrite."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_learning_progression import audit


class LearningAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = [f'm2/licao-m2-{id}/index.html' for id in ('f01', 'f02', 'f07')]
        for rel in self.paths:
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('<script>const CARTOES=' + json.dumps([
                {'t': 'ler', 'html': 'Leitura.'},
                {'t': 'escolha', 'p': 'Que acontece?', 'o': ['a', 'b'],
                 'c': 0, 'f': 'A pista esta no texto.', 'fe': ['', 'Rele a pista.']}
            ]) + ';</script>', encoding='utf-8')
        manifest = {'unit': 'm2-u1', 'lessons': [
            {'id': 'm2-' + id, 'path': rel, 'goal': 'Ler', 'evidence': 'Citar',
             'misconception': 'Confundir', 'transfer': 'Aplicar', 'next_step': 'Rever'}
            for id, rel in zip(('f01', 'f02', 'f07'), self.paths)]}
        p = self.root / 'docs/pedagogia/m2-u1-progressao.json'
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(manifest), encoding='utf-8')

    def test_valid_route(self):
        result = audit(self.root)
        self.assertEqual([], result['problems'])
        self.assertEqual(3, result['totals']['lessons_read'])
        self.assertEqual(3, result['totals']['with_specific_feedback'])
        self.assertEqual(3, len(result['pilot']))

    def test_feedback_regression(self):
        path = self.root / self.paths[0]
        path.write_text(path.read_text().replace('A pista esta no texto.', ''), encoding='utf-8')
        self.assertTrue(any('without explanatory feedback' in e for e in audit(self.root)['problems']))

    def test_missing_pilot_lesson(self):
        (self.root / self.paths[1]).unlink()
        self.assertTrue(any('missing or invalid lesson path' in e for e in audit(self.root)['problems']))

    def test_duplicated_pilot_id(self):
        p = self.root / 'docs/pedagogia/m2-u1-progressao.json'
        data = json.loads(p.read_text())
        data['lessons'][1]['id'] = 'm2-f01'
        p.write_text(json.dumps(data), encoding='utf-8')
        self.assertTrue(any('duplicate or invalid ID' in e for e in audit(self.root)['problems']))

    def test_malformed_bank(self):
        (self.root / self.paths[0]).write_text('CARTOES=[{', encoding='utf-8')
        self.assertTrue(audit(self.root)['problems'])


if __name__ == '__main__':
    unittest.main()
