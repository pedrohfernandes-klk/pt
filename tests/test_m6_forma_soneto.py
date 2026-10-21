import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def bank():return json.JSONDecoder().raw_decode((ROOT/'m6/licao-m6-f01/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class FormaSoneto(unittest.TestCase):
 def test_distinguishes_meter_and_stanzas(self):
  c=bank();self.assertEqual(len(c),24);self.assertIn('Existem sonetos com outras medidas',c[17]['html']);self.assertIn('última sílaba tónica',c[17]['html']);self.assertIn('Neste poema',c[20]['frase']);self.assertNotIn('versos de dez sílabas',c[20]['frase'])
 def test_sequence_uses_textual_evidence(self):
  c=bank();self.assertNotIn('ferido',c[21]['passos'][1]);self.assertIn('armas desfeitas',c[21]['passos'][1]);self.assertIn('fragor',c[23]['html']);self.assertIn('Não basta',c[23]['html'])
 def test_teacher_question_matches(self):
  self.assertIn(bank()[20]['p'],(ROOT/'m6/painel-m6-f01/index.html').read_text('utf-8'))
if __name__=='__main__':unittest.main()
