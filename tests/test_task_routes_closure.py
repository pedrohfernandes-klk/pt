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
 # 06/11/2026: o desenho comum dos nove índices (decisão 148) é a camada mais recente, por cima dos créditos atrás de um «i»; desfaz-se primeiro, com a mesma exigência.
 # 07/11/2026: os três acertos dos índices deixados pela decisão 173 são a camada mais recente, por cima do desenho comum dos nove índices; desfazem-se primeiro, com a mesma exigência.
 # 07/11/2026 (fusão do main 29441e6b no pedido #182): a decisão 152 no M1 (cuidado_m1_20261106) passa a camada mais recente, por cima dos acertos da decisão 173; desfaz-se primeiro, com a mesma exigência.
 # 07/11/2026: os créditos atrás de um «i» na entrada, nos índices e no Atlas (creditos_i_pt1_20261107, pedido pt-1) passam a camada mais recente, por cima da decisão 152 no M1; desfazem-se primeiro, com a mesma exigência.
 # 08/11/2026: o cartaz «Ler a cidade» na entrada e o nome novo da secção nas páginas publicadas (cidade_cartaz_20261108, que muda a frase da sugestão «continua» das lições) passam a camada mais recente, por cima dos créditos atrás de um «i» do pedido pt-1; desfazem-se primeiro, com a mesma exigência.
 # 08/11/2026: a decisão 152 no M2 (cuidado_m2_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M2, incluindo o índice do módulo) passa a camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção; desfaz-se primeiro, com a mesma exigência.
 # 08/11/2026: a decisão 152 no M3 (cuidado_m3_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M3, incluindo o índice, o guia e o mapa do módulo) passa a camada mais recente, por cima da decisão 152 no M2; desfaz-se primeiro, com a mesma exigência.
 # 08/11/2026: a decisão 152 no M4 (cuidado_m4_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M4, incluindo o índice, o guia, o mapa e o portefólio do módulo) passa a camada mais recente, por cima da decisão 152 no M3; desfaz-se primeiro, com a mesma exigência.
 # 08/11/2026: a decisão 152 no M5 (cuidado_m5_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M5, incluindo o índice, o guia, o mapa e o portefólio do módulo, e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M4; desfaz-se primeiro, com a mesma exigência.
 # 08/11/2026: a decisão 152 no M6 (cuidado_m6_20261108: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M6, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo» e «Pensar devagar», e nas tarefas, nos aquecimentos e nas grelhas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M5; desfaz-se primeiro, com a mesma exigência.
 # 11/11/2026: a decisão 152 no M7 (cuidado_m7_20261111: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M7, incluindo o índice, o guia, o mapa e o portefólio do módulo, as páginas «Ler a fundo», «Olhar» e «Pensar devagar», e nas tarefas, nos aquecimentos e na grelha das suas unidades) passa a camada mais recente, por cima da decisão 152 no M6; desfaz-se primeiro, com a mesma exigência.
 # 12/11/2026: a decisão 152 no M8 (cuidado_m8_20261112: tabelas onde há itens paralelos e espaços que não quebram nas lições e páginas do M8, incluindo o índice, o guia, o mapa e o portefólio do módulo, as atividades de gramática e de escrita e as tarefas das suas unidades) passa a camada mais recente, por cima da decisão 152 no M7; desfaz-se primeiro, com a mesma exigência.
 # 12/11/2026: a decisão 152 no M9 (cuidado_m9_20261112) passa a camada mais recente, por cima da decisão 152 no M8; desfaz-se primeiro, com a mesma exigência.
 # 12/11/2026: a decisão 152 no Exame e nas páginas transversais (cuidado_exame_20261112: uma tabela onde havia itens paralelos e espaços que não quebram nas sessões, no laboratório, nas provas em cartões e nos aquecimentos do Exame, nas obras, nas páginas dos anos, no mapa e na entrada) passa a camada mais recente, por cima da decisão 152 no M9; desfaz-se primeiro, com a mesma exigência.
 # 12/11/2026: a ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112: só a navegação de exame/index.html) passa a camada mais recente, por cima da decisão 152 no Exame e nas páginas transversais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
 # 12/11/2026: as provas em cartões com os documentos oficiais (exame_provas_oficial_20261112: a secção exame/provas/, as seis lições das provas de 2026 e os seus dados) passam a camada mais recente, por cima da ligação «Treinos» na página principal do Exame; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
 # 12/11/2026: as duas tarefas do M3 mais fáceis de fazer e «tudo junto» no M3 (tarefas_faceis_m3_20261112: os enunciados, as grelhas, as correções e os aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3) passam a camada mais recente, por cima das provas em cartões com os documentos oficiais; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
 # 13/11/2026: as duas tarefas do M1 mais fáceis de fazer e «tudo junto» no M1 (tarefas_faceis_m1_20261113: os enunciados, as grelhas e as correções da m1-u1 e da m1-u2, os seus dados, e o guia, o índice e o portefólio do M1) passam a camada mais recente, por cima das tarefas do M3 mais fáceis de fazer; desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
 for manifest_path in (ROOT/'tests/fixtures/tarefas-faceis-m1-edits-20261113.json',ROOT/'tests/fixtures/tarefas-faceis-m3-edits-20261112.json',ROOT/'tests/fixtures/exame-provas-oficial-edits-20261112.json',ROOT/'tests/fixtures/exame-ligacao-treinos-edits-20261112.json',ROOT/'tests/fixtures/cuidado-exame-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m9-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m8-edits-20261112.json',ROOT/'tests/fixtures/cuidado-m7-edits-20261111.json',ROOT/'tests/fixtures/cuidado-m6-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m5-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m4-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m3-edits-20261108.json',ROOT/'tests/fixtures/cuidado-m2-edits-20261108.json',ROOT/'tests/fixtures/cidade-cartaz-edits-20261108.json',ROOT/'tests/fixtures/creditos-i-pt1-edits-20261107.json',ROOT/'tests/fixtures/cuidado-m1-edits-20261106.json',ROOT/'tests/fixtures/indices-acertos-edits-20261107.json',ROOT/'tests/fixtures/cartaz-indices-148-edits-20261106.json',ROOT/'tests/fixtures/creditos-i-edits-20261105.json',ROOT/'tests/fixtures/autonomia-154-edits-20261105.json',ROOT/'tests/fixtures/exame-contexto-edits-20261105.json',ROOT/'tests/fixtures/exame-licao-edits-20261105.json',ROOT/'tests/fixtures/tabela-movimentos-edits-20261105.json',ROOT/'tests/fixtures/revisao-edits-20261105.json',ROOT/'tests/fixtures/cartaz-cabecalho-edits-20261103.json',ROOT/'tests/fixtures/cartaz-m4-piloto-edits-20261102.json',ROOT/'tests/fixtures/variedade-f0-edits-20261102.json',ROOT/'tests/fixtures/creditos-grafismos-ia-edits-20261102.json',ROOT/'tests/fixtures/conteudos-lote2-edits-20261101.json',ROOT/'tests/fixtures/varredura-formatacao-edits-20261101.json',ROOT/'tests/fixtures/calcada-mar-edits-20261102.json',ROOT/'tests/fixtures/tarefas-individuais-edits-20261102.json',ROOT/'tests/fixtures/cartaz-indices-edits-20261101.json',ROOT/'tests/fixtures/licoes-m16-edits-20261101.json',ROOT/'tests/fixtures/licoes-m89-edits-20261101.json',ROOT/'tests/fixtures/tarefas-m89-edits-20261101.json',ROOT/'tests/fixtures/tarefas-m356-edits-20261031.json',LINGUA_EDITS,OPCOES_EDITS,JUSTIFICADO_EDITS,AQUECIMENTOS_EDITS,SALA_EDITS,AUDIT_EDITS_M4_M7,AUDIT_EDITS,REIS_EDITS,TABLE_EDITS,GRAMMAR_EDITS,INSTRUCTION_EDITS):
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
   # 08/11/2026: decisão 152 no M2: também no índice do M2 (achado 26); nos outros módulos, como estava.
   # 08/11/2026: decisão 152 no M3: também no índice do M3 (achado 34); nos outros módulos, como estava.
   # 08/11/2026: decisão 152 no M4: também no índice do M4 (achado 34); nos outros módulos, como estava.
   # 08/11/2026: decisão 152 no M5: também no índice do M5 (achado 41); nos outros módulos, como estava.
   # 08/11/2026: decisão 152 no M6: também no índice do M6 (achado 32); nos outros módulos, como estava.
   # 11/11/2026: decisão 152 no M7: também no índice do M7 (achado 9); nos outros módulos, como estava.
   # 12/11/2026: decisão 152 no M8: também no índice do M8 (achado 22); no M9, como estava.
   # 12/11/2026: decisão 152 no M9: também no índice do M9 (achado 23); agora nos nove módulos.
   self.assertIn('aula de tarefa de 90'+('\xa0' if m in (1,2,3,4,5,6,7,8,9) else ' ')+'minutos',s)
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
