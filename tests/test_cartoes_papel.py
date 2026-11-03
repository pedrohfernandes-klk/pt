"""03/11/2026: o documento final não recebe soluções nem dados de progresso."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from cartoes_papel import pagina
from tipos_regras import DICAS_PAPEL
CARDS=json.loads((ROOT/'tests/fixtures/tipos-mais-ensaio.json').read_text('utf8'))


class Papel(unittest.TestCase):
 def test_documento_completo_sem_solucoes_ou_mutacao(self):
  cards=copy.deepcopy(CARDS)
  for c in cards:c['f']='SEGREDO_DO_RETORNO_'+c['id']
  antes=copy.deepcopy(cards);html=pagina(cards)
  self.assertEqual(cards,antes)
  self.assertEqual(html.count('class="cartao-papel"'),6)
  self.assertNotIn('SEGREDO_DO_RETORNO',html)
  self.assertNotIn('<script',html);self.assertNotIn('localStorage',html)
  for c in cards:
   self.assertIn(c['p'],html)
   self.assertIn(DICAS_PAPEL[c['t']],html)
  for c in cards:
   for k in ('fe_item','fe_razao','fe','erros'):
    if isinstance(c.get(k),list):
     for v in c[k]:
      retorno=v.get('fe') if isinstance(v,dict) else v
      if retorno:self.assertNotIn(retorno,html)
 def test_recusa_entrada_invalida_e_ids_repetidos(self):
  for cards in ([],[{'t':'inexistente'}],[CARDS[0],CARDS[0]]):
   with self.assertRaises(ValueError):pagina(cards)
 def test_escape_e_italico_sem_html_injetado(self):
  c=copy.deepcopy(CARDS[0]);c['p']='Lê _Obra_ e <script>alert(1)</script>.'
  html=pagina([c]);self.assertIn('<i>Obra</i>',html)
  self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
 def test_cli_gera_o_documento_exato(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)/'atividade.html'
   r=subprocess.run([sys.executable,str(ROOT/'scripts/cartoes_papel.py'),str(ROOT/'tests/fixtures/tipos-mais-ensaio.json'),'--saida',str(out)],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr)
   self.assertEqual(out.read_bytes(),pagina(CARDS).encode('utf8'))


if __name__=='__main__':unittest.main()
