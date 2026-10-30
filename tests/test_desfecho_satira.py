import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def bank(n):return json.JSONDecoder().raw_decode((ROOT/f'm2/licao-m2-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class DesfechoSatira(unittest.TestCase):
 def test_dramatic_order_and_reading_labels(self):
  a=bank('06');self.assertEqual(34,len(a));readings=[c for c in a if c.get('rot','').startswith('O texto,')];self.assertEqual([f'O texto, {i} de 12' for i in range(1,13)],[c['rot'] for c in readings])
  text=' '.join(c.get('html','') for c in a)
  self.assertLess(text.index('Andar'),text.index('Vem um Ermitão'));self.assertIn('segundo casamento',a[15]['html'])
  labels=re.findall(r'data-l="([^"]+)"',text);self.assertEqual(len(labels),len(set(labels)))
 def test_hearing_not_confused_with_understanding(self):
  # 30/10/2026: opções denunciadoras (pedido do docente de 29/10): a certa do cartão 24 encurta-se para «ouve a cantiga,
  # mas não mostra entender a alusão» (tests/fixtures/opcoes-denunciadoras-edits-20261030.json); continua a separar ouvir de
  # compreender.
  a=bank('06');self.assertNotIn('Pêro ouve «Quanto vos amo»; o público ouve',a[1]['html']);self.assertIn('compreensão',a[1]['html']);self.assertEqual('rever',a[23]['t']);self.assertIn('ouve a cantiga, mas não mostra entender',a[23]['o'][0]);self.assertIn('cuco',a[25]['cita']);self.assertIn('data-l="'+a[25]['l']+'"',a[21]['html'])
 def test_speakers_and_distinct_contexts(self):
  a=bank('11');self.assertEqual(24,len(a));self.assertIn('duas cenas diferentes',a[2]['html']);self.assertIn('Ermitão: Y rezaré',a[2]['html']);self.assertIn('não demonstra',a[12]['f']);self.assertIn('não transforma',a[13]['f'])
 def test_evidence_and_open_transfer(self):
  a,b=bank('06'),bank('11');self.assertEqual('emparelhar',a[30]['t']);self.assertIn('oralmente ou no caderno',a[28]['html']);self.assertIn('não há',a[28]['html'].lower());self.assertEqual('rever',b[19]['t']);self.assertIn('outras falas e ações',b[19]['f'])
 def test_teacher_panels_and_revision_loader(self):
  for n in ['06','11']:
   a=bank(n);s=(ROOT/f'm2/painel-m2-f{n}/index.html').read_text('utf-8');rows=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1].lstrip())[0]
   self.assertEqual([i for i,c in enumerate(a) if c['t']!='ler'],[r['k'] for r in rows])
   for r in rows:self.assertEqual(a[r['k']]['t'],r['t'])
   self.assertIn('rever-frase.js',(ROOT/f'm2/licao-m2-f{n}/index.html').read_text('utf-8'))
if __name__=='__main__':unittest.main()
