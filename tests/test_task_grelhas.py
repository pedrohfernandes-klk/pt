"""Grelhas /20 das tarefas de unidade (27/10/2026, decisão do docente; piloto M1; 28/10/2026, regra das soluções).

Cada tarefa com grelha tem: cinco critérios que somam 20, os três níveis descritos com um exemplo cada e o
que custa pontos; uma página do aluno com autoavaliação em papel; uma versão de correção com o feedback em
três partes; e, na tarefa, a ligação à grelha. Só a grelha /20: nenhum peso do módulo nestas páginas.
"""
from pathlib import Path
from html.parser import HTMLParser
import html,json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
DADOS=json.loads((ROOT/'docs/pedagogia/grelhas-tarefas-20261027.json').read_text('utf-8'))
# 28/10/2026 (regra do docente: nunca publicar soluções). A grelha do aluno e a versão de correção são públicas:
# nenhum descritor nem exemplo pode responder à tarefa. Cadeias tiradas da chave da correção (guardada fora do
# repositório): as palavras e as passagens que a tarefa manda analisar, as passagens que respondem ao núcleo, o
# recurso pedido e os factos e casos com que cada tema se responde. Nenhuma pode aparecer nas duas páginas.
PROIBIDAS={
 'm1-u1':[r'\bmare\b',r'\bmalu\b','se verrá cedo','se vistes meu amigo','se vistes meu amado','Ondas do mar levado','às ondas',
          'Ca em mia senhor','direi-vos como vos loarei','dona fea, velha e sandia','vos quero loar','vos loarei','loar mia senhor',
          'mais que todas las do mundo','nom fal','escárnio','Chega já','Pergaminho Vindel','Anneliina Rif','harpa','vitrina',
          'Sharrer','1680','instrumentos'],
 'm1-u2':['se moveram todos','mão armada','correndo à pressa','pera lhe dar vida','escusar morte','não cabiam pelas ruas',
          'lugares escusos','viúva que rei não tinha','Soaram as vozes','ouvindo todos bradar','Vamos pra rua','Matam o Mestre',
          'síncope','entre o p e o r','a do meio','Acorramos ao Mestre','6 de dezembro','galope','rijamente','esgravat',
          'homens e moços','bagaço','pouco amigas da natureza','reluziam','sino da quadrilha','corriam pera lá','1860','plumas',
          'Sousa Azevedo','grandes volumes de livros','públicas escrituras','Froissart','3 de setembro','peste',
          'Torre do Tombo','guarda-mor'],
}
# Também não se diz, na mesma frase, qual das cantigas cumpre a promessa nem que recurso a desmente em Guilhade.
PARES={'m1-u1':[('Guilhade',('ironia','escárnio','desment','troça','insulto','paródia')),('Dinis',('cumpr','desment','ironia'))]}

# 28/10/2026: as citações e os factos dos exemplos (outros casos do mesmo tipo) estão, letra a letra, numa lição do
# M1. Cada linha: a lição, o texto como está na lição e, quando o exemplo o cita tal e qual, o texto na grelha.
CITACOES={
 'm1-u1':[('licao-m1-f02',"Ai Deus, e u é?","«Ai Deus, e u é?»"),
          ('licao-m1-f02',"quem diz «eu» é uma rapariga, que pergunta às flores pelo amigo","quem diz «eu» é uma rapariga, que pergunta às flores pelo amigo"),
          ('licao-m1-f02',"Eu atendendo meu amig', eu a[tendendo].","“Eu atendendo meu amig', eu a[tendendo]”"),
          ('licao-m1-f02',"Sedia-m'eu na ermida de Sam Simion","“Sedia-m'eu na ermida de Sam Simion”"),
          ('licao-m1-f02',"nom hei [eu i] barqueiro nem sei remar","“nom hei [eu i] barqueiro nem sei remar”"),
          ('licao-m1-f02','Nesta ilha da ria de Vigo ficava a ermida de San Simón',None),('licao-m1-f02','DOA, um grupo galego',None),
          ('licao-m1-f02','A gravação é uma interpretação de hoje','a gravação é uma interpretação de hoje'),
          ('licao-m1-f05','Em «luna», o n do meio cai','luna > lua'),('licao-m1-f05','«lupum» > «lobo»','lupum > lobo'),
          ('licao-m1-f05','O gesto é o mesmo, cair','O gesto é o mesmo, cair'),
          ('licao-m1-f19','Uma hora à espera do autocarro: «Que rapidez!»','«Que rapidez!»'),
          ('licao-m1-f19','A sopa está boa, e alguém diz: «Que sopa boa!»','«Que sopa boa!»'),
          ('licao-m1-f19','Exagerar é dizer o que se pensa, em grande','exagerar é dizer o que se pensa, em grande')],
 'm1-u2':[('licao-m1-f02','D. Dinis numa gravura de 1594',None),('licao-m1-f02','D. Dinis, rei de 1279 a 1325','rei de 1279 a 1325'),
          ('licao-m1-f02','segura um livro pequeno na mão',None),('licao-m1-f02','Quem escreve é este rei',None),
          ('licao-m1-f05','Numa fala imaginada, a representação informal pode ser uma escolha',None),
          ('licao-m1-f05','numa fala documentada, preserva as palavras da fonte',None)],
}


