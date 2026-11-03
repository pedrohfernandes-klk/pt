"""03/11/2026: implantação comum, sem edição de páginas geradas ou progresso."""
from pathlib import Path
import json,subprocess,sys,unittest,hashlib
ROOT=Path(__file__).resolve().parents[1]
class Apoios(unittest.TestCase):
    def test_inventory_reproducible(self):
        subprocess.run([sys.executable,'scripts/inventariar_apoios_20261103.py','--check'],cwd=ROOT,check=True)
        rows=json.loads((ROOT/'tests/fixtures/apoios-paginas-20261103.json').read_text('utf-8'))
        self.assertEqual(len(rows),45)
        self.assertEqual(len({r['path'] for r in rows}),45)
        for row in rows:self.assertTrue(all(link['href'] for link in row['links']))
    def test_no_new_progress_or_content_engine(self):
        source=(ROOT/'assets/apoios-paginas.js').read_text('utf-8')
        for word in ['localStorage','sessionStorage','EPICasca','innerHTML=links','fetch(']:self.assertNotIn(word,source)
        self.assertIn('nav.appendChild(a)',source)
        self.assertIn("css.addEventListener('load',mount",source)
    def test_published_html_unchanged(self):
        # 03/11/2026: o checkout curto do CI não tem o main histórico. Confere os
        # 45 HTML por SHA-256; a comparação global por git fica no job com histórico completo.
        rows=json.loads((ROOT/'tests/fixtures/apoios-paginas-20261103.json').read_text('utf-8'))
        for row in rows:
            source=(ROOT/row['path']).read_bytes().replace(b'\r\n',b'\n')
            self.assertEqual(hashlib.sha256(source).hexdigest(),row['html_sha256'],row['path'])
