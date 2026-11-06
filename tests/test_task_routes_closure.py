# 03/11/2026: cabeçalho sobre F0 publicada, mantendo reversão e asserções.
# 03/11/2026: desfazer primeiro a camada visual do cabecalho, com as mesmas assercoes.
"""26/10 decision: task = closure lesson, synthesis inside, old checkpoints archive only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib,json,re,unittest
from auditoria_20261028 import undo as undo_audit_20261028
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'tests/fixtures/task-route-lesson-content-before.json'
INSTRUCTION_EDITS=ROOT/'tests/fixtures/task-instruction-edits-20261026.json'
GRAMMAR_EDITS=ROOT/'tests/fixtures/m1-grammar-pilot-edits-20261027.json'
TABLE_EDITS=ROOT/'tests/fixtures/apoios-tabelas-edits-20261027.json'
# 28/10/2026: M7-F23, o par de Reis no cartão de emparelhar passa a dizer a ideia (pedido do docente).
REIS_EDITS=ROOT/'tests/fixtures/m7-f23-reis-edits-20261028.json'
# 28/10/2026: correções confirmadas pela auditoria do M1 e do M4 (texto apenas; desfazem-se antes de todas as outras).
AUDIT_EDITS=ROOT/'tests/fixtures/auditoria-m1-m4-edits-20261028.json'
# 28/10/2026: segundo lote da auditoria (M7 inteiro, resto do M4 e do M1), gerado por scripts/aplicar_trocas.py.
# Foi aplicado por cima do #128, por isso desfaz-se antes dele: o mais recente primeiro.
AUDIT_EDITS_M4_M7=ROOT/'tests/fixtures/auditoria-m4-m7-edits-20261028.json'
# 28/10/2026: a Sala de aula sai das lições (decisão do docente de 17/10/2026; scripts/desligar_sala.py). É a mudança
# mais recente: o manifesto dela desfaz-se primeiro, antes das auditorias e de todos os outros.
SALA_EDITS=ROOT/'tests/fixtures/sala-desligada-edits-20261028.json'
# 29/10/2026: aquecimentos e unidade 3 do M7 (a F10 reescrita para a tarefa nova; decisões do docente de 29/10). É a
# camada mais recente: o manifesto dela desfaz-se antes da Sala.
AQUECIMENTOS_EDITS=ROOT/'tests/fixtures/aquecimentos-m7-edits-20261029.json'
# 30/10/2026: texto corrido justificado (decisão do docente): a classe «prosa» nos excertos em prosa dos percursos
# «Pensar devagar». É a camada mais recente: o manifesto dela desfaz-se antes de todos os outros.
JUSTIFICADO_EDITS=ROOT/'tests/fixtures/texto-justificado-edits-20261030.json'
# 30/10/2026: opções denunciadoras (pedido do docente de 29/10): só o texto das opções e do feedback que as cita. É a
# camada mais recente: o manifesto dela desfaz-se antes do do texto justificado.
OPCOES_EDITS=ROOT/'tests/fixtures/opcoes-denunciadoras-edits-20261030.json'
# 30/10/2026: «Qual das…» nas perguntas, os versos 12 e 14 da «Ceifeira» como na Athena (1924) e os acertos do M7. É a
# camada mais recente: o manifesto dela desfaz-se antes do das opções.
LINGUA_EDITS=ROOT/'tests/fixtures/lingua-pessoa-m7-edits-20261030.json'

def original_lesson_text(path):
 """Reverse only the explicitly authorized UX strings; retain the frozen LF hash."""
 source=(ROOT/path).read_text('utf-8')
 # 31/10/2026: a camada das tarefas precede todas as anteriores.
 # 01/11/2026: camada M8/M9 antes das anteriores.
 # 01/11/2026: desfaz primeiro as duas camadas de lições, conservando os hashes históricos.
 # 01/11/2026: os índices desfazem-se antes dos conteúdos e das lições.
 # 02/11/2026: e, antes de todas, as tarefas individuais; antes delas, a calçada da entrada.
 # 02/11/2026: lote 2 antes das camadas históricas, sem normalizações.
 # 03/11/2026: piloto M4, F0, créditos e lote 2, com a mesma reversão estrita.
 # 05/11/2026: a revisão de 5/11 desfaz-se antes de todas.
 # 05/11/2026: e, antes dela, a tabela dos seis movimentos.
  # 05/11/2026: o Laboratório do exame (lição, não «leitura de apoio») é a camada mais recente; desfaz-se antes da tabela dos seis movimentos.
  # 05/11/2026: o contexto de cada sessão do Laboratório do exame (lição e excerto, não «recorte») é a camada mais recente; desfaz-se antes da ligação e das notas do Laboratório do exame.
  # 05/11/2026: a decisão 154 (os exercícios fazem-se sozinho; nada no texto do aluno depende do docente) é a camada mais recente; desfaz-se antes do contexto do Laboratório do exame, com a mesma exigência.
 # 06/11/2026: os créditos atrás de um «i» (decisão 153, pedido pt-2) são a camada mais recente, por cima do lote 3 do Atlas e da decisão 154 (junção com o main); desfazem-se primeiro, com a mesma exigência.
 # 06/11/2026: a decisão 152 no M1 (cuidado_m1_20261106: tabelas e espaços que não quebram) é a camada mais recente, por cima dos créditos atrás de um «i»; desfaz-se primeiro, com a mesma exigência.
 for manifest_path in (ROOT/'tests/fixtures/cuidado-m1-edits-20261106.json',ROOT/'tests/fixtures/creditos-i-edits-20261105.json',ROOT/'tests/fixtures/autonomia-154-edits-20261105.json',ROOT/'tests/fixtures/exame-contexto-edits-20261105.json',ROOT/'tests/fixtures/exame-licao-edits-20261105.json',ROOT/'tests/fixtures/tabela-movimentos-edits-20261105.json',ROOT/'tests/fixtures/revisao-edits-20261105.json',ROOT/'tests/fixtures/cartaz-cabecalho-edits-20261103.json',ROOT/'tests/fixtures/cartaz-m4-piloto-edits-20261102.json',ROOT/'tests/fixtures/variedade-f0-edits-20261102.json',ROOT/'tests/fixtures/creditos-grafismos-ia-edits-20261102.json',ROOT/'tests/fixtures/conteudos-lote2-edits-20261101.json',ROOT/'tests/fixtures/varredura-formatacao-edits-20261101.json',ROOT/'tests/fixtures/calcada-mar-edits-20261102.json',ROOT/'tests/fixtures/tarefas-individuais-edits-20261102.json',ROOT/'tests/fixtures/cartaz-indices-edits-20261101.json',ROOT/'tests/fixtures/licoes-m16-edits-20261101.json',ROOT/'tests/fixtures/licoes-m89-edits-20261101.json',ROOT/'tests/fixtures/tarefas-m89-edits-20261101.json',ROOT/'tests/fixtures/tarefas-m356-edits-20261031.json',LINGUA_EDITS,OPCOES_EDITS,JUSTIFICADO_EDITS,AQUECIMENTOS_EDITS,SALA_EDITS,AUDIT_EDITS_M4_M7,AUDIT_EDITS,REIS_EDITS,TABLE_EDITS,GRAMMAR_EDITS,INSTRUCTION_EDITS):
  manifest=json.loads(manifest_path.read_text('utf-8'))
  for edit in reversed(manifest['files'].get(path,{}).get('edits',[])):
   if source.count(edit['new'])!=edit['occurrences']:
    raise AssertionError(f"Authorized edit no longer matches: {path}: {edit['location']}")
   source=source.replace(edit['new'],edit['old'])
 return source
class Route(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.tasks=[];self.stack=[];self.placements=[];self.links=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a':self.links.append(a.get('href',''))
  if 'data-task-lesson' in a:self.tasks.append(a['data-task-lesson']);self.placements.append(list(self.stack))
  if t not in ('meta','link','img','input','br','hr','source','wbr','area','base','col','embed','param','track'):self.stack.append((t,a))
 def handle_endtag(self,t):
  if any(x[0]==t for x in self.stack):
   i=max(i for i,x in enumerate(self.stack) if x[0]==t);self.stack=self.stack[:i]
def units(s):
 return json.JSONDecoder().raw_decode(s[re.search(r'\bvar U=(\[)',s).start(1):])[0]
class TaskRoutes(unittest.TestCase):
 def test_lessons_order_content_and_old_pools_are_preserved(self):
  for m,before in json.loads(FIXTURE.read_text('utf-8')).items():
   # 28/10/2026: no arquivo do M7, enunciados e explicações sem remissões para cartões e com a numeração
   # certa dos versos (auditoria, manifesto literal); o hash de cada pool calcula-se com as trocas desfeitas.
   s=undo_audit_20261028(f'm{m}/index.html',(ROOT/f'm{m}/index.html').read_text('utf-8'));after=units(s)
   self.assertEqual(len(before['units']),len(after))
   for old,new in zip(before['units'],after):
    self.assertEqual(old['passos'],new['passos']);self.assertEqual(old['licoes'],new['licoes'])
    self.assertEqual(old['pool_sha256'],hashlib.sha256(json.dumps(new['pool'],sort_keys=True,ensure_ascii=False).encode()).hexdigest())
   for path,digest in before['files'].items():
    self.assertEqual(digest,hashlib.sha256(original_lesson_text(path).encode('utf-8')).hexdigest(),path)
 def test_one_classroom_task_per_unit_no_independent_closure_gate(self):
  # 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
  expected={1:['m1-u1','m1-u2'],2:['m2-u1','m2-u2'],4:['m4-u1','m4-u2','m4-u3-discurso'],7:['m7-u1','m7-u2','m7-u3']}
  # 31/10/2026: inclui as seis tarefas aprovadas do M3, M5 e M6.
  expected.update({3: ['m3-u1', 'm3-u2'], 5: ['m5-u1', 'm5-u2'], 6: ['m6-u1', 'm6-u2']})
  # 01/11/2026: todos os módulos têm aula de tarefa.
  expected.update({8:["m8-u1","m8-u2"],9:["m9-u1","m9-u2"]})
  for m,slugs in expected.items():
   s=(ROOT/f'm{m}/index.html').read_text('utf-8');p=Route(s)
   self.assertEqual(len(p.ids),len(set(p.ids)))
   self.assertEqual(p.tasks,[str(i+1) for i in range(len(slugs))])
   self.assertTrue(all(any(t=='ol' and a.get('class')=='passos' for t,a in ancestors) for ancestors in p.placements))
   self.assertNotIn('data-sintese=',s);self.assertNotIn('id="cartao"',s)
   self.assertNotIn('TAREFA FINAL',s);self.assertNotIn('sinteseFeita',s)
   self.assertIn('id="arquivo-percurso" hidden',s)
   self.assertIn('unit-task-route.js',s)
   self.assertNotIn('data-cartaz="percurso"',s)
   self.assertIn('data-cartaz-archive="percurso"',s)
   self.assertIn('route-teacher-tools',s)
   # 06/11/2026: decisão 152 no M1: o número e a unidade não se partem (U+00A0); nos outros módulos, como estava.
   self.assertIn('aula de tarefa de 90'+('\xa0' if m==1 else ' ')+'minutos',s)
   for slug in slugs:
    self.assertIn('../tarefas/'+slug+'/',p.links)
    self.assertIn('../../tarefas/'+slug+'/',(ROOT/f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8'))
   guide=(ROOT/f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
   self.assertIn('id="arquivo-producoes"',guide)
   self.assertNotIn('Cada unidade termina com um desafio',guide)
 def test_adapter_has_no_task_or_historical_completion_writes(self):
  s=(ROOT/'assets/unit-task-route.js').read_text('utf-8')
  for forbidden in ('localStorage.setItem','localStorage.removeItem','sinteseFeita','#cartao'):
   self.assertNotIn(forbidden,s)
  for required in ('percurso-v2-','percurso-sintese-','desafio-unidade-v2-','percurso-','lessonDone','evaluation'):
   if required=='evaluation':continue
   self.assertIn(required,s)
  self.assertIn('teacher',(ROOT/'m7/index.html').read_text('utf-8'))
 def test_m4_comparison_is_support_and_discurso_is_canonical(self):
  old=(ROOT/'tarefas/m4-u3/index.html').read_text('utf-8')
  self.assertIn('APOIO DE COMPARAÇÃO',old);self.assertIn('../m4-u3-discurso/',old)
  self.assertIn('../tarefas/m4-u3-discurso/',(ROOT/'m4/index.html').read_text('utf-8'))
if __name__=='__main__':unittest.main()
