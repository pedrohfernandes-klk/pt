from pathlib import Path
import json,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank(path):return json.JSONDecoder().raw_decode((ROOT/path).read_text('utf-8').split('CARTOES=',1)[1])[0]
class AspetoContexto(unittest.TestCase):
 def test_teaching_uses_full_context(self):
  c=bank('m8/licao-m8-f06/index.html');self.assertEqual(len(c),24);self.assertIn('várias vezes',c[1]['html']);self.assertIn('não sabemos se chegou ao fim',c[1]['html']);self.assertIn('coexistir',c[1]['html']);self.assertIn('costuma escrever',c[10]['p'])
 def test_feedback_does_not_invent_interruption_or_exact_count(self):
  c=bank('m8/licao-m8-f06/index.html');self.assertIn('não diz se ela parou',c[7]['f']);self.assertIn('não é obrigatória',c[6]['f']);self.assertFalse(c[11]['v']);self.assertIn('não garante conclusão',c[11]['f']);self.assertNotIn('interrompido',c[7]['p2'])
 def test_transfer_has_complete_model(self):
  s=bank('m8/licao-m8-f06/index.html')[23]['html'];self.assertIn('não excerto de um poema',s);self.assertIn('Ela ficou comigo',s);self.assertIn('oralmente ou no caderno',s)
 def test_panel_and_challenge(self):
  c=bank('m8/licao-m8-f06/index.html')
  for x in bank('m8/painel-m8-f06/index.html'):self.assertEqual(x['p'],c[x['k']].get('p',''))
  s=(ROOT/'m8/index.html').read_text('utf-8');units=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for u in units:
   for x in u.get('pool',[]):
    if x.get('_l')!='m8-f06':continue
    text=json.dumps(x,ensure_ascii=False);self.assertNotIn('exigiria um número',text);self.assertNotIn('interrompida',text);self.assertNotIn('Sena escreveu-o',text)
if __name__=='__main__':unittest.main()
