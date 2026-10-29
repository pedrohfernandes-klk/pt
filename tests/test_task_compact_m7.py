"""Compact M7: current individual tasks plus literal migration evidence."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,unittest
from task_source_contract import without_timer, compact_task_source
from auditoria_20261028 import undo as undo_audit_20261028
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'tests/fixtures/task-compact-m7-before-after.json'
class Compact(HTMLParser):
 def __init__(self,source):
  super().__init__();self.stack=[];self.ids=[];self.links=[];self.header=[];self.criteria=[];self.questions=[];self.options=[];self.root=[];self.criteria_items=0;self.production_in_header=False;self.optional=[]
  self.feed(source)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);ancestors=[x[0] for x in self.stack]
  if 'id' in a:self.ids.append(a['id'])
  if t in ('a','script','link'):self.links.append(a.get('href',a.get('src','')))
  if self.stack and self.stack[-1][0]=='main':self.root.append(t)
  if a.get('id')=='produzir':self.production_in_header='header' in ancestors
  if 'data-task-question' in a:
   self.questions.append(a['data-task-question']);self.optional.append(any(x[0]=='details' and 'data-task-optional-preparation' in x[1] for x in self.stack))
  if t=='button' and 'data-response' in a:self.options.append(a)
  if t=='li' and any('task-criteria' in x[1].get('class','').split() for x in self.stack):self.criteria_items+=1
  if t not in ('meta','link','img','input','br','hr','source','wbr','area','base','col','embed','param','track'):self.stack.append((t,a))
 def handle_endtag(self,t):
  if any(x[0]==t for x in self.stack):
   i=max(i for i,x in enumerate(self.stack) if x[0]==t);self.stack=self.stack[:i]
 def handle_data(self,data):
  if any(x[0]=='header' for x in self.stack):self.header.append(data)
  if any('task-criteria' in x[1].get('class','').split() for x in self.stack):self.criteria.append(data)
class CompactM7(unittest.TestCase):
 def records(self):return json.loads(MANIFEST.read_text('utf-8'))['files']
 def test_literal_manifest_restores_the_exact_previous_pages(self):
  self.assertEqual(len(self.records()),3)
  for record in self.records():
   # 27/10/2026: o relógio do aluno é a única marca acrescentada depois do manifesto.
   # 28/10/2026: as trocas literais da auditoria do M7 (sem «folhas», cartões pelo nome, próclise, título,
   # itálico) desfazem-se antes de comparar com o manifesto compacto.
   # 29/10/2026 (decisão do docente): a U3 passou ao formato com escolha (manifesto sucessor); o seu retrato
   # compacto lê-se de compact_task_source, depois de a página atual ser validada contra a autorização dela.
   if record['path']=='tarefas/m7-u3/index.html':actual=without_timer(compact_task_source(record['path']))
   else:actual=without_timer(undo_audit_20261028(record['path'],(ROOT/record['path']).read_text('utf-8')))
   self.assertEqual(record['after_source'],actual)
   for key in ('before','after'):
    self.assertEqual(hashlib.sha256(record[key+'_source'].encode()).hexdigest(),record[key+'_sha256'])
   self.assertEqual(record['before_source'][record['before_source'].index('<body'):],record['before_body'])
   self.assertEqual(hashlib.sha256(actual[actual.index('<body'):].encode()).hexdigest(),record['after_body_sha256'])
   self.assertEqual(record['before_source'].count('data-task-question='),4)
 def test_three_card_source_form_concision_optional_feedback_and_links(self):
  for record in self.records():
   path=ROOT/record['path'];source=path.read_text('utf-8')
   # 29/10/2026: a U3 saiu do formato compacto; confere-se a forma do retrato compacto que continua autorizado.
   if record['path']=='tarefas/m7-u3/index.html':source=compact_task_source(record['path'])
   page=Compact(source)
   with self.subTest(page=path):
    self.assertIn('class="task-page" data-task-compact',source)
    self.assertEqual(page.root,['nav','header','section','section'])
    self.assertTrue(page.production_in_header)
    self.assertEqual(page.questions,['1','2']);self.assertEqual(page.optional,[True,True])
    self.assertEqual(page.criteria_items,3);self.assertLessEqual(len(' '.join(page.header+page.criteria).split()),180)
    self.assertEqual(len(page.ids),len(set(page.ids)))
    self.assertIn('Tarefa individual',source);self.assertIn('90 min',source)
    for forbidden in ('task-clock','task-model','prework','rondas','em grupo','data-production-minutes'):
     self.assertNotIn(forbidden,source)
    for i in range(2):
     options=page.options[i*3:i*3+3];self.assertEqual(len(options),3)
     self.assertEqual(sum(x['data-correct']=='true' for x in options),1)
     self.assertEqual(len({x['data-response'] for x in options}),3)
    lesson_links=[x for x in page.links if '/m7/licao-' in x]
    self.assertIn(len(lesson_links),(2,3))
    for href in page.links:
     url=urlsplit(href)
     if url.scheme:continue
     target=(path.parent/unquote(url.path)).resolve() if url.path else path
     if target.is_dir():target=target/'index.html'
     self.assertTrue(target.is_file(),href)
     if url.fragment:self.assertIn('id="'+url.fragment+'"',target.read_text('utf-8'))
 def test_m7_products_and_shared_compact_branch(self):
  first,voice,obj=[x['after_source'] for x in self.records()]
  for text in ('80 a 120','É em nós que é tudo','Quem sou ao menos sinta'):self.assertIn(text,first)
  for text in ('100 a 150','nome, datas, ofício','três fontes','dois minutos','duas escolhas'):self.assertIn(text,voice)
  for text in ('150 a 200','três propostas','três mudanças','três minutos','abandonos','perguntas'):self.assertIn(text,obj)
  adapter=(ROOT/'assets/task-reader.js').read_text('utf-8')
  for contract in ('page.hasAttribute("data-task-compact")','if(!compact&&node.id===','if(quiz&&!compact)','if(status&&!compact)'):
   self.assertIn(contract,adapter)
  self.assertNotIn('localStorage',adapter)
 def test_shared_feedback_counts_two_optional_or_four_legacy_groups(self):
  script=(ROOT/'assets/task-90.js').read_text('utf-8')
  harness=r"""
const vm=require('vm'),assert=require('assert'),script=JSON.parse(require('fs').readFileSync(0,'utf8'));
for(const n of [2,4]){
 const status={textContent:''},groups=[];
 for(let i=0;i<n;i++){
  const f={dataset:{},hidden:true},buttons=[true,false,false].map((c,j)=>({attrs:{'data-correct':String(c),'data-response':'feedback '+i+' '+j},handlers:{},getAttribute(k){return this.attrs[k]},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,fn){this.handlers[k]=fn}}));
  groups.push({getAttribute(){return String(i+1)},querySelector(){return f},querySelectorAll(){return buttons},buttons,f});
 }
 vm.runInNewContext(script,{Set,document:{querySelector(){return status},querySelectorAll(){return groups}}});
 groups.forEach(g=>g.buttons.forEach(b=>{b.handlers.click();assert.equal(g.f.hidden,false);assert.equal(g.f.textContent,b.attrs['data-response'])}));
 assert.equal(status.textContent,'Respostas exploradas: '+n+' de '+n+'. Podes rever qualquer escolha.');
}
"""
  result=subprocess.run(['node','-e',harness],input=json.dumps(script),text=True,capture_output=True)
  self.assertEqual(result.returncode,0,result.stderr)
if __name__=='__main__':unittest.main()
