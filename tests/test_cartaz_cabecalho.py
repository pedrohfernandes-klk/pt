"""03/11/2026: contrato da camada visual da entrada, acima dos créditos publicados."""
from pathlib import Path
import hashlib
import json
import re
from collections import Counter
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/cartaz-cabecalho-edits-20261103.json'


class CabecalhoCartaz(unittest.TestCase):
    # 03/11/2026: três trocas fechadas; retirada autorizada e destinos preservados em Mais.
    def test_camada_reversivel_e_destinos_preservados(self):
        manifest = json.loads(MANIFEST.read_text('utf-8'))
        self.assertEqual(set(manifest['files']), {'index.html'})
        record = manifest['files']['index.html']
        self.assertEqual(len(record['edits']), 3)
        current = (ROOT / 'index.html').read_text('utf-8')
        original = current
        for edit in reversed(record['edits']):
            self.assertEqual(original.count(edit['new']), edit['occurrences'])
            original = original.replace(edit['new'], edit['old'])
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), record['base_sha256_lf'])
        rebuilt = original
        for edit in record['edits']:
            self.assertEqual(rebuilt.count(edit['old']), edit['occurrences'])
            rebuilt = rebuilt.replace(edit['old'], edit['new'])
        self.assertEqual(current, rebuilt)
        self.assertEqual(Counter(re.findall(r'<a\b[^>]*href="([^"]+)"', current)),
                         Counter(re.findall(r'<a\b[^>]*href="([^"]+)"', original)))
        self.assertNotIn('<aside class="ed-sugestao"', current)
        self.assertNotIn('data-reabrir', current)
        self.assertIn('id="ed-sugestao-titulo"', current)
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
