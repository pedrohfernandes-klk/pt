"""12/11/2026: as «Provas em cartões» do Exame com os documentos oficiais (camada literal exame_provas_oficial_20261112).

A secção exame/provas/index.html, as seis lições das duas provas de 2026 e os dados de onde saem (scripts/provas/dados/). Confere:
- ligações: todas as ligações a documentos oficiais (enunciado, critérios, página da imagem) levam a eduqa.pt, aos endereços que
  a transcrição dá como originais; não fica nenhuma ligação por mudar (FICAM_COMO_ESTAVAM está vazio) e nenhuma página nem ficheiro
  de dados fala de examesnacionais.com.pt;
- autoria: «IAVE» não aparece (os PDF de 2026 só trazem a EduQA), nem a nota da marca de água «VERSÃO DE TRABALHO»;
- as frases sobre «as oito provas de 2023 a 2026» saíram e as que ficaram dizem o que as duas transcrições mostram;
- as citações novas («mecanismos de articulação interfrásica», «ou outros igualmente relevantes», as três da p. 4 dos critérios)
  estão, letra a letra, na transcrição da prova a que o cartão pertence;
- as referências presas (U+00A0, e U+2060 a seguir ao hífen da sigla): na secção (achado 28 da varredura do cuidado), na moldura
  das lições e nos títulos e rótulos nossos dos cartões; os 20 rótulos «Item N da prova…» ficam com o espaço normal, de propósito;
- nada em atributos nem no <title>;
- as transcrições não mudaram, o texto oficial dos cartões é o da base e a versão das lições é a mesma;
- a camada é fechada, reversível letra a letra, está no topo e desfaz-se primeiro em todas as cadeias; o gerador da camada dá o
  mesmo JSON; scripts/provas/gerar.py dá as páginas da árvore e, com os dados de antes, as páginas de antes.

Nenhum teste faz pedidos à rede: os endereços foram conferidos à mão a 12/11/2026 (200, application/pdf, iguais byte a byte aos
documentos com que a camada oficial foi conferida, sem marca de água). O percurso no navegador está em
tests/browser_exame_provas_oficial.py.
"""
from pathlib import Path
import hashlib
import html
import json
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
import exame_provas_oficial_20261112 as L  # noqa: E402
import verificar_camadas  # noqa: E402
from auditoria_20261028 import undo_cuidado_exame_1112, undo_exame_ligacao_treinos_1112, undo_exame_provas_oficial_1112  # noqa: E402
from provas_casos import PROVAS, ROMANOS, itens_do_grupo, plano, textos_do_grupo  # noqa: E402
from test_provas_cartoes import OFICIAL, PALAVRAS_PROIBIDAS, segmentos, sem_oficial  # noqa: E402

CAMADA_REL = 'scripts/exame_provas_oficial_20261112.json'
MANIFESTO_REL = 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
LT = 'tests/fixtures/exame-ligacao-treinos-edits-20261112.json'
EX = 'tests/fixtures/cuidado-exame-edits-20261112.json'
BASE_COMMIT = '41c77a868c3291cfafb6ac754a50565f01fa78a1'
N, WJ = '\xa0', '⁠'
SECCAO = 'exame/provas/index.html'
LICOES = [f'exame/provas/{pv}/{g}/index.html' for pv in ('2026-1f', '2026-2f') for g in ('grupo-i', 'grupo-ii', 'grupo-iii')]
PAGINAS = LICOES + [SECCAO]
GRUPOS_DADOS = [f'scripts/provas/dados/{pv}/{g}.json' for pv in ('2026-1f', '2026-2f') for g in ('grupo-i', 'grupo-ii', 'grupo-iii')]
OUTROS_DADOS = ['scripts/provas/dados/2026-1f/prova.json', 'scripts/provas/dados/2026-2f/prova.json', 'scripts/provas/dados/seccao.json']
DADOS = GRUPOS_DADOS + OUTROS_DADOS
# Os documentos, em eduqa.pt (os endereços que a transcrição dá como originais): {prova: (enunciado, critérios)}.
DOCUMENTOS = {
    '2026-1f': ('https://eduqa.pt/wp-content/uploads/2026/06/portugues_prova_639_v2_enunciado.pdf',
                'https://eduqa.pt/wp-content/uploads/2026/07/portugues_prova_639_cc.pdf'),
    '2026-2f': ('https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-V2_net.pdf',
                'https://eduqa.pt/wp-content/uploads/2026/07/EX-Port639-F2-2026-CC-VD_net.pdf'),
}
# As ligações a documentos oficiais que ficaram como estavam, por o documento não existir em eduqa.pt: nenhuma.
FICAM_COMO_ESTAVAM = set()
# As transcrições conferidas não mudam com esta camada (resumos dos ficheiros no commit da base).
TRANSCRICOES = {
    'tests/fixtures/prova-639-2026-1f-v2.json': '51d581be964e447e9191c4c2426eb07d2b22ff8560581b57a29a5f0cfcd75d69',
    'tests/fixtures/prova-639-2026-2f-v2.json': '7a501accad630074aaa59c3277e9bd1f09acaea288c58619187f960bb3b4df12',
}
# Os ficheiros que nenhuma camada tinha: o resumo de cada um no commit da base.
BASES_SEM_CAMADA = {
    SECCAO: 'bc6b475acf65dd8f7c1a943cb2a3f34fdbb075858a1cd0704f16ba309554e8dc',
    'scripts/provas/dados/2026-1f/prova.json': 'efbd2262ccc87c197c6fbafa5c248bdb6930dc76267be3fab319025bfa2a2fe3',
    'scripts/provas/dados/2026-2f/prova.json': '0fa8b0dfe9360207027e5d29650ab02b6d4e8d64255ce76825175abccc6f3fee',
    'scripts/provas/dados/seccao.json': '5aca6ad36890d1af96181416f509d089342aa8568c272b1a0d79cb1af3fa01ef',
}
EDUQA = 'EduQA, Instituto de Educação, Qualidade e Avaliação'
# As citações que a camada pôs nos cartões: têm de estar, letra a letra, na transcrição (a página é a dos critérios, igual nas duas
# fases: conferida nos PDF a 12/11/2026).
CITACOES_NOVAS = {
    'mecanismos de articulação interfrásica': 15,
    'ou outros igualmente relevantes': 4,
    'as expressões separadas por barras oblíquas': 4,
    # 12/11/2026 (revisão): a exceção que a p. 4 abre, citada também (as barras dentro das transcrições marcam a mudança de verso).
    'à exceção das utilizadas no interior de cada uma das transcrições': 4,
    'exemplos de formulações possíveis, apresentadas em alternativa': 4,
}
# Uma referência por prender: a palavra e o número (ou o romano, ou a letra) com um espaço normal entre os dois.
SOLTA = re.compile(r'\b(?:Prova|Grupo|Item|Itens|item|itens|Parte|Texto|Poema|Linhas?|linhas?|Versos?|versos?|[Vv]ersão|Sessão) (?:\d|[IVX]+\b|[A-C]\b)'
                   r'|\d\.[ªº] (?:fases?|ano)\b|\bp\. \d|\d (?:minutos|pontos|palavras)\b|\d (?:a|e|de) \d|\bM\d-F\d\d')


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def base(rel):
    """O ficheiro sem esta camada (desfeita pelo manifesto, com contagem estrita)."""
    return undo_exame_provas_oficial_1112(rel, ler(rel))


