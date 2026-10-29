"""Grelhas /20 das tarefas de unidade (27/10/2026, decisão do docente; piloto M1; 28/10/2026, regra das soluções).

Cada tarefa com grelha tem: cinco critérios que somam 20, os três níveis descritos com um exemplo cada e o
que custa pontos; uma página do aluno com autoavaliação em papel; uma versão de correção com o feedback em
três partes; e, na tarefa, a ligação à grelha. Só a grelha /20: nenhum peso do módulo nestas páginas.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,html,json,re,shutil,subprocess,sys,tempfile,unicodedata,unittest
ROOT=Path(__file__).resolve().parents[1]
DADOS=json.loads((ROOT/'docs/pedagogia/grelhas-tarefas-20261027.json').read_text('utf-8'))
# 28/10/2026 (regra do docente: nunca publicar soluções). A grelha do aluno e a versão de correção são públicas,
# e este ficheiro também: as cadeias da chave ficam guardadas em hash. 28/10/2026 (revisão do PR #122): a versão
# anterior listava-as em claro; a lista legível fica com a chave, fora do repositório. Cada valor são os primeiros
# 24 carateres hexadecimais do SHA-256 de SAL seguido das palavras da cadeia (NFC, minúsculas, \w+), unidas por um
# espaço. Cada texto público dá os seus grupos de 1 a 8 palavras seguidas, com o mesmo hash; nenhum pode coincidir.
SAL='pt-m1-20261028:'
PROIBIDAS={
 'm1-u1':{'0288cd0713e830c6295d5142','02ad401c397fc50cf1561bed','0496628c9f3aafc9ddbf0aef','080b5d560b682e21421f8709',
          '0beb24411ae944db53bebec4','1be481f8bda3f2f79f4543d6','22a3c19808d2db4e0379b55c','342cc6c4913cc5d7ce449856',
          '4ba8c402dfeba5c73b3e942d','5e24415e996c46b309fd0259','609e4105f9f1944107f2de90','67b7e157bbf295544015d189',
          '6e69abd17ff4bbb52fbab723','79b4118ee2c5ba43380feaf2','838e335b0f00780f125fa4c8','9677dcc0fa9384a16ccff731',
          '9b5fc58b9cd4f3adb72bfd74','9ce013cc0d31ae0954c0536e','a5d6c6b199e148bbacbcdbff','ab5f952494e86dc83e191a29',
          'abc431ed22f2ec1f241208b5','ac2fb5879aee8063aafb3687','adfaf3bea27665959e51f6e8','b439b93128e442de55663da7',
          'b6f488c60bc90670e971b87e','ba4cd35e3ecf8b9ce77e2b3e','bff0124ab8d9747d8db9d81f','c4c8e7bb806a46deb075395b',
          'e4cc33c18767593846f6ad0b','f0a8287652660c87d57e4fa0','f3244be7c3fe4660861de4b6','fa0d7fd51468cf4267c90f16',
          'fc7315fb60a3368847113666'},
 'm1-u2':{'02af4faace33dc583a1d6465','02b78c65a697e4336f747174','08ce4de54b0532d605f03160','0a561f3753e1c4cdd1a7b265',
          '11a9688c22667cae4d83d1db','209b424ec2dcd98f0ce8d2b6','38aa8f77842ff660bc729024','3a5cc26b7260b15c77d4bae3',
          '4198517eb459949bd782b3fb','48c651967791cd0017564618','55d3fd8b22bdabe0c5990b1f','57af092f9a5a84d5245739bd',
          '5bb32bb8d75455f0239e7b10','5bce92c442bbae2e0cec619c','5ec0fd90addb32cb6fcb825c','6289bbb1fda1c3bdf5eca049',
          '6de8bcaa052d2e85feb354b8','70d7f1329366d2e6ca3c33f0','795cf0f2d6f7d1f66e25ad51','7ae13010c0bd9ae99b37d0da',
          '7af8328209e3a84f29d0fd02','7b5176d7e111e9ac70805915','7eea7a82653fc8b07cfd8e41','82879cdcab9bece74aa2617f',
          '9aab654d165838f8ac6fd894','9aecab58d910a8dac076afbb','9b9a508214cd56dae3118cdc','a22f17b0586d3617a7f649b6',
          'ab5f952494e86dc83e191a29','bc2f2d27ddb6f00205e91311','bce06cd53d1f54b2ada449fb','be6eed8c4a8d0eb2fbc9a37a',
          'c008deffd4d1bc4890f6c914','cc6a994842594b102c4b0a74','cd0f6034a80894e929a46268','cfa50cfcb76763d5226bc557',
          'd015d4020df46e835785fb61','d43af8303be9a8b27e28d345','f526a700529b7794fbf1ba2c','fe5466be48f3e3371c3c4430',
          'fe589294415c70b32b4c016d'},
}
# Também não se juntam, na mesma frase, os nomes guardados (primeiro hash) e as palavras guardadas por prefixo.
PARES={
 'm1-u1':[('edc7e2081090f78c933652ee',{'3fc70496d431a5f758272481','4699fafaaf0e058d131a4c37','52ea3cfd37ff66749819d564','5e24415e996c46b309fd0259','81ca72dce9a41cf9633a2601','b34fd08a2a382a672b27748b','e4cc33c18767593846f6ad0b'}),
         ('8b3b5533be22e5b72226ec3a',{'1ffdfe9036e142c8c056a602','3fc70496d431a5f758272481','6e7765af1bcdd04d8dd34198','81ca72dce9a41cf9633a2601','e4cc33c18767593846f6ad0b','f41656b1bc0a282076ef64bd'})],
}
# Na página da tarefa (texto e explicações das opções) e no guia do módulo, também não.
NA_TAREFA={
 'm1-u1':{'342cc6c4913cc5d7ce449856','4ba8c402dfeba5c73b3e942d','5e24415e996c46b309fd0259','609e4105f9f1944107f2de90',
          '79b4118ee2c5ba43380feaf2','9677dcc0fa9384a16ccff731','ab5f952494e86dc83e191a29','abc431ed22f2ec1f241208b5',
          'ac2fb5879aee8063aafb3687','ae4624326d779b9124e07440','c0e33ec6d4dede22583a30fb','cf72f3415594a910141c6d9d',
          'e4cc33c18767593846f6ad0b','fc7315fb60a3368847113666'},
 'm1-u2':{'08ce4de54b0532d605f03160','0a561f3753e1c4cdd1a7b265','4198517eb459949bd782b3fb','7ae13010c0bd9ae99b37d0da',
          '7b5176d7e111e9ac70805915','82879cdcab9bece74aa2617f','ab5f952494e86dc83e191a29','bce06cd53d1f54b2ada449fb',
          'be6eed8c4a8d0eb2fbc9a37a','be979452e704528d49b858bd','e2cbb54e642adbed72494dcc','fe277d48eacd091222281d9f'},
}
NO_GUIA={'40b1df0ce261a94cbf9951c7','45338023398ec2a31f9080d2','48c651967791cd0017564618','4ba8c402dfeba5c73b3e942d',
        '5aa80cd4dc9fc558e6fa63ac','9aecab58d910a8dac076afbb','c013db507ae7419706280553'}


def palavras(texto):
    return re.findall(r'\w+',unicodedata.normalize('NFC',texto).lower())


def h(cadeia):
    return hashlib.sha256((SAL+' '.join(palavras(cadeia))).encode('utf-8')).hexdigest()[:24]


def grupos(texto,n=8):
    p=palavras(texto)
    return {h(' '.join(p[i:i+k])) for k in range(1,n+1) for i in range(len(p)-k+1)}


def prefixos(palavra):
    return {h(palavra[:k]) for k in range(1,len(palavra)+1)}


def frases(texto):
    return re.split(r'(?<=[.!?;:])\s',texto)

# 28/10/2026: as citações e os factos dos exemplos (outros casos do mesmo tipo) estão, letra a letra, numa lição do
# M1. Cada linha: a lição, o texto como está na lição e, quando o exemplo o cita tal e qual, o texto na grelha.
# 28/10/2026 (revisão do PR #122): os exemplos dos critérios 1 e 2 da unidade 1 passam a Mendinho e à aférese, e o
# critério 3 deixa de citar a frase sobre o exagero; as linhas acompanham os exemplos novos.
CITACOES={
 'm1-u1':[('licao-m1-f02',"Quem escreve é Mendinho; quem diz «eu» é a rapariga que espera","Quem escreve é Mendinho; quem diz «eu» é a rapariga que espera"),
          ('licao-m1-f02',"Eu atendendo meu amig', eu a[tendendo].","«Eu atendendo meu amig', eu a[tendendo]»"),
          ('licao-m1-f02',"Eu atendendo meu amig', eu a[tendendo].","“Eu atendendo meu amig', eu a[tendendo]”"),
          ('licao-m1-f02','a espera não cede','a espera não cede'),
          ('licao-m1-f02',"Sedia-m'eu na ermida de Sam Simion","“Sedia-m'eu na ermida de Sam Simion”"),
          ('licao-m1-f02',"nom hei [eu i] barqueiro nem sei remar","“nom hei [eu i] barqueiro nem sei remar”"),
          ('licao-m1-f02','não tem barqueiro e não sabe remar','não tem barqueiro e não sabe remar'),
          ('licao-m1-f02','Já não depende dela','já não depende dela'),
          ('licao-m1-f02','Nesta ilha da ria de Vigo ficava a ermida de San Simón',None),('licao-m1-f02','DOA, um grupo galego',None),
          ('licao-m1-f02','interpretação de hoje, não a melodia medieval','interpretação de hoje'),
          ('licao-m1-f01','só o Pergaminho Vindel, de Martim Codax, e o Sharrer, de D. Dinis, guardam melodias','desta cantiga, a melodia não chegou'),
          ('licao-m1-f05','Em «acume» cai o a do início','acume > gume'),('licao-m1-f05','alevantada > levantada','alevantada > levantada'),
          ('licao-m1-f05','O gesto é o mesmo, cair','O gesto é o mesmo, cair'),
          ('licao-m1-f19','Uma hora à espera do autocarro: «Que rapidez!»','«Que rapidez!»'),
          ('licao-m1-f19','A sopa está boa, e alguém diz: «Que sopa boa!»','«Que sopa boa!»')],
 'm1-u2':[('licao-m1-f02','D. Dinis numa gravura de 1594',None),('licao-m1-f02','D. Dinis, rei de 1279 a 1325','rei de 1279 a 1325'),
          ('licao-m1-f02','segura um livro pequeno na mão',None),('licao-m1-f02','Quem escreve é este rei',None),
          ('licao-m1-f05','Numa fala imaginada, a representação informal pode ser uma escolha',None),
          ('licao-m1-f05','numa fala documentada, preserva as palavras da fonte',None)],
 # 29/10/2026 (decisão do docente): a grelha da M7-U3 («Louco, sim»). Os exemplos usam outro tema («Ensaiar vale a pena?»),
 # «O Infante» e a «Tabacaria»; os versos, as frases e a data estão, letra a letra, nas lições do M7.
 'm7-u3':[('licao-m7-f08','Deus quer, o homem sonha, a obra nasce.','«Deus quer, o homem sonha, a obra nasce.»'),
          ('licao-m7-f08','Deus quer (vontade), o homem sonha (desejo), a obra nasce',None),
          ('licao-m7-f07','Álvaro de Campos, «Tabacaria» (15-1-1928)','15-1-1928'),
          ('licao-m7-f11','«Não sou nada.»','«Não sou nada.»'),
          ('licao-m7-f07','Estou hoje vencido, embora não saiba a verdade','Estou hoje vencido, embora não saiba a verdade')],
}
# 29/10/2026: a grelha da M7-U3 não tem chave de respostas (é um texto de opinião), por isso não entra em PROIBIDAS; o que
# não pode aparecer nas páginas públicas nem nos dados é o assunto dos temas A e B, nem os seus poemas (os exemplos são de
# outro caso do mesmo tipo). Confere-se em claro, palavra a palavra («Louco» fica de fora: está no título da tarefa).
TEMAS_M7_U3=('Valeu a pena','Bojador','mães','noivas','Sebastião','Alcácer','sebastianismo','esperamos','Madalena',
             'loucura','Mar Português','nevoeiro')


def licao(nome):
    """Texto da lição sem marcas e, a seguir, a fonte inteira (para o que só está na descrição de uma imagem).

    29/10/2026: a pasta do módulo sai do nome da lição (licao-m1-…, licao-m7-…).
    """
    s=(ROOT/nome.split('-')[1]/nome/'index.html').read_text('utf-8')
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
                    # 29/10/2026 (M7-U3): os títulos de obras escrevem-se nos dados entre _…_ e saem em itálico.
                    nome=re.sub(r'(?<![\w/])_([^_<>]{1,100}?)_(?!\w)',r'<i>\1</i>',c['nome'])
                    self.assertIn(nome.replace('«','&laquo;') if '&laquo;' in aluno else nome,aluno)
                self.assertEqual(aluno.count('class="g-crit"'),5);self.assertIn('id="autoavaliacao"',aluno)
                for parte in ('O que funciona','O que te custa pontos','Próximo passo'):self.assertIn(parte,correcao)
                # 28/10/2026: cada tabela num contentor que desliza sozinho, para a página não deslizar na horizontal no telemóvel.
                for p in (aluno,correcao):self.assertEqual(p.count('<table'),p.count('<div class="g-tab" role="region"'))
                self.assertIn('.g-tab{overflow-x:auto',aluno)
                # 28/10/2026 (revisão do PR #122): voltar à tarefa abre o cartão «Verificar», de onde se veio.
                for p in (aluno,correcao):
                    self.assertNotIn('href="../"',p)
                    self.assertEqual(p.count('href="../#entregar"'),2)
                    niveis=[int(n) for n in re.findall(r'<h([1-6])[ >]',p)]
                    self.assertEqual(niveis[0],1)
                    self.assertTrue(all(b-a<=1 for a,b in zip(niveis,niveis[1:])),niveis)
                self.assertIn('<h2 class="g-fb-t">Comentário ao aluno</h2>',correcao)
                for p in (aluno,correcao):
                    texto=str(Texto(p));baixo=texto.lower()
                    self.assertNotIn('—',texto)
                    for w in ('professor','jogar','ficha','folha','%','teams'):self.assertNotIn(w,baixo,(slug,w))
                    self.assertIn('../../../assets/appearance.css',p)

    def test_nenhuma_pagina_publica_responde_a_tarefa(self):
        self.assertEqual(set(PROIBIDAS),{'m1-u1','m1-u2'})
        # O método apanha o que deve: um grupo de palavras conhecido de cada página tem de aparecer.
        self.assertIn(h('Como é avaliado'),grupos('M1 · Unidade 1 · Como é avaliado'))
        for slug,proibidas in PROIBIDAS.items():
            t=DADOS['tarefas'][slug]
            dados=json.dumps(t,ensure_ascii=False)
            paginas=[str(Texto((ROOT/'tarefas'/slug/pasta/'index.html').read_text('utf-8'))) for pasta in ('grelha','correcao')]
            self.assertIn(h('como é avaliado'),grupos(paginas[0]));self.assertIn(h('o que funciona'),grupos(paginas[1]))
            for nome,texto in zip(('dados','grelha','correcao'),[dados]+paginas):
                with self.subTest(tarefa=slug,texto=nome):
                    self.assertEqual(grupos(texto)&proibidas,set())
                    self.assertEqual(self.pares(slug,texto),[])
            # Os exemplos usam outros casos, e a página do aluno di-lo.
            self.assertTrue(t.get('nota'))
            self.assertIn(t['nota'],paginas[0])

    def pares(self,slug,texto):
        achadas=[]
        for frase in frases(texto):
            ps=palavras(frase);hs={h(p) for p in ps}
            for nome,alvos in PARES.get(slug,()):
                if nome in hs and any(prefixos(p)&alvos for p in ps):achadas.append(frase)
        return achadas

    def test_tarefa_e_guia_nao_dao_a_resposta(self):
        # 28/10/2026 (revisão do PR #122): a página da tarefa (com as explicações das opções, que vivem em atributos)
        # e o guia do módulo também não dizem a resposta, nem mandam para os cartões que a trazem escrita.
        for slug,guardadas in NA_TAREFA.items():
            fonte=(ROOT/'tarefas'/slug/'index.html').read_text('utf-8')
            texto=str(Texto(fonte))+' '+' '.join(html.unescape(x) for x in re.findall(r'data-response="([^"]*)"',fonte))
            self.assertIn(h('Escolhe um tema'),grupos(texto))
            with self.subTest(tarefa=slug):
                self.assertEqual(grupos(texto)&guardadas,set())
                self.assertEqual(self.pares(slug,texto),[])
        guia=str(Texto((ROOT/'m1/guia-da-tarefa-m1/index.html').read_text('utf-8')))
        self.assertIn(h('Arquivo de produções'),grupos(guia))
        self.assertEqual(grupos(guia)&NO_GUIA,set())
        self.assertEqual(grupos(guia)&(NA_TAREFA['m1-u2']),set())

    def test_citacoes_dos_exemplos_estao_nas_licoes(self):
        for slug,citacoes in CITACOES.items():
            dados=json.dumps(DADOS['tarefas'][slug],ensure_ascii=False)
            for nome,na_licao,na_grelha in citacoes:
                with self.subTest(tarefa=slug,licao=nome,citacao=na_licao):
                    self.assertIn(na_licao,licao(nome))
                    if na_grelha:self.assertIn(na_grelha,dados)

    def test_m7_u3_exemplos_noutro_tema(self):
        # 29/10/2026 (decisão do docente): a grelha /20 da tarefa nova da M7-U3 está nos dados, com as duas páginas, e nenhum
        # exemplo usa o assunto dos temas A e B (o preço do mar e a espera de D. Sebastião) nem os seus poemas.
        t=DADOS['tarefas']['m7-u3']
        self.assertEqual([c['max'] for c in t['criterios']],[3,5,5,4,3])
        textos=[json.dumps(t,ensure_ascii=False)]+[str(Texto((ROOT/'tarefas/m7-u3'/pasta/'index.html').read_text('utf-8'))) for pasta in ('grelha','correcao')]
        for nome,texto in zip(('dados','grelha','correcao'),textos):
            for palavra in TEMAS_M7_U3:
                with self.subTest(texto=nome,palavra=palavra):
                    self.assertNotIn(palavra.lower(),texto.lower())
        self.assertIn('<h1>Louco, sim: argumentar com os movimentos de <i>Mensagem</i></h1>',(ROOT/'tarefas/m7-u3/grelha/index.html').read_text('utf-8'))

    def test_gerador_e_idempotente(self):
        # 28/10/2026 (revisão do PR #122): o gerador escreve numa pasta temporária (--saida) e compara-se byte a byte;
        # o teste já não reescreve a árvore de quem o corre.
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,'-B','scripts/grelhas_tarefas.py','--saida',tmp],cwd=ROOT,check=True,capture_output=True)
            for slug in DADOS['tarefas']:
                for pasta in ('grelha','correcao'):
                    with self.subTest(tarefa=slug,pasta=pasta):
                        self.assertEqual((Path(tmp)/'tarefas'/slug/pasta/'index.html').read_bytes(),(ROOT/'tarefas'/slug/pasta/'index.html').read_bytes())
                self.assertFalse((Path(tmp)/'tarefas'/slug/'index.html').exists(),'a ligação à grelha já está na tarefa')

if __name__=='__main__':unittest.main()
