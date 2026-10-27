"""Grelhas /20 das tarefas de unidade (27/10/2026, decisão do docente; piloto M1).

Cada tarefa com grelha tem: cinco critérios que somam 20, os três níveis descritos com um exemplo cada e o
que custa pontos; uma página do aluno com autoavaliação em papel; uma versão de correção com o feedback em
três partes; e, na tarefa, a ligação à grelha. Só a grelha /20: nenhum peso do módulo nestas páginas.
"""
from pathlib import Path
from html.parser import HTMLParser
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
DADOS=json.loads((ROOT/'docs/pedagogia/grelhas-tarefas-20261027.json').read_text('utf-8'))

class Texto(HTMLParser):
    def __init__(self,s):
        super().__init__();self.out=[];self.skip=0;self.feed(s[s.index('<body'):])
    def handle_starttag(self,t,a):
        if t in('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in('script','style'):self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.out.append(d)
    def __str__(self):return re.sub(r'\s+',' ',' '.join(self.out))

class Grelhas(unittest.TestCase):
    def test_dados(self):
        self.assertIn('m1-u1',DADOS['tarefas']);self.assertIn('m1-u2',DADOS['tarefas'])
        for slug,t in DADOS['tarefas'].items():
            with self.subTest(tarefa=slug):
                self.assertTrue((ROOT/'tarefas'/slug/'index.html').exists())
                self.assertEqual(len(t['criterios']),5)
                self.assertEqual(sum(c['max'] for c in t['criterios']),20)
                for c in t['criterios']:
                    self.assertEqual(set(c['niveis']),{'0','parcial','max'})
                    for desc,ex in c['niveis'].values():self.assertTrue(desc.strip() and ex.strip())
                    self.assertTrue(c['custa'])

    def test_paginas_e_ligacao(self):
        for slug,t in DADOS['tarefas'].items():
            with self.subTest(tarefa=slug):
                tarefa=(ROOT/'tarefas'/slug/'index.html').read_text('utf-8')
                self.assertEqual(tarefa.count('<a href="grelha/">'),1)
                aluno=(ROOT/'tarefas'/slug/'grelha/index.html').read_text('utf-8');correcao=(ROOT/'tarefas'/slug/'correcao/index.html').read_text('utf-8')
                for c in t['criterios']:
                    self.assertIn(c['nome'].replace('«','&laquo;') if '&laquo;' in aluno else c['nome'],aluno)
                self.assertEqual(aluno.count('class="g-crit"'),5);self.assertIn('id="autoavaliacao"',aluno)
                for parte in ('O que funciona','O que te custa pontos','Próximo passo'):self.assertIn(parte,correcao)
                for p in (aluno,correcao):
                    texto=str(Texto(p));baixo=texto.lower()
                    self.assertNotIn('—',texto)
                    for w in ('professor','jogar','ficha','folha','%','teams'):self.assertNotIn(w,baixo,(slug,w))
                    self.assertIn('../../../assets/appearance.css',p)

    def test_gerador_e_idempotente(self):
        import subprocess,sys
        antes={p:p.read_bytes() for p in (ROOT/'tarefas').glob('m1-u*/**/index.html')}
        subprocess.run([sys.executable,'-B','scripts/grelhas_tarefas.py'],cwd=ROOT,check=True,capture_output=True)
        for p,b in antes.items():self.assertEqual(b,p.read_bytes(),p)

if __name__=='__main__':unittest.main()