def cartoes(texto):
    """Os cartões de uma lição (a lista CARTOES da página)."""
    i = texto.index('CARTOES=') + len('CARTOES=')
    return json.JSONDecoder().raw_decode(texto[i:].replace('<\\/', '</'))[0]


def moldura(texto):
    """O que a página mostra fora dos cartões: sem os scripts nem os estilos, mais o fim da lição («depois»)."""
    fora = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', texto, flags=re.S)
    depois = json.loads(re.search(r'depois:("(?:[^"\\]|\\.)*")', texto).group(1))
    return fora, depois


def visivel(h):
    """O texto que se lê: sem etiquetas (nem o que elas levam nos atributos) e sem o <title>. Como plano(), de provas_casos, mas
    sem trocar os espaços que não quebram por espaços normais (é deles que estes testes tratam)."""
    h = re.sub(r'<title>.*?</title>', ' ', h, flags=re.S)
    h = re.sub(r'</?(?:i|b|em|strong|span|a|sub|small|cite)\b[^>]*>', '', h)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))


def atributos(texto):
    """Os atributos de uma página (também os do HTML que vai dentro dos cartões) e o <title>."""
    t = texto.replace('\\"', '"')
    return re.findall(r'\b[\w:-]+="[^"]*"', t) + re.findall(r'<title>.*?</title>', t, re.S)


def itens(fx, g):
    return [i for i, _ in itens_do_grupo(fx['grupos'][g - 1])]


def texto_do_item(item):
    return plano(' '.join(item['enunciado'] + item.get('enunciado_lista', [])))


TROCAS = json.loads(ler(CAMADA_REL))
MANIFESTO = json.loads(ler(MANIFESTO_REL))
POR_PASTA = {P.pasta: P for P in PROVAS}


