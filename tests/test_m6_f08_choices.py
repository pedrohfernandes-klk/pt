import json
from pathlib import Path
import re
import sys
import unittest
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_cards import lesson_cards,validate_cards


class CreativeChoices(unittest.TestCase):
    def test_task_and_course_formats_keep_the_agreed_quantity(self):
        source=(ROOT/'m6/licao-m6-f08/index.html').read_text(encoding='utf-8')
        cards=lesson_cards(ROOT/'m6/licao-m6-f08/index.html')
        self.assertEqual(validate_cards(cards),[])
        self.assertEqual(len(cards),20)
        self.assertIn('quatro fotografias, uma por parte',cards[1]['html'])
        self.assertIn('sete horas',cards[1]['html'])
        self.assertIn('25 %',cards[1]['html'])
        self.assertNotIn('seis fotografias',source.lower())
        self.assertIn('Quatro fotografias',(ROOT/'m6/guia-da-tarefa-m6/index.html').read_text(encoding='utf-8'))

    def test_challenge_copies_keep_context_and_feedback(self):
        cards=lesson_cards(ROOT/'m6/licao-m6-f08/index.html')
        text=(ROOT/'m6/index.html').read_text(encoding='utf-8')
        units,_=json.JSONDecoder().raw_decode(re.split(r'var U\s*=',text,1)[1])
        pool=[c for u in units for c in u['pool']]
        for i in (3,12):
            matches=[c for c in pool if c.get('p')==cards[i]['p']]
            self.assertEqual(len(matches),1)
            for k,v in cards[i].items():self.assertEqual(matches[0][k],v)
            self.assertIn('I',cards[i]['p2'])
        self.assertNotIn('seis fotografias',text.lower())

    def test_downloadable_slides_do_not_restore_six_photographs(self):
        path=ROOT/'m6/diapositivos/sessao-08-m6-f08.pptx'
        with ZipFile(path) as z:
            names=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
            self.assertEqual(len(names),10)
            text=' '.join(z.read(n).decode('utf-8') for n in names)
        self.assertNotIn('seis fotografias',text)
        self.assertEqual(text.count('quatro fotografias'),2)


if __name__=='__main__':unittest.main()
