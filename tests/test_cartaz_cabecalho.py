"""03/11/2026: contrato da camada visual da entrada, acima dos créditos publicados."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/cartaz-cabecalho-edits-20261103.json'


class CabecalhoCartaz(unittest.TestCase):
    def test_so_liga_css_com_reversao_estrita(self):
        manifest = json.loads(MANIFEST.read_text('utf-8'))
        self.assertEqual(set(manifest['files']), {'index.html'})
        record = manifest['files']['index.html']
        self.assertEqual(len(record['edits']), 1)
        current = (ROOT / 'index.html').read_text('utf-8')
        edit = record['edits'][0]
        self.assertEqual(current.count(edit['new']), edit['occurrences'])
        original = current.replace(edit['new'], edit['old'])
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), record['base_sha256_lf'])
        self.assertEqual(current, original.replace(edit['old'], edit['new']))
        self.assertEqual(current.replace('<link rel="stylesheet" href="assets/cartaz-cabecalho.css?v=20261103">', ''), original)
        self.assertIn('Grafismo gerado com recurso a IA', original)

    def test_gerador_idempotente(self):
        result = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', 'scripts/cartaz_cabecalho_20261103.json', '--manifesto', str(MANIFEST), '--verificar'], cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_css_sem_motor_novo_nem_imposicoes(self):
        css = (ROOT / 'assets/cartaz-cabecalho.css').read_text('utf-8')
        self.assertNotIn('!important', css)
        self.assertNotIn('@keyframes', css)
        self.assertIn('body[data-site="pt"] .raiz', css)
        self.assertIn('html.epi-projection', css)
        self.assertIn('@media print', css)
        self.assertFalse((ROOT / 'assets/cartaz-cabecalho.js').exists())


if __name__ == '__main__':
    unittest.main()
