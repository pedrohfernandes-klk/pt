"""Live compact assignments, not archived detailed briefs: eight compact tasks (M2 has the choice format)."""
from pathlib import Path
import re, unittest
from test_task_compact_m7 import Compact
ROOT=Path(__file__).resolve().parents[1]
# 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
# 28/10/2026 (decisão do docente): o M2 é o piloto do formato com aquecimento e tema à escolha; as suas
# duas tarefas saem deste contrato compacto e têm o seu em test_task_choice.py.
SLUGS=['m1-u1','m1-u2','m4-u1','m4-u2','m4-u3-discurso','m7-u1','m7-u2','m7-u3']
class CompactTasks(unittest.TestCase):
 def test_live_concision_optional_recall_and_individual_production(self):
  for slug in SLUGS:
   with self.subTest(task=slug):
    text=(ROOT/'tarefas'/slug/'index.html').read_text('utf-8');p=Compact(text)
    self.assertEqual(p.root,['nav','header','section','section'])
    self.assertTrue(p.production_in_header)
    self.assertEqual(p.questions,['1','2']);self.assertEqual(p.optional,[True,True])
    self.assertEqual(p.criteria_items,3)
    self.assertLessEqual(len(' '.join(p.header+p.criteria).split()),180)
    for token in ('Tarefa individual','90 min','consulta','Teams','duas linhas'):
     self.assertIn(token,text)
    for token in ('task-clock','em grupo','rondas','docente cria','10/10/60/10'):
     self.assertNotIn(token,text)
    for anchor in ('produzir','apoios','preparacao','criterios','entregar'):
     self.assertIn(anchor,p.ids)
    module=slug.split('-')[0]
    links=[x for x in p.links if '/'+module+'/licao-' in x]
    self.assertIn(len(links),(2,3))
    self.assertIn('task-reader.js?v=20261027-compact-1',text)
    self.assertIn('task-90.js?v=20261027-compact-1',text)
    # 27/10/2026 (pedido do docente): relógio do aluno, até 60 min de produção, no enunciado.
    self.assertIn('data-relogio data-max="60" data-passo="5" data-rotulo="Produção em papel" data-chave="pt-relogio:tarefas/'+slug+':producao"',text)
    self.assertLess(text.index('assets/relogio.js'),text.index('pt-lessons/casca.js'))
    for i in range(2):
     options=p.options[i*3:i*3+3]
     self.assertEqual(len(options),3)
     self.assertEqual(sum(o['data-correct']=='true' for o in options),1)
     self.assertTrue(all(o.get('data-response') for o in options))
 def test_task_per_unit_in_priority_modules(self):
  for module,count in [('m1',2),('m2',2),('m4',3),('m7',3)]:
   text=(ROOT/module/'index.html').read_text('utf-8')
   self.assertEqual(len(re.findall(r'<li[^>]*data-task-lesson=',text)),count)
if __name__=='__main__':unittest.main()
