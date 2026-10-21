from pathlib import Path
import unittest,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards
class Adenda(unittest.TestCase):
 def test_shared_retomas_are_optional_unscored_and_allow_individual_work(self):
  for path,index in [('m1/licao-m1-f02/index.html',19),('m9/licao-m9-f10/index.html',15)]:
   c=lesson_cards(ROOT/path)[index]
   self.assertEqual(c['t'],'ler');self.assertIn('class="retoma-partilhada"',c['html']);self.assertIn('A sós',c['html'])
   self.assertNotIn('<input',c['html']);self.assertNotIn('<textarea',c['html']);self.assertFalse(set(c)&{'c','v','pares','lacunas'})
 def test_map_does_not_restore_rigid_historical_roles(self):
  s=(ROOT/'m1/mapa-do-modulo-m1/index.html').read_text('utf-8')
  self.assertIn('alguns jograis também compunham',s);self.assertIn('contornos discutidos',s)
  self.assertNotIn('o trovador, nobre, cria o texto e a música; o jogral, de origem humilde',s)
if __name__=='__main__':unittest.main()
