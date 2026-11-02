"""02/11/2026: contrato puro F0; a prova Chromium está em browser_acrescentos.py."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Acrescentos(unittest.TestCase):
    def test_correspondencia_dos_indices_e_preservacao(self):
        result = subprocess.run(['node', 'tests/acrescentos.cjs'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('PASS 600 correspondências', result.stdout)


if __name__ == '__main__':
    unittest.main()
