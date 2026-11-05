"""05/11/2026: pedido do docente («não seria uma tabela?»). Os seis movimentos da M7-F10 numa tabela, e os intervalos de
versos das lições sem quebra de linha (traço de intervalo, espaço sem quebra e junção de palavras)."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,unittest
from auditoria_20261028 import undo_tabela_0511
ROOT=Path(__file__).resolve().parents[1]
F10='m7/licao-m7-f10/index.html'
def cards(source):return json.JSONDecoder().raw_decode(source.split('CARTOES=',1)[1].lstrip())[0]
class Tabela(HTMLParser):
 def __init__(self,source):
  super().__init__();self.rows=[];self.cur=None;self.feed(source)
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.rows.append([])
  if tag in('th','td'):self.cur={'tag':tag,'attrs':dict(attrs),'text':''};self.rows[-1].append(self.cur)
 def handle_data(self,data):
  if self.cur is not None:self.cur['text']+=data
 def handle_endtag(self,tag):
  if tag in('th','td'):self.cur=None
class TabelaMovimentos(unittest.TestCase):
 def test_seis_linhas_com_cabecalhos_e_rotulos(self):
  html=cards((ROOT/F10).read_text('utf-8'))[2]['html']
  self.assertIn('<h3>Os seis movimentos</h3><table class="apoio-tabela movimentos" role="table">',html)
  t=Tabela(html.split('<table',1)[1].split('</table>',1)[0])
  self.assertEqual([c['text'] for c in t.rows[0]],['Letra','Movimento','Exemplo','Onde'])
  self.assertTrue(all(c['attrs']['scope']=='col' for c in t.rows[0]))
  self.assertEqual([r[0]['text'] for r in t.rows[1:]],['S','N','R','M','P','C'])
  for r in t.rows[1:]:
   self.assertEqual(r[0]['attrs']['scope'],'row')
   self.assertEqual([c['attrs']['data-label'] for c in r[1:]],['Movimento','Exemplo','Onde'])
   self.assertTrue(all(c['text'].strip() for c in r))
  # Os dois parágrafos que explicam a tarefa ficam depois da tabela, como estavam.
  self.assertIn('</table><p>R e C respondem a quem discorda',html)
 def test_o_texto_da_tabela_e_o_dos_paragrafos(self):
  # Nada se inventa: cada movimento e cada citação já estavam nos seis parágrafos de antes.
  antes=cards(undo_tabela_0511(F10,(ROOT/F10).read_text('utf-8')))[2]['html']
  html=cards((ROOT/F10).read_text('utf-8'))[2]['html']
  t=Tabela(html.split('<table',1)[1].split('</table>',1)[0])
  for r in t.rows[1:]:
   letra,mov,ex=r[0]['text'],r[1]['text'],r[2]['text']
   self.assertIn(f'<b>{letra}</b>, {mov}',antes)
   for c in re.findall(r'«([^»]+)»',ex):self.assertIn('«'+c+'»',antes)
 def test_folha_das_tabelas_antes_da_aparencia(self):
  head=(ROOT/F10).read_text('utf-8').split('</head>')[0]
  self.assertLess(head.index('pt-lessons/apoios-tabelas.css'),head.index('assets/appearance.css'))
 def test_intervalos_de_versos_sem_quebra(self):
  for f in sorted(ROOT.glob('m*/licao-*/index.html')):
   s=f.read_text('utf-8')
   with self.subTest(licao=f.parent.name):
    self.assertIsNone(re.search(r'vv\.\s\d+-\d+',s))
  for f in (F10,'m1/licao-m1-f02/index.html','m1/licao-m1-f19/index.html'):
   s=(ROOT/f).read_text('utf-8')
   self.assertGreater(len(re.findall('vv\\. \\d+–⁠\\d+',s)),0,f)
if __name__=='__main__':unittest.main()
