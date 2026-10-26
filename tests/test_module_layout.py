"""Contrato de conteúdo dos índices; funciona sem histórico Git na CI."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,unittest

ROOT=Path(__file__).resolve().parents[1]

class Content(HTMLParser):
 def __init__(self,s):
  super().__init__();self.words=[];self.links=[];self.images=[];self.ids=[];self.skip=0;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ('script','style'):self.skip+=1
  if t=='a':self.links.append(a.get('href'))
  if t=='img':self.images.append(a)
  if 'id' in a:self.ids.append(a['id'])
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,s):
  if not self.skip:self.words.extend(s.split())

def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

class ModuleLayout(unittest.TestCase):
 def test_nine_modules_keep_student_content_links_images_ids_and_scripts(self):
  baseline=json.loads((ROOT/'tests/fixtures/module-layout-before.json').read_text('utf-8'))
  for module in range(1,10):
   source=(ROOT/f'm{module}/index.html').read_text('utf-8-sig')
   if module==7:
    # Authorized final task access; placement and destination are tested separately.
    source=re.sub(r'<aside class="unit-task" id="tarefa-unidade-2".*?</aside>','',source,flags=re.S)
   # The only new text is the label of an optional disclosure.
   content=Content(source.replace('<summary>Explorar ligações opcionais</summary>',''))
   values={'text':content.words,'links':content.links,'images':content.images,'ids':content.ids,
           'scripts':re.findall(r'<script\b.*?</script>',source,re.S)}
   for kind,value in values.items():
    with self.subTest(module=module,kind=kind):
     self.assertEqual(digest(value),baseline['modules'][str(module)][kind])

if __name__=='__main__':unittest.main()
