"""13/11/2026: as duas tarefas do M1 (m1-u1 e m1-u2) «mais fáceis de fazer» e «tudo junto» no M1 (camada tarefas_faceis_m1_20261113).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201). Esta camada leva-o ao M1, e este
ficheiro exige das duas tarefas do M1 o que tests/test_tarefas_faceis_m3.py exige das do M3:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, as passagens, as expressões e os
  capítulos que o enunciado de antes citava, cada pedido do enunciado de antes (com as mesmas palavras), o dossiê e a pergunta
  opcional, e os critérios, níveis, exemplos e pontos da grelha, iguais aos de antes da camada (a base do manifesto, o main 2b343fbe);
* os textos para análise são os das lições do M1, letra a letra: as três cantigas inteiras (versos, estrofes, vocabulário e linha de
  fonte) e os três passos de Fernão Lopes, parágrafo a parágrafo, feitos só de pedaços que as lições publicam (os cartões «O texto» e
  os seus «Ler mais»); a página mostra-os inteiros e pela ordem, junto da pergunta ou dos temas que os usam; as duas imagens são as
  das lições (o mesmo ficheiro e o mesmo texto alternativo), com o crédito completo atrás do «i»;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia), nenhum «5 min» nem «60 min» antigos nas
  páginas do M1 ligadas à tarefa; «com consulta» dito uma vez, no primeiro cartão; os versos citados ou copiados não contam; a
  autoavaliação da grelha não se entrega (enunciado, grelha e correção); o aquecimento com uma só ligação; no máximo 10 perguntas de
  sim ou não na verificação; as mesmas palavras no enunciado, na grelha, na correção, no aquecimento, no guia, no índice e no mapa;
* no guia da tarefa do M1 não há «Autoavaliação» para copiar para o Teams nem «par de trabalho» (nunca houve: fixa-se), e o resto
  do guia é o do main de partida, letra a letra, salvo as três trocas da camada;
* no portefólio do módulo M1 (decisão do docente de 13/11/2026) não há «trabalho de equipa» nem autoavaliação de 0 a 20 por
  parâmetro (esta nunca houve: fixa-se), sem nada no lugar; o resto da página é o do main de partida, letra a letra;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases, «Que + nome» ou «Qual das…», referências que
  não se partem, títulos de obras em itálico, exemplos com outro caso (nunca as passagens reservadas da tarefa);
* o contrato da página, que substitui o de tests/test_task_choice.py nestas duas tarefas: seis cartões com nome, dois temas, uma
  pergunta opcional com três opções, os dois relógios, os factos do dossiê com fonte e ligação que existe, as citações e os
  números de cada facto na lição para onde aponta, os nomes das secções tal como estão nas lições ligadas;
* as tarefas, grelhas, correções e aquecimentos dos outros módulos, e os aquecimentos do M1, são os do main de partida, byte a byte,
  e saem iguais dos geradores;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m1.py."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
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
from auditoria_20261028 import undo_tarefas_faceis_m1_1113, undo_tarefas_faceis_m3_1112, undo_tarefas_faceis_m5_1113  # noqa: E402
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefas_faceis_m1_20261113.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'
M3F = 'tests/fixtures/tarefas-faceis-m3-edits-20261112.json'
# 13/11/2026: por cima desta camada ficam as duas tarefas do M5 mais fáceis de fazer, com dois acertos do M3 (tarefas_faceis_m5_20261113,
# o mesmo molde), que se desfazem primeiro em todas as cadeias e partilham com ela um ficheiro, os dados das grelhas.
M5 = 'tests/fixtures/tarefas-faceis-m5-edits-20261113.json'
M5_FICHEIROS = json.loads((ROOT / M5).read_text('utf-8'))['files']
BASE_COMMIT = '2b343fbe53a1cd2155baf4039041fa806fd99312'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
TROCAS = json.loads((ROOT / CAMADA_REL).read_text('utf-8'))
SLUGS = ('m1-u1', 'm1-u2')
N = '\xa0'
DADOS_TAREFAS = [f'docs/pedagogia/tarefas-escolha/{s}.json' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
PAGINAS = [f'tarefas/{s}/{p}index.html' for s in SLUGS for p in ('', 'grelha/', 'correcao/')]
AQUECIMENTOS = [f'tarefas/{s}/aquecimento/index.html' for s in SLUGS]
GUIA, INDICE, MAPA = 'm1/guia-da-tarefa-m1/index.html', 'm1/index.html', 'm1/mapa-do-modulo-m1/index.html'
PORTEFOLIO = 'm1/portefolio-do-modulo-m1/index.html'
FICHEIROS = DADOS_TAREFAS + [GRELHAS] + PAGINAS + [GUIA, INDICE, PORTEFOLIO]
# As outras onze tarefas que saem de scripts/tarefas_escolha.py (as duas do M3 já estão no molde, pela sua camada).
OUTRAS = ('m3-u1', 'm3-u2', 'm5-u1', 'm5-u2', 'm6-u1', 'm6-u2', 'm7-u3', 'm8-u1', 'm8-u2', 'm9-u1', 'm9-u2')
CARTOES_NOMES = ['Começar', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Fechar e entregar', 'Rever a matéria']
F04, F06, F07, F19, F20 = (f'm1/licao-m1-f{n}/index.html' for n in ('04', '06', '07', '19', '20'))
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = {
    'm1-u1': ['quem fala', 'a quem', 'uma repetição', 'prolonga a espera', 'o som que cai', 'o nome do processo',
              'quem cumpre a promessa de louvar', 'uma passagem', 'fora da primeira estrofe', 'Na cantiga que não cumpre a promessa, identifica o recurso expressivo',
              'como funciona', 'duas estrofes', 'três versos', 'paralelismo', 'um refrão que rep', 'a promessa não se cumpre',
              'Cita um verso de Codax', 'o que imitaste', 'uma diferença entre a espera que inventaste e a da cantiga',
              'Uma aplicação promete «Chega já», mas adia a entrega.', 'Imagina um cartaz para um concerto de «Ondas do mar de Vigo».',
              'Entregas a proposta escrita do cartaz.', 'a imagem em duas frases', 'dois factos do', 'um verso para o cartaz',
              'Indica o que o cartaz não pode prometer a quem vai ouvir.'],
    'm1-u2': ['Como mostra Fernão Lopes a cidade a agir em conjunto, depois do grito do pajem?', 'uma passagem', 'o que ela faz ver',
              'Um rascunho inventado atribui ao pajem esta fala documentada: «Matam o Mestre! Vamos pra rua!».', 'o que não aparece no',
              'o som que cai', 'no relato, numa fala documentada ou numa fala imaginada', 'Conta um destes momentos:',
              'o grito do pajem (cap. XII', 'o sino da quadrilha (cap. CXVI', 'a fome do cerco (cap. CXLVIII', 'uma gradação criada por ti',
              'uma passagem copiada exatamente do capítulo escolhido', 'Como segunda fonte, usa uma', 'a fonte do teu plano da aula 13',
              'Conta o dia do grito ou o cerco.', 'Podes começar num lugar de hoje que tenhas observado.',
              'o que cada uma mostra ou deixa de fora', 'o que a imagem escolhe destacar', 'dois factos do', 'dentro da ação',
              'um pormenor', 'a população a agir', 'uma fala identificada como «documentada» ou «imaginada»',
              'as tuas inferências e opiniões', 'duas fontes', 'no fim', 'Risca uma frase sem a apagar e escreve uma versão melhor.'],
}
# De onde vem cada parágrafo dos textos em prosa da m1-u2: (lição, número do cartão, 'cartao' ou 'mais'), um por pedaço.
PROSA = {
    'texto-1': [[(F06, 4, 'cartao'), (F20, 2, 'mais')], [(F06, 4, 'mais')], [(F06, 8, 'cartao'), (F06, 8, 'mais')], [(F06, 8, 'cartao')]],
    'texto-2': [[(F07, 2, 'cartao'), (F07, 2, 'mais')], [(F07, 2, 'cartao'), (F07, 2, 'mais'), (F07, 2, 'cartao')]],
    'texto-3': [[(F07, 5, 'cartao'), (F07, 5, 'mais')], [(F07, 10, 'cartao')], [(F07, 10, 'cartao')]],
}
PALAVRAS_PROSA = {'texto-1': 284, 'texto-2': 131, 'texto-3': 155}
# Os cartões de onde pode vir o vocabulário de cada texto.
VOCABULARIO = {
    'm1-u1': {'texto-1': [(F19, 2)], 'texto-2': [(F04, 5), (F19, 7)], 'texto-3': [(F04, 10), (F19, 7)]},
    'm1-u2': {'texto-1': [(F06, 4), (F06, 8), (F20, 2)], 'texto-2': [(F07, 2), (F06, 8), (F20, 7)],
              'texto-3': [(F07, 5), (F07, 10), (F20, 7), (F06, 8)]},
}


def ler(rel):
    texto = (ROOT / rel).read_bytes().decode('utf-8')
    # 13/11/2026: os dados das grelhas levam agora por cima a camada das tarefas do M5 (duas chaves novas nas grelhas do M5). Este
    # teste lê-os como a camada do M1 os deixou: com a do M5 desfeita pela auditoria, com contagem estrita. Nos outros onze ficheiros
    # a árvore é o «after» desta camada, como antes.
    if rel == GRELHAS:
        texto = undo_tarefas_faceis_m5_1113(rel, texto)
    return texto


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def antes(rel):
    """O ficheiro como estava por baixo desta camada (desfeita pelo manifesto, com contagem estrita): o main de partida."""
    texto = ler(rel)
    for e in reversed(MANIFESTO['files'].get(rel, {}).get('edits', [])):
        assert texto.count(e['new']) == e['occurrences'], (rel, e['location'])
        texto = texto.replace(e['new'], e['old'])
    return texto


def do_main(rel):
    """O ficheiro no commit de partida, ou None num clone raso que não o tenha."""
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    return r.stdout.decode('utf-8') if r.returncode == 0 else None


def visivel(fonte, so_main=True, sem_nav=True):
    """O texto que se lê numa página: sem scripts, estilos nem etiquetas, com os espaços normais juntos (U+00A0 fica)."""
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


def cartoes(rel):
    """Os cartões de uma lição (CARTOES=[…], numa só linha do ficheiro)."""
    fonte = ler(rel)
    i = fonte.index('CARTOES=[')
    return json.JSONDecoder().raw_decode(fonte[i + 8:])[0]


def versos_do_cartao(c):
    """As estrofes de um cartão «O texto» em verso, tal como lá estão (uma linha «[…]» fica de fora e separa estrofes)."""
    v = re.search(r'<p class="v">(.*?)</p>', c['html'], re.S).group(1)
    linhas = [(int(m.group(1)), html.unescape(re.sub(r'<[^>]+>', '', m.group(2))))
              for m in re.finditer(r'<span class="ln" data-l="\d+-(\d+)"><span class="n">\d*</span>(.*?)</span>(?=\n|$)', v, re.S)]
    estrofes, anterior = [], None
    for i, t in linhas:
        if not estrofes or i != anterior + 1:
            estrofes.append([])
        estrofes[-1].append(t)
        anterior = i
    return estrofes


def mais_do_cartao(c):
    return re.search(r'<details class="mais">(.*)</details>', c['html'], re.S).group(1)


def vocabulario_do_cartao(c):
    """Os pares (palavra, sentido) que um cartão dá: a lista «Vocabulário» e os que vêm em itálico em «Ler mais»."""
    pares = []
    g = re.search(r'<p class="gl">(.*?)</p>', c['html'], re.S)
    if g:
        pares += [re.fullmatch(r'<b>(.*)</b>, (.*?)', item, re.S).groups() for item in g.group(1).split('; ')]
    if '<details class="mais">' in c['html']:
        pares += [(a[0].lower() + a[1:], b) for a, b in re.findall(r'<i>([^<]+)</i>, ([^;.<]+(?:, [^;.<]+)*)[;.]', mais_do_cartao(c))]
    return [list(x) for x in pares]


def fonte_do_cartao(c):
    return re.search(r'<p class="fonte">(.*?)</p>', c['html'], re.S).group(1)


def plano_do_cartao(c, onde):
    """O texto de um cartão (ou do seu «Ler mais»), sem marcas, com as aspas curvas de dentro das citações como «»."""
    h = mais_do_cartao(c) if onde == 'mais' else c['html'].split('<details class="mais">')[0]
    return html.unescape(re.sub(r'<[^>]+>', '', h)).replace('“', '«').replace('”', '»')


def palavras(texto):
    return re.findall(r"[0-9A-Za-zÀ-ÿ]+(?:[-'][0-9A-Za-zÀ-ÿ]+)*", texto)


class Pagina(HTMLParser):
    """A estrutura de uma página de tarefa: os filhos de <main>, os temas, as perguntas com opções e as ligações."""

    def __init__(self, fonte):
        super().__init__()
        self.pilha, self.raiz, self.ids, self.ligacoes, self.temas, self.perguntas, self.opcoes = [], [], [], [], [], [], []
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.pilha and self.pilha[-1][0] == 'main':
            self.raiz.append((tag, a.get('id'), a.get('data-task-card-name')))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            self.ligacoes.append(a.get('href', ''))
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


def plana(rel):
    """Texto de uma página do sítio, sem marcas nem entidades, com os espaços juntos (como tests/test_task_choice.py)."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler(rel))))


