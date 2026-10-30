"""Contratos da decisão de 30/10: variedade, fontes e opções sem pistas de tamanho."""
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from auditar_aquecimentos_m1 import auditar
from aquecimentos import plano, texto_visivel
import re


# 30/10/2026: aquecimento em cartões (decisão do docente)
class AquecimentosM1Opcoes(unittest.TestCase):
    def test_variedade_e_opcoes_equilibradas_incluindo_empates_e_lacunas(self):
        for n in (1, 2):
            d=json.loads((ROOT / f'docs/pedagogia/aquecimentos/m1-u{n}.json').read_text('utf-8'))
            with self.subTest(slug=d['slug']):
                self.assertIn(len(d['cartoes']), (12, 13))
                ativos=[c for c in d['cartoes'] if c['t'] != 'ler']
                self.assertGreaterEqual(len(ativos),10)
                self.assertGreaterEqual(len({c['t'] for c in ativos}),5)
                self.assertEqual(d['momento'],'No início da aula de tarefa')
                self.assertEqual(auditar(d)['erros'],[])
                fontes=' '.join(plano(ROOT,p) for p in d['licoes_das_citacoes'])
                for c in d['cartoes']:
                    for citacao in re.findall('«([^»]+)»',texto_visivel(c)):
                        self.assertIn(citacao,fontes)

    def test_medicao_recusa_vantagem_e_distribuicao_denunciadora(self):
        d={'slug':'controlo','cartoes':[{'t':'escolha','o':['abc','abc','abcd'],'c':2}]}
        self.assertTrue(auditar(d)['erros'])
        d['cartoes'][0]['o']=['abc','abc','abc']
        self.assertTrue(auditar(d)['erros'])  # Empates contam, não escondem a pista.