def licao(nome):
    """Texto da lição sem marcas e, a seguir, a fonte inteira (para o que só está na descrição de uma imagem)."""
    s=(ROOT/'m1'/nome/'index.html').read_text('utf-8')
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>|\\n',' ',s)))+' '+html.unescape(s)


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
                # 28/10/2026: cada tabela num contentor que desliza sozinho, para a página não deslizar na horizontal no telemóvel.
                for p in (aluno,correcao):self.assertEqual(p.count('<table'),p.count('<div class="g-tab" role="region"'))
                self.assertIn('.g-tab{overflow-x:auto',aluno)
                for p in (aluno,correcao):
                    texto=str(Texto(p));baixo=texto.lower()
                    self.assertNotIn('—',texto)
                    for w in ('professor','jogar','ficha','folha','%','teams'):self.assertNotIn(w,baixo,(slug,w))
                    self.assertIn('../../../assets/appearance.css',p)

    def test_nenhuma_pagina_publica_responde_a_tarefa(self):
        self.assertEqual(set(PROIBIDAS),{'m1-u1','m1-u2'})
        for slug,proibidas in PROIBIDAS.items():
            t=DADOS['tarefas'][slug]
            dados=json.dumps(t,ensure_ascii=False)
            paginas=[str(Texto((ROOT/'tarefas'/slug/pasta/'index.html').read_text('utf-8'))) for pasta in ('grelha','correcao')]
            for texto in [dados]+paginas:
                for cadeia in proibidas:
                    with self.subTest(tarefa=slug,cadeia=cadeia):
                        self.assertIsNone(re.search(cadeia,texto,re.I),cadeia)
                for frase in re.split(r'(?<=[.!?;:])\s',texto):
                    for nome,palavras in PARES.get(slug,()):
                        if nome in frase:
                            for palavra in palavras:
                                self.assertNotIn(palavra,frase.lower(),(slug,frase))
            # Os exemplos usam outros casos, e a página do aluno di-lo.
            self.assertTrue(t.get('nota'))
            self.assertIn(t['nota'],paginas[0])

    def test_citacoes_dos_exemplos_estao_nas_licoes(self):
        for slug,citacoes in CITACOES.items():
            dados=json.dumps(DADOS['tarefas'][slug],ensure_ascii=False)
            for nome,na_licao,na_grelha in citacoes:
                with self.subTest(tarefa=slug,licao=nome,citacao=na_licao):
                    self.assertIn(na_licao,licao(nome))
                    if na_grelha:self.assertIn(na_grelha,dados)

    def test_gerador_e_idempotente(self):
        import subprocess,sys
        antes={p:p.read_bytes() for p in (ROOT/'tarefas').glob('m1-u*/**/index.html')}
        subprocess.run([sys.executable,'-B','scripts/grelhas_tarefas.py'],cwd=ROOT,check=True,capture_output=True)
        for p,b in antes.items():self.assertEqual(b,p.read_bytes(),p)

if __name__=='__main__':unittest.main()