def todos_os_textos(f):
    return ([i for p in f['perguntas'] for i in p['textos']] + [i for t in f['temas'] for i in t['material'].get('textos', [])]
            + f.get('temas_material', {}).get('textos', []))


def todos_os_exemplos(f):
    return ([x for p in f['perguntas'] for x in p['exemplos']] + [x for t in f['temas'] for x in t['material'].get('exemplos', [])]
            + f.get('temas_comum', {}).get('exemplos', []))


class TarefasFaceisM1(unittest.TestCase):
    maxDiff = None

    # ---------- a tarefa pede o mesmo ----------

    def test_a_tarefa_pede_o_mesmo(self):
        for slug in SLUGS:
            rel = f'docs/pedagogia/tarefas-escolha/{slug}.json'
            d, a = json.loads(ler(rel)), json.loads(antes(rel))
            f = d['facil']
            with self.subTest(tarefa=slug):
                # As chaves de antes ficam todas, iguais: a camada só acrescenta «facil».
                self.assertNotIn('facil', a)
                self.assertEqual({k: v for k, v in d.items() if k != 'facil'}, a)
                self.assertEqual(list(d)[-1], 'facil')
                # O título, os títulos das duas perguntas, as letras e os nomes dos dois temas.
                self.assertEqual([solto(p['titulo']) for p in f['perguntas']],
                                 [solto(re.match(r'<strong>(.*?)</strong>', n).group(1)) for n in a['nucleo']])
                self.assertEqual([(t['letra'], t['nome']) for t in f['temas']], [(t['letra'], t['nome']) for t in a['temas']])
                self.assertEqual(len(f['perguntas']), 2)
                # Os números: os do «lead» de antes, no quadro, junto de cada parte e na verificação.
                lead, quadro = solto(a['lead']), f['quadro']['linhas']
                if slug == 'm1-u1':
                    self.assertIn('<strong>200 a 240 palavras no total</strong>', lead)
                    self.assertIn('cerca de 60 por resposta e 80 a 120 no tema escolhido', lead)
                    self.assertEqual([solto(l[2]) for l in quadro[2:5]], ['orientação: cerca de 60', 'orientação: cerca de 60', 'orientação: 80 a 120'])
                    self.assertEqual(solto(quadro[-1][2]), '200 a 240')
                    self.assertEqual([solto(p['meta']) for p in f['perguntas']], ['Orientação: cerca de 60 palavras.'] * 2)
                    self.assertEqual(solto(f['temas_nota']), 'Orientação: 80 a 120 palavras.')
                    self.assertIn('Tenho 200 a 240 palavras?', [solto(x) for x in f['verificar']])
                else:
                    self.assertIn('cerca de <strong>40 palavras por resposta</strong>', lead)
                    self.assertIn('Crónica: título e <strong>160 a 200 palavras</strong>', lead)
                    self.assertIn('As respostas, as fontes e as duas linhas finais ficam fora dessa contagem.', lead)
                    self.assertEqual([solto(l[2]) for l in quadro[2:5]], ['cerca de 40', 'cerca de 40', 'crónica: título e 160 a 200'])
                    self.assertEqual(quadro[-1][2], '')
                    self.assertEqual([solto(p['meta']) for p in f['perguntas']], ['Cerca de 40 palavras.'] * 2)
                    self.assertEqual(solto(f['temas_nota']), 'Crónica: título e 160 a 200 palavras.')
                    self.assertIn('A crónica tem título e 160 a 200 palavras?', [solto(x) for x in f['verificar']])
                # Tudo o que o enunciado de antes citava entre «» ou localizava por capítulo continua pedido.
                pedido = solto(sem_marcas(json.dumps([f['perguntas'], f['temas'], f.get('temas_comum'), f['finais']], ensure_ascii=False)))
                velho = solto(sem_marcas(' '.join(a['nucleo'] + [t['texto'] for t in a['temas']] + a['clareza'].get('incluir', []))))
                for citado in re.findall(r'«([^»]+)»', velho):
                    self.assertIn(f'«{citado}»', pedido, citado)
                for ref in re.findall(r'cap(?:ítulo|\.) [IVXLC]+', velho):
                    self.assertIn(ref, pedido, ref)
                # Cada pedido do enunciado de antes, com as mesmas palavras.
                self.assertGreaterEqual(len(PEDIDOS[slug]), 26)
                for pedaco in PEDIDOS[slug]:
                    self.assertIn(pedaco, velho, pedaco)
                    self.assertIn(pedaco, pedido, pedaco)
                # A pergunta das duas linhas finais é a de antes.
                pergunta = re.search(r'(?:palavras|fontes): (.*?\?)', a['fecho']).group(1)
                self.assertIn(pergunta[0].upper() + pergunta[1:], re.sub(r'^Responde: (.)', lambda m: m.group(1).upper(), f['finais']['passos'][0]))
                self.assertEqual(f['finais']['passos'][1], a['fecho'].split('? ')[1])
                # O dossiê e a pergunta opcional são os de antes (a página lê-os das chaves antigas).
                self.assertEqual(d['dossie'], a['dossie'])
                self.assertEqual(d['opcional'], a['opcional'])

    def test_criterios_da_grelha_iguais(self):
        agora, base = json.loads(ler(GRELHAS))['tarefas'], json.loads(antes(GRELHAS))['tarefas']
        self.assertEqual(list(agora), list(base))
        for slug, t in agora.items():
            with self.subTest(grelha=slug):
                novas = {'autoavaliacao_so_tua', 'trocas_aluno'} if slug in SLUGS else set()
                self.assertEqual(set(t) - set(base[slug]), novas)
                self.assertEqual({k: v for k, v in t.items() if k not in novas}, base[slug])
                self.assertEqual(sum(c['max'] for c in t['criterios']), 20)
        for slug in SLUGS:
            t = agora[slug]
            self.assertIs(t['autoavaliacao_so_tua'], True)
            # As trocas são só as palavras que o enunciado novo trocou; cada uma ocorre nos textos da grelha.
            antigos = [a for a, _ in t['trocas_aluno']]
            fonte = json.dumps({k: v for k, v in t.items() if k != 'trocas_aluno'}, ensure_ascii=False)
            for a in antigos:
                self.assertIn(a, fonte)
            grelha = visivel(ler(f'tarefas/{slug}/grelha/index.html'), so_main=False, sem_nav=False)
            self.assertNotRegex(grelha, r'[Ff]echo')
            self.assertNotRegex(visivel(ler(f'tarefas/{slug}/index.html')), r'[Ff]echo')
        # Na m1-u1, as mesmas oito trocas das grelhas do M3 (a m3-u2 tem a mesma frase sobre o que não conta).
        self.assertEqual(agora['m1-u1']['trocas_aluno'], agora['m3-u2']['trocas_aluno'])
        self.assertEqual(len(agora['m1-u1']['trocas_aluno']), 8)
        grelha = visivel(ler('tarefas/m1-u1/grelha/index.html'), so_main=False, sem_nav=False)
        self.assertEqual(grelha.count('Duas linhas finais: '), 2)
        self.assertEqual(grelha.count('Duas linhas finais genéricas, sem verso.'), 1)
        # Na m1-u2, a grelha dizia «Núcleo 1», «Núcleo 2», «o fecho» e «nos excertos»: são dez trocas, estas, exatas.
        # 13/11/2026: mais três pares, «no excerto» em vez de «nos excertos» (o enunciado novo tem um só excerto, o Texto 1).
        self.assertEqual(agora['m1-u2']['trocas_aluno'], [
            [f'Núcleo comum (duas respostas de cerca de 40{N}palavras) e uma crónica à escolha', f'Duas perguntas (duas respostas de cerca de 40{N}palavras) e uma crónica à escolha'],
            ['O núcleo, as fontes e o fecho ficam fora da contagem', 'As respostas, as fontes e as duas linhas finais ficam fora da contagem'],
            ['Núcleo 1: ', f'Pergunta{N}1: '], ['Núcleo 2: ', f'Pergunta{N}2: '],
            ['não está nos excertos, não nomeias', 'não está no excerto, não nomeias'], ['nos excertos do cap.', 'no excerto do cap.'],
            ['Dizer o que está nos excertos sem os confrontar com a fala.', 'Dizer o que está no excerto sem o confrontar com a fala.'],
            ['Contar o núcleo, as fontes ou o fecho nas', 'Contar as respostas, as fontes ou as duas linhas finais nas'],
            ['e o fecho de duas linhas.', 'e as duas linhas finais.'],
            ['Entregar sem o fecho de duas linhas.', 'Entregar sem as duas linhas finais.']])

    # ---------- os textos são os das lições, letra a letra ----------

    def test_textos_em_verso_letra_a_letra_das_licoes(self):
        f = json.loads(ler(DADOS_TAREFAS[0]))['facil']
        pagina = ler(ENUNCIADOS[0])
        f19, f04 = cartoes(F19), cartoes(F04)
        codax, dinis, guilhade = f19[1], f04[4], f04[9]
        self.assertEqual([(c['rot'], solto(c['titulo'])) for c in (codax, dinis, guilhade)],
                         [('O texto', 'A. Martim Codax, «Ondas do mar de Vigo»'), ('O texto', "A: D. Dinis, «Quer'eu em maneira de proençal»"),
                          ('O texto', 'B: João Garcia de Guilhade, «Ai dona fea, fostes-vos queixar»')])
        # D. Dinis: as estrofes 1 e 3 estão no cartão, com «[…]» no meio; a estrofe 2 está em «Ler mais», verso a verso.
        e13 = versos_do_cartao(dinis)
        self.assertEqual([len(e) for e in e13], [7, 7])
        segunda = re.search(r'<p>No lugar de \[…\], a estrofe 2:</p><p class="v">(.*?)</p>', mais_do_cartao(dinis), re.S).group(1)
        e2 = [html.unescape(v) for v in segunda.split('<br>')]
        das_licoes = {'texto-1': versos_do_cartao(codax), 'texto-2': [e13[0], e2, e13[1]], 'texto-3': versos_do_cartao(guilhade)}
        self.assertEqual([len(e) for e in das_licoes['texto-1']], [3, 3, 3, 3])
        self.assertEqual([len(e) for e in das_licoes['texto-2']], [7, 7, 7])
        self.assertEqual([len(e) for e in das_licoes['texto-3']], [6, 6, 6])
        # As linhas de fonte: a de Codax e a de Guilhade são as das lições; a de D. Dinis é a da lição até aos dois pontos e, daí em
        # diante (a lição diz «estrofes 1 e 3»; aqui a cantiga está inteira), as duas frases que as lições usam nas outras duas.
        fontes = {'texto-1': fonte_do_cartao(codax), 'texto-3': fonte_do_cartao(guilhade)}
        cabeca, cauda = fonte_do_cartao(dinis).split(': ', 1)
        self.assertEqual(cauda, 'estrofes 1 e 3, sem refrão; a estrofe 2 está em «Ler mais».')
        self.assertTrue(fontes['texto-1'].endswith(': a cantiga inteira, com a grafia da edição.'))
        self.assertTrue(fontes['texto-3'].endswith(' Entre parênteses retos, letras acrescentadas pelos editores.'))
        self.assertIn(' Entre parênteses retos, letras acrescentadas pelos editores.', mais_do_cartao(dinis))
        fontes['texto-2'] = cabeca + ': a cantiga inteira, com a grafia da edição. Entre parênteses retos, letras acrescentadas pelos editores.'
        # 13/11/2026 (revisão): a fonte do Texto 3 diz, como as dos Textos 1 e 2, a época do autor e que a cantiga está inteira, na
        # grafia da edição. O resto é a linha da lição, letra a letra; «séc. XIII» é o que a lição F04 diz de Guilhade no subtítulo
        # («D. Dinis e João Garcia de Guilhade, séc. XIII»); «a cantiga inteira, com a grafia da edição» é a frase da lição F19.
        self.assertIn('João Garcia de Guilhade, séc. XIII', solto(ler('m1/licao-m1-f04/index.html')))
        nome, resto = 'João Garcia de Guilhade', ', «Ai dona fea, fostes-vos queixar», cantiga 1520, '
        cauda3 = '. Entre parênteses retos, letras acrescentadas pelos editores.'
        self.assertTrue(fontes['texto-3'].startswith(nome + resto) and fontes['texto-3'].endswith('(FCSH/NOVA)' + cauda3))
        self.assertTrue(fontes['texto-1'].startswith(f'Martim Codax (séc.{N}XIII), '))
        fontes['texto-3'] = (nome + f' (séc.{N}XIII)' + fontes['texto-3'][len(nome):-len(cauda3)]
                             + ': a cantiga inteira, com a grafia da edição' + cauda3)
        self.assertEqual([t['id'] for t in f['textos']], ['texto-1', 'texto-2', 'texto-3'])
        self.assertEqual([t['titulo'] for t in f['textos']], ['«Ondas do mar de Vigo», de Martim Codax', f"«Quer'eu em maneira de proençal», de D.{N}Dinis",
                                                           '«Ai dona fea, fostes-vos queixar», de João Garcia de Guilhade'])
        origens = {'texto-1': r'm1/licao-m1-f19/index\.html, linha \d+, cartão 2 \(copiado letra a letra\)',
                   'texto-2': r'm1/licao-m1-f04/index\.html, linha \d+, cartão 5, com a estrofe 2 de «Ler mais» \(copiado letra a letra\); m1/licao-m1-f19/index\.html, linha \d+, cartão 7 \(duas palavras do vocabulário\)',
                   'texto-3': r'm1/licao-m1-f04/index\.html, linha \d+, cartão 10 \(copiado letra a letra\); m1/licao-m1-f19/index\.html, linha \d+, cartão 7 \(duas palavras do vocabulário\)'}
        for t in f['textos']:
            estrofes = das_licoes[t['id']]
            n_versos = sum(len(e) for e in estrofes)
            with self.subTest(texto=t['id']):
                self.assertRegex(t['origem'], '^' + origens[t['id']] + '$')
                # Os versos, estrofe a estrofe; cada estrofe leva o seu número («Estrofe 1»…), porque a pergunta 2 fala da primeira.
                self.assertEqual([e['versos'] for e in t['estrofes']], estrofes)
                self.assertEqual([e['rotulo'] for e in t['estrofes']], [f'Estrofe{N}{k}' for k in range(1, len(estrofes) + 1)])
                # O vocabulário: só pares que as lições dão, nos cartões de onde o texto vem.
                dados = [par for rel, k in VOCABULARIO['m1-u1'][t['id']] for par in vocabulario_do_cartao(cartoes(rel)[k - 1])]
                for par in t['glossario']:
                    self.assertIn(par, dados, par)
                self.assertEqual(len({p for p, _ in t['glossario']}), len(t['glossario']))
                if t['id'] == 'texto-1':
                    self.assertEqual(t['glossario'], vocabulario_do_cartao(codax))
                # Todas as palavras que os cartões do próprio texto explicam estão no vocabulário.
                rel, k = VOCABULARIO['m1-u1'][t['id']][0]
                for palavra, _ in vocabulario_do_cartao(cartoes(rel)[k - 1]):
                    self.assertIn(palavra, [p for p, _ in t['glossario']], palavra)
                self.assertEqual(solto(t['fonte']), solto(fontes[t['id']]))
                # 13/11/2026 (revisão): a referência ao século não se parte (U+00A0), nas duas fontes que a trazem.
                if t['id'] in ('texto-1', 'texto-3'):
                    self.assertIn(f'(séc.{N}XIII)', t['fonte'])
                # Na página, o texto está inteiro e contínuo, pela ordem, com os versos numerados de 5 em 5 (só versos contam).
                bloco = re.search(r'<section class="tt-texto[^"]*" id="' + t['id'] + r'".*?</section>', pagina, re.S).group(0)
                versos = [html.unescape(v) for v in re.findall(r'<span class="tt-l">(.*?)</span></span>', bloco)]
                self.assertEqual(versos, [v for e in estrofes for v in e])
                self.assertEqual(re.findall(r'<span class="tt-n">(\d*)</span>', bloco), [str(k) if k % 5 == 0 else '' for k in range(1, n_versos + 1)])
                self.assertEqual(bloco.count('<p class="tt-estrofe">'), len(estrofes))
                self.assertNotIn('[…]', bloco)
                for palavra, sentido in t['glossario']:
                    self.assertIn(f'<li><b>{palavra}</b>: {sentido}</li>', bloco)
                self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)
                self.assertEqual(pagina.count(f'id="{t["id"]}"'), 1)
        self.assertEqual(sum(len(e) for es in das_licoes.values() for e in es), 51)
        self.assertEqual(pagina.count('<span class="tt-l">'), 51)
        # A barra marca, nos Textos 2 e 3, os versos fora da primeira estrofe, os que a pergunta 2 deixa citar.
        self.assertEqual([t.get('escolher') for t in f['textos']], [None, {'de': 8, 'ate': 21}, {'de': 7, 'ate': 18}])
        self.assertEqual(pagina.count('<span class="tt-v tt-esc">'), 14 + 12)
        for k, primeiro in ((2, 'Ca mia senhor quiso Deus fazer tal,'), (3, 'Dona fea, se Deus mi perdom,')):
            bloco = re.search(rf'<section class="tt-texto[^"]*" id="texto-{k}".*?</section>', pagina, re.S).group(0)
            self.assertEqual(html.unescape(re.search(r'<span class="tt-v tt-esc"><span class="tt-n">\d*</span><span class="tt-l">(.*?)</span>', bloco).group(1)), primeiro)
        # Cada texto fica no cartão da pergunta que o usa, uma só vez; nenhum texto ficou remetido para o manual.
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1'], ['texto-2', 'texto-3']])
        self.assertEqual(sorted(todos_os_textos(f)), ['texto-1', 'texto-2', 'texto-3'])
        self.assertNotRegex(visivel(pagina), r'(?i)\bmanual\b|Onde está o texto')
        self.assertNotIn('class="tt-onde"', pagina)

    def test_textos_em_prosa_letra_a_letra_das_licoes(self):
        f = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        pagina = ler(ENUNCIADOS[1])
        lidas = {rel: cartoes(rel) for rel in (F06, F07, F20)}
        self.assertEqual([t['id'] for t in f['textos']], list(PROSA))
        self.assertEqual([solto(sem_marcas(t['titulo'])) for t in f['textos']], [
            'Crónica de D. João I, capítulo XII (o grito do pajem), de Fernão Lopes',
            'Crónica de D. João I, capítulo CXVI (as torres e o sino da quadrilha), de Fernão Lopes',
            'Crónica de D. João I, capítulo CXLVIII (a fome do cerco), de Fernão Lopes'])
        fontes = {'texto-1': fonte_do_cartao(lidas[F06][3]), 'texto-2': fonte_do_cartao(lidas[F07][1]), 'texto-3': fonte_do_cartao(lidas[F07][9])}
        self.assertEqual(fontes['texto-1'], fonte_do_cartao(lidas[F06][7]))
        for t in f['textos']:
            with self.subTest(texto=t['id']):
                self.assertNotIn('estrofes', t)
                self.assertEqual([x['n'] for x in t['paragrafos']], [f'[{k}]' for k in range(1, len(PROSA[t['id']]) + 1)])
                for x, origens in zip(t['paragrafos'], PROSA[t['id']]):
                    # O parágrafo é feito só destes pedaços, pela ordem, juntos com um espaço ou com vírgula e espaço…
                    self.assertEqual(len(x['partes']), len(origens), x['n'])
                    resto = x['t']
                    for parte in x['partes']:
                        self.assertTrue(resto.startswith(parte) or resto[:2] == ', ' and resto[2:].startswith(parte) or resto[:1] == ' ' and resto[1:].startswith(parte), (x['n'], parte[:40]))
                        resto = resto[resto.index(parte) + len(parte):]
                    self.assertEqual(resto, '', x['n'])
                    # … e cada pedaço está, letra a letra, no cartão da lição (ou no seu «Ler mais») de onde vem.
                    for parte, (rel, k, onde) in zip(x['partes'], origens):
                        c = lidas[rel][k - 1]
                        self.assertEqual(c['rot'], 'O texto', (rel, k))
                        self.assertEqual(plano_do_cartao(c, onde).count(parte), 1, (x['n'], rel, k, onde, parte[:50]))
                        self.assertGreater(len(palavras(parte)), 8, parte)
                    self.assertNotRegex(x['t'], r'[“”"<>]')
                # Contínuo: nenhum corte no meio. Só o Texto 1 e o Texto 2 acabam em «[…]», onde a frase continua no capítulo (as
                # lições não dão a continuação), e a linha de fonte di-lo.
                junto = ' '.join(x['t'] for x in t['paragrafos'])
                self.assertEqual(len(palavras(junto)), PALAVRAS_PROSA[t['id']])
                if t['id'] == 'texto-3':
                    self.assertNotIn('[…]', junto)
                    self.assertTrue(junto.endswith('nas praças, e em outros lugares.'))
                    self.assertEqual(t['fonte'], fontes[t['id']])
                else:
                    self.assertEqual(junto.count('[…]'), 1)
                    self.assertTrue(junto.endswith(' […].'), junto[-30:])
                    self.assertTrue(fontes[t['id']].endswith(', grafia atualizada; cortes marcados com […].'))
                    self.assertEqual(t['fonte'], fontes[t['id']].replace('; cortes marcados com […].', '. Depois de […], a frase continua no capítulo.'))
                # O vocabulário: só pares que as lições dão (os dois últimos casos vêm numa frase do «Ler mais» da lição F07).
                dados = [par for rel, k in VOCABULARIO['m1-u2'][t['id']] for par in vocabulario_do_cartao(lidas[rel][k - 1])]
                for par in t['glossario']:
                    if par in (['i', 'aí'], ['alféloas', 'doces de açúcar ou mel']):
                        self.assertIn('<i>I</i> é «aí»; <i>alféloas</i> são doces de açúcar ou mel', mais_do_cartao(lidas[F07][4]))
                        continue
                    self.assertIn(par, dados, par)
                    self.assertIn(par[0].split()[0].rstrip('s'), junto, par)
                self.assertEqual(len({p for p, _ in t['glossario']}), len(t['glossario']))
                # Na página, o texto está inteiro, pela ordem, com os parágrafos numerados como nas lições.
                bloco = re.search(r'<section class="tt-texto[^"]*" id="' + t['id'] + r'".*?</section>', pagina, re.S).group(0)
                self.assertEqual([(n, html.unescape(p)) for n, p in re.findall(r'<p class="tt-par"><span class="tt-pn">(\[\d\])</span> (.*?)</p>', bloco)],
                                 [(x['n'], x['t']) for x in t['paragrafos']])
                self.assertEqual(bloco.count('<div class="tt-prosa">'), 1)
                for palavra, sentido in t['glossario']:
                    self.assertIn(f'<li><b>{palavra}</b>: {sentido}</li>', bloco)
                self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)
                self.assertEqual(pagina.count(f'id="{t["id"]}"'), 1)
        # O Texto 1 (toda a turma) fica na pergunta 1; os Textos 2 e 3 servem aos dois temas e ficam no cartão dos temas.
        self.assertEqual([p['textos'] for p in f['perguntas']], [['texto-1'], []])
        self.assertEqual(f['temas_material']['textos'], ['texto-2', 'texto-3'])
        self.assertEqual(sorted(todos_os_textos(f)), ['texto-1', 'texto-2', 'texto-3'])
        self.assertEqual(pagina.count(f'<details class="tf-so-tema tf-dois-temas"><summary>Para os dois temas: os Textos{N}2{N}e{N}3 (o cerco de Lisboa)</summary>'), 1)
        dentro = pagina[pagina.index('<details class="tf-so-tema tf-dois-temas">'):]
        dentro = dentro[:dentro.index('</details>')]
        self.assertEqual(re.findall(r'<section class="tt-texto tt-curto" id="(texto-\d)"', dentro), ['texto-2', 'texto-3'])
        # As passagens que as lições citam do capítulo estão no Texto 1 (os excertos são partes dele).
        texto1 = ' '.join(x['t'] for x in f['textos'][0]['paragrafos'])
        for excerto in ('se moveram todos com mão armada', 'não cabiam pelas ruas principais', 'Matam o Mestre nos paços da rainha!'):
            self.assertIn(excerto, texto1)
        self.assertNotIn('Vamos pra rua', texto1)
        # Nenhum texto ficou remetido para o manual, e nada veio de fora das lições.
        self.assertNotRegex(visivel(pagina), r'(?i)\bmanual\b|Onde está o texto')
        self.assertNotIn('class="tt-onde"', pagina)
        self.assertNotIn('archive.org', pagina)

    def test_imagens_das_licoes_com_credito(self):
        f = json.loads(ler(DADOS_TAREFAS[1]))['facil']
        pagina = ler(ENUNCIADOS[1])
        itens = f['temas_figuras']['itens']
        self.assertEqual([(x['id'], solto(x['rotulo']), x['src'], x['de']) for x in itens], [
            ('imagem-1', 'Imagem 1', '../../img/fontes/morte-conde-andeiro.jpg', F06),
            ('imagem-2', 'Imagem 2', '../../img/fontes/cerco-lisboa-froissart.jpg', F07)])
        for x in itens:
            with self.subTest(imagem=x['id']):
                # A imagem é a da abertura da lição: o mesmo ficheiro (que existe no repositório) e o mesmo texto alternativo.
                abre = cartoes(x['de'])[0]
                self.assertEqual(abre['rot'], 'Abre')
                self.assertIn(f'<img src="{x["src"]}" alt="{x["alt"]}"', abre['html'])
                self.assertGreater(len(x['alt']), 80)
                ficheiro = (ROOT / 'tarefas/m1-u2' / x['src']).resolve()
                self.assertTrue(ficheiro.is_file() and ficheiro.read_bytes()[:3] == b'\xff\xd8\xff', x['src'])
                self.assertIn('Domínio público.', abre['html'])
                # Na página: numerada, com largura e altura, o crédito completo atrás do «i» e a legenda à vista.
                self.assertEqual(pagina.count(
                    f'<figure class="tf-fig tf-fig-n" id="{x["id"]}"><p class="tf-fig-rotulo"><span class="tt-num">{x["rotulo"]}</span> {x["nome"]}</p>'
                    f'<img src="{x["src"]}" alt="{x["alt"]}" width="{x["largura"]}" height="{x["altura"]}" loading="lazy">'
                    f'<details class="info-i info-i--linha" name="info-i"><summary aria-label="{x["credito_rotulo"]}"><span aria-hidden="true">i</span></summary>'
                    f'<p class="info-i-texto">{x["credito"]}</p></details><figcaption>{x["legenda"]}</figcaption></figure>'), 1)
                self.assertIn('Domínio público.', x['credito'])
        # Os créditos são os que o sítio já publica, com a ligação à origem.
        olhar = solto(ler('m1/olhar-andeiro/index.html'))
        self.assertIn('José de Sousa Azevedo, _Morte do Conde Andeiro_ (c. 1860), Museu Nacional de Soares dos Reis, Porto. Domínio público. Wikimedia Commons.', olhar)
        self.assertIn('"creditoUrl":"https://commons.wikimedia.org/w/index.php?curid=1539861"', olhar)
        self.assertEqual(solto(itens[0]['credito']), 'José de Sousa Azevedo, <i>Morte do Conde Andeiro</i> (c. 1860), Museu Nacional de Soares dos Reis, Porto. Domínio público. '
                         '<a href="https://commons.wikimedia.org/w/index.php?curid=1539861" rel="noopener">Wikimedia Commons</a>.')
        self.assertIn(f'<p class="info-i-texto">{itens[1]["credito"].split(" <a ")[0]}</p>', cartoes(F07)[0]['html'])
        ligacao = '<a href="https://commons.wikimedia.org/wiki/File:Siege_of_Lisbon_1384.JPG" rel="noopener">commons.wikimedia.org</a>'
        self.assertIn(ligacao.replace('"', '\\"'), ler('m1/m1-promessa-do-cronista/index.html'))
        self.assertTrue(itens[1]['credito'].endswith(' ' + ligacao))
        # Só estas duas imagens, à vista antes dos dois temas (servem aos dois); a m1-u1 não tem imagens.
        self.assertEqual(pagina.count('<figure'), 2)
        self.assertEqual(pagina.count('<img '), 2)
        self.assertNotIn('data:image', pagina)
        self.assertLess(pagina.index('id="imagens"'), pagina.index('<div class="task-themes">'))
        self.assertLess(pagina.index('<p class="tf-p tf-topo">'), pagina.index('id="imagens"'))
        self.assertNotIn('<figure', ler(ENUNCIADOS[0]))
        self.assertNotIn('<img ', ler(ENUNCIADOS[0]))
        # O dossiê descreve as mesmas duas imagens (factos 1 e 2), como antes.
        d = json.loads(ler(DADOS_TAREFAS[1]))
        self.assertIn('<i>Morte do Conde Andeiro</i>', d['dossie'][0]['facto'])
        self.assertIn('iluminura das <i>Crónicas</i> de Froissart', d['dossie'][1]['facto'])

    def test_exemplos_com_outro_caso(self):
        # Os exemplos mostram como se faz com outro caso: vêm da grelha pública e nunca usam as passagens reservadas da tarefa (a
        # lista «reservadas» do aquecimento).
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        quantos = {'m1-u1': 4, 'm1-u2': 5}
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            reservadas = json.loads(ler(f'docs/pedagogia/aquecimentos/{slug}.json'))['reservadas']
            self.assertGreater(len(reservadas), 30)
            # (dentro de uma citação «…», a grelha usa aspas curvas; na página, as falas ficam todas entre «»)
            publico = solto(json.dumps(grelhas[slug], ensure_ascii=False)).replace('“', '«').replace('”', '»')
            exemplos = todos_os_exemplos(f)
            self.assertEqual(len(exemplos), quantos[slug] + (1 if slug == 'm1-u1' else 0))
            for x in exemplos:
                self.assertNotIn('html', x)
                self.assertNotIn('de', x)
                for r in reservadas:
                    self.assertNotIn(r, solto(sem_marcas(x['titulo'])), x['titulo'])
                for p in x['paragrafos']:
                    texto = p if isinstance(p, str) else p['t']
                    with self.subTest(tarefa=slug, exemplo=texto[:50]):
                        for r in reservadas:
                            self.assertNotIn(r, solto(texto))
                        # «Passo» e «Alínea» ficam presos ao número ou à letra (U+00A0), como as outras referências.
                        if isinstance(p, dict):
                            self.assertRegex(p['al'], rf'^(?:Passos?|Alíneas?){N}')
                            self.assertNotRegex(p['al'], r'(?:Passos?|Alíneas?) |\d (?:a|e) \d|\) (?:a|e) [a-h]\)')
                        limpo = solto(re.sub(r'</?i>', '_', texto))
                        # (um exemplo da m1-u1 usa só o segundo caso da grelha, «alevantada»: sem o primeiro, «também» não faz
                        # sentido e sai; o primeiro caso, «acume», é reservado, porque é o da pergunta opcional)
                        if limpo == 'Em alevantada > levantada cai o «a» do início: aférese.':
                            limpo = 'Em alevantada > levantada cai também o «a» do início: aférese.'
                        self.assertIn(limpo, publico)
            pagina = ler(f'tarefas/{slug}/index.html')
            # Em desdobrável fechado no ecrã, que não sai em papel.
            self.assertEqual(pagina.count('<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>'), quantos[slug])
            self.assertEqual(len(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra"><summary>Ver (?:um exemplo com outro caso|dois exemplos com outros casos)</summary>', pagina)),
                             quantos[slug])
            self.assertNotRegex(pagina, r'<details[^>]*tf-so-ecra[^>]* open')
            self.assertNotRegex(pagina, r'<details[^>]* open')
        css = ler('assets/task-textos.css')
        impressao = css[css.index('@media print{'):]
        self.assertIn('[data-task-facil] .tf-so-ecra{display:none!important}', impressao)
        self.assertIn('[data-task-facil] .tt-texto{break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] :is(h2,h3,h4,summary,.tt-rotulo,.tf-meta,.tf-antes,.tf-fig){break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tf-topo{break-after:avoid}', impressao)
        self.assertIn('[data-task-facil] .tt-estrofe{margin:0 0 14px;max-width:none;break-inside:avoid}', css)
        # Em papel, nenhum parágrafo, nenhuma imagem e nenhuma lista comum aos dois temas se parte.
        self.assertIn('[data-task-facil] .tt-par{margin:0 0 4pt;break-inside:avoid}', impressao)
        self.assertIn('[data-task-facil] .tf-fig-n{margin:4pt 0 6pt;break-inside:avoid;break-after:auto}', impressao)
        self.assertIn('[data-task-facil] .tf-comum{margin:6pt 0;padding:5pt 10pt 3pt;break-inside:avoid}', impressao)

    # ---------- as decisões do docente, em todos os sítios ----------

    def test_tempos_10_10_55_15_em_todos_os_sitios(self):
        for slug in SLUGS:
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            f = d['facil']
            pagina = ler(f'tarefas/{slug}/index.html')
            with self.subTest(tarefa=slug):
                tempos = [solto(l[0]['t'] if isinstance(l[0], dict) else l[0]) for l in f['quadro']['linhas'] if l[0]]
                self.assertEqual(tempos, ['10 min', '10 min', '55 min', '15 min', '90 min'])
                self.assertEqual([solto(l[1]) for l in f['quadro']['linhas']],
                                 ['Aquecimento em cartões', 'Leitura do enunciado', 'Pergunta 1', 'Pergunta 2', 'Tema A ou B', 'Revisão e entrega', 'Total'])
                self.assertEqual(f['quadro']['linhas'][2][0], {'t': f'55{N}min', 'linhas': 3})
                self.assertEqual(f['producao_minutos'], 55)
                self.assertEqual(d['aquecer']['minutos'], 10)
                # Na página: o quadro, e os dois relógios (10 e 55 minutos).
                quadro = re.search(r'<table class="tf-quadro">.*?</table>', pagina, re.S).group(0)
                self.assertEqual(re.findall(r'<th scope="row(?:group)?"(?: rowspan="3")?>(\d+)\xa0min</th>', quadro), ['10', '10', '55', '15', '90'])
                self.assertIn(f'<th scope="rowgroup" rowspan="3">55{N}min</th><td>Pergunta{N}1</td>', quadro)
                self.assertEqual(re.findall(r'data-relogio data-max="(\d+)" data-passo="(\d)" data-rotulo="([^"]+)" data-chave="pt-relogio:tarefas/' + slug + r':(\w+)"', pagina),
                                 [('10', '1', 'Aquecimento', 'aquecimento'), ('55', '5', 'Produção em papel', 'producao')])
                self.assertEqual(pagina.count('data-relogio'), 2)
                self.assertIn(f'Faz o aquecimento (10{N}minutos).', pagina)
                self.assertIn(f'Nos 10{N}minutos de leitura, lê as duas perguntas e os passos dos dois temas.', pagina)
                self.assertIn(f'<p class="task-kicker">Tarefa individual, 90{N}minutos</p>', pagina)
        # O aquecimento diz «Dez minutos»; o guia da tarefa tem os mesmos quatro momentos, que somam 90.
        for rel in AQUECIMENTOS:
            self.assertEqual(ler(rel).count('Dez minutos com consulta.'), 1)
        guia = ler(GUIA)
        tabela = re.search(r'<p>Cada aula de 90\xa0minutos:</p><table class="apoio-tabela" role="table">(.*?)</table>', guia, re.S).group(1)
        linhas = re.findall(r'<th scope="row" role="rowheader">([^<]+)</th><td role="cell" data-label="Tempo">(\d+)\xa0minutos</td>', tabela)
        self.assertEqual(linhas, [('aquecimento em cartões, no telemóvel e com consulta', '10'), ('leitura do enunciado', '10'),
                                  ('produção com consulta', '55'), ('revisão e entrega', '15')])
        self.assertEqual(sum(int(t) for _, t in linhas), 90)
        self.assertEqual(tabela.count('<tr role="row">'), 5)
        # Nenhum «5 min» nem «60 min» antigos (nem «5 minutos», «60 minutos», «60 de produção») nas páginas do M1 ligadas à tarefa.
        for rel in PAGINAS + AQUECIMENTOS + [GUIA, INDICE, MAPA, PORTEFOLIO]:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                self.assertNotRegex(fonte, r'(?<![\d,.])(?:5|60)[ \xa0]min')
                self.assertNotRegex(fonte, r'\b60 de produção|\b5 de leitura')
                self.assertNotIn('10/5/60/15', fonte)

    def test_consulta_versos_autoavaliacao_e_aquecimento(self):
        contas = {'m1-u1': 'Não contam para as palavras: os versos citados ou copiados e as duas linhas finais.',
                  'm1-u2': 'Não contam para as palavras da crónica: as respostas, as fontes e as duas linhas finais.'}
        entregas = {'m1-u1': 'Fotografa as respostas, o texto do teu tema e as duas linhas finais.',
                    'm1-u2': 'Fotografa as respostas, a crónica com a lista das fontes e as duas linhas finais.'}
        alineas_por_pergunta = {'m1-u1': [8, 5], 'm1-u2': [3, 6]}
        for slug in SLUGS:
            pagina = ler(f'tarefas/{slug}/index.html')
            texto = visivel(pagina)
            cabeca = pagina.split('<header>', 1)[1].split('</header>', 1)[0]
            with self.subTest(tarefa=slug):
                # «Com consulta» diz-se uma vez, no primeiro cartão, e diz o que é.
                frase = 'Trabalhas à mão. O aquecimento e a tarefa são com consulta: podes usar as lições do site, o caderno e o dicionário.'
                self.assertIn(f'<p class="tf-p">{frase}</p>', cabeca)
                self.assertEqual(texto.count('com consulta'), 1)
                self.assertEqual(len(re.findall(r'\bconsulta\b', texto)), 1)
                # O que não conta para as palavras: uma vez no enunciado, por baixo do quadro, e igual na grelha do aluno. Na m1-u1,
                # os versos citados ou copiados (decisão do docente); na m1-u2, o que o enunciado de antes já deixava de fora.
                conta = contas[slug]
                self.assertIn(f'<p class="tf-nota">{conta}</p>', cabeca)
                self.assertEqual(texto.count('Não contam para as palavras'), 1)
                grelha = ler(f'tarefas/{slug}/grelha/index.html')
                if slug == 'm1-u1':
                    self.assertEqual(grelha.count(conta), 1)
                else:
                    self.assertEqual(grelha.count('As respostas, as fontes e as duas linhas finais ficam fora da contagem'), 1)
                self.assertNotIn('que não contam para as palavras', grelha)
                # A autoavaliação é só para o aluno: não se entrega (enunciado, grelha e correção).
                self.assertIn('<p class="tf-nota tf-grelha-nota">A autoavaliação da grelha é só para ti: não se entrega.</p>', cabeca)
                self.assertEqual(texto.count('autoavaliação'), 2)
                entrega = pagina[pagina.index('<h2>Entrega no Teams</h2>'):pagina.index('</section>', pagina.index('<h2>Entrega no Teams</h2>'))]
                self.assertEqual(re.findall(r'<li>(.*?)</li>', entrega), [entregas[slug], 'Confirma que as fotografias mostram o trabalho completo.',
                                                                          'Entrega as fotografias na tarefa do Teams.'])
                self.assertEqual(grelha.count('Esta autoavaliação é só para ti: não se entrega.'), 1)
                self.assertNotIn('Entrega esta autoavaliação', grelha)
                self.assertNotIn('comenta a diferença', grelha)
                correcao = ler(f'tarefas/{slug}/correcao/index.html')
                self.assertIn('<thead><tr><th>Critério</th><th class="n">Máx.</th><th class="n">Docente</th><th>Observações</th></tr></thead>', correcao)
                self.assertNotIn('Aluno</th>', correcao)
                self.assertNotIn('Diferença entre a tua nota e a minha', correcao)
                self.assertNotIn('Onde nos afastámos', correcao)
                # Cada linha da tabela de notas tem quatro células (critério, máximo, docente, observações); antes tinha cinco.
                linhas = re.findall(r'<tr(?: class="total")?>(.*?)</tr>', correcao[correcao.index('<tbody>'):correcao.index('</tbody>')])
                self.assertEqual(len(linhas), 6)
                for l in linhas:
                    self.assertEqual(len(re.findall(r'<t[dh][ >]', l)), 4, l[:80])
                for parte in ('<h2 class="g-fb-t">Comentário ao aluno</h2>', '<h3>O que funciona</h3>', '<h3>O que te custa pontos</h3>', '<h3>Próximo passo</h3>'):
                    self.assertEqual(correcao.count(parte), 1)
                # O aquecimento é o primeiro passo, com uma só ligação.
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertIn(f'<ol class="tf-fazer"><li>Faz o aquecimento (10{N}minutos).<span class="task-aquecer tf-abrir"><a href="aquecimento/">Abrir o aquecimento em cartões</a></span></li>', cabeca)
                self.assertLess(cabeca.index('href="aquecimento/"'), cabeca.index('O que entregas'))
                # A verificação final: 10 perguntas de sim ou não (o máximo), numa só lista.
                lista = re.search(r'<fieldset class="task-checklist" aria-labelledby="entregar-title">(.*?)</fieldset>', pagina, re.S).group(1)
                perguntas = re.findall(r'<label><input type="checkbox"> <span>(.*?)</span></label>', lista)
                self.assertEqual(lista.count('<label>'), len(perguntas))
                self.assertLessEqual(len(perguntas), 10)
                self.assertGreaterEqual(len(perguntas), 9)
                self.assertTrue(all(p.endswith('?') for p in perguntas), perguntas)
                self.assertEqual(pagina.count('class="task-checklist"'), 1)
                self.assertIn('<p class="tf-p" id="criterios">Responde sim ou não. Se for não, completa o teu trabalho.</p>', pagina)
                # Um pedido por alínea ou passo: cada alínea é uma frase só, curta. A pergunta 1 da m1-u2 pede três coisas (escolher,
                # citar, explicar) e tem três alíneas; as outras têm cinco ou mais, como as do M3.
                d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))['facil']
                contadas = []
                for p in d['perguntas']:
                    alineas = p.get('alineas') or [x for g in p['grupos'] for x in g['alineas']]
                    contadas.append(len(alineas))
                    for x in alineas:
                        self.assertEqual(len(re.findall(r'[.?!](?:\s|$)', re.sub(r'<[^>]+>', '', x))), 1, x)
                        self.assertLessEqual(len(x.split()), 14, x)
                self.assertEqual(contadas, alineas_por_pergunta[slug])
                # Cada passo dos temas (e cada condição de um passo) é também uma frase só, com 20 palavras no máximo.
                passos = [x for t in d['temas'] for x in t['passos']] + d.get('temas_comum', {}).get('passos', [])
                self.assertGreaterEqual(len(passos), 8)
                for x in passos:
                    for frase in ([x] if isinstance(x, str) else [x['t']] + x['sub']):
                        self.assertLessEqual(len(re.findall(r'[.?!;:](?:\s|$)', re.sub(r'<[^>]+>', '', frase))), 2, frase)
                        self.assertLessEqual(len(re.sub(r'<[^>]+>', '', frase).split()), 20, frase)

    def test_tudo_junto_as_mesmas_palavras(self):
        # O enunciado novo diz «as duas perguntas», «a letra do teu tema», «as respostas ligam-se» e «duas linhas finais»: a grelha, a
        # correção, o aquecimento, o guia, o índice e o mapa usam as mesmas palavras, e as antigas saem de todos.
        for slug in SLUGS:
            for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                rel = f'tarefas/{slug}/{parte}index.html'
                with self.subTest(pagina=rel):
                    texto = visivel(ler(rel), so_main=False, sem_nav=False)
                    for velha in ('úcleo', 'tema escolhido', 'articulad'):
                        self.assertNotIn(velha, texto)
                    self.assertNotRegex(texto, r'[Ff]echo')
                    self.assertNotRegex(texto, r'(?<!a letra d)o tema no topo')
            enunciado = visivel(ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Responde a duas perguntas.', enunciado)
            self.assertIn(f'Escreve a letra do teu tema (A{N}ou{N}B) no topo.', enunciado)
            self.assertIn(f'A letra do meu tema (A{N}ou{N}B) está no topo?', enunciado)
            self.assertIn(f'<meta name="description" content="Aula de tarefa com consulta: aquecimento, duas perguntas e um tema à escolha, em papel, durante 90{N}minutos, com entrega no Teams.">', ler(f'tarefas/{slug}/index.html'))
        # m1-u1: as mesmas palavras das grelhas do M3.
        enunciado = visivel(ler(ENUNCIADOS[0]))
        self.assertIn('As respostas ligam-se (não estão soltas)?', enunciado)
        for parte in ('grelha/', 'correcao/'):
            p = ler(f'tarefas/m1-u1/{parte}index.html')
            self.assertIn('Respostas ligadas, extensão e escrita revista', p)
            self.assertIn('a letra do teu tema está no topo', p)
        grelha = ler('tarefas/m1-u1/grelha/index.html')
        self.assertEqual(grelha.count('Respostas ligadas, extensão e escrita revista'), 3)
        self.assertIn('<p>Duas perguntas e um tema à escolha (A ou B), à mão, entre 200 e ', grelha)
        self.assertIn('a letra do tema no topo', grelha)
        self.assertIn('<li>Não escrever no topo a letra do teu tema (A ou B).</li>', grelha)
        # O enunciado diz «lugar» (e não «posição»), como a grelha e o aquecimento já diziam; e «dá-lhe o nome», como eles.
        self.assertIn('Indica o lugar desse som: início, meio ou fim da palavra.', enunciado)
        self.assertNotRegex(enunciado, r'\bposição\b')
        self.assertIn('o lugar na palavra (início, meio ou fim)', visivel(grelha, so_main=False))
        self.assertIn('diz sempre o som, o lugar e o nome', ler(AQUECIMENTOS[0]))
        self.assertIn('Os nomes das repetições: refrão, paralelismo e leixa-pren.', enunciado)
        self.assertIn('(refrão, paralelismo ou leixa-pren)', visivel(grelha, so_main=False))
        # m1-u2: «Pergunta 1» e «Pergunta 2» em vez de «Núcleo 1» e «Núcleo 2», na grelha e na correção; «as duas linhas finais».
        for parte in ('grelha/', 'correcao/'):
            p = ler(f'tarefas/m1-u2/{parte}index.html')
            self.assertIn(f'Pergunta{N}1: a cidade como uma só figura', p)
            self.assertIn(f'Pergunta{N}2: a fala, a marca e o registo', p)
        grelha = visivel(ler('tarefas/m1-u2/grelha/index.html'), so_main=False)
        self.assertIn(f'Duas perguntas (duas respostas de cerca de 40{N}palavras) e uma crónica à escolha, tema A ou B', grelha)
        self.assertIn('e as duas linhas finais.', grelha)
        self.assertIn('Entregar sem as duas linhas finais.', grelha)
        self.assertIn('Contar as respostas, as fontes ou as duas linhas finais nas', grelha)
        enunciado = visivel(ler(ENUNCIADOS[1]))
        # O enunciado usa as palavras da grelha: «onde cai», «excerto», «confronta», «identificada»/«marcada» ficam como estavam.
        self.assertIn('Indica onde cai: no início, no meio ou no fim da palavra.', enunciado)
        self.assertNotRegex(enunciado, r'\bposição\b')
        self.assertIn('o som que cai, onde cai e o nome do processo', grelha)
        self.assertIn(f'Compara essa fala com o excerto do capítulo{N}XII', enunciado)
        self.assertIn('Identifica o que não aparece no excerto.', enunciado)
        # 13/11/2026: a grelha e a versão de correção dizem «no excerto», como o enunciado (há um só, o Texto 1); «excertos» sai.
        self.assertEqual(grelha.count('não está no excerto do cap.'), 2)
        self.assertIn('Não apontas a parte da fala que não está no excerto, não nomeias o processo', grelha)
        self.assertIn('Dizer o que está no excerto sem o confrontar com a fala.', grelha)
        self.assertIn('Apontas a parte da fala que não está no excerto do cap.', visivel(ler('tarefas/m1-u2/correcao/index.html'), so_main=False))
        for parte in ('', 'grelha/', 'correcao/'):
            self.assertNotIn('excertos', visivel(ler(f'tarefas/m1-u2/{parte}index.html'), so_main=False, sem_nav=False), parte)
        self.assertIn('Confronta duas fontes.', enunciado)
        self.assertIn('Duas fontes confrontadas', grelha)
        # Os dois aquecimentos do M1 não mudaram (já usavam as mesmas palavras): não estão na camada e são os do main de partida.
        for slug in SLUGS:
            for rel in (f'tarefas/{slug}/aquecimento/index.html', f'docs/pedagogia/aquecimentos/{slug}.json'):
                self.assertNotIn(rel, MANIFESTO['files'])
                base = do_main(rel)
                if base is not None:
                    self.assertEqual(ler(rel), base, rel)
        # O guia, o índice e o mapa do M1.
        self.assertEqual(ler(GUIA).count('<p> Respondes às duas perguntas e escolhes um tema, A ou B. Os critérios são os mesmos para os dois temas.'), 1)
        self.assertEqual(ler(INDICE).count(f'a tarefa atual pede uma crónica de 160 a 200{N}palavras, além das duas perguntas.'), 1)
        for rel in (GUIA, INDICE, MAPA):
            self.assertNotIn('núcleo comum', ler(rel), rel)
            self.assertNotRegex(visivel(ler(rel), so_main=False, sem_nav=False), r'(?i)\bnúcleo\b')
        # O mapa não descreve as partes da aula de tarefa: não mudou.
        self.assertNotIn(MAPA, MANIFESTO['files'])
        base = do_main(MAPA)
        if base is not None:
            self.assertEqual(ler(MAPA), base)

    def test_guia_sem_autoavaliacao_para_o_teams_nem_par_de_trabalho(self):
        # Decisão do docente (13/11/2026, vale para os guias da tarefa): a «Autoavaliação» que se copiava para o Teams e «pergunta ao
        # teu par de trabalho» saem. O guia do M1 nunca as teve (é uma página sem o modelo de produção do guia do M3): fixa-se que
        # não as tem, nem no texto nem no código, e que nada entrou no lugar.
        guia, base = ler(GUIA), antes(GUIA)
        lido = visivel(guia, so_main=False, sem_nav=False)
        for texto in (guia, base):
            self.assertNotRegex(texto, r'(?i)auto-?avalia')
            self.assertNotRegex(texto, r'r-auto|data-auto|dataset\.auto|D\.auto|class="niveis"|aria-pressed="')
            self.assertNotRegex(texto, r'(?i)par de trabalho|antes de mim|copiar para o Teams')
        self.assertNotRegex(lido, r'(?i)\bpar(?:es)?\b|\bgrupos?\b|\bequipas?\b|\bduplas?\b|em conjunto|\bcolegas?\b')
        self.assertEqual(lido.count('Individual.'), 3)
        # O resto da página é o main de partida, letra a letra, salvo as três trocas da camada (dois tempos e «as duas perguntas»).
        edits = MANIFESTO['files'][GUIA]['edits']
        self.assertEqual(len(edits), 3)
        do_commit = do_main(GUIA)
        if do_commit is not None:
            self.assertEqual(do_commit, base)
        self.assertEqual(sha_lf(base), MANIFESTO['files'][GUIA]['base_sha256_lf'])
        de_novo = base
        for e in edits:
            self.assertEqual(de_novo.count(e['old']), 1, e['location'])
            de_novo = de_novo.replace(e['old'], e['new'])
        self.assertEqual(de_novo, guia)
        self.assertEqual(len(guia) - len(base), sum(len(e['new']) - len(e['old']) for e in edits))
        # As páginas das duas tarefas dizem o mesmo: a autoavaliação da grelha é só do aluno e não se entrega; nenhum par nem grupo.
        for slug in SLUGS:
            self.assertIn('A autoavaliação da grelha é só para ti: não se entrega.', ler(f'tarefas/{slug}/index.html'))
            self.assertIn('Esta autoavaliação é só para ti: não se entrega.', ler(f'tarefas/{slug}/grelha/index.html'))
            for parte in ('', 'grelha/', 'correcao/'):
                self.assertNotRegex(visivel(ler(f'tarefas/{slug}/{parte}index.html'), so_main=False, sem_nav=False),
                                    r'(?i)par de trabalho|trabalho de (?:grupo|pares)|em pares|com (?:o|a) (?:teu|tua) colega')

    def test_portefolio_sem_trabalho_de_equipa_nem_autoavaliacao_de_0_a_20(self):
        # Decisão do docente (13/11/2026): no portefólio do módulo saem a autoavaliação de 0 a 20 por parâmetro e «trabalho de
        # equipa», sem pôr nada no lugar. O portefólio do M1 nunca teve a autoavaliação (fixa-se); «trabalho de equipa» sai da lista.
        pagina, base = ler(PORTEFOLIO), antes(PORTEFOLIO)
        lido = visivel(pagina, so_main=False, sem_nav=False)
        self.assertEqual(base.count('trabalho de equipa'), 1)
        self.assertNotRegex(pagina, r'(?i)trabalho de equipa|\bequipas?\b|trabalho de (?:grupo|pares)|par de trabalho')
        for texto in (pagina, base):
            self.assertNotRegex(texto, r'(?i)auto-?avalia')
            self.assertNotRegex(texto, r'\b0 a 20\b(?!0)|(?<!\d)/20(?!\d)')
        self.assertEqual(lido.count('É a base da avaliação qualitativa do módulo: autonomia, responsabilidade, pensamento crítico, entre outros. '
                                    'Não tem nota própria; o que faltar pesa nos parâmetros.'), 1)
        # Nada entrou no lugar: a página é a do main de partida menos « trabalho de equipa,», letra a letra.
        edits = MANIFESTO['files'][PORTEFOLIO]['edits']
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0]['old'].replace(' trabalho de equipa,', ''), edits[0]['new'])
        self.assertEqual(base.replace(' trabalho de equipa,', ''), pagina)
        self.assertEqual(len(base) - len(pagina), len(' trabalho de equipa,'))
        do_commit = do_main(PORTEFOLIO)
        if do_commit is not None:
            self.assertEqual(do_commit, base)

    # ---------- as regras do texto ----------

    def test_regras_do_texto(self):
        for rel in PAGINAS:
            with self.subTest(pagina=rel):
                fonte = ler(rel)
                texto = visivel(fonte)
                baixo = texto.lower()
                for palavra in ('professor', 'jogar', 'jogador', 'ficha', 'folha', 'em grupo', 'em pares', 'fernandes'):
                    self.assertNotIn(palavra, baixo, palavra)
                self.assertNotRegex(baixo, r'\bjog(?:o|os|a|am|ar)\b')
                self.assertNotIn('—', texto)
                self.assertNotRegex(texto, r'\bQual (?!d[aeo]s? )')
                self.assertNotRegex(texto, r'\b[Vv]ocê\b')
        for slug in SLUGS:
            fonte = ler(f'tarefas/{slug}/index.html')
            texto = visivel(fonte)
            principal = fonte[fonte.index('<main'):fonte.index('</main>')]
            with self.subTest(enunciado=slug):
                # «·» só no molde comum (o título da janela e a navegação), nunca numa frase nossa.
                self.assertNotIn('·', texto)
                # Títulos de obras em itálico (fora dos textos alternativos e dos rótulos para leitores de ecrã).
                sem_italicos = re.sub(r'<i>[^<]*</i>|alt="[^"]*"|aria-label="[^"]*"', '', principal)
                for obra in ('Crónica de D', 'Morte do Conde Andeiro', 'Cantigas Medievais', 'Crónicas'):
                    self.assertNotIn(obra, sem_italicos, obra)
                if slug == 'm1-u2':
                    self.assertEqual(principal.count(f'<i>Crónica de D.{N}João{N}I</i>'), 6)
                    self.assertGreaterEqual(principal.count('<i>Morte do Conde Andeiro</i>'), 3)
                else:
                    self.assertEqual(principal.count('<i>Cantigas Medievais Galego-Portuguesas</i>'), 3)
                # Referências que não se partem (U+00A0), como nas páginas do M3, e mais as que estas páginas trazem: as imagens, a
                # aula, os capítulos, as alíneas e os passos.
                for padrao in (r'\b(?:Texto|Textos|Pergunta|pergunta|Tema|Temas|tema|Lição|lição|canto|Canto|estância|estâncias|verso|versos|Imagem|aula|Passo|Passos|Alínea|Alíneas|Estrofe) (?:\d|[AB]\b|[IVX]+\b|F\d|[a-h]\))',
                               r'\d (?:min|minutos|palavras)\b', r'\b[IVX]+, \d', r'\d (?:a|e|ou) \d', r'\bA (?:ou|e) B\b',
                               r'\b(?:cap\.|capítulo) [IVXLC]+\b', r'\bD\. (?:Dinis|João|Pedro)', r'\bJoão I\b', r'\bséculo [IVX]+\b', r'\bc\. \d'):
                    # (o «Tema » que só os leitores de ecrã leem antes da letra de cada tema, no molde comum, fica de fora)
                    self.assertNotRegex(visivel(fonte.replace('<span class="sr-only">Tema </span>', '')), padrao)
                # As falas do aluno em discurso direto ficam entre «» (nenhuma aspa direita nem curva nas nossas frases).
                self.assertNotRegex(texto, r'[“”"]')
        # O molde não é o piloto por aprovar: os comentários dizem que foi aprovado.
        for rel in ('scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py', 'scripts/grelhas_tarefas.py', 'assets/task-textos.css', 'assets/task-reader.js',
                    'scripts/tarefas_faceis_m1_20261113.py'):
            self.assertNotIn('por aprovar', ler(rel), rel)

    # ---------- o contrato da página (substitui o de tests/test_task_choice.py nestas duas tarefas) ----------

    def test_contrato_da_pagina(self):
        for slug in SLUGS:
            rel = f'tarefas/{slug}/index.html'
            fonte = ler(rel)
            p = Pagina(fonte)
            d = json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json'))
            with self.subTest(tarefa=slug):
                self.assertIn('<main class="task-page task-choice-page" data-task-compact data-task-choice data-task-facil data-task-opening="Começar" data-task-index="nomes">', fonte)
                self.assertEqual([t for t, _, _ in p.raiz], ['nav', 'header', 'section', 'section', 'section', 'section', 'section'])
                self.assertEqual([i for _, i, _ in p.raiz][2:], ['produzir', 'pergunta-2', 'tema', 'entregar', 'apoios'])
                self.assertEqual(['Começar'] + [c for _, _, c in p.raiz][2:], CARTOES_NOMES)
                self.assertEqual(p.temas, ['A', 'B'])
                self.assertEqual(len(re.findall(r'<h3 id="tema-([AB])"><span><span class="sr-only">Tema </span>\1</span> ', fonte)), 2)
                self.assertEqual(len(p.ids), len(set(p.ids)))
                # O primeiro cartão: o que vais fazer, o que entregas, o quadro, a grelha.
                cabeca = fonte.split('<header>', 1)[1].split('</header>', 1)[0]
                self.assertEqual(re.findall(r'<h2 class="task-part"[^>]*>(.*?)</h2>', cabeca), ['O que vais fazer', 'Relógio do aquecimento', 'O que entregas', 'Tempo e tamanho'])
                self.assertEqual(cabeca.count('<ol class="tf-fazer">'), 1)
                self.assertEqual(len(re.findall(r'<li>', cabeca.split('<ol class="tf-fazer">')[1].split('</ol>')[0])), 5)
                self.assertIn('<p class="tf-p">Fotografias do teu trabalho em papel, na tarefa do Teams.</p>', cabeca)
                self.assertEqual(fonte.count('<a href="grelha/">'), 1)
                self.assertIn('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>', cabeca)
                # Uma só pergunta opcional, num desdobrável, com três opções, uma certa, explicações diferentes.
                self.assertEqual(p.perguntas, [('1', True)])
                self.assertEqual(len(p.opcoes), 3)
                self.assertEqual(sum(a['data-correct'] == 'true' for a in p.opcoes), 1)
                self.assertEqual(len({a['data-response'] for a in p.opcoes}), 3)
                self.assertEqual(len(re.findall(r'<span class="task-letter">[ABC]<span class="sr-only">:</span></span> ', fonte)), 3)
                # Os recursos: os mesmos do molde de 28/10, o leitor do molde novo e a folha desta versão (facil-8: a folha ganhou
                # as regras da prosa, das imagens numeradas e do que serve aos dois temas; as páginas do M3 pedem a de antes).
                self.assertLess(fonte.index('assets/relogio.js'), fonte.index('pt-lessons/casca.js'))
                for recurso in ('task-choice.css?v=20261028-escolha-2', 'task-90.js?v=20261027-compact-1', 'task-reader.js?v=20261112-facil-7',
                                'task-textos.css?v=20261113-facil-8', 'info-i.css?v=20261105', 'info-i.js?v=20261105'):
                    self.assertEqual(fonte.count(recurso), 1, recurso)
                for fora in ('task-clock', 'rondas', '10/10/60/10'):
                    self.assertNotIn(fora, fonte)
                # As duas linhas finais, a entrega e a letra do tema.
                for frase in ('<h2 id="finais-titulo">Duas linhas finais</h2>', '<h2>Entrega no Teams</h2>', '<h2 id="entregar-title">Antes de entregar, verifica</h2>'):
                    self.assertEqual(fonte.count(frase), 1, frase)
                # Dossiê do tema B: cada facto com a sua fonte e a ligação, que existe; citações e números na página para onde aponta.
                dossie = re.findall(r'<section class="task-dossier tf-dossie".*?</section>', fonte, re.S)
                self.assertEqual(len(dossie), 1)
                factos = re.findall(r'<li>(.*?)<span class="tf-origem">Fonte: <a href="([^"]+)">(.*?)</a></span></li>', dossie[0])
                self.assertEqual(len(factos), dossie[0].count('<li>'))
                self.assertEqual([(x, h, n) for x, h, n in factos], [(x['facto'], x['href'], x['fonte']) for x in d['dossie']])
                self.assertEqual(len(factos), 5)
                for facto, href, _ in factos:
                    alvo = plana(str((Path(rel).parent / href / 'index.html').as_posix()).replace('tarefas/' + slug + '/../../', ''))
                    texto = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', facto)))
                    for pedaco in re.findall(r'«([^»]+)»', texto) + re.findall(r'\b\d{3,4}\b', texto):
                        self.assertIn(pedaco, alvo, (href, pedaco))
                # Todas as ligações internas existem; as âncoras apontam para ids da página; para fora, só os créditos das imagens.
                licoes = [h for h in p.ligacoes if '/m1/licao-' in h]
                self.assertGreaterEqual(len(set(licoes)), 4)
                fora = []
                for href in p.ligacoes:
                    url = urlsplit(href)
                    if url.scheme:
                        self.assertIn((url.scheme, url.netloc), (('https', 'commons.wikimedia.org'), ('https', 'pedrohfernandes-klk.github.io')), href)
                        fora.append(url.netloc)
                        continue
                    if not url.path:
                        self.assertIn(url.fragment, p.ids, href)
                        continue
                    alvo = (ROOT / rel).parent / unquote(url.path)
                    self.assertTrue(((alvo / 'index.html') if alvo.is_dir() else alvo).is_file(), href)
                self.assertEqual(fora.count('commons.wikimedia.org'), 2 if slug == 'm1-u2' else 0)
                self.assertGreaterEqual(len([h for h in p.ligacoes if h.startswith('#texto-')]), 3)
                self.assertIn('#dossie', p.ligacoes)
                # «Rever a matéria»: uma linha por pergunta ou tema; o nome da página e os nomes das secções entre «» são os da lição.
                rever = re.search(r'<ul class="tf-rever-lista">(.*?)</ul>', fonte, re.S).group(1)
                itens = re.findall(r'<li><b>((?:Pergunta|Tema)\xa0[12AB]|Temas\xa0A\xa0e\xa0B)\.</b> Lição\xa0F\d\d, <a href="([^"]+)">(.*?)</a>\.? (.*?)</li>', rever)
                self.assertEqual(len(itens), rever.count('<li>'))
                self.assertGreaterEqual(len(itens), 5)
                self.assertEqual({solto(x[0]) for x in itens} & {'Pergunta 1', 'Pergunta 2', 'Tema A', 'Tema B'}, {'Pergunta 1', 'Pergunta 2', 'Tema A', 'Tema B'})
                motor = plana('assets/pt-lessons/jogo.js')
                for _, href, nome, resto in itens:
                    alvo = plana(href.replace('../../', '') + 'index.html')
                    self.assertIn(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', nome))), alvo, href)
                    self.assertRegex(href, r'^\.\./\.\./m1/licao-m1-f\d\d/$')
                    seccoes = re.findall(r'«([^»]+)»', resto)
                    self.assertGreaterEqual(len(seccoes), 1, resto)
                    for secao in seccoes:
                        secao = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', secao)))
                        self.assertTrue(secao in alvo or secao in motor, (href, secao))
                self.assertEqual(fonte.count(f'<p class="tf-p">{d["facil"]["rever_texto"]}</p>'), 1)
                self.assertTrue(d['facil']['rever_texto'].startswith(f'Os Textos{N}1,{N}2{N}e{N}3 '))
                self.assertTrue(d['facil']['rever_texto'].endswith(' já estão nesta página. As lições servem para rever a matéria.'))
        # m1-u1: os dois grupos de alíneas da pergunta 1 com as letras seguidas (a a e; f a h).
        u1 = ler(ENUNCIADOS[0])
        self.assertEqual(re.findall(r'<ol class="tf-alineas"(?: start="(\d)")?>', u1.split('id="produzir"')[1].split('</section>')[0]), ['', '6'])
        # m1-u2: três grupos na pergunta 2 (a; b a d; e, f); o que a crónica tem nos dois temas, um pedido por linha, depois dos temas.
        u2 = ler(ENUNCIADOS[1])
        self.assertEqual(re.findall(r'<ol class="tf-alineas"(?: start="(\d)")?>', u2.split('id="pergunta-2"')[1].split('</section>')[0]), ['', '2', '5'])
        comum = re.search(r'<div class="tf-comum" id="comum" role="group" aria-labelledby="comum-titulo"><h3 id="comum-titulo">Nos dois temas, a tua crónica tem tudo isto</h3><ol class="tf-passos">(.*?)</ol>', u2).group(1)
        self.assertEqual(re.findall(r'<li>(.*?)</li>', comum), [
            'Dá um título à crónica.', 'Começa dentro da ação.', 'Mostra um pormenor.', 'Põe a população a agir.',
            'Inclui uma fala identificada como «documentada» ou «imaginada».', 'Assinala as tuas inferências e opiniões.',
            'Confronta duas fontes.', 'Lista as duas fontes no fim.', 'Risca uma frase sem a apagar e escreve uma versão melhor.'])
        self.assertLess(u2.index('</article></div><div class="tf-comum"'), u2.index('<details class="tf-so-tema tf-dois-temas">'))
        self.assertNotIn('tf-comum', u1)
        self.assertNotIn('tf-dois-temas', u1)
        leitor = ler('assets/task-reader.js')
        self.assertIn('page.getAttribute("data-task-opening")||(compact?"Enunciado":"A aula de tarefa")', leitor)
        self.assertIn('node.getAttribute("data-task-card-name")||', leitor)
        self.assertIn('(page.getAttribute("data-task-index")==="nomes"?"":String(i+1)+". ")+item.label', leitor)

    # ---------- as tarefas dos outros módulos não mudam ----------

    def test_as_outras_tarefas_nao_mudam(self):
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(sorted(OUTRAS + SLUGS), sorted(p.stem for p in (ROOT / 'docs/pedagogia/tarefas-escolha').glob('*.json')))
        grelhas = json.loads(ler(GRELHAS))['tarefas']
        for slug in OUTRAS:
            with self.subTest(tarefa=slug):
                no_molde = slug in ('m3-u1', 'm3-u2')
                # 13/11/2026: a m5-u1 e a m5-u2 passaram também ao molde, pela camada que fica por cima desta
                # (tarefas_faceis_m5_20261113, com o seu teste, tests/test_tarefas_faceis_m5.py). Os dados das grelhas leem-se aqui
                # como esta camada os deixou (sem as chaves novas do M5); os dados e a página das duas tarefas são os da árvore, e
                # pedem a folha da sua versão (facil-9).
                no_molde_m5 = slug in ('m5-u1', 'm5-u2')
                self.assertEqual('facil' in json.loads(ler(f'docs/pedagogia/tarefas-escolha/{slug}.json')), no_molde or no_molde_m5)
                self.assertEqual(bool({'autoavaliacao_so_tua', 'trocas_aluno'} & set(grelhas[slug])), no_molde)
                pagina = ler(f'tarefas/{slug}/index.html')
                if no_molde_m5:
                    self.assertEqual(pagina.count('task-textos.css?v=20261113-facil-9'), 1)
                    self.assertNotIn('facil-8', pagina)
                    self.assertEqual(undo_tarefas_faceis_m5_1113(f'tarefas/{slug}/index.html', pagina).count('data-task-facil'), 0)
                elif no_molde:
                    # As páginas do M3 continuam a pedir a folha de antes e não usam nenhuma das classes novas.
                    self.assertEqual(pagina.count('task-textos.css?v=20261112-facil-7'), 1)
                    for marca in ('facil-8', 'tt-prosa', 'tt-par', 'tf-figs', 'tf-fig-n', 'tf-comum', 'tf-dois-temas', 'tf-intro'):
                        self.assertNotIn(marca, pagina)
                else:
                    for marca in ('data-task-facil', 'task-textos.css', 'facil-', 'class="tf-', 'class="tt-'):
                        self.assertNotIn(marca, pagina)
                    self.assertIn('task-reader.js?v=20261028-escolha-2', pagina)
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertNotIn(f'tarefas/{slug}/{parte}index.html', MANIFESTO['files'])
        # Todas as páginas de tarefas/ que não são as seis desta camada (as tarefas, grelhas, correções e aquecimentos dos outros
        # módulos, e os dois aquecimentos do M1) são as do main de partida, byte a byte; e os dados também.
        todas = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'tarefas').rglob('*') if p.is_file())
        self.assertGreater(len(todas), 60)
        # 13/11/2026: os ficheiros que a camada de cima muda (as tarefas do M5 mais fáceis de fazer: as páginas e os dados da m5-u1 e
        # da m5-u2 e, pelo acerto do tema B, os da m3-u2) comparam-se com essa camada desfeita pela auditoria, com contagem estrita:
        # por baixo dela, continuam a ser os do main de partida, byte a byte.
        de_cima = 0
        for rel in todas + sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/pedagogia').rglob('*.json')):
            if rel in MANIFESTO['files']:
                continue
            r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
            if r.returncode == 0:
                with self.subTest(igual_ao_main=rel):
                    conteudo = (ROOT / rel).read_bytes()
                    if rel in M5_FICHEIROS:
                        de_cima += 1
                        conteudo = undo_tarefas_faceis_m5_1113(rel, conteudo.decode('utf-8')).encode('utf-8')
                    self.assertEqual(conteudo, r.stdout)
        self.assertIn(de_cima, (0, 14))
        # Os três geradores, com os dados da árvore, dão todas as páginas da árvore, byte a byte (as treze tarefas, as grelhas, as
        # correções e os aquecimentos).
        with tempfile.TemporaryDirectory() as tmp:
            for comando in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                            ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(p.relative_to(tmp).as_posix() for p in Path(tmp).rglob('index.html'))
            for slug in OUTRAS + SLUGS:
                for parte in ('', 'grelha/', 'aquecimento/', 'correcao/'):
                    self.assertIn(f'tarefas/{slug}/{parte}index.html', geradas)
            for rel in geradas:
                with self.subTest(pagina=rel):
                    self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes())

    # ---------- a camada ----------

    def test_camada_fechada_reversivel_e_no_topo(self):
        # 13/11/2026: por cima desta camada fica a das tarefas do M5 mais fáceis de fazer: a ordem ganha mais uma posição (esta passa
        # a segunda, logo por cima das tarefas do M3) e as camadas são 49, com a mesma exigência.
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[2], ('tarefas_faceis_m3_20261112', 'tarefas-faceis-m3-edits-20261112'))
        self.assertEqual(len(verificar_camadas.LAYERS), 49)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), 49)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertIn('não se edita à mão', MANIFESTO['_nota'])
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(len(TROCAS), sum(len(v['edits']) for v in MANIFESTO['files'].values()))
        self.assertEqual(len(MANIFESTO['files']), 12)
        # 13/11/2026: confere-se com a camada do M5, que está por cima, desfeita primeiro.
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar',
                            '--desfazer-antes', M5], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f'{len(TROCAS)} trocas em 12 ficheiros: {len(TROCAS)} aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        for t in TROCAS:
            self.assertTrue(t['achado'].startswith('13/11/2026: '), t['local'])
            self.assertEqual(t['ocorrencias'], 1)
        # Ida e volta, letra a letra: a árvore é o «after» do manifesto; desfeita a camada, cada ficheiro é a base (o main de partida);
        # voltando a aplicar, é outra vez a árvore.
        for rel, registo in MANIFESTO['files'].items():
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                self.assertEqual(sha_lf(atual), registo['after_sha256_lf'])
                base = antes(rel)
                self.assertEqual(sha_lf(base), registo['base_sha256_lf'])
                self.assertNotEqual(base, atual)
                de_novo = base
                for e in registo['edits']:
                    self.assertEqual(de_novo.count(e['old']), e['occurrences'], e['location'])
                    de_novo = de_novo.replace(e['old'], e['new'])
                self.assertEqual(de_novo, atual)
                # A base é o ficheiro do commit de partida, byte a byte (quando o repositório o tem: num clone raso, vale o resumo).
                do_commit = do_main(rel)
                if do_commit is not None:
                    self.assertEqual(do_commit, base)
                # O desfazer da auditoria dá o mesmo, e não desfaz nada segunda vez.
                self.assertEqual(undo_tarefas_faceis_m1_1113(rel, atual), base)
                self.assertEqual(undo_tarefas_faceis_m1_1113(rel, base), base)
        # Com a camada que fica logo abaixo (as tarefas do M3) partilha só os dados das grelhas: aí, o desfazer da auditoria tira
        # primeiro esta e depois a do M3; nos outros onze ficheiros, o desfazer da camada do M3 dá a base desta.
        m3 = json.loads(ler(M3F))['files']
        self.assertEqual(set(MANIFESTO['files']) & set(m3), {GRELHAS})
        # 13/11/2026: com a camada do M5, que fica por cima, partilha também só os dados das grelhas.
        self.assertEqual(set(MANIFESTO['files']) & set(M5_FICHEIROS), {GRELHAS})
        for rel in MANIFESTO['files']:
            if rel != GRELHAS:
                self.assertEqual(undo_tarefas_faceis_m3_1112(rel, ler(rel)), antes(rel), rel)
        sem_as_duas = undo_tarefas_faceis_m3_1112(GRELHAS, ler(GRELHAS))
        self.assertEqual(sha_lf(antes(GRELHAS)), m3[GRELHAS]['after_sha256_lf'])
        self.assertEqual(sha_lf(sem_as_duas), m3[GRELHAS]['base_sha256_lf'])
        for chave in ('autoavaliacao_so_tua', 'trocas_aluno'):
            self.assertNotIn(chave, sem_as_duas)

    def test_gerador_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m1_20261113', ROOT / 'scripts/tarefas_faceis_m1_20261113.py')
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
        todas, finais = C.construir()
        self.assertEqual(todas, TROCAS)
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(C.FICHEIROS, FICHEIROS)
        self.assertEqual(C.BASE_COMMIT, BASE_COMMIT)
        # As três páginas do módulo mudam só nas cinco trocas escritas à mão (três no guia, uma no índice, uma no portefólio).
        self.assertEqual(sorted((f, a, b, n) for f, a, b, n, _ in C.EDICOES),
                         sorted((t['ficheiro'], t['antigo'], t['novo'], t['ocorrencias']) for t in TROCAS if t['ficheiro'] in (GUIA, INDICE, PORTEFOLIO)))
        self.assertEqual([f for f, *_ in C.EDICOES], [GUIA, GUIA, GUIA, INDICE, PORTEFOLIO])
        # A camada do M3, que fica por baixo e partilha os dados das grelhas, continua a dar o seu JSON, com esta desfeita primeiro.
        spec = importlib.util.spec_from_file_location('tarefas_faceis_m3_20261112', ROOT / 'scripts/tarefas_faceis_m3_20261112.py')
        C3 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C3)
        self.assertEqual(C3.construir()[0], json.loads(ler('scripts/tarefas_faceis_m3_20261112.json')))

    def test_leitura_historica_dos_enunciados(self):
        # Os contratos históricos leem as tarefas como eram antes do pedido #192 (scripts/tarefas_claras_historico.py). Com esta camada
        # por cima, a leitura dá a base do manifesto do #192, letra a letra, nos enunciados e nos dados da M1-U1 e da M1-U2, a partir
        # da página inteira ou com esta camada já desfeita; e não desfaz nada segunda vez.
        import tarefas_claras_historico as historico
        claras = json.loads(ler('tests/fixtures/tarefas-claras-edits-20261110.json'))['files']
        nossos = sorted(set(MANIFESTO['files']) & set(claras))
        self.assertEqual(nossos, sorted(DADOS_TAREFAS + ENUNCIADOS))
        for rel in nossos:
            with self.subTest(ficheiro=rel):
                atual = ler(rel)
                antes_192 = historico.desfazer(rel, atual)
                self.assertEqual(sha_lf(antes_192), claras[rel]['base_sha256_lf'])
                self.assertEqual(historico.desfazer(rel, antes(rel)), antes_192)
                self.assertEqual(historico.desfazer(rel, antes_192), antes_192)
                self.assertEqual(historico.desfazer_faceis(rel, atual), antes(rel))
                self.assertEqual(historico.desfazer_faceis(rel, antes(rel)), antes(rel))
        for rel in MANIFESTO['files']:
            if rel != GRELHAS:
                self.assertEqual(historico.desfazer_faceis(rel, ler(rel)), antes(rel), rel)
        # Nos dados das grelhas, a leitura tira esta camada e, a seguir, a do M3.
        self.assertEqual(sha_lf(historico.desfazer_faceis(GRELHAS, ler(GRELHAS))), json.loads(ler(M3F))['files'][GRELHAS]['base_sha256_lf'])
        fonte = ler('scripts/tarefas_claras_historico.py')
        corpo = fonte[fonte.index('def desfazer_faceis(path, text):'):fonte.index('def desfazer(path, text):')]
        self.assertLess(corpo.index('TAREFAS_FACEIS_M1.get(rel)'), corpo.index('TAREFAS_FACEIS_M3.get(rel)'))
        self.assertIn("_sha_lf(text) == no_topo['after_sha256_lf']", corpo)
        self.assertIn("assert text.count(edit['new']) == edit['occurrences'], f'Tarefas do M1 mais fáceis de fazer não confere: {rel}'", corpo)

    def test_registos_cadeias_e_caminhos_dos_fluxos(self):
        meu = MANIFESTO_REL
        # A auditoria desfaz primeiro esta camada; o corte da Sala também; as bases das camadas que partilham ficheiros com ela também.
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertIn('def undo_tarefas_faceis_m1_1113(path, text):', auditoria)
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m3_1112\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m1_1113\(path, text\)\n')
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('tarefas-faceis-m1-edits-20261113.json'), sala.index('tarefas-faceis-m3-edits-20261112.json'))
        for rel in ('scripts/cuidado_m6_20261108.py', 'scripts/cuidado_m7_20261111.py'):
            self.assertIn('return desfazer_faceis(rel, (ROOT / rel).read_bytes().decode(\'utf-8\'))', ler(rel), rel)
        indices = ler('scripts/cartaz_indices_148_20261106.py')
        corpo = indices[indices.index('def base(rel):'):]
        self.assertLess(corpo.index('json.loads(TAREFAS_FACEIS_M1.read_text'), corpo.index('json.loads(TAREFAS_FACEIS_M3.read_text'))
        m3 = ler('scripts/tarefas_faceis_m3_20261112.py')
        self.assertIn("m1 = ROOT / 'tests/fixtures/tarefas-faceis-m1-edits-20261113.json'", m3[m3.index('def ler(rel):'):m3.index('def base(rel):')])
        for rel in ('tests/browser_cartaz_indices.cjs', 'tests/browser_cartaz_m4_piloto.cjs', 'tests/browser_creditos_i_pt1.cjs'):
            texto = ler(rel)
            self.assertLess(texto.index('((tarefasFaceisM1['), texto.index('((tarefasFaceisM3['), rel)
        # Nos fluxos e nos outros testes, cada cadeia de desfazer começa por esta camada, sem nada entre ela e a das tarefas do M3.
        cadeias = 0
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            # (13/11/2026: o teste da camada do M5 tem as suas próprias asserções sobre as cadeias)
            if p.name in ('test_tarefas_faceis_m1.py', 'test_tarefas_faceis_m3.py', 'test_tarefas_faceis_m5.py'):
                continue
            texto = '\n'.join(linha for linha in p.read_text('utf-8').split('\n') if not linha.lstrip().startswith('#'))
            plano = re.sub(r"['\"]\s*,\s*['\"]", ' ', texto)
            with self.subTest(ficheiro=p.name):
                self.assertEqual(plano.count('--desfazer-antes ' + M3F), plano.count(f'--desfazer-antes {meu} --desfazer-antes {M3F}'))
                self.assertEqual(plano.count('--desfazer-antes {tf}'), plano.count('--desfazer-antes {t1} --desfazer-antes {tf}'))
                self.assertEqual(plano.count('--desfazer-antes {TF}'), plano.count('--desfazer-antes {T1} --desfazer-antes {TF}'))
                # (13/11/2026: nas listas de manifestos, a camada do M5 vem antes desta: a lista abre por ela, e esta continua colada à do M3)
                self.assertEqual(plano.count(f"ROOT/'{M3F}',"), plano.count(f"(ROOT/'{M5}',ROOT/'{meu}',ROOT/'{M3F}',"))
                self.assertEqual(plano.count("ROOT/'{tf}',"), plano.count("(ROOT/'{t5}',ROOT/'{t1}',ROOT/'{tf}',"))
                self.assertEqual(plano.count("ROOT/'{TF}',"), plano.count("(ROOT/'{T5}',ROOT/'{T1}',ROOT/'{TF}',"))
                self.assertEqual(plano.count("' + TF"), plano.count("' + T1 + ' --desfazer-antes ' + TF"))
                # 13/11/2026: cada cadeia começa agora pela camada do M5, logo seguida desta, sem nada entre as duas; a exigência é a
                # mesma, com mais um elo à cabeça.
                self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--desfazer-antes {M5} --desfazer-antes {meu}'))
                self.assertEqual(plano.count('--desfazer-antes {t1}'), plano.count('--desfazer-antes {t5} --desfazer-antes {t1}'))
                self.assertEqual(plano.count('--desfazer-antes {T1}'), plano.count('--desfazer-antes {T5} --desfazer-antes {T1}'))
                # Nenhuma cadeia dos fluxos desfaz esta camada sem ser à cabeça (13/11/2026: logo a seguir à do M5).
                if p.suffix == '.yml':
                    self.assertEqual(plano.count('--desfazer-antes ' + meu), plano.count(f'--verificar --desfazer-antes {M5} --desfazer-antes {meu}'))
                cadeias += plano.count(f'--desfazer-antes {meu} --desfazer-antes {M3F}')
        self.assertGreater(cadeias, 40)
        # No teste da camada do M3, as cadeias são as mesmas, com esta à cabeça.
        # (13/11/2026: com a do M5 antes desta)
        self.assertIn("plano.count(f'--verificar --desfazer-antes {M5} --desfazer-antes {M1} --desfazer-antes {meu}')", ler('tests/test_tarefas_faceis_m3.py'))
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        # 13/11/2026: no fluxo, esta camada confere-se com a do M5 desfeita primeiro, e a do M3 com as duas.
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m1_20261113.json --manifesto {meu} --verificar --desfazer-antes {M5}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m3_20261112.json --manifesto {M3F} --verificar --desfazer-antes {M5} --desfazer-antes {meu}\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m1.py' -v", tarefas)
        self.assertIn('        run: python tests/browser_tarefas_faceis_m1.py\n', tarefas)
        self.assertTrue((ROOT / 'tests/browser_tarefas_faceis_m1.py').is_file())
        # Os fluxos que conferem ou desfazem esta camada arrancam quando ela muda.
        for nome in ('pt-tarefas-qa.yml', 'pt-apoios-qa.yml', 'pt-exame-laboratorio-qa.yml', 'cartaz-qa.yml'):
            texto = ler('.github/workflows/' + nome)
            for caminho in ('scripts/tarefas_faceis_m1_20261113.*', meu):
                self.assertIn(f"'{caminho}'", texto, nome)
            self.assertRegex(texto.split('\non:')[0], r'\n# 13/11/2026: as duas tarefas do M1 mais fáceis de fazer e «tudo junto» no M1, a camada tarefas_faceis_m1_20261113 ')
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])

        # No fluxo das tarefas, tudo o que a camada muda, os geradores, o molde e os seus testes estão nos caminhos do pedido.
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        cabeca = tarefas[tarefas.index('  pull_request:\n    paths:\n'):tarefas.index('\npermissions:')]
        padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
        self.assertGreater(len(padroes), 50)
        for rel in FICHEIROS + AQUECIMENTOS + ['scripts/tarefas_faceis_m1_20261113.py', CAMADA_REL, meu, 'scripts/tarefa_facil.py', 'scripts/tarefas_escolha.py',
                                              'scripts/grelhas_tarefas.py', 'scripts/aquecimentos.py', 'scripts/tarefas_claras_historico.py',
                                              'assets/task-textos.css', 'assets/task-reader.js', 'tests/test_tarefas_faceis_m1.py',
                                              'tests/browser_tarefas_faceis_m1.py', 'img/fontes/morte-conde-andeiro.jpg', 'img/fontes/cerco-lisboa-froissart.jpg']:
            self.assertTrue(any(q.match(rel) for q in padroes), rel)


if __name__ == '__main__':
    unittest.main()
