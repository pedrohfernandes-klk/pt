"""02/11/2026: adaptador comum F2/F3; tipos concretos têm testes separados."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContratoTipos(unittest.TestCase):
    def test_contrato_e_pista_do_motor(self):
        r = subprocess.run(['node','tests/tipos-mais-contrato.cjs'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('PASS contrato v1',r.stdout)


if __name__=='__main__':
    unittest.main()