class ExameProvasOficial(unittest.TestCase):
    maxDiff = None

    # ---------- ligações ----------
    def test_ligacoes_dos_documentos_levam_a_eduqa(self):
        self.assertEqual(FICAM_COMO_ESTAVAM, set(), 'os quatro documentos existem em eduqa.pt: nenhuma ligação fica como estava')
        self.assertEqual(set(DOCUMENTOS), set(POR_PASTA))
        for pasta, P in POR_PASTA.items():
            fontes = P.fx['prova']['fontes']
            # Os endereços são os que a transcrição já dava como originais, e é a eles que os testes das provas agora obrigam.
            self.assertEqual((fontes['enunciado_original_url'], fontes['criterios_original_url']), DOCUMENTOS[pasta])
            self.assertEqual((P.url_enunciado, P.url_criterios), DOCUMENTOS[pasta])
            self.assertEqual(P.cfg['autoria']['ligacoes'], 'originais')
        for rel in PAGINAS:
            s = ler(rel).replace('\\"', '"')
            pasta = re.search(r'\d{4}-\df', rel)
            hrefs = re.findall(r'href="(https?://[^"]+)"', s)
            documentos = [h for h in hrefs if re.search(r'\.pdf\b|exames|eduqa|iave', h, re.I)]
            with self.subTest(pagina=rel):
                self.assertNotIn('examesnacionais', s)
                self.assertTrue(documentos)
                permitidos = [u for p in ([pasta.group(0)] if pasta else DOCUMENTOS) for u in DOCUMENTOS[p]]
                for h in documentos:
                    if h in FICAM_COMO_ESTAVAM:
                        continue
                    self.assertTrue(h.startswith('https://eduqa.pt/wp-content/uploads/'), h)
                    self.assertIn(h.split('#')[0], permitidos, h)
                if rel == SECCAO:
                    # No bloco de cada prova, o enunciado e os critérios, uma vez cada.
                    self.assertEqual(sorted(documentos), sorted(u for us in DOCUMENTOS.values() for u in us))
                    self.assertEqual(s.count('Documentos em eduqa.pt: <a href="'), 2)
                else:
                    en, cc = DOCUMENTOS[pasta.group(0)]
                    # No menu («Enunciado da prova (PDF)», «Critérios de classificação (PDF)») e no crédito.
                    self.assertEqual((documentos.count(en), documentos.count(cc)), (2, 2))
                    self.assertIn(f'<a href="{en}" target="_blank" rel="noopener">Enunciado da prova (PDF)</a>'
                                  f'<a href="{cc}" target="_blank" rel="noopener">Critérios de classificação (PDF)</a>', s)
                    self.assertIn(f'Documentos em eduqa.pt: <a href="{en}" target="_blank" rel="noopener">enunciado da versão{N}2 (PDF)</a> e '
                                  f'<a href="{cc}" target="_blank" rel="noopener">critérios de classificação (PDF)</a>.', s)
                    resto = [h for h in documentos if h not in (en, cc)]
                    img = POR_PASTA[pasta.group(0)].imagem()
                    if img and rel.endswith(f'/grupo-{ROMANOS[img["grupo"] - 1].lower()}/index.html'):
                        # A imagem do Grupo III: a página 13 do enunciado, no menu, nos dois cartões de leitura e em cada «ver».
                        pagina = f'{en}#page={img["pagina_pdf"]}'
                        vers = [c for c in cartoes(ler(rel)) if 'ver' in c]
                        self.assertEqual(set(resto), {pagina})
                        self.assertEqual(len(resto), 1 + 2 + len(vers))
                        self.assertGreaterEqual(len(vers), 5)
                        self.assertIn(f'<a href="{pagina}" target="_blank" rel="noopener">A imagem do Grupo{N}III (enunciado, p.{N}13, PDF)</a>', s)
                    else:
                        self.assertEqual(resto, [])
        for rel in DADOS:
            self.assertNotIn('examesnacionais', ler(rel), rel)

    # ---------- autoria e marca de água ----------
    def test_autoria_sem_iave_e_sem_a_nota_da_marca_de_agua(self):
        for P in PROVAS:
            # A fonte da autoria é a transcrição: em 2026, a EduQA.
            self.assertEqual(P.fx['prova']['autor_instituicao'], EDUQA)
            self.assertEqual(set(P.cfg['autoria']) - {'_sobre'}, {'texto', 'texto_curto', 'ligacoes'})
            for chave in ('texto', 'texto_curto'):
                self.assertIn(EDUQA, P.cfg['autoria'][chave])
                self.assertIn(f'p.{N}1', P.cfg['autoria'][chave])
        for rel in PAGINAS + DADOS:
            s = ler(rel)
            with self.subTest(ficheiro=rel):
                self.assertNotIn('IAVE', s)
                for frase in ('VERSÃO DE TRABALHO', 'marca de água', 'Cópias públicas', 'cópia pública', 'Originais', 'Autor:', 'Autor da prova'):
                    self.assertNotIn(frase, s)
        for rel in LICOES:
            s = ler(rel)
            P = POR_PASTA[re.search(r'\d{4}-\df', rel).group(0)]
            with self.subTest(licao=rel):
                self.assertEqual(s.count(P.cfg['autoria']['texto']), 1)
                abre = cartoes(s)[0]
                self.assertEqual(abre['rot'], 'Abre')
                self.assertIn(f'(os PDF trazem o logótipo da {EDUQA})', abre['html'])
        s = ler(SECCAO)
        for P in PROVAS:
            self.assertEqual(s.count(P.cfg['autoria']['texto_curto']), len(PROVAS))
        # As transcrições continuam a dizer que a cópia de onde partiram tinha a marca: é um facto dessa cópia, que as páginas já
        # não usam; nenhuma frase visível depende desse campo (nem de prova.paginas).
        gerador = ler('scripts/provas/gerar.py')
        for campo in ('marca_de_agua', "['paginas']", '"paginas"'):
            self.assertNotIn(campo, gerador)

    # ---------- as frases sem apoio ----------
    def test_frases_sobre_as_provas_so_dizem_o_que_as_duas_de_2026_mostram(self):
        proibidas = ('oito provas', 'cinco provas', 'de 2023 a 2026', 'em três (', 'em três, a apreciação', 'sempre numa breve exposição',
                     'tem sempre', 'vale sempre', 'pede sempre')
        for rel in LICOES + GRUPOS_DADOS:
            s = ler(rel)
            with self.subTest(ficheiro=rel):
                for frase in proibidas:
                    self.assertNotIn(frase, s)
                self.assertEqual(s.count('<p>Nas duas provas de 2026'), 1)
                # Fora das referências dos textos (que são da prova), nenhum cartão nosso fala de provas de outros anos.
                self.assertNotRegex(s, r'provas? de 202[345]|fase de 202[345]')
        self.assertEqual(sorted(POR_PASTA), ['2026-1f', '2026-2f'], 'as frases dizem «as duas provas de 2026»: são as que o repositório tem')
        f1, f2 = POR_PASTA['2026-1f'].fx, POR_PASTA['2026-2f'].fx
        for fx in (f1, f2):
            # Grupo I: acaba numa breve exposição (item 7), com introdução, desenvolvimento e conclusão, e o item 6 pede que se
            # identifiquem afirmações.
            g1 = itens(fx, 1)
            self.assertEqual([i['n'] for i in g1], [1, 2, 3, 4, 5, 6, 7])
            ultimo = texto_do_item(g1[-1])
            for palavra in ('breve exposição', 'uma introdução', 'um desenvolvimento', 'uma conclusão'):
                self.assertIn(palavra, ultimo)
            self.assertIn('Identifique, de entre as afirmações', texto_do_item(g1[5]))
            # Grupo II: sete itens de escolha múltipla, com quatro opções.
            g2 = itens(fx, 2)
            self.assertEqual(len(g2), 7)
            for i in g2:
                self.assertTrue(i['tipo'].startswith('seleção: escolha múltipla'), i['tipo'])
                self.assertEqual([o['letra'] for o in i['opcoes']], list('ABCD'))
            # Grupo III: 44 pontos, conta sempre, um texto «bem estruturado» de 200 a 350 palavras, um discurso valorativo.
            (g3,) = itens(fx, 3)
            self.assertEqual((g3['cotacao'], g3['obrigatorio']), (44, True))
            self.assertIn(['III', 44], fx['cotacoes']['obrigatorios']['itens'])
            self.assertEqual((g3['extensao']['min_palavras'], g3['extensao']['max_palavras']), (200, 350))
            pedido = texto_do_item(g3)
            for palavra in ('bem estruturado', 'duzentas', 'trezentas e cinquenta palavras', 'discurso valorativo'):
                self.assertIn(palavra, pedido)
            criterios = json.dumps(g3['criterios'], ensure_ascii=False)
            for parametro in ('"id": "A"', '"id": "B"', '"id": "C"'):
                self.assertIn(parametro, criterios)
        # O género de cada fase.
        pedido1, pedido2 = texto_do_item(itens(f1, 3)[0]), texto_do_item(itens(f2, 3)[0])
        for palavra in ('apreciação crítica', 'a descrição da imagem', 'pelo menos, três aspetos', 'uma conclusão'):
            self.assertIn(palavra, pedido1)
        for palavra in ('texto de opinião', 'ponto de vista', 'dois argumentos', 'exemplo significativo'):
            self.assertIn(palavra, pedido2)
        # «Os itens 1 a 4 sobre o texto e os itens 5 a 7 de gramática» é leitura nossa, e a frase di-lo.
        for rel in (GRUPOS_DADOS[1], GRUPOS_DADOS[4]):
            self.assertEqual(ler(rel).count(f'os itens{N}1 a{N}4 sobre o texto e os itens{N}5 a{N}7 de gramática (leitura nossa).</p>'), 1)

    # ---------- as formulações dos critérios ----------
    def test_citacoes_novas_estao_na_transcricao(self):
        vistas = {}
        for rel in GRUPOS_DADOS:
            P = POR_PASTA[re.search(r'\d{4}-\df', rel).group(0)]
            for e in MANIFESTO['files'][rel]['edits']:
                velhas = re.findall(r'«([^«»]*)»', e['old'])
                for cit in re.findall(r'«([^«»]*)»', e['new']):
                    if cit in velhas:
                        continue
                    with self.subTest(ficheiro=rel, citacao=cit):
                        self.assertTrue(P.oficial(cit), 'citação que não está, letra a letra, na transcrição')
                        self.assertIn(cit, CITACOES_NOVAS)
                    vistas.setdefault(cit, set()).add(P.pasta)
        self.assertEqual(set(vistas), set(CITACOES_NOVAS))
        self.assertEqual(vistas['mecanismos de articulação interfrásica'], {'2026-1f', '2026-2f'})
        for P in PROVAS:
            # Onde estão, na transcrição: o parâmetro C do Grupo III e, no Grupo I, a nota dos critérios e a instrução de cada item.
            (g3,) = itens(P.fx, 3)
            self.assertIn('utiliza, adequadamente, mecanismos de articulação interfrásica;', json.dumps(g3['criterios'], ensure_ascii=False))
            nota = P.fx['grupos'][0]['nota_dos_criterios']
            self.assertIn('as expressões separadas por barras oblíquas', nota)
            # 12/11/2026 (revisão): a frase da p. 4, inteira, com a exceção entre os dois traços.
            self.assertIn('as expressões separadas por barras oblíquas ‒ à exceção das utilizadas no interior de cada uma das transcrições ‒ '
                          'correspondem a exemplos de formulações possíveis, apresentadas em alternativa.', nota)
            self.assertIn('correspondem a exemplos de formulações possíveis, apresentadas em alternativa.', nota)
            restritas = [i for i in itens(P.fx, 1) if i['tipo'].startswith('construção')]
            self.assertEqual([i['n'] for i in restritas], [1, 2, 4, 5, 7])
            for i in restritas:
                self.assertRegex(plano(i['criterios']['instrucao']), r'[Dd]evem ser abordados (?:os|dois dos) tópicos seguintes, ou outros igualmente relevantes')

    def test_conectores_e_topicos_com_a_formulacao_do_criterio(self):
        velhas = ('ligadas por conectores', 'conectores pela relação certa', 'parágrafos marcados, conectores,',
                  'os tópicos são exemplos de formulações possíveis')
        for rel in LICOES + GRUPOS_DADOS:
            s = ler(rel)
            for frase in velhas:
                self.assertNotIn(frase, s, rel)
        topicos = ('Os critérios não trazem uma resposta modelo: indicam tópicos a abordar, «ou outros igualmente relevantes». Dentro dos '
                   'tópicos, «as expressões separadas por barras oblíquas», «à exceção das utilizadas no interior de cada uma das '
                   'transcrições», são «exemplos de formulações possíveis, apresentadas em alternativa» (p. 4 dos critérios).</p>')
        for rel, n in zip(GRUPOS_DADOS, (5, 0, 0, 5, 0, 0)):
            self.assertEqual(ler(rel).count(topicos), n, rel)
        # 12/11/2026 (revisão): a frase nunca aparece sem a exceção da p. 4. Em cinco dos dez cartões, os tópicos mostrados por cima
        # dela trazem versos transcritos, com a barra a marcar a mudança de verso: sem a exceção, liam-se como alternativas.
        com_versos = []
        for rel in GRUPOS_DADOS:
            for k, c in enumerate(json.loads(ler(rel))['cartoes']):
                h = c.get('html', '')
                self.assertEqual('barras oblíquas' in h, topicos in h, (rel, k))
                self.assertEqual(h.count('«as expressões separadas por barras oblíquas»'),
                                 h.count('«as expressões separadas por barras oblíquas», «à exceção das utilizadas no interior de cada uma das transcrições»,'))
                if topicos in h and re.search(r'«[^«»]* / [^«»]*»', h):
                    com_versos.append((re.search(r'\d{4}-\df', rel).group(0), k))
        self.assertEqual(com_versos, [('2026-1f', 47), ('2026-1f', 56), ('2026-2f', 13), ('2026-2f', 24), ('2026-2f', 79)])
        for rel, n in zip(GRUPOS_DADOS, (0, 0, 2, 0, 0, 3)):
            with self.subTest(ficheiro=rel):
                D = json.loads(ler(rel))
                com = [c for c in D['cartoes'] if '«mecanismos de articulação interfrásica»' in c.get('html', '')]
                self.assertEqual(len(com), n)
                if n:
                    self.assertEqual([c['rot'] for c in com][-2:], ['Revê com a grelha', 'Para levar'])
                    # O parâmetro C, na grelha oficial que o cartão «Escreve no caderno» mostra, diz o mesmo (texto dos critérios).
                    (caderno,) = [c for c in D['cartoes'] if c.get('rot') == 'Escreve no caderno']
                    self.assertIn('utiliza, adequadamente, mecanismos de articulação interfrásica;', caderno['html'])
                # «conectores» só fica onde o cartão trata dos conectores (exercícios e a regra da p. 2 dos critérios), nunca como
                # leitura nossa do parâmetro C.
                for c in D['cartoes']:
                    if c.get('rot') in ('Revê com a grelha', 'Para levar'):
                        self.assertNotIn('conectores', sem_oficial(c.get('html', '')), c.get('rot'))

    # ---------- referências presas ----------
    def test_referencias_presas_na_seccao(self):
        s = ler(SECCAO)
        formas = {f'Prova{N}639, 2.ª{N}fase, 2026, versão{N}2': 1, f'Prova{N}639, 1.ª{N}fase, 2026, versão{N}2': 1, f'Prova{N}639, 12.º{N}ano': 1,
                  f'200{N}a{N}350{N}palavras': 2, f'120{N}minutos': 2, f'200{N}pontos': 2, f'Versão{N}2': 2, f'2.ª{N}fases': 3,
                  f'<span class="pv-quando">2026, 2.ª{N}fase</span>': 1, f'<span class="pv-quando">2026, 1.ª{N}fase</span>': 1,
                  f', Prova{N}639</h2>': 2, f'enunciado da versão{N}2 (PDF)': 2, f'(p.{N}1)': 2}
        for forma, n in formas.items():
            self.assertEqual(s.count(forma), n, forma)
        for grupo, n in (('III', 4), ('II', 4), ('I', 6)):
            self.assertEqual(len(re.findall(rf'Grupo{N}{grupo}\b', s)), n, grupo)
        self.assertEqual(s.count(WJ), 0)
        # Nada por prender no texto que se lê.
        self.assertEqual(SOLTA.findall(visivel(s)), [])
        self.assertEqual(json.loads(ler('scripts/provas/dados/seccao.json'))['nao_partir'], True)

    def test_referencias_presas_na_moldura_das_licoes(self):
        for rel in LICOES:
            s = ler(rel)
            P = POR_PASTA[re.search(r'\d{4}-\df', rel).group(0)]
            g = [k for k, slug in P.grupos.items() if f'/{slug}/' in rel][0]
            nome, n = ROMANOS[g - 1], len(P.grupos)
            fora, depois = moldura(s)
            with self.subTest(licao=rel):
                self.assertIs(P.cfg['nao_partir'], True)
                exatas = [f'<h1 class="c-sr">{P.nome_preso}, Grupo{N}{nome}: ',
                          f'<div class="c-menu-cab"><p>{P.nome_preso}<br>Grupo{N}{nome} de{N}{ROMANOS[n - 1]}</p>',
                          f'<span class="aqui" style="--k:3">Estás em: Grupo{N}{nome}</span>',
                          f'Provas em cartões: Grupo{N}{nome} do {P.fx["prova"]["titulo"]}, {P.nome_preso}, versão{N}{P.versao}. ']
                if g > 1:
                    exatas += [f'>Grupo anterior: Grupo{N}{ROMANOS[g - 2]}</a>']
                    self.assertIn(f'>← Grupo{N}{ROMANOS[g - 2]}</a>', depois)
                if g < n:
                    exatas += [f'>Grupo seguinte: Grupo{N}{ROMANOS[g]}</a>', f'seguinteRotulo:"Grupo{N}{ROMANOS[g]}"']
                    self.assertIn(f'>Grupo{N}{ROMANOS[g]} →</a>', depois)
                for forma in exatas:
                    self.assertEqual(s.count(forma), 1, forma)
                # O fim da lição: as lições dos módulos com a junção a seguir ao hífen da sigla e as sessões com o número preso.
                siglas = re.findall(r'<span class="pe-t">(M\d-.?F\d\d): ', depois)
                self.assertEqual(len(siglas), len([x for x in P.cfg['grupos'][g - 1]['licoes'] if '/licao-' in x]))
                self.assertTrue(siglas and all(re.fullmatch(rf'M\d-{WJ}F\d\d', x) for x in siglas), siglas)
                sessoes = re.findall(r'<span class="pe-t">(Sessão.\d+): ', depois)
                self.assertEqual(sessoes, [f'Sessão{N}{int(x[1:])}' for x in P.cfg['grupos'][g - 1]['sessoes']])
                # Nada por prender no que a moldura mostra. As referências dos textos, «como a prova os indica», são da
                # transcrição e ficam como estão: tiram-se antes de procurar.
                texto = visivel(fora) + ' ' + visivel(depois)
                for f in [t['fonte'] for t in textos_do_grupo(P.fx['grupos'][g - 1])]:
                    self.assertIn(plano(f).rstrip('.'), texto)
                    texto = texto.replace(plano(f).rstrip('.'), ' ')
                self.assertEqual(SOLTA.findall(texto), [])
                # O que não se prende: o nome acessível de recurso do motor e o <title>.
                self.assertIn(f'titulo:"Grupo {nome}"', s)
                self.assertIn(f'<title>{P.nome}: Grupo {nome}</title>', s)

    def test_referencias_presas_nos_titulos_e_rotulos_dos_cartoes(self):
        oficiais = presos = 0
        for rel_d, rel_p in zip(GRUPOS_DADOS, LICOES):
            D, antes = json.loads(ler(rel_d)), json.loads(base(rel_d))
            with self.subTest(dados=rel_d):
                self.assertEqual(SOLTA.findall(D['aprendes']), [])
                for c, c0 in zip(D['cartoes'], antes['cartoes']):
                    rot, titulo = c.get('rot', ''), c.get('titulo', '')
                    if re.search(r'\bItem \d+ da prova\b', rot):
                        # De propósito: é por este rótulo, com o espaço normal, que os testes, a medição das opções, a camada de
                        # baixo e o motor (assets/exame/provas-licao.js) reconhecem o item tal como está na prova.
                        oficiais += 1
                        self.assertEqual(rot, c0['rot'])
                        self.assertNotIn(N, rot)
                    else:
                        self.assertEqual(SOLTA.findall(rot), [], rot)
                        self.assertNotRegex(rot, r'Item.\d+ da prova')
                    self.assertEqual(SOLTA.findall(titulo), [], titulo)
                    presos += N in rot or N in titulo
                    # Só os espaços mudam nos títulos e nos rótulos.
                    self.assertEqual((rot.replace(N, ' '), titulo.replace(N, ' ')), (c0.get('rot', ''), c0.get('titulo', '')))
                    self.assertNotIn(WJ, rot + titulo)
                # A página mostra os mesmos títulos e rótulos.
                pagina = cartoes(ler(rel_p))
                self.assertEqual([(c.get('rot'), c.get('titulo')) for c in pagina], [(c.get('rot'), c.get('titulo')) for c in D['cartoes']])
        self.assertEqual(oficiais, 20)
        self.assertGreaterEqual(presos, 60)
        self.assertIn('/\\bItem \\d+ da prova\\b/', ler('assets/exame/provas-licao.js'))
        self.assertEqual(OFICIAL.pattern, r'\bItem \d+ da prova\b(?! \(adaptado)')

    def test_nada_em_atributos_nem_no_title(self):
        for rel in PAGINAS:
            s, antes = ler(rel), base(rel)
            with self.subTest(pagina=rel):
                self.assertEqual([a for a in atributos(s) if N in a or WJ in a], [a for a in atributos(antes) if N in a or WJ in a])
                self.assertEqual([a for a in atributos(s) if N in a or WJ in a], [])
                # O <title> e a descrição são os de antes, letra a letra.
                for padrao in (r'<title>.*?</title>', r'<meta name="description" content="[^"]*">'):
                    self.assertEqual(re.findall(padrao, s), re.findall(padrao, antes))
                    self.assertEqual(len(re.findall(padrao, s)), 1)
                # Os atributos que mudam são só as ligações dos documentos.
                mudados = set(atributos(s)) ^ set(atributos(antes))
                self.assertTrue(all(a.startswith('href="https://') and ('eduqa.pt' in a or 'examesnacionais' in a) for a in mudados), mudados)
        # As indicações de fonte dos cartões (<p class="fonte">) ficam sem espaços presos, como a camada de baixo as deixou.
        for rel in GRUPOS_DADOS:
            for m in re.findall(r'<p class=\\"fonte\\">.*?</p>', ler(rel)):
                self.assertNotIn(N, m)
                self.assertNotIn(WJ, m)

    # ---------- o que não muda ----------
    def test_transcricoes_texto_oficial_e_versao_como_estavam(self):
        for rel, resumo in TRANSCRICOES.items():
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), resumo, rel)
            self.assertNotIn(rel, MANIFESTO['files'])
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in (ROOT / 'tests/fixtures').glob('prova-639-*.json')}, set(TRANSCRICOES))
        mudados = 0
        for rel in GRUPOS_DADOS:
            D, antes = json.loads(ler(rel)), json.loads(base(rel))
            P = POR_PASTA[re.search(r'\d{4}-\df', rel).group(0)]
            self.assertEqual({k: v for k, v in D.items() if k not in ('cartoes', 'aprendes')},
                             {k: v for k, v in antes.items() if k not in ('cartoes', 'aprendes')})
            self.assertEqual(len(D['cartoes']), len(antes['cartoes']))
            for k, (c, c0) in enumerate(zip(D['cartoes'], antes['cartoes'])):
                with self.subTest(dados=rel, cartao=k + 1):
                    self.assertEqual(set(c), set(c0))
                    # Só mudam o HTML dos cartões de leitura, os títulos e os rótulos; os exercícios ficam iguais, inteiros.
                    for campo in set(c) - {'html', 'titulo', 'rot'}:
                        self.assertEqual(c[campo], c0[campo], campo)
                    if c['t'] != 'ler':
                        self.assertNotIn('html', c)
                        continue
                    h, h0 = c['html'], c0['html']
                    mudados += h != h0
                    # Os blocos que reproduzem a prova ou os critérios: iguais, letra a letra.
                    for padrao in (r'<div class="v prova-l[^"]*">.*?</div>', r'<p class="gl">.*?</p>', r'<p class="papel-q">.*?</p>',
                                   r'<table class="(?:empilha grelha|cl)">.*?</table>', r'<ul class="(?:prova-lista|papel-l)">.*?</ul>',
                                   r'<ol class="prova-obs">.*?</ol>'):
                        self.assertEqual(re.findall(padrao, h, re.S), re.findall(padrao, h0, re.S), padrao)
                    # As citações que já lá estavam ficam; as novas são as do critério.
                    cits, cits0 = re.findall(r'«([^«»]*)»', h), re.findall(r'«([^«»]*)»', h0)
                    self.assertEqual([x for x in cits if x not in CITACOES_NOVAS], [x for x in cits0 if x not in CITACOES_NOVAS])
            # O texto novo cumpre as regras de escrita (sem travessões, «·», «professor», «jogar», «ficha», «folha»): fora das
            # citações que são da prova ou dos critérios, nada disso no que a camada escreveu.
            for e in MANIFESTO['files'][rel]['edits']:
                for pedaco in segmentos(e['new'].replace('\\"', '"')):
                    self.assertEqual(PALAVRAS_PROIBIDAS.findall(P.nosso(pedaco)), [], pedaco)
                self.assertNotRegex(e['new'], r'\bQual [a-zà-ú]+ [a-zà-ú]')
        # Os cartões de leitura que mudam no HTML: os 6 «Abre» e os 19 com a indicação de fonte dos critérios (a autoria; entre eles
        # estão os dez «Confere com os critérios» e os seis «Para levar»), mais os dois «Revê com a grelha» do parâmetro C.
        self.assertEqual(mudados, 27)
        for P in PROVAS:
            antes = json.loads(base(f'scripts/provas/dados/{P.pasta}/prova.json'))
            self.assertEqual(P.cfg['versao_licao'], antes['versao_licao'])
            for chave in ('prova', 'ano', 'fase', 'versao', 'imagens_com_licenca', 'opcoes_equilibradas', 'seccao'):
                self.assertEqual(P.cfg[chave], antes[chave], chave)
            self.assertEqual([{k: v for k, v in g.items() if k not in ('o_que', 'aprendes')} for g in P.cfg['grupos']],
                             [{k: v for k, v in g.items() if k not in ('o_que', 'aprendes')} for g in antes['grupos']])
        for rel in LICOES:
            for padrao in (r'versao:"[^"]+"', r'\?v=[\w.-]+', r'var K="[^"]+"'):
                self.assertEqual(re.findall(padrao, ler(rel)), re.findall(padrao, base(rel)), (rel, padrao))
        antes = json.loads(base('scripts/provas/dados/seccao.json'))
        agora = json.loads(ler('scripts/provas/dados/seccao.json'))
        # 12/11/2026 (revisão): em «seguir» sai «as oito do programa atual» (sem apoio nos documentos nem no repositório, que só tem
        # as duas provas de 2026); fica o plano do sítio. O resto da secção é o de antes.
        self.assertEqual({k: v for k, v in agora.items() if 'nao_partir' not in k and k != 'seguir'},
                         {k: v for k, v in antes.items() if k != 'seguir'})
        self.assertEqual(antes['seguir'].replace('as provas mais recentes, as oito do programa atual, sempre', 'as provas mais recentes, sempre'),
                         agora['seguir'])
        self.assertEqual(agora['seguir'], 'Primeiro as provas mais recentes, sempre com os critérios de classificação. Cada prova chega aqui '
                         'em três lições, uma por grupo, quando estiver conferida com o enunciado e com os critérios.')
        s = ler(SECCAO)
        self.assertEqual(s.count(f'<p>{agora["seguir"]}</p></section>'), 1)
        for frase in ('programa atual', 'as oito', 'oito provas'):
            self.assertNotIn(frase, visivel(s))

    # ---------- a camada ----------
    def test_camada_fechada_reversivel_e_no_topo(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 16 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        m = MANIFESTO
        self.assertEqual(set(m), {'base_commit', '_nota', 'files'})
        self.assertEqual(m['base_commit'], BASE_COMMIT)
        self.assertTrue(m['_nota'].startswith('12/11/2026: as «Provas em cartões» do Exame'))
        for frase in ('exame_provas_oficial_20261112', '«Item N da prova…»', 'eduqa.pt', 'não se edita à mão'):
            self.assertIn(frase, m['_nota'])
        self.assertEqual(set(m['files']), set(PAGINAS + DADOS))
        self.assertEqual(set(m['files']), {t['ficheiro'] for t in TROCAS})
        ex = json.loads(ler(EX))['files']
        # Com a decisão 152 no Exame, partilha as seis lições e os seis grupo-x.json; com a ligação «Treinos», nada.
        self.assertEqual(set(m['files']) & set(ex), set(LICOES + GRUPOS_DADOS))
        self.assertEqual(set(m['files']) & set(json.loads(ler(LT))['files']), set())
        self.assertEqual(set(m['files']) - set(ex), set(BASES_SEM_CAMADA))
        for t in TROCAS:
            self.assertEqual(set(t), {'ficheiro', 'local', 'antigo', 'novo', 'ocorrencias', 'achado'})
            self.assertEqual(t['ocorrencias'], 1)
            self.assertTrue(t['achado'].startswith('12/11/2026: '))
            self.assertNotRegex(t['local'] + t['achado'], r'—|\bprofessor|\bjog[oa]')
        for rel, registo in m['files'].items():
            with self.subTest(ficheiro=rel):
                self.assertEqual(set(registo), {'base_sha256_lf', 'after_sha256_lf', 'edits'})
                atual = ler(rel)
                self.assertNotIn('\r', atual)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                b = base(rel)
                self.assertEqual(sha_lf(b), registo['base_sha256_lf'])
                # A base é o ficheiro como a camada de baixo o deixou (ou, onde não havia camada, o do commit da base).
                self.assertEqual(registo['base_sha256_lf'], ex[rel]['after_sha256_lf'] if rel in ex else BASES_SEM_CAMADA[rel])
                # Ida e volta, letra a letra: refazer as trocas sobre a base devolve o ficheiro; o antigo não sobra fora do novo.
                refeito = b
                for e in registo['edits']:
                    self.assertEqual(refeito.count(e['old']), e['occurrences'], e['location'])
                    refeito = refeito.replace(e['old'], e['new'])
                self.assertEqual(refeito, atual)
                for e in registo['edits']:
                    self.assertEqual(atual.count(e['new']), e['occurrences'], e['location'])
                    self.assertEqual(atual.replace(e['new'], '\0').count(e['old']), 0, e['location'])
                    self.assertEqual(b.count(e['new']), 0, e['location'])
                # As camadas de baixo desfazem primeiro esta, com contagem estrita, e chegam à mesma base.
                self.assertEqual(undo_exame_ligacao_treinos_1112(rel, atual), b)
                if rel in ex:
                    self.assertEqual(sha_lf(undo_cuidado_exame_1112(rel, atual)), ex[rel]['base_sha256_lf'])
        # No topo das camadas.
        self.assertEqual(verificar_camadas.LAYERS[0], ('exame_provas_oficial_20261112', 'exame-provas-oficial-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('exame_ligacao_treinos_20261112', 'exame-ligacao-treinos-edits-20261112'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'))
        self.assertEqual(len(verificar_camadas.LAYERS), 46)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 46)
        # As duas camadas de baixo que mexem nestes ficheiros continuam a conferir, com as de cima desfeitas (esta primeiro).
        for camada, manifesto in (('cuidado_exame_20261112', 'cuidado-exame-edits-20261112'), ('conteudos_lote2_20261101', 'conteudos-lote2-edits-20261101')):
            with self.subTest(camada=camada):
                self.assertTrue(set(json.loads(ler(f'tests/fixtures/{manifesto}.json'))['files']) & set(m['files']))
                i = verificar_camadas.LAYERS.index((camada, manifesto))
                comando = [sys.executable, 'scripts/aplicar_trocas.py', f'scripts/{camada}.json', '--manifesto', f'tests/fixtures/{manifesto}.json',
                           '--verificar']
                for _, acima in verificar_camadas.LAYERS[:i]:
                    comando += ['--desfazer-antes', f'tests/fixtures/{acima}.json']
                r = subprocess.run(comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertIn('0 por aplicar; manifesto em dia.', r.stdout)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('exame-provas-oficial-edits-20261112.json'), sala.index('exame-ligacao-treinos-edits-20261112.json'))
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_exame_provas_oficial_1112(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_exame_ligacao_treinos_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_exame_provas_oficial_1112\(path, text\)\n')
        # O gerador da camada de baixo desfaz primeiro esta (a base das provas em cartões, de prova.json, de seccao.json e da secção).
        cuidado = ler('scripts/cuidado_exame_20261112.py')
        corpo = cuidado[cuidado.index('def base(rel):'):cuidado.index('def edicoes(')]
        self.assertLess(corpo.index('json.loads(PROVAS_OFICIAL.read_text'), corpo.index('json.loads(MANIFESTO.read_text'))
        self.assertIn("PROVAS_OFICIAL = ROOT / 'tests/fixtures/exame-provas-oficial-edits-20261112.json'", cuidado)
        # Nos fluxos e nos outros testes, a cadeia de desfazer começa por esta camada, sem nada entre ela e a ligação «Treinos».
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_exame_provas_oficial.py':
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano_ = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano_.count('--desfazer-antes ' + LT), plano_.count(f'--desfazer-antes {meu} --desfazer-antes {LT}'))
                self.assertEqual(plano_.count('--desfazer-antes {lt}'), plano_.count('--desfazer-antes {po} --desfazer-antes {lt}'))
                self.assertEqual(plano_.count('--desfazer-antes {LT}'), plano_.count('--desfazer-antes {PO} --desfazer-antes {LT}'))
                self.assertEqual(plano_.count(f"ROOT/'{LT}',"), plano_.count(f"(ROOT/'{meu}',ROOT/'{LT}',"))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça.
                if p.suffix == '.yml':
                    self.assertEqual(plano_.count('--desfazer-antes ' + meu), plano_.count('--verificar --desfazer-antes ' + meu))
                cadeias += plano_.count(f'--desfazer-antes {meu} --desfazer-antes {LT}')
        self.assertGreater(cadeias, 40)
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        exame = ler('.github/workflows/pt-exame-laboratorio-qa.yml')
        proprio = f'python scripts/aplicar_trocas.py scripts/exame_provas_oficial_20261112.json --manifesto {meu} --verificar\n'
        self.assertIn(proprio, tarefas)
        self.assertIn(proprio, exame)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/exame_ligacao_treinos_20261112.json --manifesto {LT} --verificar --desfazer-antes {meu}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/cuidado_exame_20261112.json --manifesto {EX} --verificar --desfazer-antes {meu} --desfazer-antes {LT}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_exame_provas_oficial.py' -v", tarefas)
        # No fluxo do Exame, o teste corre com os outros do exame, e o de navegador a seguir ao da ligação «Treinos».
        self.assertIn("python -m unittest discover -s tests -p 'test_exame*.py' -v", exame)
        self.assertIn('          python tests/browser_exame_provas_oficial.py\n', exame)
        self.assertLess(exame.index('python tests/browser_exame_ligacao_treinos.py'), exame.index('python tests/browser_exame_provas_oficial.py'))
        self.assertTrue((ROOT / 'tests/browser_exame_provas_oficial.py').is_file())
        self.assertIn('python scripts/provas/opcoes.py --exigir', exame)
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda.
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/exame_provas_oficial_20261112.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])
        self.assertRegex(cartaz.split('\non:')[0], r'\n# 12/11/2026: as provas em cartões com os documentos oficiais, a camada exame_provas_oficial_20261112 ')

        # Nos fluxos que correm o teste desta camada, tudo o que ela muda e os seus testes estão nos caminhos do pedido.
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        da_camada = PAGINAS + DADOS + ['scripts/provas/gerar.py', 'scripts/exame_provas_oficial_20261112.py', CAMADA_REL, meu,
                                       'tests/test_exame_provas_oficial.py', 'tests/browser_exame_provas_oficial.py']
        for texto in (tarefas, exame):
            cabeca = texto[texto.index('  pull_request:\n    paths:\n'):texto.index('\npermissions:')]
            padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
            self.assertGreater(len(padroes), 50)
            for rel in da_camada:
                self.assertTrue(any(q.match(rel) for q in padroes), rel)

    def test_gerador_da_o_mesmo_json_e_as_paginas(self):
        trocas, finais = L.construir()
        self.assertEqual(trocas, TROCAS)
        self.assertEqual(ler(CAMADA_REL), json.dumps(trocas, ensure_ascii=False, indent=1) + '\n')
        self.assertEqual(set(finais), set(MANIFESTO['files']))
        for rel, (b, final) in finais.items():
            self.assertEqual(final, ler(rel), rel)
            self.assertEqual(sha_lf(b), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
        # As páginas da árvore saem do gerador das provas, byte a byte; com os dados de antes (sem as chaves novas), o mesmo
        # gerador dá as páginas de antes (L.construir() confere-o e falha se não for assim).
        r = subprocess.run([sys.executable, '-B', 'scripts/provas/gerar.py', '--verificar'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Tudo igual ao que está na árvore.', r.stdout)
        antes = L.gerar_com({rel: b for rel, (b, _) in finais.items() if rel in DADOS})
        for rel in PAGINAS:
            self.assertEqual(antes[rel], finais[rel][0], rel)
        # As chaves novas é que mudam o gerador: sem elas nos dados de antes.
        for rel in OUTROS_DADOS:
            self.assertNotIn('nao_partir', finais[rel][0])
            self.assertNotIn('"ligacoes"', finais[rel][0])
            self.assertIn('"nao_partir": true', finais[rel][1])


if __name__ == '__main__':
    unittest.main()
