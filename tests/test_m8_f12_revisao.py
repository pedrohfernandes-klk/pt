"""F12 review, teacher index and unit challenge remain pedagogically aligned."""
from pathlib import Path
import json
import unittest
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
def data(path,marker):
    return json.JSONDecoder().raw_decode((ROOT/path).read_text('utf-8').split(marker,1)[1])[0]

class Options(HTMLParser):
    def __init__(self,text):
        super().__init__();self.active=False;self.values=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='select':self.active='data-r-k' in a
        if tag=='option' and self.active:self.values.append(int(a['value']))
    def handle_endtag(self,tag):
        if tag=='select':self.active=False

class F12Review(unittest.TestCase):
    def setUp(self):
        self.cards=data('m8/licao-m8-f12/index.html','CARTOES=')
        self.units=data('m8/index.html','var U=')
        self.pool=[c for c in self.units[1]['pool'] if c.get('_l')=='m8-f12']

    def test_aspect_feedback_matches_the_lesson_in_challenge(self):
        for index in (8,17):
            card=self.cards[index]
            copied=next(c for c in self.pool if c['p']==card['p'])
            self.assertEqual(card['f'],copied['f'])
            self.assertEqual(card['p2'],copied['p2'])
        self.assertEqual(self.cards[8]['c'],2)
        self.assertIn('Um hábito também envolve repetição',self.cards[8]['f'])
        self.assertIn('não é necessária uma contagem exata',self.cards[8]['f'])
        self.assertIn('não diz que a pintora parou',self.cards[17]['f'])

    def test_challenge_requires_evidence_instead_of_universal_preference(self):
        comparison=next(c for c in self.pool if c['p']==self.cards[6]['p'])
        self.assertEqual(comparison['o'],self.cards[6]['o'])
        self.assertEqual(comparison['fe'],self.cards[6]['fe'])
        inference=next(c for c in self.pool if c.get('o',[''])[0]=='Inferência sustentada')
        self.assertTrue(inference['voc']);self.assertEqual(inference['c'],0)
        self.assertIn('palavras ou ações do texto',inference['p'])
        self.assertNotIn('preferem fazer o quê',json.dumps(self.pool,ensure_ascii=False))

    def test_duplicate_recycled_without_losing_author_coverage(self):
        authors=[c for c in self.pool if c.get('pares')==self.cards[14]['pares']]
        self.assertEqual(len(authors),1)
        reference=next(c for c in self.pool if 'exemplo inventado' in c.get('p',''))
        self.assertEqual([v for _,v in reference['pares']],['o conto','a revista','um poema','uma carta'])
        self.assertIn('informação anterior',reference['f'])
        self.assertEqual(len(self.cards),22)
        self.assertEqual(len(self.units[1]['pool']),53)
        self.assertEqual(len(self.pool),15)

    def test_teacher_only_offers_current_interactive_cards(self):
        expected=[{'k':i,'t':c['t'],'p':c.get('p',c.get('frase',''))} for i,c in enumerate(self.cards) if c['t']!='ler']
        panel_path='m8/painel-m8-f12/index.html'
        self.assertEqual(data(panel_path,'CARTOES='),expected)
        self.assertEqual(Options((ROOT/panel_path).read_text('utf-8')).values,[c['k'] for c in expected])
        self.assertNotIn(10,[c['k'] for c in expected])

    def test_retrieval_has_antecedent_and_hypothesis_is_labelled(self):
        self.assertIn('Li o conto. Ele surpreendeu-me',self.cards[1]['html'])
        self.assertIn('hipótese',self.cards[11]['p'])
        self.assertEqual(self.cards[11]['certas'],[8,9,10])
        words=self.cards[11]['frase'].split()
        self.assertEqual([words[i] for i in self.cards[11]['certas']],['o','que','calam.'])

    def test_reading_sources_are_linked_and_distinguish_original_from_reproduction(self):
        for lesson,url in [('03','https://ensina.rtp.pt/artigo/jorge-sena-poesia/'),('04','https://ensina.rtp.pt/artigo/as-palavras-de-eugenio-de-andrade/'),('05','https://searanova.publ.pt/2023/08/07/poesia-prece-no-mediterraneo/')]:
            reading=data(f'm8/licao-m8-f{lesson}/index.html','CARTOES=')[3]['html']
            self.assertIn('href="'+url+'"',reading)
            self.assertIn('rel="noopener"',reading)
            self.assertIn(url,self.cards[10]['html'])
        prece=data('m8/licao-m8-f05/index.html','CARTOES=')[3]['html']
        for clue in ('Ágora','2019','Reprodução consultada','2023'):self.assertIn(clue,prece)
        sena=data('m8/licao-m8-f03/index.html','CARTOES=')[3]['html']
        self.assertIn('Fidelidade',sena);self.assertIn('nota 2',sena)
        eugenio=data('m8/licao-m8-f04/index.html','CARTOES=')[3]['html']
        self.assertNotIn('_Até Amanhã_',eugenio)
        self.assertIn('Publicação consultada',eugenio)

if __name__=='__main__':unittest.main()
