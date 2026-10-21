from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'m8/licao-m8-f04/index.html').read_text('utf-8').split('CARTOES=',1)[1])[0]
class PalavrasEscuta(unittest.TestCase):
 def test_video_has_task_and_alternative(self):
  c=bank();self.assertEqual(len(c),25);s=c[3]['html'];self.assertIn('data-rtp-leitura',s);self.assertIn('Antes:',s);self.assertIn('Depois:',s);self.assertIn('Sem vídeo',s);self.assertIn('não depende de imitar',s);self.assertNotIn('<video',s);self.assertIn('Fonte: RTP Ensina',s)
 def test_cut_model_is_complete_and_deletion_only(self):
  examples=re.findall(r'<dd>(.*?)</dd>',bank()[6]['html']);self.assertEqual([len(t.split()) for t in examples],[17,13,9,6]);tokens=lambda s:re.findall(r'\w+',s.lower());base=tokens(examples[0])
  for text in examples[1:]:
   iterator=iter(base)
   for word in tokens(text):self.assertTrue(any(t==word for t in iterator),word)
  self.assertIn('não garante',bank()[6]['html']);self.assertIn('omit',bank()[19]['f'] if 'omit' in bank()[19]['f'] else bank()[19]['pares'][1][1])
 def test_metaphor_not_just_absence_of_como(self):
  self.assertIn('não basta',bank()[8]['f']);self.assertIn('didática',bank()[14]['p']);self.assertIn('não se reconhece apenas',bank()[2]['html'])
 def test_panel_and_challenge_follow_revision(self):
  c=bank();s=(ROOT/'m8/painel-m8-f04/index.html').read_text('utf-8');panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
  for x in panel:self.assertEqual(x['p'],c[x['k']].get('p',c[x['k']].get('frase','')))
  s=(ROOT/'m8/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s.split('var U=',1)[1])[0]
  for unit in u:
   for x in unit.get('pool',[]):
    if x.get('_l')=='m8-f04':self.assertNotIn('a última diz mais com menos',x.get('f',''));self.assertNotIn('metáfora sem «como»',x.get('f',''))
if __name__=='__main__':unittest.main()
