"""15/11/2026: a tarefa m4-u2 no molde «mais fácil de fazer», com «Tema A ou B» (decisão do docente), «tudo junto» no M4 e o
acerto do M8 (os quatro poemas da m8-u1 estão no manual), na camada tarefa_m4u2_tema_b_20261115.

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1, ao M5, ao M6, ao M7, ao M8
e ao M9. Esta camada leva-o à tarefa da unidade 2 do M4, que era escrita à mão. Este ficheiro exige dela o que
tests/test_tarefas_faceis_m9.py exige das do M9:

* a tarefa pede o mesmo no tema A (cada pedido do enunciado de antes, letra a letra: o espetáculo, a extensão, a citação com ato e
  cena, os pormenores e o vocabulário teatral, distinguir as duas obras, as duas linhas finais, as duas perguntas opcionais) e o
  tema B é a pergunta do docente, letra a letra, com a mesma extensão e os mesmos critérios; sai «Se não foste ao teatro»;
* as falas de Garrett (domínio público) são só as que as lições do M4 citam, conferidas letra a letra no cartão da lição de origem;
  o diálogo do retrato inteiro e contínuo; nenhuma citação junta texto dos dois lados de um «[…]»; a razão da promessa de Telmo só
  como o resumo da lição; a peça lê-se «no livro» (nenhuma lição do M4 diz «no manual»; nunca «edição da turma»);
* os exemplos usam outro caso, inventado e dito como inventado, sem frases da peça nem do espetáculo, sem dar feita nenhuma alínea,
  sem nenhuma resposta do aquecimento (incluindo as dos cartões de verdadeiro ou falso e as explicações f e fe) nem as suas ideias
  por outras palavras, e sem a resposta certa das perguntas opcionais;
* as decisões do docente: tempos 10/10/55/15 (quadro, relógios, guia); «com consulta» dito uma vez, no primeiro cartão; as passagens
  citadas ou copiadas não contam para as palavras (a mesma frase no enunciado e no guia; a m4-u2 não tem grelha /20); o aquecimento
  com uma só ligação; no máximo 10 perguntas de sim ou não; as mesmas palavras no enunciado, no aquecimento, no guia, no índice, no
  mapa e no portefólio («duas linhas finais», nunca «síntese»; o título novo);
* o acerto do M8: as linhas de fonte dos Textos 2, 3 e 4 da m8-u1 dizem «O poema completo lê-se no manual.», como a do Texto 1, e a
  alínea, a grelha e o guia dizem «o manual, a publicação que a lição indica ou outra edição»;
* as regras do texto; o contrato da página; as outras tarefas, grelhas, correções e aquecimentos iguais ao main, byte a byte;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base (o main 015ee060), gerador que dá o mesmo JSON,
  registada na auditoria, em scripts/desligar_sala.py, na leitura histórica e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em tests/browser_tarefas_faceis_m4.py."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
from auditoria_20261028 import undo_tarefa_m4u2_1115, undo_tarefas_faceis_m9_1114  # noqa: E402
# 15/11/2026: a revisão geral (revisao_geral_20261115), por cima de todas, muda a página e os dados da m5-u2 (sai o facto de 2025 do
# dossiê, cuja única fonte era o vídeo que sai da M5-F15): esses dois ficheiros leem-se com ela desfeita, com contagem estrita.
from auditoria_20261028 import undo_revisao_geral_1115  # noqa: E402
REVISAO_DE_CIMA = json.loads((ROOT / 'tests/fixtures/revisao-geral-edits-20261115.json').read_text('utf-8'))['files']
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefa_m4u2_tema_b_20261115.json'
MANIFESTO_REL = 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'
M9F = 'tests/fixtures/tarefas-faceis-m9-edits-20261114.json'
M8F = 'tests/fixtures/tarefas-faceis-m8-edits-20261113.json'
# 15/11/2026: por cima desta camada fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
REVISAOF = 'tests/fixtures/revisao-geral-edits-20261115.json'  # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
FILAF = 'tests/fixtures/fila-final-edits-20261115.json'  # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
SINTESEF = 'tests/fixtures/sintese-duas-linhas-edits-20261115.json'
BASE_COMMIT = '015ee060613875e1b1377a905a8d5f4c2dbc0ad0'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
N = '\xa0'
DADOS = 'docs/pedagogia/tarefas-escolha/m4-u2.json'
DADOS_AQ = 'docs/pedagogia/aquecimentos/m4-u2.json'
DADOS_M8 = 'docs/pedagogia/tarefas-escolha/m8-u1.json'
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
ENUNCIADO, AQUECIMENTO = 'tarefas/m4-u2/index.html', 'tarefas/m4-u2/aquecimento/index.html'
M8_PAGINAS = ['tarefas/m8-u1/index.html', 'tarefas/m8-u1/grelha/index.html']
GUIA, INDICE, MAPA = 'm4/guia-da-tarefa-m4/index.html', 'm4/index.html', 'm4/mapa-do-modulo-m4/index.html'
PORTEFOLIO, GUIA_M8 = 'm4/portefolio-do-modulo-m4/index.html', 'm8/guia-da-tarefa-m8/index.html'
MODULO = [GUIA, INDICE, MAPA, PORTEFOLIO]
# 15/11/2026 (revisão): a lição F20 e o plano da aula 11 deixam de ligar a cena do incêndio à opção «Se não foste ao teatro».
LICAO_F20, AULA_11 = 'm4/licao-m4-f20/index.html', 'm4/aulas/aula-11/index.html'
FICHEIROS = [DADOS_AQ, DADOS_M8, GRELHAS, ENUNCIADO, AQUECIMENTO] + M8_PAGINAS + MODULO + [LICAO_F20, AULA_11, GUIA_M8]
FLS = '<i>Frei Luís de Sousa</i>'
TITULO = f'O espetáculo ou Telmo, em {FLS}'
PERGUNTA = f'Que juízo merece Telmo, quando cala o nome do retrato no ato II de {FLS}: cumpre a palavra dada ou engana Maria?'
CONSULTA = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
NAO_CONTAM = 'Não contam para as palavras: as passagens citadas ou copiadas e as duas linhas finais.'
CARTOES_NOMES = ['Começar', 'Tema A ou B', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']
L = {'08': 'm4/licao-m4-f08/index.html', '20': 'm4/licao-m4-f20/index.html', '26': 'm4/licao-m4-f26/index.html',
     '27': 'm4/licao-m4-f27/index.html', 'QS': 'm4/m4-frei-luis-quem-sabia/index.html'}
# O que o enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = ['Descreve um momento do espetáculo de que te recordes.',
           'Relaciona-o com Frei Luís de Sousa , de Garrett: cita uma passagem curta, com ato e cena.',
           'Explica a tua opinião com pormenores observados e vocabulário teatral preciso.',
           'Distingue as duas obras e não inventes cenas.', 'TPC: Frei Luís de Sousaaa , de Raquel Castro', 'LU.CA',
           'apreciação crítica', 'com título', '180 a 240 palavras', 'o que aprendeste', 'onde se vê essa aprendizagem no teu trabalho',
           'Fotografa o texto e as duas linhas finais.', 'Entrega no Teams', 'Escreve à mão' if False else 'à mão']
# O diálogo do retrato (ato II, cena I): [n], fala, (lição, cartão, onde: 'pr' nas falas do cartão ou 'mais' no «Ler mais»).
DIALOGO = [
    ('[1]', 'MARIA: Oh! mas é verdade… vinde cá: (Leva-o diante dos três retratos que estão no fundo; e apontando para o de D. João) de quem é este retrato aqui, Telmo?'),
    ('[2]', 'TELMO, olha, e vira a cara de repente: Esse é… há de ser… é um da família, destes senhores da casa de Vimioso que aqui estão tantos.'),
    ('[3]', 'MARIA, ameaçando-o com o dedo: Tu não dizes a verdade, Telmo.'),
    ('[4]', 'TELMO, quase ofendido: Eu nunca menti, senhora D. Maria de Noronha.'),
    ('[5]', 'MARIA: Mas não diz a verdade toda o senhor Telmo Pais; que é quase o mesmo.'),
    ('[6]', 'TELMO: O mesmo!… Disse-vos o que sei, e o que é verdade; é um cavaleiro da família de meu outro amo que Deus… que Deus tenha em bom lugar.'),
    ('[7]', 'MARIA: E não tem nome o cavaleiro?'),
    ('[8]', 'TELMO, embaraçado: Há de ter: mas eu é que…'),
    ('[9]', 'MARIA, como quem lhe vai tapar a boca: Agora é que tu ias mentir de todo… cala-te.'),
]
# As falas curtas do Texto 2: (linha, lição, cartão, ato e cena, a frase da lição que dá o ato e a cena, ou None quando a lição
# dá o ato e a cena na linha de fonte do cartão).
CURTAS = [
    ('À fé de escudeiro honrado, senhora D. Madalena, a minha boca não se abre mais.', '27', 16, f'Ato{N}I, cena{N}II', 'Telmo a Madalena, ato I, cena II.'),
    ('Senão a mim.', 'QS', 2, f'Ato{N}I, cena{N}II', 'Ato I, cena II'),
    ('«Vivo ou morto, Madalena, hei de ver-vos pelo menos ainda uma vez neste mundo.»', 'QS', 2, f'Ato{N}I, cena{N}II', 'Ato I, cena II'),
    ('Não sei para que são estes mistérios: cuidam que eu hei de ser sempre criança!', '27', 16, f'Ato{N}II, cena{N}I', 'Maria a Telmo, ato II, cena I'),
    ('Aquele era D. João de Portugal, um honrado fidalgo, e um valente cavaleiro.', '08', 4, f'Ato{N}II, cena{N}II', 'Na cena II, Manuel entra'),
    ('eu sabia de um saber cá de dentro; ninguém mo tinha dito; e eu queria ficar certa.', '08', 4, f'Ato{N}II, cena{N}II', 'Na cena II, Manuel entra'),
]
PROMESSA = 'Telmo, aio de D. João de Portugal, prometeu a Madalena não alimentar a dúvida sobre a morte dele.'
# As ideias que o aquecimento da m4-u2 já ensina, por outras palavras (raízes): nenhuma pode aparecer nos exemplos.
IDEIAS_DO_AQUECIMENTO = (r'cadeira|\bluz\b|\bpausa|silênci|\bvidro|\bcostas|intérprete|recriaç|porta aberta|\bcor\b|\bfoco|cenografia|'
                         r'marcaç|desenho de luz|didascál|\baspas|memória|registo|vídeo|intenç|encenador|\bprov')
# 15/11/2026: o acerto do M8, frase a frase.
FONTES_M8 = [
    f'Eugénio de Andrade, «As Palavras», de <i>Até Amanhã</i>. O poema completo lê-se no manual. A lição{N}F04 também diz onde o ler: cartão «O texto».',
    f'Eugénio de Andrade, «Adeus», de <i>Os Amantes sem Dinheiro</i> (1950). O poema completo lê-se no manual. A lição{N}F04 também diz onde o ler: cartão «Outra leitura».',
    f'Ana Luísa Amaral, «Prece no Mediterrâneo», <i>Ágora</i>, Assírio &amp; Alvim, 2019. O poema completo lê-se no manual. A lição{N}F05 também diz onde o ler: cartão «O texto».',
    f'Ana Luísa Amaral, «A verdade histórica», em <i>PÁ: Poesia &amp; Outras Artes</i>, n.º{N}0, Casa Comum/U.Porto Press, setembro de 2023. O poema completo lê-se no manual. A lição{N}F05 também diz onde o ler: cartão «Outra leitura».',
]
EDICAO_M8 = 'o manual, a publicação que a lição indica ou outra edição'
# 15/11/2026 (revisão): o que esta camada muda no molde (scripts/tarefa_facil.py), troca a troca, letra a letra. Desfeitas estas
# trocas, o molde tem de ser o do main, byte a byte: qualquer outra mudança no molde falha.
MOLDE_TROCAS = [
    ('''    cada tema da m8-u1; o conto da m8-u2); em «temas_material», «textos» passa a ser opcional.

M4 (15/11/2026, camada tarefa_m4u2_tema_b_20261115: a m4-u2, que era escrita à mão, passa às tarefas de escolha, com «Tema A ou B»).
Uma chave nova, opcional; as páginas sem ela saem iguais, byte a byte:
  * «opcionais»: uma lista de perguntas opcionais ({"pergunta", "opcoes"}), como nas tarefas individuais, com «opcional_rotulo»;
    a m4-u2 guarda assim as duas perguntas opcionais que já tinha, letra a letra.
"""''',
     '''    cada tema da m8-u1; o conto da m8-u2); em «temas_material», «textos» passa a ser opcional.
