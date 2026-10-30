"""M4: opções equilibradas, treino distinto das tarefas e citações verificáveis."""
from pathlib import Path
import json
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from auditar_aquecimentos_m1 import auditar
from aquecimentos import plano, texto_visivel, validar

SLUGS=('m4-u1','m4-u2','m4-u3-discurso')


# 30/10/2026: aquecimento em cartões (decisão do docente); ligações tratadas noutra camada.
class AquecimentosM4(unittest.TestCase):
    def test_baralhos_completos_variedade_e_opcoes_sem_pistas_de_tamanho(self):
        for slug in SLUGS:
            d=json.loads((ROOT/f'docs/pedagogia/aquecimentos/{slug}.json').read_text('utf-8'))
            with self.subTest(slug=slug):
                self.assertEqual(validar(ROOT,d),[])
                self.assertIn(len(d['cartoes']),(12,13))
                ativos=[c for c in d['cartoes'] if c['t']!='ler']
                self.assertEqual(len(ativos),10)
                self.assertGreaterEqual(len({c['t'] for c in ativos}),5)
                self.assertEqual(d['momento'],'No início da aula de tarefa')
                medicao=auditar(d)
                self.assertEqual(medicao['erros'],[])
                self.assertEqual(medicao['grupos_de_opcoes'],6)
                for c in ativos:
                    if c['t'] in ('escolha','rever'):
                        self.assertIsNone(c['fe'][c['c']])
                        self.assertEqual(len(set(x for x in c['fe'] if x)),len(c['o'])-1)

    def test_todas_as_citacoes_e_reservas_conferem_sem_limite_minimo(self):
        for slug in SLUGS:
            d=json.loads((ROOT/f'docs/pedagogia/aquecimentos/{slug}.json').read_text('utf-8'))
            fontes=' '.join(plano(ROOT,p) for p in d['licoes_das_citacoes'])
            for n,c in enumerate(d['cartoes'],1):
                with self.subTest(slug=slug,cartao=n):
                    texto=texto_visivel(c)
                    for citacao in re.findall('«([^»]+)»',texto):
                        self.assertIn(citacao,fontes)
                    if c['t']!='ler':
                        for r in d['reservadas']:self.assertNotIn(r.casefold(),texto.casefold())

    def test_casos_criados_nao_se_apresentam_como_o_espetaculo_ou_o_discurso_avaliado(self):
        for slug in ('m4-u2','m4-u3-discurso'):
            d=json.loads((ROOT/f'docs/pedagogia/aquecimentos/{slug}.json').read_text('utf-8'))
            abertura=texto_visivel(d['cartoes'][0])
            self.assertIn('inventad',abertura)
        self.assertFalse((ROOT/'tarefas/m4-u3/aquecimento/index.html').exists())


if __name__=='__main__':
    unittest.main()
