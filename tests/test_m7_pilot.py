from pathlib import Path
import json,re,unittest
from html.parser import HTMLParser
# 07/11/2026: a camada dos créditos atrás de um «i» do pedido pt-1 desfaz-se para conferir o figcaption de antes.
from auditoria_20261028 import undo_creditos_i_pt1_0711
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
  # 11/11/2026: decisão 152 no M7 (achado 22): «3.ª estrofe» leva espaço que não quebra (U+00A0) no retorno.
  b=cards('13');self.assertIn('3.ª\xa0estrofe',b[11]['f']);self.assertIn('interpela',b[11]['p2'])
  self.assertNotIn('Ó céu',b[8]['p']);self.assertIn('emoções contrárias',b[8]['lacunas'][1]['o'])
  s=(ROOT/'m7/index.html').read_text('utf-8');u=json.JSONDecoder().raw_decode(s[re.search(r'\bU\s*=\s*(\[)',s).start(1):])[0]
  pool=[c for x in u for c in x['pool'] if c.get('_l')=='m7-f13'];self.assertFalse(any('passa a reagir' in c.get('p','') for c in pool))
 def test_opening_figures_are_outside_details(self):
  for n in range(1,10):
   text=(ROOT/f'm{n}/index.html').read_text('utf-8');figs=Figures(text).figures
   # 07/11/2026: decisões 153, 176 e 177 (pedido pt-1). O crédito da imagem documental passa para trás de um «i» e o figcaption
   # sai (camada creditos_i_pt1_20261107, por cima, conferida em tests/test_creditos_i_pt1.py): o figcaption de antes confere-se
   # na página com essa camada desfeita, e a imagem continua com o seu crédito, agora no «i» da sua moldura.
   self.assertEqual(len(figs),1);self.assertIn('<figcaption',undo_creditos_i_pt1_0711(f'm{n}/index.html',text))
   self.assertIn('<details class="info-i" name="info-i">',text[text.index('<figure class="doc">'):text.index('</figure>',text.index('<figure class="doc">'))])
   # 02/11/2026: só no piloto M4 a imagem documental integra os recursos nativos (06/11/2026: deixou de valer com a decisão 148).
   # 06/11/2026: decisão 148, volta a exigir-se o mesmo nos nove: a imagem documental fica fora de qualquer details (a seguir
   # às unidades, fora de «Recursos do módulo»).
   self.assertNotIn('details',figs[0])
if __name__=='__main__':unittest.main()
