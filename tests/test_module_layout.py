"""Contrato de conteúdo dos índices; funciona sem histórico Git na CI."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,unittest
from auditoria_20261028 import undo as undo_audit_20261028

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
   # 28/10/2026: «produção em papel» e «trabalho em papel» também no M4 e no M7 (auditoria; manifesto literal).
   # 28/10/2026 (segundo lote): o undo desfaz também, e antes, o manifesto do M7 e do resto do M4 e do M1
   # (cartões de tarefa do M1 sem «·»; arquivo do M7 sem remissões para cartões).
   source=undo_audit_20261028(f'm{module}/index.html',source)
   # Exact authorised UX wording only; restore it for the frozen index snapshot.
   # 28/10/2026 (PR #122): mais duas cadeias literais autorizadas no M1 («trabalho em papel» nos cartões das tarefas).
   # 28/10/2026 (revisão do PR #122): e uma terceira, «produção em papel» em «Como se cumpre uma unidade», como no M2.
   edits=[e for key in ('authorized_instruction_edits_20261028','authorized_instruction_edits_20261027')
          for e in baseline.get(key,{}).get(f'm{module}',[])]
   for edit in edits:
    self.assertEqual(source.count(edit['new']),1)
    self.assertNotIn(edit['old'],source)
    source=source.replace(edit['new'],edit['old'])
   if module==7 and 'task_route_change_20261026' not in baseline:
    # Authorized final task access; placement and destination are tested separately.
    source=re.sub(r'<aside class="unit-task" id="tarefa-unidade-2".*?</aside>','',source,flags=re.S)
   # 26/10: M1/M4/M7 presentation baseline explicitly includes task lessons. Original lesson
   # content/order/pools are frozen independently by test_task_routes_closure.py.
   content=Content(source.replace('<summary>Explorar ligações opcionais</summary>',''))
   values={'text':content.words,'links':content.links,'images':content.images,'ids':content.ids,
           'scripts':re.findall(r'<script\b.*?</script>',source,re.S)}
   for kind,value in values.items():
    with self.subTest(module=module,kind=kind):
     self.assertEqual(digest(value),baseline['modules'][str(module)][kind])

if __name__=='__main__':unittest.main()
