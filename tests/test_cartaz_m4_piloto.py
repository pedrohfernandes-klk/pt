# 03/11/2026: contratos do piloto conferidos sob a nova camada, sem os relaxar.
"""02/11/2026: contratos do piloto visual M4, sem relaxar o conteúdo publicado."""
import hashlib,json,re,subprocess,sys,unittest
from html.parser import HTMLParser
from pathlib import Path
from auditoria_20261028 import undo_m4_piloto, undo_fundos_modulos
ROOT=Path(__file__).resolve().parents[1]
class Inventory(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.scripts=[];self.in_script=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='script':self.in_script=True;self.scripts.append([a,''])
 def handle_endtag(self,tag):
  if tag=='script':self.in_script=False
 def handle_data(self,text):
  if self.in_script:self.scripts[-1][1]+=text
class M4Piloto(unittest.TestCase):
 def setUp(self):
  self.raw=(ROOT/'m4/index.html').read_text('utf-8');self.after=undo_fundos_modulos('m4/index.html',self.raw);self.before=undo_m4_piloto('m4/index.html',self.raw)
 def test_conserva_ids_ligacoes_scripts_e_dados(self):
  a,b=Inventory(self.before),Inventory(self.after)
  self.assertEqual(sorted(a.ids),sorted(b.ids));self.assertEqual(sorted(a.links),sorted(b.links))
  self.assertEqual(a.scripts,[x for x in b.scripts if 'cartaz-m4-piloto.js' not in x[0].get('src','')])
  self.assertEqual(re.findall(r'<p class="prova-esperada">(.*?)</p>',self.before),re.findall(r'<p class="prova-esperada">(.*?)</p>',self.after))
 def test_reversao_exata_e_idempotencia(self):
  manifest=json.loads((ROOT/'tests/fixtures/cartaz-m4-piloto-edits-20261102.json').read_text('utf-8'))
  self.assertEqual(list(manifest['files']),['m4/index.html'])
  self.assertEqual(hashlib.sha256(self.before.encode()).hexdigest(),manifest['files']['m4/index.html']['base_sha256_lf'])
  run=subprocess.run([sys.executable,'scripts/aplicar_trocas.py','scripts/cartaz_m4_piloto_20261102.json','--manifesto','tests/fixtures/cartaz-m4-piloto-edits-20261102.json','--verificar','--desfazer-antes','tests/fixtures/fundos-modulos-edits-20261103.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
  self.assertEqual(run.returncode,0,run.stdout+run.stderr)
 def test_adesao_exclusiva_e_sem_novo_motor(self):
  for n in range(1,10):
   text=(ROOT/f'm{n}/index.html').read_text('utf-8')
   self.assertEqual('data-m4-piloto=' in text,n==4)
   self.assertEqual('cartaz-m4-piloto.css' in text,n==4)
  js=(ROOT/'assets/cartaz-m4-piloto.js').read_text('utf-8')
  self.assertNotRegex(js,r'(?:localStorage|sessionStorage)|MutationObserver|innerHTML')
  self.assertNotIn('!important',(ROOT/'assets/cartaz-m4-piloto.css').read_text('utf-8'))
 def test_titulos_e_controlo_comum_com_destino_explicito(self):
  self.assertEqual(len(re.findall(r'<h2 class="cz-fold-t" id="unidade-pedagogica-[123]">',self.after)),3)
  self.assertEqual(self.after.count('data-appearance-control=""'),1)
  self.assertEqual(self.after.count('class="teacher-access"'),1)
  self.assertNotIn('style="position:fixed;left:12px;bottom:64px',self.after)
if __name__=='__main__':unittest.main()
