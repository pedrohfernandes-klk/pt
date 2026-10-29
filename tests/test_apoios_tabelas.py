"""A complete comparison table, with narrowly authorized changes to one reading card."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,unittest
from test_task_routes_closure import original_lesson_text
from auditoria_20261028 import undo as undo_audit_20261028
ROOT=Path(__file__).resolve().parents[1]
PATH='m7/licao-m7-f15/index.html'
class Table(HTMLParser):
 def __init__(self,source):
  super().__init__();self.rows=[];self.cells=[];self.current=None;self.feed(source)
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.rows.append([])
  if tag in ('th','td'):
   self.current={'tag':tag,'attrs':dict(attrs),'text':''};self.rows[-1].append(self.current);self.cells.append(self.current)
 def handle_data(self,data):
  if self.current:self.current['text']+=data
 def handle_endtag(self,tag):
  if tag in ('th','td'):self.current=None
def cards(source):return json.JSONDecoder().raw_decode(source.split('CARTOES=',1)[1].lstrip())[0]
class TableAid(unittest.TestCase):
 def test_exact_source_contract_and_no_changes_to_questions_keys_or_other_cards(self):
  source=(ROOT/PATH).read_text('utf-8');before=original_lesson_text(PATH)
  record=json.loads((ROOT/'tests/fixtures/apoios-tabelas-edits-20261027.json').read_text('utf-8'))['files'][PATH]
  self.assertEqual(hashlib.sha256(before.encode()).hexdigest(),record['base_sha256_lf'])
  # 28/10/2026: as pistas[0] e [1] da F15 mudaram na auditoria do M7 (manifesto literal, fora dos cartões);
  # o hash de depois das tabelas confere-se com essas trocas desfeitas. Os cartões comparam-se na página real.
  self.assertEqual(hashlib.sha256(undo_audit_20261028(PATH,source).encode()).hexdigest(),record['after_sha256_lf'])
  old,new=cards(before),cards(source)
  self.assertEqual(len(old),len(new));self.assertEqual(len(new),21)
  for index,(a,b) in enumerate(zip(old,new)):
   if index==11:
    self.assertEqual({k:v for k,v in a.items() if k!='html'},{k:v for k,v in b.items() if k!='html'})
    self.assertEqual(a['html'].split('<div class="caixa"><h3>Como se formam')[0],b['html'].split('<div class="caixa"><table')[0])
   else:self.assertEqual(a,b,index+1)
  self.assertIn('var K="licao-m7-f15",ID="M7-F15"',source)
 def test_all_seven_concepts_have_headers_definitions_and_examples(self):
  source=cards((ROOT/PATH).read_text('utf-8'))[11]['html'];table=Table(source)
  self.assertEqual([c['text'] for c in table.rows[0]],['Conceito','Definição','Exemplo'])
  self.assertTrue(all(c['attrs']['scope']=='col' for c in table.rows[0]))
  self.assertEqual([r[0]['text'] for r in table.rows[1:]],['Sigla','Acrónimo','Truncação','Amálgama','Empréstimo','Extensão semântica','Onomatopeia'])
  self.assertEqual(len(table.rows),8)
  for row in table.rows[1:]:
   self.assertEqual(len(row),3);self.assertEqual(row[0]['attrs']['scope'],'row')
   self.assertEqual([c['attrs']['data-label'] for c in row[1:]],['Definição','Exemplo'])
   self.assertTrue(all(c['text'].strip() for c in row))
  self.assertEqual([r[2]['text'] for r in table.rows[1:]],['PTM','ONU','foto ← fotografia','portunhol ← português + espanhol','futebol ← football','rato, do computador','tiquetaque'])
 def test_styles_are_opt_in_and_loaded_before_the_appearance_layer(self):
  source=(ROOT/PATH).read_text('utf-8');head=source.split('</head>')[0]
  self.assertLess(head.index('apoios-tabelas.css'),head.index('assets/appearance.css'))
  css=(ROOT/'assets/pt-lessons/apoios-tabelas.css').read_text('utf-8')
  self.assertIn('@media(max-width:620px)',css);self.assertIn('@media print',css)
  self.assertNotIn('tr:first-child',css);self.assertNotIn('display:none',css)
  self.assertNotIn('!important',css)
if __name__=='__main__':unittest.main()
