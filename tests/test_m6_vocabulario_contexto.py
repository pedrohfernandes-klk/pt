import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards
from sync_teacher_labels import expected_cards


class VocabularioNoContexto(unittest.TestCase):
    def test_vocabulary_belongs_to_the_text_just_read(self):
        c=lesson_cards(ROOT/'m6/licao-m6-f06/index.html')
        self.assertEqual(validate_cards(c),[])
        self.assertEqual(len(c),27)
        self.assertEqual(c[24]['t'],'emparelhar')
        self.assertEqual(len(c[24]['pares']),4)
        self.assertEqual(len({p[1] for p in c[24]['pares']}),4)
        self.assertIn('Ave-Marias',c[24]['p'])
        for word in ('calafates','varinas','escaleres','canastras'):
            self.assertTrue(any(word in p[0] for p in c[24]['pares']))
            self.assertIn(word,c[15]['html'])
        self.assertNotIn('Horas Mortas',c[24]['p'])
        self.assertIn('observação ou de uma cena inventada',c[26]['html'])

    def test_original_future_vocabulary_stays_in_the_right_lesson(self):
        c=lesson_cards(ROOT/'m6/licao-m6-f07/index.html')
        self.assertEqual(c[31]['pares'],[['emparedados','fechados entre paredes'],['chimera','sonho impossível'],['transmigrar','mudar de vida, renascer'],['fel','amargura']])
        lesson=ROOT/'m6/licao-m6-f06/index.html'
        s=(ROOT/'m6/painel-m6-f06/index.html').read_text('utf-8')
        panel=json.JSONDecoder().raw_decode(s.split('CARTOES=',1)[1])[0]
        self.assertEqual(panel,expected_cards(lesson))
        self.assertNotIn('Liga cada palavra de «Horas Mortas»',s)


if __name__=='__main__':unittest.main()
