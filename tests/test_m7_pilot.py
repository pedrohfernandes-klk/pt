from pathlib import Path
import json,re,unittest
from html.parser import HTMLParser
class Figures(HTMLParser):
 def __init__(self,text):super().__init__();self.stack=[];self.figures=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=="figure" and "doc" in attrs.get("class","").split():self.figures.append(list(self.stack))
  if tag not in ["img","meta","link","br","hr","input","source","wbr"]:self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
ROOT=Path(__file__).resolve().parents[1]
def cards(n):return json.JSONDecoder().raw_decode((ROOT/f'm7/licao-m7-f{n}/index.html').read_text('utf-8').split('CARTOES=',1)[1].lstrip())[0]
class M7Pilot(unittest.TestCase):
 def test_bank_sizes_and_supported_comparison(self):
  a,b=cards('02'),cards('13');self.assertEqual([len(a),len(b)],[23,24])
  self.assertEqual(a[19]['t'],'escolha');self.assertEqual(a[19]['c'],0)
  self.assertIn('diferença',a[15]['html']);self.assertNotIn('dizem o mesmo',a[19]['p'])
  self.assertIn('oralmente ou no caderno',b[20]['html']);self.assertIn('várias respostas sustentadas',b[20]['html'])
  self.assertNotIn('<input',b[20]['html']);self.assertNotIn('<textarea',b[20]['html'])
 def test_reaction_precedes_direct_address(self):
  b=cards('13');self.assertIn('3.ª estrofe',b[11]['f']);self.assertIn('interpela',b[11]['p2'])
  self.assertNotIn('Ó céu',b[8]['p']);self.assertIn('emoções contrárias',b[8]['lacunas'][1]['o'])
  s=(ROOT/'m7/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s[re.search(r'\bU\s*=\s*(\[)',s).start(1):])[0]
  pool=[c for x in u for c in x['pool'] if c.get('_l')=='m7-f13'];self.assertFalse(any('passa a reagir' in c.get('p','') for c in pool))
 def test_opening_figures_are_outside_details(self):
  for n in range(1,10):
   text=(ROOT/f'm{n}/index.html').read_text('utf-8');figs=Figures(text).figures
   self.assertEqual(len(figs),1);self.assertNotIn('details',figs[0]);self.assertIn('<figcaption',text)
if __name__=='__main__':unittest.main()
