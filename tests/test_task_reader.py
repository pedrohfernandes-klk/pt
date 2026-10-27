"""Task reader: original source contract, tu consistency and shared-shell boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=json.loads((ROOT/'tests/fixtures/task-reader-before.json').read_text('utf-8'))
class TaskReader(unittest.TestCase):
 def test_original_content_identifiers_links_quotes_and_rubrics_survive(self):
  for slug,old in FIXTURE['pages'].items():
   with self.subTest(task=slug):
    source=(ROOT/f'tarefas/{slug}/index.html').read_text('utf-8')
    body=source.split('<body',1)[1]
    if slug=='m4-u1':
     expected=old['original_body']
     for before,after in FIXTURE['tu_changes'].items():expected=expected.replace(before,after)
     self.assertEqual(expected,body)
    else:self.assertEqual(old['body_sha256'],hashlib.sha256(body.encode()).hexdigest())
    self.assertEqual(old['criteria'],re.findall(r'<div class="task-criteria">(.*?)</div>',source,re.S))
    self.assertEqual(old['blockquotes'],re.findall(r'<blockquote>(.*?)</blockquote>',source,re.S))
    self.assertEqual(old['ids'],re.findall(r'\bid="([^"]+)"',source))
    # Existing hrefs retain their order, including hash links; only reader CSS is new.
    hrefs=re.findall(r'\bhref="([^"]+)"',source)
    self.assertEqual(old['hrefs'],[h for h in hrefs if '/pt-lessons/lesson.css?' not in h and '/task-reader.css?' not in h])
    self.assertEqual(source.count('data-task-question='),4)
 def test_shared_shell_assets_are_ordered_for_fallback_and_existing_feedback(self):
  for slug in FIXTURE['pages']:
   source=(ROOT/f'tarefas/{slug}/index.html').read_text('utf-8')
   self.assertLess(source.index('pt-lessons/lesson.css'),source.index('assets/task-90.css'))
   self.assertLess(source.index('assets/task-90.js'),source.index('pt-lessons/casca.js'))
   self.assertLess(source.index('pt-lessons/casca.js'),source.index('assets/task-reader.js'))
   self.assertNotIn('data-casca',source) # No half-loaded shell hides the original long page.
  legacy=(ROOT/'tarefas/m4-u3/index.html').read_text('utf-8')
  self.assertNotIn('assets/task-reader.js',legacy)
 def test_adapter_moves_nodes_and_never_scores_or_persists(self):
  source=(ROOT/'assets/task-reader.js').read_text('utf-8')
  for required in ('EPICasca.pagina(root)','controller.num(','controller.barra(','controller.acoes(',
                   'controller.rolarTopo(','controller.menu.','appendChild(node)',
                   'positions.reverse()','hashchange','beforeprint','afterprint'):
   self.assertIn(required,source)
  for forbidden in ('localStorage','sessionStorage','cloneNode','page.innerHTML','EPICasca=','EPIJogo.montar'):
   self.assertNotIn(forbidden,source)
  css=(ROOT/'assets/task-reader.css').read_text('utf-8')
  self.assertNotRegex(css,r'#[0-9a-fA-F]{3,8}\b')
  self.assertIn('@media print',css)
  self.assertIn('.task-reader-card[hidden]',css)
 def test_instructional_imperatives_use_tu_without_changing_citations(self):
  forbidden=r'\b(?:Escolham|copiem|Preparem|Escrevam|Localizem|expliquem|respondam|Descrevam|Procurem|Confirmem|tratem|Mostrem|Anotem|Experimentem|Distribuam|ensaiem|registem|revejam|Abram|Compare)\b'
  for slug in FIXTURE['pages']:
   source=(ROOT/f'tarefas/{slug}/index.html').read_text('utf-8')
   source=re.sub(r'<blockquote>.*?</blockquote>','',source,flags=re.S)
   source=re.sub(r'<div class="task-criteria">.*?</div>','',source,flags=re.S)
   self.assertNotRegex(source,forbidden,slug)
  fish=(ROOT/'tarefas/m4-u1/index.html').read_text('utf-8')
  for preserved in ('grupo de 2 ou 3','todos falam','150 a 200 palavras','três a quatro minutos'):
   self.assertIn(preserved,fish)
if __name__=='__main__':unittest.main()
