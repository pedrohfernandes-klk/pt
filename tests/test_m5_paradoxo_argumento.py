import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards

class ParadoxoArgumento(unittest.TestCase):
    def test_model_distinguishes_order_from_semantic_tension(self):
        c=lesson_cards(ROOT/'m5/licao-m5-f04/index.html')
        self.assertEqual(validate_cards(c),[]);self.assertEqual(len(c),28)
        self.assertEqual(c[26]['t'],'frase')
        self.assertEqual(c[26]['palavras'],['a','violencia','de','um','pae','é','sempre','amor.'])
        self.assertIn('não na ordem',c[26]['f'])
        self.assertIn('Reformulação para experimentar',c[22]['html'])
        self.assertIn('afirmação da personagem',c[22]['html'])
        self.assertIn('uma fala de Teresa e uma ameaça',c[27]['html'])
        self.assertIn('dois desenhos',c[27]['html'])

    def test_original_text_and_other_interactions_stay_usable(self):
        c=lesson_cards(ROOT/'m5/licao-m5-f04/index.html')
        self.assertIn('a violencia de um pae é sempre amor',c[6]['html'])
        self.assertIn('Morrerás',c[18]['html'])
        self.assertEqual(c[23]['pares'][1],['Tadeu ama a filha','inferência discutível'])
        self.assertEqual(c[24]['t'],'ordenar')
        self.assertEqual(len(c[24]['passos']),4)

if __name__=='__main__':unittest.main()
