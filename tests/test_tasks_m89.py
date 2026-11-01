"""01/11/2026: decisões 20 a 25 nas tarefas e nos guias do M8 e M9."""
from pathlib import Path
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TasksM89(unittest.TestCase):
    def test_extras_sem_exemplos_e_quatro_blocos(self):
        for m in (8, 9):
            s = (ROOT / f'm{m}/guia-da-tarefa-m{m}/index.html').read_text('utf-8')
            extras, _ = json.JSONDecoder().raw_decode(s.split('T=', 1)[1])
            self.assertTrue(extras)
            for extra in extras:
                self.assertTrue(extra['extra'])
                self.assertFalse({'exemplo', 'fraco'} & extra.keys())
            blocks, _ = json.JSONDecoder().raw_decode(s.split('BLOCOS=', 1)[1])
            self.assertEqual([x[0] for x in blocks], [10, 5, 60, 15])
            self.assertIn('Extras sem nota', s)

    def test_pesos_coerentes_e_entregas_das_duas_unidades(self):
        for m in (8, 9):
            for path in (f'm{m}/index.html', f'm{m}/guia-da-tarefa-m{m}/index.html', f'm{m}/mapa-do-modulo-m{m}/index.html'):
                s = (ROOT / path).read_text('utf-8')
                weights = re.search(r'<p class="avaliacao-tarefas">(.*?)</p>', s)[1]
                self.assertEqual(re.findall(r'(\d+) %', weights), ['30', '30', '10', '30'])
                self.assertIn('mesma grelha /20', weights)
            portfolio = (ROOT / f'm{m}/portefolio-do-modulo-m{m}/index.html').read_text('utf-8')
            for u in (1, 2):
                self.assertIn(f'../../tarefas/m{m}-u{u}/', portfolio)
            self.assertNotIn(f'M{m}_Tarefa3', portfolio)

    def test_camada_literal_aplicada_e_reversivel(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py',
                            'scripts/tarefas_m89_20261101.json', '--manifesto',
                            'tests/fixtures/tarefas-m89-edits-20261101.json', '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class LeiturasM8(unittest.TestCase):
    def test_leituras_acrescentadas_sem_alterar_cartoes_anteriores(self):
        from auditoria_20261028 import undo_tarefas_m89
        for n,title,maxlines in [('04','Adeus',2),('05','A verdade histórica',4)]:
            path=ROOT/f'm8/licao-m8-f{n}/index.html'
            s=path.read_text('utf-8'); old=undo_tarefas_m89(path,s)
            cards=lambda text: json.JSONDecoder().raw_decode(text.split('CARTOES=',1)[1])[0]
            before,after=cards(old),cards(s)
            self.assertEqual(len(after),len(before)+1)
            index=next(i for i,c in enumerate(after) if c.get('titulo')==title)
            self.assertEqual(after[index+1]['rot'],'Para levar')
            self.assertEqual(after[:index]+after[index+1:],before)
            self.assertLessEqual(after[index]['html'].split('</blockquote>')[0].count('<br>')+1,maxlines)
            self.assertIn('versao:"20261101-m89-1"',s)
            self.assertIn('https://',after[index]['html'])

if __name__ == '__main__':
    unittest.main()
