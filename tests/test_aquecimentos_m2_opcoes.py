"""M2: equilíbrio, segunda tentativa, fontes e substituições parciais em rever."""
from copy import deepcopy
from pathlib import Path
import json
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from auditar_aquecimentos_m1 import auditar
from aquecimentos import plano, texto_visivel, validar

SLUGS=('m2-u1','m2-u2')


def dados(slug):
    return json.loads((ROOT/f'docs/pedagogia/aquecimentos/{slug}.json').read_text('utf-8'))


def medir(d):
    copia=deepcopy(d)
    # O motor apresenta _itálico_ sem os delimitadores; medem-se os caracteres visíveis.
    for c in copia['cartoes']:
        for q in ([c] if c.get('t') in ('escolha','rever') else c.get('lacunas',[])):
            q['o']=[re.sub(r'_([^_]+)_',r'\1',x) for x in q['o']]
    return auditar(copia)


# 30/10/2026: revisão prévia das tarefas M2, sem alterar páginas ou contratos congelados.
class AquecimentosM2(unittest.TestCase):
    def test_variedade_segunda_tentativa_e_opcoes_equilibradas(self):
        for slug in SLUGS:
            d=dados(slug)
            with self.subTest(slug=slug):
                self.assertEqual(validar(ROOT,d),[])
                self.assertIn(len(d['cartoes']),(12,13))
                ativos=[c for c in d['cartoes'] if c['t']!='ler']
                self.assertEqual(len(ativos),10)
                self.assertGreaterEqual(len({c['t'] for c in ativos}),5)
                self.assertEqual(d['momento'],'No início da aula de tarefa')
                self.assertEqual(medir(d)['erros'],[])
                for c in ativos:
                    self.assertTrue(c.get('p2'))
                    self.assertNotEqual(c['p'].strip(),c['p2'].strip())
                    if c['t'] in ('escolha','rever'):
                        self.assertIsNone(c['fe'][c['c']])
                        self.assertEqual(len({x for x in c['fe'] if x}),len(c['o'])-1)

    def test_citacoes_incluindo_as_curtas_e_passagens_reservadas(self):
        for slug in SLUGS:
            d=dados(slug);fontes=' '.join(plano(ROOT,p) for p in d['licoes_das_citacoes'])
            self.assertTrue(d['reservadas'])
            for n,c in enumerate(d['cartoes'],1):
                with self.subTest(slug=slug,cartao=n):
                    texto=texto_visivel(c).replace('**','')
                    for q in re.findall('«([^»]+)»',texto):
                        for verso in q.split(' / '):self.assertIn(verso.strip(),fontes)
                    if c['t']!='ler':
                        for r in d['reservadas']:self.assertNotIn(r.casefold(),texto.casefold())

    def test_rever_substitui_um_fragmento_sem_repetir_a_moldura(self):
        for slug in SLUGS:
            for c in dados(slug)['cartoes']:
                if c['t']!='rever':continue
                self.assertNotEqual(c['frase'],c['trecho'])
                self.assertEqual(c['frase'].count(c['trecho']),1)
                antes,depois=c['frase'].split(c['trecho'])
                self.assertTrue(antes.strip())
                self.assertTrue(depois.strip())
                for opcao in c['o']:
                    frase=c['frase'].replace(c['trecho'],opcao,1)
                    self.assertEqual(frase,antes+opcao+depois)
                    self.assertNotIn(antes.strip(),opcao)

    def test_menu_remete_para_as_licoes_de_treino(self):
        for slug in SLUGS:
            d=dados(slug)
            destinos={h.removeprefix('../../../').rstrip('/') for h,_ in d['menu']}
            self.assertEqual(destinos,set(d['licoes_das_citacoes']))
            self.assertTrue(all(t.startswith('Relembrar F') for _,t in d['menu']))
            self.assertTrue(all(p.startswith('m2/licao-m2-f') for p in destinos))

    def test_medicao_conta_caracteres_visiveis_do_italico(self):
        d={'slug':'teste','cartoes':[{'t':'escolha','o':['_livro_','livros','livrão'],'c':0}]}
        self.assertEqual(medir(d)['grupos'][0]['caracteres'],[5,6,6])


if __name__=='__main__':
    if '--medir' in sys.argv:
        r=[medir(dados(s)) for s in SLUGS]
        print(json.dumps(r,ensure_ascii=False,indent=2))
        raise SystemExit(1 if any(x['erros'] for x in r) else 0)
    unittest.main()
