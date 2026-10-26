"""A entrada pós-visita deve ensinar o drama, com apoio para quem não o viu."""
from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards

class PonteTPC(unittest.TestCase):
 def setUp(self):
  self.cards=lesson_cards(ROOT/'m4/licao-m4-f28/index.html')
 def test_percurso_continua_curto_e_com_o_mesmo_progresso(self):
  self.assertEqual(len(self.cards),15)
  self.assertEqual(sum(c['t']!='ler' for c in self.cards),7)
  self.assertEqual(validate_cards(self.cards),[])
  s=(ROOT/'m4/recursos/tpc-entrada.js').read_text('utf-8')
  self.assertIn('K="licao-m4-f28"',s)
  self.assertIn('save(K+"-a1"',s)
  self.assertNotIn('versao:',s)
  self.assertEqual(self.cards[0]['aula']['tempo'],'45 minutos.')
  self.assertNotIn('Lupi',self.cards[0]['aula']['entrega'])
 def test_o_caso_e_o_modelo_conduzem_ao_conflito_de_garrett(self):
  self.assertIn('data-cc-op',self.cards[0]['html'])
  self.assertIn('inventadas para a aula',self.cards[0]['html'])
  for name in ('Madalena','Manuel','Maria','D. João','Telmo'):
   self.assertIn(name,self.cards[1]['html'])
  self.assertIn('contínuos terrores',self.cards[3]['html'])
  self.assertIn('17591',self.cards[3]['html'])
  self.assertIn('conflito',self.cards[12]['p'])
 def test_gestos_genericos_sao_apoio_e_a_visita_nao_e_requisito(self):
  self.assertIn('<details>',self.cards[9]['html'])
  self.assertIn('não observações do espetáculo',self.cards[9]['html'])
  self.assertIn('Se não assististe',self.cards[11]['html'])
  self.assertIn('não se avalia a memória',self.cards[11]['html'])
  self.assertIn('licao-m4-f07',self.cards[14]['html'])