"""'''),
    ('''    # 15/11/2026 (m4-u2, camada tarefa_m4u2_tema_b_20261115): a pergunta opcional sai num bloco à parte («quiz»), para a chave «opcionais»;
    # sem ela, o bloco é o de antes, letra a letra.
    op = f.get('opcional') or d.get('opcional') or f['opcionais'][0]  # 13/11/2026 (M7)''',
     '''    op = f.get('opcional') or d['opcional']  # 13/11/2026 (M7)'''),
    ('''    quiz = (f'<details data-task-optional-preparation><summary>{f["opcional_titulo"]}</summary><div class="task-quiz" aria-label="Uma pergunta opcional">\\n'
            f'<article class="task-question" data-task-question="1" aria-labelledby="q1"><h3 id="q1">{op["pergunta"]}</h3>{opcoes(op["opcoes"])}</article>\\n'
            f'<p data-task-status role="status">Respostas exploradas: 0 de 1. Podes rever qualquer escolha.</p></div></details>\\n')
    if f.get('opcionais'):
        # 15/11/2026 (m4-u2, camada tarefa_m4u2_tema_b_20261115): uma tarefa de escolha que já tinha duas perguntas opcionais
        # guarda as duas, como as tarefas individuais (pagina_individual). As páginas sem a chave saem iguais, byte a byte.
        ops = f['opcionais']
        quiz = (f'<details data-task-optional-preparation><summary>{f["opcional_titulo"]}</summary><div class="task-quiz" aria-label="{f["opcional_rotulo"]}">\\n'
                + ''.join(f'<article class="task-question" data-task-question="{k}" aria-labelledby="q{k}"><h3 id="q{k}">{k}. {o["pergunta"]}</h3>{opcoes(o["opcoes"])}</article>\\n'
                          for k, o in enumerate(ops, 1))
                + f'<p data-task-status role="status">Respostas exploradas: 0 de {len(ops)}. Podes rever qualquer escolha.</p></div></details>\\n')
''', ''),
    ('''             + lista([f'<b>{x["para"]}.</b> {x["texto"]}' for x in f['rever']], 'ul', 'tf-rever-lista') + '\\n'
             + quiz + f'</section>\\n')''',
     '''             + lista([f'<b>{x["para"]}.</b> {x["texto"]}' for x in f['rever']], 'ul', 'tf-rever-lista') + '\\n'
             f'<details data-task-optional-preparation><summary>{f["opcional_titulo"]}</summary><div class="task-quiz" aria-label="Uma pergunta opcional">\\n'
             f'<article class="task-question" data-task-question="1" aria-labelledby="q1"><h3 id="q1">{op["pergunta"]}</h3>{opcoes(op["opcoes"])}</article>\\n'
             f'<p data-task-status role="status">Respostas exploradas: 0 de 1. Podes rever qualquer escolha.</p></div></details>\\n'
             f'</section>\\n')'''),
]


def molde_sem_a_camada(texto):
    """15/11/2026 (revisão): o molde com as trocas desta camada desfeitas, cada uma com contagem estrita (uma vez)."""
    for novo, velho in MOLDE_TROCAS:
        assert texto.count(novo) == 1, novo[:80]
        texto = texto.replace(novo, velho)
    return texto


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def ler_sem_fila(rel):
    # 15/11/2026: a fila final (fila_final_20261115) fica por cima desta camada e muda o portefólio do M4: a página desta camada é a da árvore
    # com ela desfeita.
    texto = ler(rel)
    for e in reversed(json.loads(ler(FILAF))['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def antes(rel):
    """O ficheiro como estava por baixo desta camada (desfeita pelo manifesto, com contagem estrita): o main de partida."""
    texto = ler(rel)
    # 15/11/2026: por cima desta camada fica a fila final (fila_final_20261115), que muda o portefólio do M4 («já fotografadas; não escreves
    # outras»): desfaz-se primeiro, com contagem estrita, quando o ficheiro a traz.
    for e in reversed(json.loads(ler(FILAF))['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    for e in reversed(MANIFESTO['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def do_main(rel):
    """O ficheiro no commit de partida (os fluxos que correm este teste descarregam o histórico: fetch-depth: 0)."""
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    assert r.returncode == 0, f'{rel}: falta o commit de partida {BASE_COMMIT[:8]} (o fluxo tem de fazer checkout com fetch-depth: 0)'
    return r.stdout.decode('utf-8')


def visivel(fonte, so_main=True, sem_nav=True):
    if so_main and '<main' in fonte:
        fonte = fonte[fonte.index('<main'):fonte.index('</main>')]
    fonte = re.sub(r'<(script|style)\b.*?</\1>', ' ', fonte, flags=re.S)
    if sem_nav:
        fonte = re.sub(r'<nav\b.*?</nav>', ' ', fonte, flags=re.S)
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte))).strip()


def solto(texto):
    return texto.replace(N, ' ')


def sem_marcas(texto):
    return re.sub(r'[ \t\r\n]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', texto)))


def cartoes(k):
    """Os cartões de uma lição do M4 (CARTOES=[…] nas lições; em «Quem sabia, e quando», os itens de montar(…))."""
    fonte = ler(L[k])
    if 'CARTOES=[' in fonte:
        return json.JSONDecoder().raw_decode(fonte[fonte.index('CARTOES=[') + 8:])[0]
    i = fonte.index('itens:[', fonte.index('montar({casca:CASCA')) + 6
    return json.JSONDecoder().raw_decode(fonte[i:])[0]


def no_cartao(k, i):
    c = cartoes(k)[i - 1]
    return sem_marcas(c.get('html', '') + json.dumps({a: b for a, b in c.items() if a != 'html'}, ensure_ascii=False))


def respostas_do_aquecimento(aq):
    """As respostas que o aquecimento dá (como em tests/test_tarefas_faceis_m9.py, com os cartões de verdadeiro ou falso e as
    explicações f e fe)."""
    tira = lambda s: solto(re.sub(r'_([^_]+)_', r'\1', re.sub(r'\*\*', '', s))).strip().rstrip('.').lower()
    out = []
    for c in aq['cartoes']:
        if c['t'] == 'escolha':
            out.append(tira(c['o'][c['c']]))
        elif c['t'] == 'completar':
            frase = c['frase']
            for i, l in enumerate(c['lacunas'], 1):
                out.append(tira(l['o'][l['c']]))
                frase = frase.replace(f'[{i}]', l['o'][l['c']])
            out.append(tira(frase))
        elif c['t'] == 'rever':
            out.append(tira(c['o'][c['c']]))
            out.append(tira(c['frase'].replace(c['trecho'], c['o'][c['c']])))
        elif c['t'] == 'ordenar':
            out += [tira(x.split(' ', 1)[1]) for x in c['passos']]
        elif c['t'] == 'emparelhar':
            out += [tira(b) for a, b in c['pares']] + [tira(a) for a, b in c['pares']]
        if c['t'] == 'vf' and c.get('v'):
            out.append(tira(c['p']))
        explicacoes = [c.get('f')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe')])
        for e in explicacoes:
            if e:
                out += [tira(x) for x in re.split(r'(?<=[.;:!?])\s+', e) if len(tira(x).split()) >= 3]
    return [x for x in out if x]


class Pagina(HTMLParser):
    def __init__(self, fonte):
        super().__init__()
        self.pilha, self.raiz, self.ids, self.temas, self.perguntas, self.opcoes = [], [], [], [], [], []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.pilha and self.pilha[-1][0] == 'main':
            self.raiz.append((tag, a.get('id'), a.get('data-task-card-name')))
        if 'id' in a:
            self.ids.append(a['id'])
        if 'data-task-theme' in a:
            self.temas.append(a['data-task-theme'])
        if 'data-task-question' in a:
            self.perguntas.append((a['data-task-question'], any(x[0] == 'details' for x in self.pilha)))
        if tag == 'button' and 'data-response' in a:
            self.opcoes.append(a)
        if tag not in ('meta', 'link', 'br', 'img', 'input'):
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        if any(x[0] == tag for x in self.pilha):
            self.pilha = self.pilha[:max(i for i, x in enumerate(self.pilha) if x[0] == tag)]


class TarefaM4u2TemaB(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo, e o tema B é a pergunta do docente ----------

    def test_a_tarefa_pede_o_mesmo_e_o_tema_b_e_a_pergunta_do_docente(self):
        d, f = json.loads(ler(DADOS)), json.loads(ler(DADOS))['facil']
        velha, pagina = antes(ENUNCIADO), ler(ENUNCIADO)
        self.assertEqual(velha, do_main(ENUNCIADO))
        lido_velho, lido = solto(visivel(velha)), solto(visivel(pagina))
        for pedaco in PEDIDOS:
            with self.subTest(pedido=pedaco):
                self.assertIn(pedaco, lido_velho)
                self.assertIn(pedaco, lido)
        # Os dados são novos (a página era escrita à mão): não estavam no main e não são da camada.
        self.assertFalse(subprocess.run(['git', 'cat-file', '-e', f'{BASE_COMMIT}:{DADOS}'], cwd=ROOT, capture_output=True).returncode == 0)
        self.assertNotIn(DADOS, MANIFESTO['files'])
        self.assertEqual(d['slug'], 'm4-u2')
        self.assertEqual(d['unidade'], 2)
        self.assertEqual(d['titulo'], TITULO)
        self.assertEqual(re.search(r'<h1>(.*?)</h1>', pagina).group(1), TITULO)
        self.assertIn('<title>Aula de tarefa · O espetáculo ou Telmo, em Frei Luís de Sousa · M4</title>', pagina)
        # Os dois temas: A, a apreciação crítica do espetáculo (o mesmo espetáculo, com os mesmos dados); B, a pergunta, letra a letra.
        self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [('A', 'Apreciação crítica do espetáculo'), ('B', 'Telmo e o retrato')])
        self.assertEqual(re.findall(r'data-task-theme="([AB])"', pagina), ['A', 'B'])
        self.assertIn('<i>TPC: Frei Luís de Sousaaa</i>, de Raquel Castro, visto no LU.CA', velha)
        self.assertIn('<i>TPC: Frei Luís de Sousaaa</i>, de Raquel Castro, visto no LU.CA', f['temas'][0]['intro'])
        self.assertEqual(solto(f['temas'][1]['intro']), 'Escreve um texto de opinião sobre esta pergunta: «' + solto(PERGUNTA) + '»')
        self.assertEqual(pagina.count(PERGUNTA.replace('ato II', f'ato{N}II')), 1)
        self.assertIn('com <i>TPC: Frei Luís de Sousaaa</i>, com texto e encenação de Raquel Castro, a partir de Garrett, no LU.CA Teatro Luís de Camões'.split('com ', 1)[1],
                      f['temas'][0]['antes'][0])
        self.assertIn('com texto e encenação de Raquel Castro, a partir de Garrett', no_cartao('20', 11))
        self.assertIn('LU.CA Teatro Luís de Camões', no_cartao('20', 11))
        # A mesma extensão e os mesmos critérios nos dois temas.
        self.assertIn('<strong>180 a 240 palavras</strong>', solto(velha))
        self.assertEqual([solto(x[2]) for x in f['quadro']['linhas']], ['', '', '180 a 240', '', '180 a 240'])
        self.assertEqual(solto(f['temas_nota']), 'Um só texto: 180 a 240 palavras.')
        self.assertEqual(solto(f['depois'][0]['meta']), '180 a 240 palavras, sobre o tema A ou o tema B.')
        criterios_antes = re.findall(r'<li>([^<]*)</li>', velha[velha.index('<ul class="task-criteria">'):])[:3]
        self.assertEqual(criterios_antes, ['Juízos com critério e pormenores observados.', 'Relação clara com Garrett, sustentada numa citação exata.',
                                           'Escrita correta e vocabulário teatral preciso.'])
        verificar = ' '.join(solto(x) for x in f['verificar'])
        for parte in ('pormenores e com um critério', 'passagem curta e exata da peça', 'vocabulário teatral preciso', 'revi a escrita'):
            self.assertIn(parte, verificar)
        grupos = f['depois'][0]['grupos']
        self.assertEqual([solto(g['intro']) for g in grupos], ['Se escolheste o tema A:', 'Se escolheste o tema B:', 'No fim do texto:'])
        a, b = (' '.join(solto(sem_marcas(x)) for x in g['alineas']) for g in grupos[:2])
        for parte in ('título', 'Descreve um momento do espetáculo de que te recordes.', 'cita uma passagem curta, com ato e cena.',
                      'pormenores observados e vocabulário teatral preciso.', 'Distingue as duas obras e não inventes cenas.'):
            self.assertIn(parte, a)
        for parte in ('Responde à pergunta', 'pormenores da cena', 'Cita uma passagem curta da peça, com ato e cena.', 'vocabulário teatral preciso',
                      'Não inventes falas nem cenas.'):
            self.assertIn(parte, b)
        # Um pedido por alínea.
        for g in grupos:
            for x in g['alineas']:
                self.assertEqual(len(re.findall(r'[.!?](?:\s|$)', solto(sem_marcas(x)))), 1, x)
        # As duas linhas finais: a pergunta de antes, em dois passos.
        self.assertIn('Escreve duas linhas: o que aprendeste e onde se vê essa aprendizagem no teu trabalho.', velha)
        self.assertEqual(f['finais']['passos'], ['Escreve o que aprendeste.', 'Diz onde se vê essa aprendizagem no teu trabalho.'])
        # As duas perguntas opcionais de antes, letra a letra (as perguntas, as opções, a certa e as respostas).
        antigas = re.findall(r'<h3 id="q\d">([^<]*)</h3>', velha)
        self.assertEqual([o['pergunta'] for o in f['opcionais']], antigas)
        botoes = lambda fonte: re.findall(r'<button type="button" aria-pressed="false" data-correct="(true|false)" data-response="([^"]*)">([^<]*)</button>', fonte)
        self.assertEqual(botoes(pagina), botoes(velha))
        self.assertEqual(len(botoes(pagina)), 6)
        # Sai a opção «Se não foste ao teatro» (o desdobrável e qualquer referência).
        self.assertIn('Se não foste ao teatro', velha)
        for rel in (ENUNCIADO, AQUECIMENTO, DADOS, DADOS_AQ, GUIA):
            # (nos dados, fora as notas internas «_nota», que contam a história da decisão)
            lido_rel = solto(visivel(ler(rel), so_main=False, sem_nav=False)) if rel.endswith('.html') else json.dumps(
                {k: v for k, v in json.loads(ler(rel)).get('facil', json.loads(ler(rel))).items() if k != '_nota'}, ensure_ascii=False)
            self.assertNotRegex(lido_rel, r'(?i)não foste ao teatro|faltaste|alternativa de leitura|leitura silenciosa|ler em voz alta|lê em voz alta', rel)

    # ---------- as falas de Garrett, letra a letra, das lições ----------

    def test_falas_de_garrett_so_das_licoes_letra_a_letra(self):
        f = json.loads(ler(DADOS))['facil']
        pagina = ler(ENUNCIADO)
        t1 = f['textos'][0]
        self.assertEqual([t['id'] for t in f['textos']], ['texto-1'])
        self.assertEqual([(p['n'], p['t']) for p in t1['paragrafos']], DIALOGO)
        # [1] a [5]: as falas do cartão 13 da F26, do cartão 2 da F08 e do cartão 10 de «Quem sabia, e quando», letra a letra;
        # [6] a [9]: o «Ler mais» do cartão 13 da F26 («A conversa continua:») e o do cartão 4 da F08, seguidos, sem cortes.
        falas = lambda k, i: [re.sub(r'^\[\d\] ', '', sem_marcas(x)) for x in re.findall(r'<p class="pr"[^>]*>(.*?)</p>', cartoes(k)[i - 1]['html'])]
        self.assertEqual(falas('26', 13), [t for _, t in DIALOGO[:5]])
        self.assertEqual(falas('08', 2), [t for _, t in DIALOGO[:5]])
        qs = [sem_marcas(x) for x in re.findall(r'<p>(.*?)</p>', cartoes('QS')[9]['html'].split('<blockquote class="cit prosa">')[1].split('</blockquote>')[0])]
        self.assertEqual(['MARIA: ' + qs[0]] + qs[1:], [t for _, t in DIALOGO[:5]])
        continua = ' '.join(t for _, t in DIALOGO[5:])
        self.assertIn('A conversa continua: «' + continua + '»', sem_marcas(cartoes('26')[12]['html']))
        self.assertIn('ortografia atualizada: «' + continua + '»', sem_marcas(cartoes('08')[3]['html']))
        self.assertTrue(sem_marcas(cartoes('26')[12]['html']).split('A conversa continua: «')[0].rstrip().endswith('Telmo foi aio de D. João: por isso sabe de quem é o retrato.'))
        for _, t in DIALOGO:
            self.assertNotIn('[…]', t)
            self.assertEqual(pagina.count(html.escape(t, quote=False)), 1, t)
        self.assertEqual(t1['glossario'], [['vinde cá', 'venha cá'], ['D. João', 'D. João de Portugal, primeiro marido de Madalena, dado por morto em Alcácer Quibir'],
                                           ['casa de Vimioso', 'a família de D. João']])
        gl = sem_marcas(re.search(r'<p class="gl">(.*?)</p>', cartoes('26')[12]['html']).group(1))
        for p, s in t1['glossario']:
            self.assertIn(f'{p}, {s}', gl)
        self.assertTrue(t1['fonte'].startswith(f'Almeida Garrett, {FLS} (1844), ato{N}II, cena{N}I, ortografia atualizada.'))
        self.assertIn('Almeida Garrett, <i>Frei Luís de Sousa</i> (1844), ato II, cena I, ortografia atualizada.', solto(cartoes('26')[12]['html']))
        self.assertEqual((cartoes('26')[12]['rot'], cartoes('26')[12]['titulo']), ('O texto', 'B. O retrato'))
        self.assertIn('cartão «O texto» (B. O retrato)', t1['fonte'])
        self.assertIn('«Ler mais»', t1['fonte'])
        # O Texto 2: só falas curtas que as lições citam, cada uma com o ato e a cena que a lição lhe dá.
        o = f['temas_material']['onde'][0]
        self.assertEqual(o['id'], 'texto-2')
        self.assertEqual([c['linhas'] for c in o['citacoes']], [[x[0]] for x in CURTAS])
        for c, (linha, k, i, onde, frase) in zip(o['citacoes'], CURTAS):
            with self.subTest(fala=linha):
                self.assertIn(linha, no_cartao(k, i))
                self.assertIn(frase, solto(no_cartao(k, i)))
                self.assertTrue(c['intro'].startswith(onde + '.'), c['intro'])
                self.assertLessEqual(len(linha.split()), 25)
                self.assertNotIn('[…]', linha)
                self.assertEqual(pagina.count(html.escape(linha, quote=False)), 1, linha)
                rotulo = re.search(r'cartão «([^»]+)»', c['intro'])
                if rotulo:
                    self.assertEqual(solto(cartoes(k)[i - 1]['rot']), solto(rotulo.group(1)))
                if 'Ler mais' in c['intro']:
                    self.assertIn(linha, sem_marcas(cartoes(k)[i - 1]['html'].split('<details class="mais">')[-1]))
        # «Senão a mim.» e a carta vêm da mesma fala citada, sem nada dos dois lados de um «[…]».
        qs2 = sem_marcas(cartoes('QS')[1]['html'])
        self.assertRegex(qs2, r'Tudo foi inútil; e a ninguém mais ficou resto de dúvida…\s*TELMO: Senão a mim\.')
        self.assertIn('Ato I, cena II', solto(qs2))
        # A razão da promessa de Telmo só está parafraseada na lição F27: a página dá o resumo da lição, dito como resumo.
        self.assertIn(PROMESSA, no_cartao('27', 16))
        self.assertEqual(f['temas'][1]['antes'][1], f'A lição{N}F27 resume assim a promessa (é um resumo, não uma fala da peça): «{PROMESSA}»')
        # A peça lê-se no livro; nenhuma lição do M4 diz «no manual»; nunca «edição da turma».
        lido = solto(visivel(pagina))
        self.assertNotRegex(lido, r'\bmanual\b|edição da turma')
        self.assertEqual(lido.count('A peça inteira lê-se no livro.'), 3)
        for k in L:
            self.assertNotIn(' manual', sem_marcas(json.dumps(cartoes(k), ensure_ascii=False)).replace('manuais/', ''), k)
        # Sem imagens e sem ligações para fora.
        principal = pagina[pagina.index('<main'):pagina.index('</main>')]
        for fora in ('<img', '<figure', 'data:image', 'href="http'):
            self.assertNotIn(fora, principal)

    def test_exemplos_com_outro_caso(self):
        f = json.loads(ler(DADOS))['facil']
        pagina = ler(ENUNCIADO)
        aq = json.loads(ler(DADOS_AQ))
        exemplos = [t['material']['exemplos'][0] for t in f['temas']]
        self.assertEqual([len(t['material']['exemplos']) for t in f['temas']], [1, 1])
        self.assertEqual(f['depois'][0]['exemplos'], [])
        apoios = re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver um exemplo com outro caso</summary>.*?</details>', pagina, re.S)
        self.assertEqual(len(apoios), 2)
        self.assertEqual(pagina.count('<aside class="tf-exemplo">'), 2)
        textos = ' '.join(solto(p['t']) for ex in exemplos for p in ex['paragrafos'])
        baixo = textos.lower()
        for ex in exemplos:
            self.assertIn('Um caso inventado', ex['titulo'])
            self.assertTrue(ex['contexto'].startswith('Caso inventado, só para mostrar a forma'), ex['contexto'])
        # Nem frases da peça nem do espetáculo, nem nomes das obras e das personagens.
        for fora in [t for _, t in DIALOGO] + [x[0] for x in CURTAS] + aq['reservadas']:
            palavras = solto(fora).strip('«»').split()
            for j in range(0, max(1, len(palavras) - 3)):
                self.assertNotIn(' '.join(palavras[j:j + 4]).lower(), baixo, fora)
        for nome in ('Telmo', 'Maria', 'Madalena', 'Manuel', 'João', 'Garrett', 'TPC', 'Raquel', 'LU.CA', 'Frei', 'retrato', 'Porta aberta', 'promessa', 'palavra dada'):
            self.assertNotIn(nome.lower(), baixo, nome)
        # Nenhuma resposta do aquecimento, nenhuma frase do aquecimento, nenhuma das suas ideias por outras palavras.
        respostas = respostas_do_aquecimento(aq)
        self.assertGreaterEqual(len(respostas), 30)
        for r in respostas:
            self.assertNotRegex(baixo, r'\b' + re.escape(r) + r'\b', r)
        self.assertNotRegex(baixo, IDEIAS_DO_AQUECIMENTO)
        # Não dão feita nenhuma alínea (os rótulos não são letras de alíneas) nem a resposta certa das perguntas opcionais.
        for ex in exemplos:
            for p in ex['paragrafos']:
                self.assertNotRegex(p['al'], r'[a-k]\)')
        for op in f['opcionais']:
            certa = [o['texto'] for o in op['opcoes'] if o['certa']]
            self.assertEqual(len(certa), 1)
            self.assertNotIn(certa[0].rstrip('.').lower(), baixo)
        self.assertNotIn('sem aspas', baixo)
        # O apoio fica fechado no ecrã e não sai em papel.
        self.assertEqual(pagina.count('tf-so-ecra'), 3)

    # ---------- as decisões do docente ----------

    def test_tempos_consulta_contagem_aquecimento_e_verificacao(self):
        d = json.loads(ler(DADOS))
        f, pagina = d['facil'], ler(ENUNCIADO)
        lido = solto(visivel(pagina))
        quadro = pagina[pagina.index('<table class="tf-quadro">'):pagina.index('</table>')]
        tempos = [int(x) for x in re.findall(r'<th scope="row">(\d+)' + N + 'min</th>', quadro)]
        self.assertEqual(tempos, [10, 10, 55, 15, 90])
        self.assertEqual(d['aquecer']['minutos'], 10)
        self.assertEqual(f['producao_minutos'], 55)
        self.assertEqual(pagina.count('data-max="10" data-passo="1" data-rotulo="Aquecimento"'), 1)
        self.assertEqual(pagina.count('data-max="55" data-passo="5" data-rotulo="Produção em papel"'), 1)
        self.assertIn('data-max="60"', do_main(ENUNCIADO))
        self.assertEqual(pagina.count('data-relogio'), 2)
        self.assertEqual(f['kicker'], 'Tarefa individual, 90 minutos'.replace('90 ', f'90{N}'))
        self.assertEqual(f['fazer'][0], f'Faz o aquecimento (10{N}minutos).')
        guia = solto(visivel(ler(GUIA), so_main=False, sem_nav=False))
        self.assertIn('fazes os cartões durante 10 minutos. Seguem-se 10 minutos de leitura, 55 de produção em papel e 15 de revisão e entrega no Teams.', guia)
        for rel in (ENUNCIADO, AQUECIMENTO, GUIA):
            self.assertNotRegex(solto(visivel(ler(rel), so_main=False, sem_nav=False)), r'(?<![\d,])\b(?:5|60) min(?:utos)?\b|\b[Ss]essenta minutos', rel)
        # «Com consulta», uma vez, no primeiro cartão.
        self.assertEqual(f['modo'], CONSULTA)
        self.assertEqual(lido.count('com consulta'), 1)
        self.assertEqual(len(re.findall(r'\bconsultas?\b', lido.lower())), 1)
        cabeca = pagina[pagina.index('<header>'):pagina.index('</header>')]
        self.assertIn(f'<p class="tf-p">{CONSULTA}</p>', cabeca)
        # O que não conta para as palavras: a mesma frase no enunciado e no guia.
        self.assertEqual(f['quadro']['notas'][1], NAO_CONTAM)
        self.assertEqual(lido.count(NAO_CONTAM), 1)
        self.assertEqual(guia.count(NAO_CONTAM), 1)
        self.assertEqual(f['finais']['texto'], 'Ficam fora da contagem.')
        # A m4-u2 não tem grelha /20 (nem antes nem agora): nenhuma ligação à grelha, nenhuma grelha nova inventada.
        self.assertNotIn('m4-u2', json.loads(ler(GRELHAS))['tarefas'])
        self.assertNotIn('grelha/', pagina)
        self.assertFalse((ROOT / 'tarefas/m4-u2/grelha').exists())
        self.assertNotIn('autoavaliação', lido.lower())
        # O aquecimento é o primeiro passo, com uma só ligação.
        self.assertEqual(pagina.count('href="aquecimento/"'), 1)
        self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
        # A verificação: no máximo dez perguntas de sim ou não.
        self.assertLessEqual(len(f['verificar']), 10)
        self.assertEqual(len(f['verificar']), 9)
        for x in f['verificar']:
            self.assertTrue(x.endswith('?'), x)
            self.assertEqual(x.count('?'), 1, x)
        self.assertEqual(pagina.count('<label><input type="checkbox">'), len(f['verificar']))
        # A fala do aluno em discurso direto: as citações da peça entre «».
        self.assertIn('Põe-nas entre aspas: «…».', f['depois'][0]['citar'])
        # O aquecimento serve os dois temas e mudou pouco, no molde: só três cartões e as falas novas nas reservadas.
        aq, aq_antes = json.loads(ler(DADOS_AQ)), json.loads(antes(DADOS_AQ))
        self.assertEqual(antes(DADOS_AQ), do_main(DADOS_AQ))
        self.assertEqual(len(aq['cartoes']), len(aq_antes['cartoes']))
        mudados = [k for k, (x, y) in enumerate(zip(aq['cartoes'], aq_antes['cartoes'])) if x != y]
        self.assertEqual(mudados, [0, 4, 11])
        self.assertEqual({k: v for k, v in aq.items() if k not in ('cartoes', 'reservadas')}, {k: v for k, v in aq_antes.items() if k not in ('cartoes', 'reservadas')})
        self.assertEqual(aq['reservadas'][:len(aq_antes['reservadas'])], aq_antes['reservadas'])
        for x in [t for _, t in DIALOGO[5:]] + [x[0].strip('«»') for x in CURTAS]:
            self.assertIn(x, aq['reservadas'])
        levar = aq['cartoes'][-1]['html']
        for parte in ('tema A', 'tema B', 'com ato e cena', 'Telmo'):
            self.assertIn(parte, levar)
        self.assertNotIn('na tua apreciação', json.dumps(aq, ensure_ascii=False))
        self.assertIn('Dez minutos com consulta', aq['cartoes'][0]['html'])

    def test_tudo_junto_no_m4(self):
        for rel in MODULO:
            with self.subTest(pagina=rel):
                lido = solto(visivel(ler(rel), so_main=False, sem_nav=False))
                self.assertNotRegex(lido, r'(?i)síntese', rel)
                self.assertIn('duas linhas finais', lido)
                self.assertIn(solto(sem_marcas(TITULO)), lido)
                self.assertNotIn('Apreciação crítica do espetáculo', ler(rel).split('id="arquivo-producoes"')[0])
                self.assertEqual(antes(rel), do_main(rel))
        self.assertNotRegex(ler(INDICE), r'(?i)síntese integrada|uma síntese')
        self.assertIn('"title":"O espetáculo ou Telmo, em Frei Luís de Sousa"', ler(INDICE))
        portefolio = solto(visivel(ler(PORTEFOLIO), so_main=False, sem_nav=False))
        self.assertNotRegex(portefolio, r'(?i)trabalho de equipa|em equipa|em grupo|em pares|autoavaliação')
        self.assertIn('autonomia, responsabilidade, pensamento crítico', portefolio)
        guia = ler(GUIA)
        self.assertNotRegex(solto(visivel(guia, so_main=False, sem_nav=False)), r'(?i)autoavaliação|par de trabalho|três antes de mim|faltaste')
        self.assertIn('<li><a href="../../tarefas/m4-u2/">Unidade 2 · ' + TITULO + '</a>', guia)
        # As trocas do módulo são só as da camada, e cada página fica, fora delas, como no main.
        for rel in MODULO + [GUIA_M8]:
            self.assertTrue(MANIFESTO['files'][rel]['edits'], rel)
        # O enunciado usa as mesmas palavras que o aquecimento e os guias: «duas linhas finais», «tema A ou B».
        lido = solto(visivel(ler(ENUNCIADO)))
        for palavra in ('duas linhas finais', 'Escolhe um tema: A ou B', 'apreciação crítica', 'texto de opinião'):
            self.assertIn(palavra, lido)
        self.assertNotRegex(lido, r'(?i)\bsíntese\b|Relembrar|Fecha o trabalho')

    def test_achados_da_revisao_15_11(self):
        # 15/11/2026 (revisão): os achados confirmados, cada um com a prova na árvore.
        # (1) Nenhuma página do M4 liga a cena do incêndio à opção «Se não foste ao teatro» da tarefa.
        f20 = sem_marcas(json.dumps(cartoes('20'), ensure_ascii=False))
        self.assertNotIn('cena da tarefa da unidade', f20)
        fogo = [c for c in cartoes('20') if c.get('titulo') == 'O fogo de Manuel']
        self.assertEqual(len(fogo), 1)
        self.assertIn('<p>Compara o que ouviste na leitura em voz alta com o que leste em silêncio.</p></div></details>', fogo[0]['html'])
        self.assertNotIn('faltou ao teatro', fogo[0]['html'])
        aula = ler(AULA_11)
        self.assertNotIn('É a cena de quem faltou ao teatro', aula)
        self.assertEqual(aula.count('Cada aluno compara o que ouviu com o que leu em silêncio.'), 1)
        for rel in [ENUNCIADO, AQUECIMENTO, DADOS, DADOS_AQ] + MODULO:
            corpo = ler(rel).replace('sai a opção «Se não foste ao teatro»', '')
            self.assertNotRegex(corpo, r'(?i)não foste ao teatro|faltaste ao teatro|faltou ao teatro|cena da tarefa da unidade', rel)
        for rel in (LICAO_F20, AULA_11):
            self.assertEqual(len(MANIFESTO['files'][rel]['edits']), 1, rel)
        # (2) A F27 é da unidade 3, que vem depois da aula de tarefa: o «Rever a matéria» não manda «reler» uma lição que ainda não se deu.
        unidades = re.findall(r'"lessons":\[([^\]]*)\],"steps":\[([^\]]*)\]', ler(INDICE))
        self.assertEqual(len(unidades), 3)
        dadas = set(re.findall(r'"(m4-[a-z0-9-]+)"', unidades[0][1] + unidades[1][1]))
        self.assertIn('m4-f27', unidades[2][1])
        self.assertNotIn('m4-f27', dadas)
        f = json.loads(ler(DADOS))['facil']
        fora_da_unidade = 0
        for x in f['rever']:
            alvo = re.search(r'\.\./\.\./m4/(?:licao-)?(m4-[a-z0-9-]+)/', x['texto']).group(1)
            if alvo not in dadas:
                fora_da_unidade += 1
                self.assertNotIn('Relê', x['texto'])
                self.assertIn(f'da unidade{N}3', x['texto'])
        self.assertEqual(fora_da_unidade, 1)
        promessa = [x for x in f['rever'] if x['para'] == 'A promessa de Telmo']
        self.assertEqual(len(promessa), 1)
        self.assertIn(f'da unidade{N}3. Se quiseres, lê «Recusar, contar ou fugir?»', promessa[0]['texto'])
        # (3) No mapa, os critérios da tarefa 2 servem os dois temas: nada de palco nem de espetáculo; três critérios, como antes.
        crit = re.search(r'<span class="tn">2</span><div><b>O espetáculo ou Telmo, em <i>Frei Luís de Sousa</i></b><span class="peso">25.%, individual</span><span class="crit">([^<]*)</span>', ler(MAPA)).group(1)
        self.assertEqual(crit, 'Descrição e juízo; Relação com Garrett; Língua e género')
        self.assertEqual(len(crit.split('; ')), len(re.search(r'<span class="tn">2</span>.*?<span class="crit">([^<]*)</span>', do_main(MAPA)).group(1).split('; ')))
        self.assertNotRegex(crit, r'(?i)palco|espetáculo')
        # (4) No índice, a apreciação crítica tem as palavras da tarefa (180 a 240).
        self.assertIn(f'"p":"Como se chama o texto de 180{N}a{N}240{N}palavras que nasce das notas?"', ler(INDICE))
        self.assertNotIn(f'150{N}a{N}200{N}palavras que nasce', ler(INDICE))
        self.assertIn('180 a 240 palavras', solto(visivel(ler(ENUNCIADO))))
        # (5) O exemplo do tema B não tem a forma da pergunta (um compromisso cumprido contra alguém enganado) nem a fórmula
        # «juízo dividido: …, mas …»: um juízo com um só lado, um critério e um pormenor.
        ex_b = f['temas'][1]['material']['exemplos'][0]
        texto_b = ' '.join(solto(p['t']) for p in ex_b['paragrafos']).lower()
        self.assertNotRegex(texto_b, r'dividid|, mas |\bcumpr|engan|palavra|promet|compromiss|aceitou|regra que|mentir|menti\b|verdade|cala|esconde|vira|olhar')
        self.assertEqual([p['al'] for p in ex_b['paragrafos']], ['Um juízo, com o critério:', 'Um pormenor que o apoia:'])
        # (6) Ver o fim de test_contrato_da_pagina: o molde, desfeitas as trocas desta camada, é o do main.

    def test_acerto_do_m8_os_poemas_estao_no_manual(self):
        f = json.loads(ler(DADOS_M8))['facil']
        blocos = [o for t in f['temas'] for o in t['material']['onde']]
        self.assertEqual([o['fonte'] for o in blocos], FONTES_M8)
        velhos = [o['fonte'] for t in json.loads(antes(DADOS_M8))['facil']['temas'] for o in t['material']['onde']]
        self.assertEqual(velhos[0], FONTES_M8[0])
        for velho, novo in zip(velhos[1:], FONTES_M8[1:]):
            # Como no Texto 1: a linha de antes, com «O poema completo lê-se no manual.» e o cartão da lição «também».
            self.assertEqual(novo, velho.replace(' diz onde ler o poema completo: cartão', ' também diz onde o ler: cartão')
                             .replace(f' A lição{N}F0', f' O poema completo lê-se no manual. A lição{N}F0'))
        self.assertIn(f'Indica onde leste os poemas: {EDICAO_M8}.', f['depois'][1]['alineas'])
        self.assertIn('leem-se no manual', f['rever_texto'])
        pagina = solto(visivel(ler(M8_PAGINAS[0])))
        self.assertEqual(pagina.count('O poema completo lê-se no manual.'), 4)
        self.assertIn(f'Indica onde leste os poemas: {EDICAO_M8}.', pagina)
        grelha = solto(visivel(ler(M8_PAGINAS[1]), so_main=False))
        self.assertIn(f'Não indicar onde leste os poemas ({EDICAO_M8}).', grelha)
        self.assertNotIn('(o manual ou outra edição)', grelha)
        self.assertIn([f'Não identificar a edição consultada.', f'Não indicar onde leste os poemas ({EDICAO_M8}).'],
                      json.loads(ler(GRELHAS))['tarefas']['m8-u1']['trocas_aluno'])
        guia = solto(visivel(ler(GUIA_M8), so_main=False, sem_nav=False))
        self.assertIn('lê os dois poemas de cada tema antes da aula, no manual.', guia)
        self.assertIn('dizem também onde ler cada poema', guia)
        # A versão de correção não diz onde se leu: não muda. A m8-u2 (o conto) não muda.
        for rel in ('tarefas/m8-u1/correcao/index.html', 'tarefas/m8-u2/index.html', 'tarefas/m8-u2/grelha/index.html',
                    'docs/pedagogia/tarefas-escolha/m8-u2.json'):
            self.assertEqual(ler(rel), do_main(rel), rel)
        # Nada mais diz, no M8, só uma parte disto.
        for p in [ROOT / x for x in M8_PAGINAS + [GUIA_M8, 'tarefas/m8-u1/correcao/index.html']]:
            self.assertNotIn('o manual ou outra edição', p.read_text('utf-8'))

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        # No enunciado e no aquecimento, todo o texto; nas páginas do módulo, o que a camada escreve (o resto é do main).
        novos = {rel: ' '.join(visivel('<main>' + e['new'] + '</main>') for e in MANIFESTO['files'][rel]['edits']) for rel in MODULO + [GUIA_M8]}
        for rel in (ENUNCIADO, AQUECIMENTO) + tuple(MODULO) + (GUIA_M8,):
            with self.subTest(pagina=rel):
                texto = novos.get(rel) or visivel(ler(rel))
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        fonte = ler(ENUNCIADO)
        texto = visivel(fonte)
        self.assertNotIn('·', texto)
        self.assertNotRegex(texto, r'[—–]')
        self.assertNotRegex(texto, r'[“”"]')
        self.assertNotRegex(solto(texto), r'[?!]\s*[.,:;]')
        principal = fonte[fonte.index('<main'):fonte.index('</main>')]
        sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"|data-response="[^"]*"', '', principal)
        self.assertNotIn('Frei Luís de Sousa', sem_italicos)
        self.assertNotIn('TPC', sem_italicos.replace('não descreve <i>TPC</i>', ''))
        for padrao in (r'\b(?:Texto|Textos|Tema|tema|Lição|lição|ato|Ato|cena|Alínea|alínea|alíneas) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-k]\))',
                       r'\d (?:min|minutos|palavras)\b', r'(?:\d|\]|\)|\b[IVX]+) (?:a|e|ou) (?:\d|\[|[a-k]\)|[IVX]+\b)', r'\bA (?:ou|e) B\b'):
            self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
        self.assertNotRegex(texto.lower(), r'\bsozinh[oa]\b|\bo aluno\b|\ba aluna\b|\bpar de\b|\bem equipa\b|\bprofessor')
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/tarefa_m4u2_tema_b_20261115.py'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página ----------

    def test_contrato_da_pagina(self):
        d = json.loads(ler(DADOS))
        f, fonte = d['facil'], ler(ENUNCIADO)
        p = Pagina(fonte)
        self.assertEqual(fonte.count('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil '
                                     'data-task-opening="Começar" data-task-index="nomes">'), 1)
        self.assertEqual([x[0] for x in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section'])
        self.assertEqual(['Começar'] + [x[2] for x in p.raiz if x[0] == 'section'], CARTOES_NOMES)
        self.assertEqual([x[1] for x in p.raiz if x[0] == 'section'], ['tema', 'o-teu-texto', 'entregar', 'apoios'])
        self.assertEqual(len(p.ids), len(set(p.ids)), [x for x in p.ids if p.ids.count(x) > 1])
        self.assertEqual(p.temas, ['A', 'B'])
        self.assertEqual(p.perguntas, [('1', True), ('2', True)])
        self.assertEqual(len(p.opcoes), 6)
        self.assertEqual([o['data-correct'] for o in p.opcoes].count('true'), 2)
        self.assertIn('<p data-task-status role="status">Respostas exploradas: 0 de 2. Podes rever qualquer escolha.</p>', fonte)
        principal = fonte[fonte.index('<main'):fonte.index('</main>')]
        for href in re.findall(r'<a href="([^"]+)"', principal):
            if href.startswith('#'):
                self.assertIn(href[1:], p.ids, href)
            else:
                self.assertFalse(href.startswith('http'), href)
                alvo = (ROOT / 'tarefas/m4-u2' / href.split('#')[0]).resolve()
                self.assertTrue((alvo / 'index.html').is_file(), href)
        self.assertEqual(f['folha_versao'], '20261113-facil-12')
        self.assertEqual(fonte.count('assets/task-textos.css?v=20261113-facil-12"'), 1)
        self.assertIn('assets/task-reader.js?v=20261112-facil-7"', fonte)
        self.assertEqual(fonte.count('<button type="button" data-task-print hidden>Imprimir o enunciado</button>'), 1)
        # «Rever a matéria»: cada lição existe, com o título dito e os cartões que se mandam reler.
        for x in f['rever']:
            for href, nome in re.findall(r'<a href="([^"]+)">([^<]+)</a>', x['texto']):
                alvo = (ROOT / 'tarefas/m4-u2' / href).resolve() / 'index.html'
                self.assertTrue(alvo.is_file(), href)
                self.assertIn(html.unescape(nome).replace('«', '').replace('»', ''), html.unescape(ler(alvo.relative_to(ROOT).as_posix())).replace('«', '').replace('»', ''))
        nomes = {'08': ['A resposta de Telmo'], '27': ['Recusar, contar ou fugir?'], '20': ['Conceito']}
        for k, ns in nomes.items():
            todos = [c.get('rot') for c in cartoes(k)] + [c.get('titulo') for c in cartoes(k)]
            for n in ns:
                self.assertIn(n, todos, (k, n))
        # O gerador dá a página e o aquecimento, byte a byte; a página nova só sai dos dados novos.
        with tempfile.TemporaryDirectory() as tmp:
            for comando in ('scripts/tarefas_escolha.py', 'scripts/aquecimentos.py', 'scripts/grelhas_tarefas.py'):
                r = subprocess.run([sys.executable, comando, '--saida', tmp], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for rel in [ENUNCIADO, AQUECIMENTO] + M8_PAGINAS + ['tarefas/m8-u1/correcao/index.html']:
                self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes(), rel)
            self.assertFalse((Path(tmp) / 'tarefas/m4-u2/grelha').exists())
        # O molde ganhou uma só chave opcional («opcionais»); as páginas sem ela saem iguais (test_as_outras_tarefas_nao_mudam).
        molde, molde_main = ler('scripts/tarefa_facil.py'), do_main('scripts/tarefa_facil.py')
        self.assertNotIn("f.get('opcionais')", molde_main)
        self.assertEqual(molde.count("if f.get('opcionais'):"), 1)
        # 15/11/2026 (revisão): mais forte. Desfeitas, letra a letra, as quatro trocas desta camada no molde (MOLDE_TROCAS), o molde é
        # o do main, byte a byte: qualquer outra mudança no molde, dentro ou fora do bloco «opcionais», falha aqui.
        self.assertEqual(molde_sem_a_camada(molde), molde_main)
        self.assertEqual(ler('assets/task-textos.css'), do_main('assets/task-textos.css'))

    # ---------- as outras tarefas não mudam ----------

    def test_as_outras_tarefas_nao_mudam(self):
        pastas = ['tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos', 'docs/pedagogia/tarefas-individuais']
        r = subprocess.run(['git', 'ls-tree', '-r', '--name-only', BASE_COMMIT] + pastas + [GRELHAS], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        nomes = r.stdout.split()
        self.assertGreater(len(nomes), 100)
        na_arvore = sorted(p.relative_to(ROOT).as_posix() for pasta in pastas for p in (ROOT / pasta).rglob('*') if p.is_file())
        # Um ficheiro novo: os dados da m4-u2.
        self.assertEqual(sorted([n for n in nomes if n != GRELHAS] + [DADOS]), na_arvore)
        iguais = 0
        for rel in nomes:
            if rel in FICHEIROS:
                continue
            with self.subTest(igual_ao_main=rel):
                conteudo = (ROOT / rel).read_bytes()
                # 15/11/2026: os ficheiros que a revisão geral (revisao_geral_20261115) muda nestas pastas (a página e os dados da m5-u2)
                # comparam-se com ela desfeita pela auditoria, com contagem estrita: por baixo dela, são os do main de partida, byte a byte.
                if rel in REVISAO_DE_CIMA:
                    conteudo = undo_revisao_geral_1115(rel, conteudo.decode('utf-8')).encode('utf-8')
                    self.assertNotEqual(conteudo, (ROOT / rel).read_bytes(), rel)
                self.assertEqual(conteudo, subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True).stdout)
                iguais += 1
        self.assertEqual(iguais, len(nomes) - len([x for x in FICHEIROS if x in nomes]))
        self.assertEqual([x for x in FICHEIROS if x not in nomes and x.startswith(('tarefas/', 'docs/'))], [])

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 15/11/2026: por cima da tarefa m4-u2 fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115): a ordem ganha mais uma posição, com a mesma exigência.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: a ordem ganha mais uma posição, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('revisao_geral_20261115', 'revisao-geral-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('sintese_duas_linhas_20261115', 'sintese-duas-linhas-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[3], ('tarefa_m4u2_tema_b_20261115', 'tarefa-m4u2-tema-b-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[4], ('tarefas_faceis_m9_20261114', 'tarefas-faceis-m9-edits-20261114'))
        self.assertEqual(verificar_camadas.LAYERS[5], ('tarefas_faceis_m8_20261113', 'tarefas-faceis-m8-edits-20261113'))
        # 15/11/2026: mais uma camada, sintese_duas_linhas_20261115, no topo.
        # 15/11/2026: mais uma camada, fila_final_20261115, no topo.
        # 15/11/2026: mais uma camada, revisao_geral_20261115, no topo.
        self.assertEqual(len(verificar_camadas.LAYERS), 57)
        # 15/11/2026: mais uma camada, sintese_duas_linhas_20261115, no topo.
        # 15/11/2026: mais uma camada, revisao_geral_20261115, no topo.
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 57)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        # 15/11/2026 (revisão): mais dois ficheiros, a lição F20 e o plano da aula 11 (sai a ligação à opção «Se não foste ao teatro»).
        self.assertEqual(len(FICHEIROS), 14)
        self.assertEqual(len(set(FICHEIROS)), 14)
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        # 15/11/2026: a fila final desfaz-se primeiro (partilha o portefólio do M4).
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
                            '--desfazer-antes', REVISAOF, '--desfazer-antes', FILAF], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 14 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('15/11/2026: '), t['local'])
            self.assertEqual(t['ocorrencias'], 1)
            self.assertNotIn('—', t['local'])
        for rel, registo in MANIFESTO['files'].items():
            with self.subTest(ficheiro=rel):
                atual = ler_sem_fila(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = antes(rel)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                self.assertNotEqual(base, atual)
                de_novo = base
                for e in registo['edits']:
                    self.assertEqual(de_novo.count(e['old']), e['occurrences'], e['location'])
                    de_novo = de_novo.replace(e['old'], e['new'])
                # Ida e volta, letra a letra, até ao main.
                self.assertEqual(de_novo, atual)
                self.assertEqual(do_main(rel), base)
                self.assertEqual(undo_tarefa_m4u2_1115(rel, atual), base)
                self.assertEqual(undo_tarefa_m4u2_1115(rel, base), base)
        # Com a camada do M9, que fica por baixo, partilha os dados das grelhas; o desfazer do M9 tira primeiro esta.
        m9 = json.loads(ler(M9F))['files']
        self.assertEqual(set(MANIFESTO['files']) & set(m9), {GRELHAS})
        self.assertEqual(sha_lf(antes(GRELHAS)), m9[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(undo_tarefas_faceis_m9_1114(GRELHAS, ler(GRELHAS))), m9[GRELHAS]['base_sha256_lf'])
        # Confere-se também a camada do M9 e a do M8 com esta desfeita primeiro.
        # 15/11/2026: por cima desta camada fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        for camada, manifesto, cadeia in (('tarefas_faceis_m9_20261114', M9F, [REVISAOF, FILAF, SINTESEF, MANIFESTO_REL]), ('tarefas_faceis_m8_20261113', M8F, [REVISAOF, FILAF, SINTESEF, MANIFESTO_REL, M9F])):
            r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', f'scripts/{camada}.json', '--manifesto', manifesto, '--verificar']
                               + [x for c in cadeia for x in ('--desfazer-antes', c)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefa_m4u2_tema_b_20261115', ROOT / 'scripts/tarefa_m4u2_tema_b_20261115.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', ler(CAMADA_REL))
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(sorted(C.FICHEIROS), sorted(FICHEIROS))
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        for rel, (a, b) in finais.items():
            self.assertEqual(a, antes(rel), rel)
            self.assertEqual(b, ler_sem_fila(rel), rel)
        for nome in ('tarefas_faceis_m9_20261114', 'tarefas_faceis_m8_20261113', 'tarefas_faceis_m7_20261113', 'tarefas_faceis_m6_20261113',
                     'tarefas_faceis_m5_20261113', 'tarefas_faceis_m1_20261113', 'tarefas_faceis_m3_20261112'):
            spec = importlib.util.spec_from_file_location(nome, ROOT / f'scripts/{nome}.py')
            outra = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(outra)
            self.assertEqual(outra.construir()[0], json.loads(ler(f'scripts/{nome}.json')), nome)

    def test_leitura_historica(self):
        import tarefas_claras_historico as historico
        m3 = json.loads(ler('tests/fixtures/tarefas-faceis-m3-edits-20261112.json'))['files']
        for rel in MANIFESTO['files']:
            with self.subTest(faceis=rel):
                sem = historico.desfazer_faceis(rel, ler(rel))
                esperado = m3[GRELHAS]['base_sha256_lf'] if rel == GRELHAS else None
                if esperado:
                    self.assertEqual(sha_lf(sem), esperado)
                elif rel in json.loads(ler(M8F))['files']:
                    self.assertEqual(sha_lf(sem), json.loads(ler(M8F))['files'][rel]['base_sha256_lf'])
                else:
                    self.assertEqual(sem, antes(rel))
                self.assertEqual(historico.desfazer_faceis(rel, sem), sem)
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        self.assertLess(corpo.index('TAREFA_M4U2.get(rel)'), corpo.index('TAREFAS_FACEIS_M9.get(rel)'))

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefa_m4u2_1115(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m9_1114\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefa_m4u2_1115\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefa-m4u2-tema-b-edits-20261115.json'), sala.index('tarefas-faceis-m9-edits-20261114.json'))
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFA_M4U2.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M9.read_text'))
        for rel in ('scripts/tarefas_faceis_m3_20261112.py', 'scripts/tarefas_faceis_m1_20261113.py', 'scripts/tarefas_faceis_m5_20261113.py',
                    'scripts/tarefas_faceis_m6_20261113.py', 'scripts/tarefas_faceis_m7_20261113.py', 'scripts/tarefas_faceis_m8_20261113.py',
                    'scripts/tarefas_faceis_m9_20261114.py'):
            fonte = ler(rel)
            leitura = fonte[fonte.index('def ler(rel):'):fonte.index('def base(rel):')]
            self.assertIn("m4u2 = ROOT / 'tests/fixtures/tarefa-m4u2-tema-b-edits-20261115.json'", leitura, rel)
            if 'm9 = ROOT' in leitura:
                self.assertLess(leitura.index('m4u2 = ROOT'), leitura.index('m9 = ROOT'), rel)
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertEqual(texto.count('for(const e of [...((tarefaM4u2['), 1, rel)
            self.assertLess(texto.index('((tarefaM4u2['), texto.index('((tarefasFaceisM9['), rel)
        # Em todos os fluxos e testes: onde a camada do M9 se desfaz, esta desfaz-se logo antes, sem nada pelo meio, e é a primeira.
        fluxos = sorted((ROOT / '.github/workflows').glob('*.yml'))
        com_cadeia = 0
        for p in fluxos:
            fluxo = p.read_text('utf-8')
            self.assertEqual(fluxo.count(f'--desfazer-antes {M9F}'), fluxo.count(f'--desfazer-antes {meu} --desfazer-antes {M9F}'), p.name)
            # 15/11/2026: por cima desta camada fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
            self.assertEqual(fluxo.count(f'--desfazer-antes {meu}'), fluxo.count(f'--verificar --desfazer-antes {REVISAOF} --desfazer-antes {FILAF} --desfazer-antes {SINTESEF} --desfazer-antes {meu}'), p.name)
            self.assertEqual(fluxo.count("'scripts/tarefas_faceis_m9_20261114.*'"), fluxo.count("'scripts/tarefa_m4u2_tema_b_20261115.*'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/test_tarefas_faceis_m9.py'"), fluxo.count("- 'tests/test_tarefas_faceis_m4.py'"), p.name)
            self.assertEqual(fluxo.count("- 'tests/browser_tarefas_faceis_m9.py'"), fluxo.count("- 'tests/browser_tarefas_faceis_m4.py'"), p.name)
            com_cadeia += bool(fluxo.count(f'--desfazer-antes {meu}'))
        self.assertEqual(com_cadeia, 7)
        for p in sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_tarefas_faceis_m4.py':
                continue
            texto = p.read_text('utf-8')
            with self.subTest(teste=p.name):
                self.assertEqual(texto.count(f"'--desfazer-antes', '{M9F}'"), texto.count(f"'--desfazer-antes', '{meu}', '--desfazer-antes', '{M9F}'"))
                self.assertEqual(texto.count(f'--desfazer-antes {M9F}'), texto.count(f'--desfazer-antes {meu} --desfazer-antes {M9F}'))
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        # 15/11/2026: por cima desta camada fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m9_20261114.json --manifesto {M9F} --verificar --desfazer-antes {REVISAOF} --desfazer-antes {FILAF} --desfazer-antes {SINTESEF} --desfazer-antes {meu}\n', tarefas)
        # 15/11/2026: por cima desta camada fica «duas linhas finais» em vez de «síntese integrada» (sintese_duas_linhas_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima de «duas linhas finais» fica a fila final (fila_final_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        # 15/11/2026: por cima da fila final fica a revisão geral (revisao_geral_20261115), a camada mais recente: desfaz-se primeiro, com a mesma exigência, sem nada pelo meio.
        self.assertIn(f'python scripts/aplicar_trocas.py {CAMADA_REL} --manifesto {meu} --verificar --desfazer-antes {REVISAOF} --desfazer-antes {FILAF} --desfazer-antes {SINTESEF}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m4.py' -v\n", tarefas)
        self.assertIn('      - name: Tarefa m4-u2 mais fácil de fazer\n        run: python tests/browser_tarefas_faceis_m4.py\n', tarefas)
        self.assertLess(tarefas.index("-p 'test_tarefas_faceis_m9.py'"), tarefas.index("-p 'test_tarefas_faceis_m4.py'"))
        for caminho in ("'tarefas/m4-u2/**'", "'m4/index.html'", "'m4/guia-da-tarefa-m4/**'", "'m4/mapa-do-modulo-m4/**'",
                        "'m4/portefolio-do-modulo-m4/**'", "'tarefas/m8-u1/**'", "'m8/guia-da-tarefa-m8/**'", "'docs/pedagogia/tarefas-escolha/m4-u2.json'",
                        "'docs/pedagogia/aquecimentos/m4-u2.json'", "'scripts/tarefa_facil.py'",
                        # 15/11/2026 (revisão): os dois ficheiros novos da camada.
                        "'m4/licao-m4-f20/**'", "'m4/aulas/aula-11/**'"):
            self.assertIn(f'      - {caminho}\n', tarefas, caminho)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), 1)
        self.assertEqual(re.findall(r'timeout-minutes: \d+', tarefas), re.findall(r'timeout-minutes: \d+', do_main('.github/workflows/pt-tarefas-qa.yml')))
        trabalho = tarefas[tarefas.index('  lessons:'):]
        self.assertLess(trabalho.index('fetch-depth: 0'), trabalho.index('actions/setup-python'))
        correm = [p.name for p in fluxos if "-p 'test_tarefas_faceis_m4.py'" in p.read_text('utf-8') or re.search(r'unittest discover -s tests(?: -v)?\s*$', p.read_text('utf-8'), re.M)]
        self.assertEqual(correm, ['pt-tarefas-qa.yml'])


if __name__ == '__main__':
    unittest.main()
