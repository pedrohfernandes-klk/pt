"""03/11/2026: dois fundos isolados, sem alterar conteúdo e contratos das páginas."""
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
from auditoria_20261028 import undo_fundos_modulos
from test_cartaz_m4_piloto import Inventory
ROOT=Path(__file__).resolve().parents[1]
class FundosModulos(unittest.TestCase):
 def test_reversao_integral_e_contratos(self):
  files=json.loads((ROOT/'tests/fixtures/fundos-modulos-edits-20261103.json').read_text('utf-8'))['files']
  self.assertEqual(set(files),{'m4/index.html','m6/index.html'})
  for rel,record in files.items():
   after=(ROOT/rel).read_text('utf-8');before=undo_fundos_modulos(rel,after)
   self.assertEqual(hashlib.sha256(before.encode()).hexdigest(),record['base_sha256_lf'])
   a,b=Inventory(before),Inventory(after)
   self.assertEqual(a.ids,b.ids);self.assertEqual(a.links,b.links)
   self.assertEqual(a.scripts,[s for s in b.scripts if '/fundos.js?' not in s[0].get('src','')])
   self.assertNotIn('class="cz-motion-title"',after)
 def test_camada_idempotente(self):
  r=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/fundos_modulos_20261103.json','--manifesto','tests/fixtures/fundos-modulos-edits-20261103.json','--verificar'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
  self.assertEqual(r.returncode,0,r.stdout+r.stderr)
 def test_motor_existente_e_grafismos_reproduziveis(self):
  paths=[ROOT/'assets/fundo-m4-cardume.svg',ROOT/'assets/fundo-m6-cidade.svg',ROOT/'scripts/fundos_modulos_20261103.json']
  old=[p.read_bytes() for p in paths]
  subprocess.run([sys.executable,'scripts/gerar_fundos_modulos_20261103.py'],cwd=ROOT,check=True)
  self.assertEqual(old,[p.read_bytes() for p in paths])
  css=(ROOT/'assets/fundos-modulos.css').read_text('utf-8')
  self.assertNotIn('!important',css);self.assertNotIn('infinite',css)
  self.assertIn('prefers-reduced-motion:no-preference',css)
  self.assertIn('animation-play-state:paused',css)
  self.assertIn('@media print',css)
if __name__=='__main__':unittest.main()
