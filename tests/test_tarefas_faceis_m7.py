"""13/11/2026: as três tarefas do M7 (m7-u1, m7-u2 e m7-u3) «mais fáceis de fazer» e «tudo junto» no M7 (camada tarefas_faceis_m7_20261113).

O docente aprovou o molde das tarefas «mais fáceis de fazer», publicado no M3 (pedido #201) e levado ao M1, ao M5 e ao M6. Esta camada
leva-o ao M7, e este ficheiro exige das três tarefas do M7 o que tests/test_tarefas_faceis_m3.py e tests/test_tarefas_faceis_m6.py
exigem das do M3 e do M6:

* a tarefa pede o mesmo: os títulos, os nomes e as letras dos temas, os números de palavras, cada pedido do enunciado de antes (com as
  mesmas palavras), o dossiê e as perguntas opcionais, e os critérios, níveis, exemplos e pontos da grelha da m7-u3, iguais aos de
  antes da camada (a base do manifesto, o main fe614d67);
* os textos para análise são os das lições do M7, letra a letra: cada verso da página é um verso de um cartão «O texto» da lição, pela
  ordem, com o vocabulário e a linha de fonte da lição; nada veio de fora; não há imagens;
* as decisões do docente, em todos os sítios: tempos 10/10/55/15 (quadro, relógios, guia); «com consulta» dito uma vez, no primeiro
  cartão; os versos citados ou copiados não contam para as palavras; a autoavaliação da grelha não se entrega; o aquecimento com uma
  só ligação; no máximo 10 perguntas de sim ou não na verificação; as mesmas palavras no enunciado, na grelha, na correção, no
  aquecimento e no guia («opinião», «comparação», «duas linhas finais»);
* no guia da tarefa do M7 saem a «Autoavaliação» que se copiava para o Teams e «pergunta ao teu par de trabalho» (a regra passa a
  chamar-se «Dois antes de mim»); no portefólio do M7 sai «trabalho de equipa», sem nada no lugar;
* as regras do texto: sem as palavras proibidas, sem «·» nem «—» nas nossas frases, «Que + nome» ou «Qual das…», referências que não
  se partem, exemplos com outro caso (nenhum verso dos textos da tarefa nos exemplos);
* o contrato das páginas: os cartões com nome, os dois relógios, as ligações internas com alvo, as lições ligadas existem e têm as
  secções que a página manda reler;
* as tarefas, grelhas, correções e aquecimentos dos outros módulos são os do main de partida, byte a byte, e os geradores dão as
  páginas da árvore;
* a camada: no topo da pilha, com manifesto, reversível letra a letra até à base, gerador que dá o mesmo JSON, registada na
  auditoria (desfazer), em scripts/desligar_sala.py, na leitura histórica dos enunciados e nas cadeias e caminhos dos fluxos.

Revisão de 13/11/2026 (dois revisores) e os três acertos do M1 e do M5 que o docente mandou ir no mesmo pedido (classe Acertos, no
fim): a camada passa a ter 22 ficheiros (mais o índice e o mapa do M7 e os sete dos acertos); a m1-u2 diz, no enunciado e na grelha,
com as mesmas palavras, que a passagem copiada não conta; a carta de exemplo da m5-u1 usa só o que a lição F17 dá; os dois exemplos
da grelha do M5 já não citam os textos da própria tarefa. As camadas do M1 e do M5 não se reescrevem: os seus testes leem os seus
ficheiros com esta camada desfeita.

O navegador (390 e 1280 px, claro e escuro, teclado, relógio, ligações internas e impressão) está em
tests/browser_tarefas_faceis_m7.py."""
from pathlib import Path
import html
import json
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'scripts'))
from auditoria_20261028 import undo_tarefas_faceis_m7_1113  # noqa: E402
import verificar_camadas  # noqa: E402

CAMADA_REL = 'scripts/tarefas_faceis_m7_20261113.json'
MANIFESTO_REL = 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'
BASE_COMMIT = 'fe614d6750b7c4b93fd58f739415f6a250310552'
MANIFESTO = json.loads((ROOT / MANIFESTO_REL).read_text('utf-8'))
N = '\xa0'
SLUGS = ('m7-u1', 'm7-u2', 'm7-u3')
ENUNCIADOS = [f'tarefas/{s}/index.html' for s in SLUGS]
GRELHAS = 'docs/pedagogia/grelhas-tarefas-20261027.json'
GUIA, PORTEFOLIO = 'm7/guia-da-tarefa-m7/index.html', 'm7/portefolio-do-modulo-m7/index.html'
INDICE, MAPA = 'm7/index.html', 'm7/mapa-do-modulo-m7/index.html'
# 13/11/2026, revisão: os ficheiros dos três acertos do M1 e do M5 (os dados e as páginas que mudam; as versões de correção não mudam).
ACERTOS = ['docs/pedagogia/tarefas-escolha/m1-u2.json', 'tarefas/m1-u2/index.html', 'tarefas/m1-u2/grelha/index.html',
           'docs/pedagogia/tarefas-escolha/m5-u1.json', 'tarefas/m5-u1/index.html', 'tarefas/m5-u1/grelha/index.html', 'tarefas/m5-u2/grelha/index.html']
FICHEIROS = ['docs/pedagogia/tarefas-escolha/m7-u3.json', GRELHAS, 'docs/pedagogia/aquecimentos/m7-u1.json', 'docs/pedagogia/aquecimentos/m7-u3.json',
             'tarefas/m7-u1/index.html', 'tarefas/m7-u2/index.html', 'tarefas/m7-u1/aquecimento/index.html', 'tarefas/m7-u3/index.html',
             'tarefas/m7-u3/grelha/index.html', 'tarefas/m7-u3/aquecimento/index.html', 'tarefas/m7-u3/correcao/index.html', GUIA, PORTEFOLIO,
             INDICE, MAPA] + ACERTOS
NAO_CONTAM = 'Não contam para as palavras: os versos citados ou copiados e as duas linhas finais.'
# 13/11/2026, revisão: no atributo, o nome do cartão leva espaço normal, como «Pergunta 1» e «Tema A ou B» nas outras páginas do molde.
CARTOES = {'m7-u1': ['A comparação', 'Fechar e entregar', 'Rever a matéria'],
           'm7-u2': ['Parte 1: o perfil', 'Parte 2: o texto', 'Parte 3: escolhas e fontes', 'Parte 4: a apresentação', 'Fechar e entregar', 'Rever a matéria'],
           'm7-u3': ['Tema A ou B', 'O teu texto', 'Fechar e entregar', 'Rever a matéria']}
PALAVRAS = {'m7-u1': '80' + N + 'a' + N + '120', 'm7-u2': '100' + N + 'a' + N + '150', 'm7-u3': '180' + N + 'a' + N + '220'}
# O que cada enunciado de antes pedia, com as suas palavras: cada pedaço está no enunciado de antes e continua no de agora.
PEDIDOS = {
    'm7-u1': ['«É em nós que é tudo»', '«Quem sou ao menos sinta»', 'Explica o que os finais afirmam ou desejam.', 'Usa uma passagem de cada poema',
              'apoia a comparação', 'a tua leitura', 'uma dúvida que os poemas deixam', 'a voz poética do autor', 'Fotografa a comparação e as duas linhas finais.',
              'Que diferença existe entre «é» e «sinta»?', 'Que comparação podes sustentar nos poemas?', 'Ambos se voltam para o interior, por caminhos diferentes.'],
    'm7-u2': ['A apresentação é individual.', 'ofício', 'deve discordar de ti numa ideia', 'poema, carta ou nota', 'duas escolhas de linguagem com exemplos teus',
              'ista três fontes, com data', 'as diferenças entre elas', 'esponde a uma pergunta feita ou prevista', 'egista a pergunta e a resposta numa linha.',
              'Fotografa o perfil, o texto, as duas escolhas explicadas, as três fontes, a pergunta com resposta e as duas linhas finais.',
              'O que torna uma voz ficcional reconhecível?', 'Que justificação apresenta uma prova?', '«Repito “talvez” porque esta voz desconfia das certezas.»'],
    'm7-u3': ['Começa por uma opinião com uma condição (S).', 'aceita uma acusação e muda-lhe o sentido (R), ou admite uma dificuldade com «embora» (C).',
              'Acrescenta uma condição necessária (N), um contraste com «mas» (M) ou uma pergunta que leve a pensar (P).', 'sem a copiar.',
              'Marca as letras na margem; a conclusão não leva letra.', 'Cita um verso exato de <i>Mensagem</i>, entre «»', 'ndica o poema', 'xplica o verso no seu contexto.',
              'Acrescenta um facto datado das lições, distinguindo-o da interpretação do poema, ou compara com Garrett (<i>Frei Luís de Sousa</i>) ou Reis.',
              'No tema B, o facto escolhido tem de ter data: 1578, 1933 ou 1934.', '«Valeu a pena? Tudo vale a pena / Se a alma não é pequena.»',
              'Concordas quando são outras pessoas a pagar o preço do sonho?', 'Considera as mães, os filhos e as noivas da primeira estrofe',
              'Esperar que alguém volte para resolver os problemas dá força a um país ou tira-lh', 'Se usares um facto, indica a data: 1578, 1933 ou 1934.',
              'que movimento vais voltar a usar, e onde?', 'Valeu a pena?', 'Por quem, ou pelo quê, ainda esperamos?', 'Fotografa o texto e as duas linhas finais.',
              'Ler em voz alta só ajuda quando quem ouve pode interromper.'],
}
# De onde vem cada texto: a lição, os cartões «O texto» (pela ordem), o cartão do vocabulário e o cartão da linha de fonte.
TEXTOS = {
    'm7-u1': {'texto-1': ('m7/licao-m7-f14/index.html', (3, 9), 9, 9, 24, [6, 6, 6, 6]), 'texto-2': ('m7/licao-m7-f15/index.html', (3,), None, 3, 12, [4, 4, 4])},
    'm7-u2': {},
    'm7-u3': {'texto-1': ('m7/licao-m7-f08/index.html', (10,), 10, 10, 12, [6, 6]), 'texto-2': ('m7/licao-m7-f09/index.html', (3,), 13, 3, 10, [5, 5])},
}
PROIBIDAS = re.compile(r'\b(professor\w*|jog(o|os|ar|a|as|am|ou)|fichas?|folhas?|pares|grupos?|colegas?)\b', re.I)


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def base(rel):
    r = subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True)
    assert r.returncode == 0, rel
    return r.stdout.decode('utf-8')


def dados(slug):
    pasta = 'tarefas-escolha' if slug == 'm7-u3' else 'tarefas-individuais'
    return json.loads(ler(f'docs/pedagogia/{pasta}/{slug}.json'))


def visivel(pagina):
    """O texto que se lê na página (sem etiquetas, scripts nem atributos)."""
    corpo = pagina[pagina.index('<main'):pagina.index('</main>')]
    corpo = re.sub(r'<script.*?</script>', ' ', corpo, flags=re.S)
    return html.unescape(re.sub(r'[ \t\r\n]+', ' ', re.sub(r'<[^>]+>', ' ', corpo)))


def cartoes(rel):
    fonte = ler(rel)
    return json.JSONDecoder().raw_decode(fonte[fonte.index('CARTOES=[') + 8:])[0]


def estrofes_da_licao(rel, numeros):
    out = []
    for k in numeros:
        c = cartoes(rel)[k - 1]
        assert c['t'] == 'ler' and c['rot'].startswith('O texto'), (rel, k)
        v = re.search(r'<p class="v">(.*?)</p>', c['html'], re.S).group(1)
        anterior = None
        for m in re.finditer(r'<span class="ln" data-l="\d+-(\d+)"><span class="n">\d*</span>(.*?)</span>(?=\n|$)', v, re.S):
            i = int(m.group(1))
            if anterior is None or i != anterior + 1:
                out.append([])
            out[-1].append(html.unescape(re.sub(r'<[^>]+>', '', m.group(2))))
            anterior = i
    return out


class MesmaTarefa(unittest.TestCase):
    def test_cada_pedido_de_antes_continua_no_enunciado(self):
        for slug in SLUGS:
            antes, agora = base(f'tarefas/{slug}/index.html'), ler(f'tarefas/{slug}/index.html')
            for pedido in PEDIDOS[slug]:
                with self.subTest(slug=slug, pedido=pedido):
                    # (os espaços que não quebram do enunciado novo comparam-se como espaços)
                    self.assertIn(pedido, antes.replace(N, ' '))
                    self.assertIn(pedido, agora.replace(N, ' '))

    def test_titulos_palavras_e_temas(self):
        for slug in SLUGS:
            antes, agora = base(f'tarefas/{slug}/index.html'), ler(f'tarefas/{slug}/index.html')
            with self.subTest(slug=slug):
                self.assertEqual(re.search(r'<h1>(.*?)</h1>', antes).group(1), re.search(r'<h1>(.*?)</h1>', agora).group(1))
                self.assertIn(PALAVRAS[slug].replace(N, ' '), visivel(antes).replace(N, ' '))
                self.assertIn(PALAVRAS[slug], agora)
                self.assertEqual(re.search(r'<title>(.*?)</title>', antes).group(1), re.search(r'<title>(.*?)</title>', agora).group(1))
        agora = ler('tarefas/m7-u3/index.html')
        self.assertEqual(re.findall(r'data-task-theme="([AB])"', agora), ['A', 'B'])

    def test_dossie_e_chaves_antigas_da_m7_u3_ficam(self):
        antes, agora = json.loads(base('docs/pedagogia/tarefas-escolha/m7-u3.json')), dados('m7-u3')
        self.assertEqual({k: v for k, v in agora.items() if k != 'facil'}, antes)
        pagina = ler('tarefas/m7-u3/index.html')
        for facto in agora['dossie']:
            self.assertIn(facto['fonte'], pagina)
            self.assertTrue((ROOT / 'tarefas/m7-u3' / facto['href'] / 'index.html').resolve().is_file())
        self.assertEqual(pagina.count('<span class="tf-origem">'), 5)
        # A pergunta opcional é a de antes, com «opinião» onde dizia «tese».
        troca = lambda x: json.loads(json.dumps(x, ensure_ascii=False).replace('tese', 'opinião'))
        self.assertEqual(agora['facil']['opcional'], troca(antes['opcional']))

    def test_perguntas_opcionais_das_individuais_sao_as_de_antes(self):
        for slug in ('m7-u1', 'm7-u2'):
            antes, agora = base(f'tarefas/{slug}/index.html'), ler(f'tarefas/{slug}/index.html')
            botoes = lambda t: re.findall(r'<button type="button" aria-pressed="false" data-correct="(true|false)" data-response="([^"]*)">([^<]*)</button>', t)
            self.assertEqual(botoes(antes), botoes(agora))
            self.assertEqual(len(botoes(agora)), 6)

    def test_grelha_da_m7_u3_criterios_niveis_exemplos_e_pontos(self):
        antes, agora = json.loads(base(GRELHAS))['tarefas'], json.loads(ler(GRELHAS))['tarefas']
        novas = {'autoavaliacao_so_tua', 'correcao_estreita', 'trocas_aluno'}
        self.assertEqual({k: v for k, v in agora['m7-u3'].items() if k not in novas}, antes['m7-u3'])
        self.assertEqual(set(agora['m7-u3']) - set(antes['m7-u3']), novas)
        # 13/11/2026, revisão: as outras grelhas são as de antes, salvo o que os três acertos do M1 e do M5 mudam (as trocas de
        # palavras da m1-u2 e os exemplos de dois critérios da m5-u1 e de um da m5-u2; ver a classe Acertos). Os critérios, os níveis
        # (a frase de cada nível) e os pontos de todas ficam iguais.
        for slug in antes:
            if slug == 'm7-u3':
                continue
            a, b = json.loads(json.dumps(antes[slug])), json.loads(json.dumps(agora[slug]))
            self.assertEqual([(c['nome'], c['max'], [v[0] for v in c['niveis'].values()], c['custa']) for c in b['criterios']],
                             [(c['nome'], c['max'], [v[0] for v in c['niveis'].values()], c['custa']) for c in a['criterios']], slug)
            if slug == 'm1-u2':
                self.assertEqual([x[0] for x in a['trocas_aluno']][2:7] + [x[0] for x in a['trocas_aluno']][8:], [x[0] for x in b['trocas_aluno']][2:7] + [x[0] for x in b['trocas_aluno']][8:])
                a['trocas_aluno'] = b['trocas_aluno'] = None
            elif slug == 'm5-u1':
                for k, niveis in ((2, ('parcial', 'max')), (3, ('parcial', 'max'))):
                    for n in niveis:
                        self.assertNotEqual(a['criterios'][k]['niveis'][n][1], b['criterios'][k]['niveis'][n][1])
                        a['criterios'][k]['niveis'][n][1] = b['criterios'][k]['niveis'][n][1] = None
            elif slug == 'm5-u2':
                self.assertNotEqual(a['criterios'][2]['niveis']['max'][1], b['criterios'][2]['niveis']['max'][1])
                a['criterios'][2]['niveis']['max'][1] = b['criterios'][2]['niveis']['max'][1] = None
            self.assertEqual(b, a, slug)
        self.assertEqual([c['max'] for c in agora['m7-u3']['criterios']], [3, 5, 5, 4, 3])


class TextosDasLicoes(unittest.TestCase):
    def test_cada_verso_e_o_da_licao_letra_a_letra(self):
        for slug in SLUGS:
            f = dados(slug)['facil']
            self.assertEqual([t['id'] for t in f['textos']], list(TEXTOS[slug]))
            pagina = ler(f'tarefas/{slug}/index.html')
            for t in f['textos']:
                rel, numeros, c_voc, c_fonte, versos, forma = TEXTOS[slug][t['id']]
                with self.subTest(slug=slug, texto=t['id']):
                    da_licao = estrofes_da_licao(rel, numeros)
                    self.assertEqual([e['versos'] for e in t['estrofes']], da_licao)
                    self.assertEqual([len(e) for e in da_licao], forma)
                    self.assertEqual(sum(forma), versos)
                    bloco = pagina[pagina.index(f'<section class="tt-texto tt-curto" id="{t["id"]}"'):]
                    bloco = bloco[:bloco.index('</section>')]
                    self.assertEqual([html.unescape(x) for x in re.findall(r'<span class="tt-l">(.*?)</span>', bloco)], [v for e in da_licao for v in e])
                    self.assertEqual(bloco.count('<p class="tt-estrofe">'), len(forma))
                    # o vocabulário e a linha de fonte são os da lição
                    arr = cartoes(rel)
                    for palavra, sentido in t.get('glossario', []):
                        self.assertIn(f'<b>{palavra}</b>, {sentido}', arr[c_voc - 1]['html'])
                    fonte = re.search(r'<p class="fonte">(.*?)</p>', arr[c_fonte - 1]['html']).group(1)
                    self.assertEqual(re.sub(r'_([^_]+)_', r'<i>\1</i>', fonte), t['fonte'])
                    self.assertIn(rel, t['origem'])
                    self.assertIn(f'<p class="tt-fonte">{t["fonte"]}</p>', bloco)

    def test_so_os_dois_poemas_de_mensagem_entram_completos_na_m7_u3_e_nao_ha_imagens(self):
        pagina = ler('tarefas/m7-u3/index.html')
        self.assertEqual(re.findall(r'<span class="tt-num">(.*?)</span>', pagina), ['Texto' + N + '1', 'Texto' + N + '2'])
        self.assertIn('«Mar Português», de Fernando Pessoa', pagina)
        self.assertIn('«D.' + N + 'Sebastião, Rei de Portugal», de Fernando Pessoa', pagina)
        for rel in ENUNCIADOS:
            self.assertNotIn('<img', ler(rel), rel)
        self.assertNotIn('tt-texto', ler('tarefas/m7-u2/index.html'))

    def test_os_exemplos_usam_outro_caso(self):
        """Nenhum verso dos textos da tarefa aparece nos exemplos nem nos apoios (desdobráveis que não saem em papel)."""
        for slug in SLUGS:
            f = dados(slug)['facil']
            versos = [v for t in f['textos'] for e in t['estrofes'] for v in e['versos']]
            pagina = ler(f'tarefas/{slug}/index.html')
            apoios = ' '.join(re.findall(r'<details class="tf-so-tema tf-(?:exemplos|mais) tf-so-ecra">.*?</details>', pagina, re.S))
            self.assertTrue(apoios, slug)
            for v in versos:
                self.assertNotIn(v.rstrip(',.;!?'), apoios, (slug, v))
            for trecho in ('Louco, sim', 'Valeu a pena', 'É em nós que é tudo', 'Quem sou ao menos sinta'):
                self.assertNotIn(trecho, apoios, (slug, trecho))
        # as citações dos exemplos estão nas lições do M7, no guia ou no aquecimento
        fontes = ' '.join(ler(str(p.relative_to(ROOT))) for p in sorted((ROOT / 'm7').glob('licao-m7-f*/index.html'))).replace('\\"', '"')
        fontes += ler(GUIA) + ler('docs/pedagogia/aquecimentos/m7-u2.json') + ler(GRELHAS)
        for trecho in ("O que em mim sente 'stá pensando", 'a entreter a razão', 'Ouvi-la alegra e entristece', 'Ah, poder ser tu, sendo eu!',
                       'Quem está ao pé dele está só ao pé dele',
                       'Hoje levantei catorze contentores.', 'Estou hoje vencido, embora não saiba a verdade',
                       'Artificial, sim, artificial, porque escolheu cada pausa em vez de a deixar ao acaso.'):
            self.assertIn(trecho, fontes, trecho)
            self.assertTrue(any(trecho in ler(e) for e in ENUNCIADOS), trecho)

    def test_os_exemplos_nao_dao_parte_da_resposta(self):
        """13/11/2026, revisão: dois exemplos davam feito o que a tarefa pede e saíram do enunciado."""
        # m7-u2, parte 3: a tarefa pede três fontes com data e as diferenças entre elas, e a ajuda diz que as fontes são a carta a Adolfo
        # Casais Monteiro ou uma lição dos heterónimos. O exemplo que dava a carta, a lição F01, a lição F11 e a diferença já escrita
        # saiu; a parte fica com um só exemplo, o da escolha de linguagem (um verso de Caeiro), e nenhum exemplo fala de fontes.
        f2 = dados('m7-u2')['facil']
        self.assertEqual([len(p.get('exemplos', [])) for p in f2['partes']], [1, 1, 1, 0])
        u2 = ler('tarefas/m7-u2/index.html')
        exemplos = ' '.join(re.findall(r'<details class="tf-so-tema tf-exemplos tf-so-ecra">.*?</details>', u2, re.S))
        self.assertEqual(exemplos.count('<aside class="tf-exemplo">'), 3)
        for fora in ('Casais Monteiro', '1935', 'F01', 'F11', 'a vida inventada prepara o estilo', 'Estes dados ajudam', 'A diferença', 'fonte'):
            self.assertNotIn(fora, visivel('<main>' + exemplos + '</main>'), fora)
        self.assertIn('Uma fonte pode ser a carta a Adolfo Casais Monteiro ou uma lição dos heterónimos.', u2)
        # m7-u3: a tarefa aceita qualquer verso de Mensagem. O verso de «O Infante» com a explicação feita fica só na grelha, como no
        # main (onde o enunciado dizia que o verso e o facto faltavam de propósito); o enunciado volta a dizê-lo.
        f3 = dados('m7-u3')['facil']
        self.assertEqual(len(f3['depois'][0]['exemplos']), 2)
        u3 = ler('tarefas/m7-u3/index.html')
        exemplos = ' '.join(re.findall(r'<details class="tf-so-tema tf-(?:exemplos|mais) tf-so-ecra">.*?</details>', u3, re.S))
        for fora in ('Deus quer, o homem sonha, a obra nasce', 'O Infante', 'O verso e o facto não estão neste exemplo'):
            self.assertNotIn(fora, exemplos, fora)
        self.assertNotIn('Deus quer, o homem sonha, a obra nasce.»', visivel(u3))
        self.assertIn('O verso de <i>Mensagem</i> e o facto datado faltam de propósito: no teu texto, entram depois de [S] ou de [M].', u3)
        self.assertIn('faltam de propósito: no teu texto, entram depois de [S] ou de [M].', base(GUIA))
        self.assertIn('«Deus quer, o homem sonha, a obra nasce.»', ler('tarefas/m7-u3/grelha/index.html'))
        self.assertEqual(u3.count('<summary>Ver dois exemplos com outros casos</summary>'), 1)


class DecisoesDoDocente(unittest.TestCase):
    def test_tempos_10_10_55_15_no_quadro_e_nos_relogios(self):
        for slug in SLUGS:
            pagina = ler(f'tarefas/{slug}/index.html')
            with self.subTest(slug=slug):
                quadro = pagina[pagina.index('<table class="tf-quadro">'):pagina.index('</table>')]
                tempos = [int(x) for x in re.findall(r'<th scope="row(?:group)?"[^>]*>(\d+)' + N + 'min</th>', quadro)]
                self.assertEqual(tempos, [10, 10, 55, 15, 90])
                self.assertEqual(sum(tempos[:4]), 90)
                self.assertEqual(pagina.count('data-max="10" data-passo="1" data-rotulo="Aquecimento"'), 1)
                self.assertEqual(pagina.count('data-max="55" data-passo="5" data-rotulo="Produção em papel"'), 1)
                self.assertNotRegex(visivel(pagina), r'\b60[ ' + N + r']min|\b5[ ' + N + r']min|10[ ' + N + r']a[ ' + N + r']15')
        self.assertEqual(ler('tarefas/m7-u2/index.html').count('data-max="2" data-passo="0.5" data-rotulo="Apresentação da voz"'), 1)
        # 13/11/2026, revisão: no índice do módulo, o aquecimento das três unidades tem 10 minutos (o da unidade 1 dizia «10 a 15 min»),
        # e nem o índice nem o mapa nem o guia dizem «10 a 15».
        indice = ler(INDICE)
        for rel in (INDICE, MAPA, GUIA):
            self.assertNotRegex(ler(rel), r'10[ ' + N + r']a[ ' + N + r']15', rel)
        chips = re.findall(r'<span class="t">(Aquecer para a aula de tarefa da Unidade' + N + r'?[ ]?\d)[^<]*</span>.*?<span class="chip">([^<]*)</span>', indice, re.S)
        self.assertEqual([c[1] for c in chips], ['10' + N + 'min'] * 3, chips)
        self.assertEqual(indice, base(INDICE).replace('<span class="chip">10' + N + 'a' + N + '15' + N + 'min</span>', '<span class="chip">10' + N + 'min</span>'))
        self.assertEqual(base(INDICE).count('<span class="chip">10' + N + 'a' + N + '15' + N + 'min</span>'), 1)
        for rel in ('tarefas/m7-u1/aquecimento/index.html', 'docs/pedagogia/aquecimentos/m7-u1.json'):
            self.assertNotIn('quinze', ler(rel))
            self.assertNotRegex(ler(rel), '60[ ' + N + ']minutos')
            self.assertIn('55' + N + 'minutos de produção', ler(rel))

    def test_consulta_uma_vez_versos_nao_contam_uma_ligacao_e_dez_perguntas(self):
        for slug in SLUGS:
            pagina, f = ler(f'tarefas/{slug}/index.html'), dados(slug)['facil']
            with self.subTest(slug=slug):
                texto = visivel(pagina)
                self.assertEqual(texto.count('com consulta'), 1)
                self.assertIn('podes usar as lições do site, o caderno e o dicionário', texto[:texto.index('O que entregas')])
                self.assertEqual(pagina.count('href="aquecimento/"'), 1)
                self.assertLessEqual(len(f['verificar']), 10)
                self.assertTrue(all(x.endswith('?') for x in f['verificar']))
                self.assertEqual(pagina.count('<label><input type="checkbox">'), len(f['verificar']))
                self.assertIn('Não conta' if slug == 'm7-u2' else NAO_CONTAM, texto)
                self.assertEqual(pagina.count('data-task-print'), 2)
                # 13/11/2026, revisão: a lista de cada tarefa pergunta pelas duas linhas finais, que o enunciado pede e a rubrica conta.
                self.assertIn('Escrevi as duas linhas finais?', f['verificar'])
        # 13/11/2026, revisão: a lista da m7-u3 tem dez perguntas e cobre o que o critério «Forma» da grelha exige (palavras, total,
        # conectores, escrita revista e as duas linhas), como a lista do main.
        v3 = dados('m7-u3')['facil']['verificar']
        self.assertEqual(len(v3), 10)
        self.assertIn('Citei um verso exato de <i>Mensagem</i>, entre «», indiquei o poema e expliquei-o no seu contexto?', v3)
        self.assertIn('Tenho 180' + N + 'a' + N + '220' + N + 'palavras, com o total no fim, e revi a escrita e os conectores?', v3)
        self.assertIn('180' + N + 'a' + N + '220' + N + 'palavras, conectores certos, texto revisto e as duas linhas.', base('tarefas/m7-u3/index.html'))
        # 13/11/2026, revisão: a regra da contagem diz-se com a mesma frase no enunciado, na grelha e no guia (como na m3-u2).
        self.assertEqual(visivel(ler('tarefas/m7-u3/index.html')).count(NAO_CONTAM), 1)
        self.assertIn('mais duas linhas finais. ' + NAO_CONTAM + ' O aquecimento em cartões não conta para a nota.</p>', ler('tarefas/m7-u3/grelha/index.html'))
        self.assertIn('mais duas linhas finais. ' + NAO_CONTAM + ' Ficheiro: M7_Tarefa3_Opiniao (fotografias).', ler(GUIA))
        self.assertIn(NAO_CONTAM, ler('tarefas/m3-u2/grelha/index.html'))
        for rel in ('tarefas/m7-u3/grelha/index.html', GUIA):
            self.assertNotIn('fora da contagem', ler(rel), rel)
        u3 = ler('tarefas/m7-u3/index.html')
        self.assertIn('A autoavaliação da grelha é só para ti: não se entrega.', u3)
        self.assertIn('Esta autoavaliação é só para ti: não se entrega.', ler('tarefas/m7-u3/grelha/index.html'))
        correcao = ler('tarefas/m7-u3/correcao/index.html')
        self.assertNotIn('Aluno</th>', correcao)
        self.assertNotIn('Diferença entre', correcao)

    def test_as_mesmas_palavras_em_todos_os_sitios(self):
        u3 = visivel(ler('tarefas/m7-u3/index.html'))
        self.assertEqual(len(re.findall(r'\btese\b', u3)), 1)  # só a ponte para as lições
        self.assertIn('Nas lições, a opinião que defendes chama-se «tese».', u3)
        for rel in ('tarefas/m7-u3/grelha/index.html', 'tarefas/m7-u3/correcao/index.html', 'tarefas/m7-u3/aquecimento/index.html',
                    'docs/pedagogia/aquecimentos/m7-u3.json'):
            with self.subTest(rel=rel):
                t = ler(rel)
                self.assertNotRegex(t, r'[Tt]ese\b')
                self.assertNotIn('outra voz', t)
                self.assertNotIn('confronto', t)
                self.assertNotIn('Fecho', t)
                self.assertIn('opinião', t)
        guia = ler(GUIA)
        tarefa2 = guia[guia.index('{"n":2,'):guia.index('{"n":3,')]
        self.assertNotRegex(tarefa2, r'[Tt]ese\b')
        self.assertNotIn('outra voz', tarefa2)
        self.assertIn('"Opinião e conclusão"', tarefa2)
        self.assertIn('"Facto ou comparação"', tarefa2)
        # os temas do aquecimento da m7-u3 dizem-se como no enunciado
        aq = ler('docs/pedagogia/aquecimentos/m7-u3.json')
        for frase in ('Concordas quando são outras pessoas a pagar o preço do sonho? Considera as mães, os filhos e as noivas da primeira estrofe.',
                      'Esperar que alguém volte para resolver os problemas dá força a um país ou tira-lhe força?'):
            self.assertIn(frase, aq)
            self.assertIn(frase.split('? ')[0], u3)
        # a grelha: cada troca ocorre (o gerador exige-o) e os pontos não mudam
        grelha = ler('tarefas/m7-u3/grelha/index.html')
        for palavra in ('Opinião e conclusão', 'Facto ou comparação', 'Duas linhas finais: ', 'que te ensinou esse movimento'):
            self.assertIn(palavra, grelha)
        # 13/11/2026, revisão: o mapa do módulo lista os critérios da tarefa da unidade 3 com os nomes da grelha, pela ordem da grelha.
        mapa = ler(MAPA)
        nomes = [c['nome'] for c in json.loads(ler(GRELHAS))['tarefas']['m7-u3']['criterios']]
        for a, b in json.loads(ler(GRELHAS))['tarefas']['m7-u3']['trocas_aluno']:
            nomes = [n.replace(a, b) for n in nomes]
        self.assertEqual(nomes, ['Opinião e conclusão', 'Movimentos', 'Verso de _Mensagem_', 'Facto ou comparação', 'Forma'])
        self.assertIn('<span class="crit">' + '; '.join(nomes).replace('_Mensagem_', '<i>Mensagem</i>') + '</span>', mapa)
        self.assertNotRegex(mapa, r'\bTese\b|outra voz')
        self.assertEqual(mapa, base(MAPA).replace('Tese e conclusão; Movimentos; Verso de <i>Mensagem</i>; Facto ou outra voz; Forma',
                                                  'Opinião e conclusão; Movimentos; Verso de <i>Mensagem</i>; Facto ou comparação; Forma'))
        # 13/11/2026, revisão: o guia diz «duas linhas finais», como os enunciados, e já não diz «síntese» (os guias do M3 e do M6 também não).
        self.assertNotIn('síntese', guia)
        for frase in ('com duas linhas finais; as retomas', 'escreves duas linhas finais no trabalho e entregas fotografias', 'das fontes e das duas linhas finais."'):
            self.assertEqual(guia.count(frase), 1, frase)
        self.assertEqual(base(GUIA).count('síntese'), 3)

    def test_guia_sem_autoavaliacao_nem_par_e_com_os_quatro_tempos(self):
        guia, antes = ler(GUIA), base(GUIA)
        blocos = json.loads(re.search(r'BLOCOS=(\[\[.*?\]\]),T=', guia).group(1))
        self.assertEqual([b[0] for b in blocos], [10, 10, 55, 15])
        self.assertEqual(re.findall(r'<b>([^<]*), (\d+)' + N + 'min</b>', guia), [('Aquecer', '10'), ('Ler o enunciado', '10'), ('Produzir', '55'), ('Rever, apresentar e entregar', '15')])
        self.assertEqual(guia.count('class="bloco"'), 4)
        for fora in ('Autoavaliação', 'AUTOAVALIAÇÃO', 'autoavaliação', 'r-auto', 'dataset.auto', 'par de trabalho', 'Três antes de mim', 'três antes de mim', 'dás-te um nível'):
            self.assertIn(fora, antes, fora)
            self.assertNotIn(fora, guia, fora)
        self.assertIn('<b>Dois antes de mim.</b> Antes de chamares o docente:<ol><li>relê o enunciado;</li><li>vê a rubrica.</li></ol>Só depois levantas o braço.', guia)
        self.assertEqual(guia.count('dois antes de mim'), 2)
        # a rubrica das três produções é a de antes, com as palavras do enunciado novo na da unidade 3
        pontos = lambda t: re.findall(r'"pontos":\[[\d,]+\]', t)
        self.assertEqual(pontos(guia), pontos(antes))
        # 13/11/2026, revisão: na unidade 2 (a produção 1 do guia), a entrega diz «das duas linhas finais» onde dizia «da síntese»; o
        # resto é igual, letra a letra.
        self.assertEqual(guia[guia.index('{"n":1,'):guia.index('{"n":2,')],
                         antes[antes.index('{"n":1,'):antes.index('{"n":2,')].replace('das fontes e da síntese."', 'das fontes e das duas linhas finais."'))
        self.assertEqual(guia[guia.index('{"n":3,'):guia.index('var ESTADO')], antes[antes.index('{"n":3,'):antes.index('var ESTADO')])
        portefolio, p_antes = ler(PORTEFOLIO), base(PORTEFOLIO)
        self.assertNotIn('trabalho de equipa', portefolio)
        self.assertEqual(portefolio, p_antes.replace(' trabalho de equipa,', ''))
        self.assertNotIn('0 a 20', p_antes)


class RegrasDoTexto(unittest.TestCase):
    def test_palavras_proibidas_sinais_e_qual(self):
        for slug in SLUGS:
            texto = visivel(ler(f'tarefas/{slug}/index.html'))
            with self.subTest(slug=slug):
                self.assertIsNone(PROIBIDAS.search(texto), PROIBIDAS.search(texto))
                self.assertNotIn('—', texto)
                # «·» só na navegação de sempre («M7 · Unidade N»)
                self.assertEqual(texto.count('·'), 1)
                # (fora dos versos: «Qual a Sorte a não dá.» é de Pessoa)
                sem_versos = visivel(re.sub(r'<div class="tt-versos">.*?</div>', ' ', ler(f'tarefas/{slug}/index.html'), flags=re.S))
                self.assertNotRegex(sem_versos, r'\bQual (?!d[aeo]s?\b|destas\b)')
                self.assertNotIn('Pedro', texto)
        for rel in (GUIA,):
            novo = ' '.join(e['new'] for e in MANIFESTO['files'][rel]['edits'])
            self.assertNotIn('—', novo)

    def test_referencias_que_nao_se_partem(self):
        for slug in SLUGS:
            # (sem o nome acessível das letras dos temas, «Tema A», que o molde põe só para os leitores de ecrã)
            texto = visivel(ler(f'tarefas/{slug}/index.html').replace('<span class="sr-only">Tema </span>', ''))
            with self.subTest(slug=slug):
                self.assertNotRegex(texto, r'\d (min|minutos|palavras)\b')
                self.assertNotRegex(texto, r'\b(Textos?|Lição|lição|versos?) (\d|F\d)')
                self.assertNotRegex(texto, r'\d (a|e|ou) \d')
                self.assertNotRegex(texto, r'\b[Tt]emas? [AB]\b')

    def test_contrato_das_paginas(self):
        for slug in SLUGS:
            pagina = ler(f'tarefas/{slug}/index.html')
            with self.subTest(slug=slug):
                self.assertEqual(re.findall(r'data-task-card-name="([^"]+)"', pagina), CARTOES[slug])
                # 13/11/2026, revisão: nenhum nome de cartão leva, no atributo, espaço que não parte nem o sinal que junta palavras.
                for nome in re.findall(r'data-task-card-name="([^"]*)"', pagina):
                    self.assertNotRegex(nome, '[\xa0\u2060]')
                self.assertIn('data-task-opening="Começar" data-task-index="nomes"', pagina)
                self.assertEqual(pagina.count('task-textos.css?v=20261113-facil-11'), 1)
                self.assertEqual(pagina.count('task-reader.js?v=20261112-facil-7'), 1)
                ids = re.findall(r'\bid="([^"]+)"', pagina)
                self.assertEqual(len(ids), len(set(ids)))
                for alvo in re.findall(r'href="#([^"]+)"', pagina):
                    self.assertIn(alvo, ids)
                for i in ('aquecer', 'produzir', 'entregar', 'apoios', 'criterios'):
                    self.assertIn(i, ids)
                self.assertIn('<p class="task-kicker">Tarefa individual, 90' + N + 'minutos</p>', pagina)
                # as lições ligadas existem e têm as secções que a página manda reler
                f = dados(slug)['facil']
                for x in f['rever']:
                    licao = re.search(r'href="\.\./\.\./(m7/licao-m7-f\d+)/"', x['texto']).group(1)
                    rots = {c.get('rot') for c in cartoes(licao + '/index.html')}
                    for seccao in re.findall(r'Relê(?: os versos de Reis em)? «([^»]+)»', x['texto']) + re.findall(r' e «(Para levar|O essencial)»', x['texto']):
                        self.assertIn(seccao, rots, (slug, licao, seccao))
        self.assertEqual(ler('tarefas/m7-u3/index.html').count('data-task-choice'), 1)
        for slug in ('m7-u1', 'm7-u2'):
            self.assertIn('data-task-individual', ler(f'tarefas/{slug}/index.html'))
            self.assertNotIn('data-task-choice', ler(f'tarefas/{slug}/index.html'))
        css = ler('assets/task-textos.css')
        for marca in ('facil-11', 'data-task-individual'):
            self.assertIn(marca, css)
        # 13/11/2026, revisão: a regra da tabela num ecrã estreito vale só para a tabela do apoio da m7-u3 (.tf-tabela-apoio); o quadro
        # das modalidades da m3-u2, que também é uma .tf-tabela num desdobrável, fica como o main o tinha.
        self.assertIn('[data-task-facil] details.tf-mais .tf-tabela.tf-tabela-apoio :is(th,td){padding:6px 6px;overflow-wrap:anywhere}', css)
        self.assertNotIn('details.tf-mais .tf-tabela :is(th,td)', css)
        com_tabela = sorted(p.parent.name for p in (ROOT / 'tarefas').glob('*/index.html') if 'class="tf-tabela' in p.read_text('utf-8'))
        self.assertEqual(com_tabela, ['m3-u2', 'm7-u3'])
        self.assertEqual(ler('tarefas/m7-u3/index.html').count('<table class="tf-tabela tf-tabela-apoio">'), 1)
        self.assertNotIn('tf-tabela-apoio', ler('tarefas/m3-u2/index.html'))
        css_base = base('assets/task-textos.css')
        self.assertTrue(css.startswith(css_base[:css_base.index('@media print{')]))


class GeradoresEOutrosModulos(unittest.TestCase):
    def test_os_geradores_dao_as_paginas_da_arvore(self):
        with tempfile.TemporaryDirectory() as tmp:
            for cmd in (['scripts/tarefas_escolha.py', '--saida', tmp], ['scripts/grelhas_tarefas.py', '--saida', tmp],
                        ['scripts/tarefas_individuais_faceis.py', '--saida', tmp], ['scripts/aquecimentos.py', '--saida', tmp]):
                r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            geradas = sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob('index.html'))
            self.assertGreaterEqual(len(geradas), 13 + 26 + 2 + 20)
            for rel in geradas:
                self.assertEqual((Path(tmp) / rel).read_bytes(), (ROOT / rel).read_bytes(), rel)
            for rel in ENUNCIADOS + [f for f in FICHEIROS if f.startswith('tarefas/')]:
                self.assertIn(rel, geradas)

    def test_as_tarefas_dos_outros_modulos_sao_as_do_main_de_partida(self):
        r = subprocess.run(['git', 'ls-tree', '-r', '--name-only', BASE_COMMIT, 'tarefas', 'docs/pedagogia/tarefas-escolha', 'docs/pedagogia/aquecimentos'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        nomes = r.stdout.split()
        self.assertGreater(len(nomes), 80)
        iguais = 0
        for rel in nomes:
            if rel in FICHEIROS:
                continue
            self.assertEqual((ROOT / rel).read_bytes(), subprocess.run(['git', 'show', f'{BASE_COMMIT}:{rel}'], cwd=ROOT, capture_output=True).stdout, rel)
            iguais += 1
        # 13/11/2026, revisão: eram 10 os ficheiros da camada nestas pastas; com os acertos do M1 e do M5 são 17 (mais os dados, o
        # enunciado e a grelha da m1-u2 e da m5-u1 e a grelha da m5-u2). Todos os outros continuam iguais ao main, byte a byte, e
        # também as versões de correção e os aquecimentos da m1-u2, da m5-u1 e da m5-u2.
        self.assertEqual(iguais, len(nomes) - 17)
        self.assertEqual(len([f for f in FICHEIROS if f in nomes]), 17)
        for rel in ('tarefas/m1-u2/correcao/index.html', 'tarefas/m5-u1/correcao/index.html', 'tarefas/m5-u2/correcao/index.html', 'tarefas/m5-u2/index.html',
                    'tarefas/m1-u1/index.html', 'tarefas/m5-u1/aquecimento/index.html', 'tarefas/m3-u2/index.html', 'docs/pedagogia/tarefas-escolha/m5-u2.json'):
            self.assertIn(rel, nomes)
            self.assertNotIn(rel, FICHEIROS)


class Camada(unittest.TestCase):
    def test_no_topo_com_manifesto_e_reversivel_ate_a_base(self):
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(len(verificar_camadas.LAYERS), 51)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(FICHEIROS), 22)
        self.assertEqual(len(set(FICHEIROS)), 22)
        for rel in FICHEIROS:
            with self.subTest(rel=rel):
                texto = ler(rel)
                desfeito = undo_tarefas_faceis_m7_1113(rel, texto)
                self.assertNotEqual(desfeito, texto)
                self.assertEqual(desfeito, base(rel))
                # e de volta, letra a letra
                for e in MANIFESTO['files'][rel]['edits']:
                    self.assertEqual(desfeito.count(e['old']), e['occurrences'])
                    desfeito = desfeito.replace(e['old'], e['new'])
                self.assertEqual(desfeito, texto)
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('0 por aplicar; manifesto em dia', r.stdout)

    def test_o_gerador_da_camada_da_o_mesmo_json(self):
        import tarefas_faceis_m7_20261113 as camada
        todas, finais = camada.construir()
        self.assertEqual(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', ler(CAMADA_REL))
        self.assertEqual(sorted(finais), sorted(FICHEIROS))
        self.assertEqual(camada.BASE_COMMIT, BASE_COMMIT)
        for troca in todas:
            self.assertTrue(troca['achado'].startswith('13/11/2026: '))

    def test_registada_na_auditoria_no_desligar_na_leitura_historica_e_nos_fluxos(self):
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertRegex(auditoria, r'def undo_tarefas_faceis_m6_1113\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_tarefas_faceis_m7_1113\(path, text\)\n')
        self.assertIn("tarefas_faceis_m7 = ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'", ler('scripts/desligar_sala.py'))
        historico = ler('scripts/tarefas_claras_historico.py')
        self.assertLess(historico.index('TAREFAS_FACEIS_M7.get(rel)'), historico.index('TAREFAS_FACEIS_M6.get(rel)'))
        for nome in ('tarefas_faceis_m1_20261113', 'tarefas_faceis_m3_20261112', 'tarefas_faceis_m5_20261113', 'tarefas_faceis_m6_20261113'):
            self.assertIn("m7 = ROOT / 'tests/fixtures/tarefas-faceis-m7-edits-20261113.json'", ler(f'scripts/{nome}.py'), nome)
        m6, m7 = 'tests/fixtures/tarefas-faceis-m6-edits-20261113.json', MANIFESTO_REL
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')):
            fluxo = p.read_text('utf-8')
            # em todas as cadeias, a camada do M7 desfaz-se logo antes da do M6, sem nada pelo meio
            self.assertEqual(fluxo.count(f'--desfazer-antes {m6}'), fluxo.count(f'--desfazer-antes {m7} --desfazer-antes {m6}'), p.name)
            self.assertEqual(fluxo.count(f'--desfazer-antes {m7}'), fluxo.count(f'--verificar --desfazer-antes {m7}'), p.name)
            self.assertEqual(fluxo.count("'scripts/tarefas_faceis_m6_20261113.*'"), fluxo.count("'scripts/tarefas_faceis_m7_20261113.*'"), p.name)
        # 13/11/2026, revisão: a camada passou a mudar o índice do M7, e o gerador da decisão 148 e os três testes de navegador que leem
        # os índices como eram desfazem-na primeiro, antes da do M6.
        cartaz = ler('scripts/cartaz_indices_148_20261106.py')
        self.assertLess(cartaz.index('if TAREFAS_FACEIS_M7.is_file():'), cartaz.index('if TAREFAS_FACEIS_M6.is_file():'))
        for nome in ('browser_cartaz_indices.cjs', 'browser_cartaz_m4_piloto.cjs', 'browser_creditos_i_pt1.cjs'):
            cjs = ler('tests/' + nome)
            self.assertEqual(cjs.count('for(const e of [...((tarefasFaceisM7['), 1, nome)
            self.assertLess(cjs.index('for(const e of [...((tarefasFaceisM7['), cjs.index('for(const e of [...((tarefasFaceisM6['), nome)
        # e as camadas do M1 e do M5, cujos ficheiros os acertos mudam, continuam fechadas: conferem com esta desfeita primeiro
        for nome, fixo in (('tarefas_faceis_m1_20261113', 'tarefas-faceis-m1-edits-20261113'), ('tarefas_faceis_m5_20261113', 'tarefas-faceis-m5-edits-20261113')):
            outro = json.loads(ler(f'tests/fixtures/{fixo}.json'))['files']
            self.assertTrue(set(ACERTOS) & set(outro), nome)
            self.assertEqual(base(f'scripts/{nome}.json'), ler(f'scripts/{nome}.json'), nome)
            self.assertEqual(base(f'tests/fixtures/{fixo}.json'), ler(f'tests/fixtures/{fixo}.json'), nome)
        self.assertEqual(set(ACERTOS) - set(json.loads(ler('tests/fixtures/tarefas-faceis-m1-edits-20261113.json'))['files'])
                         - set(json.loads(ler('tests/fixtures/tarefas-faceis-m5-edits-20261113.json'))['files']), set())
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m6_20261113.json --manifesto {m6} --verificar --desfazer-antes {m7}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m7_20261113.json --manifesto {m7} --verificar\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m7.py' -v\n", tarefas)
        self.assertIn('run: python tests/browser_tarefas_faceis_m7.py\n', tarefas)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), 1)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), base('.github/workflows/pt-tarefas-qa.yml').count('timeout-minutes: 40'))


class Acertos(unittest.TestCase):
    """13/11/2026: os três acertos do M1 e do M5 que o docente mandou ir neste pedido. As camadas do M1 e do M5 não se reescrevem: os
    acertos ficam nesta camada, por cima delas (como os dois acertos do M3 ficaram na camada do M5)."""

    def mudou(self, rel):
        """As linhas que mudam entre a base e a árvore: [(antes, agora)]."""
        import difflib
        a, b = base(rel).split('\n'), ler(rel).split('\n')
        return [('\n'.join(a[i1:i2]), '\n'.join(b[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op != 'equal']

    def test_a_m1_u2_a_passagem_copiada_nao_conta(self):
        frase = 'Não contam para as palavras da crónica: as respostas, a passagem copiada, as fontes e as duas linhas finais.'
        d = json.loads(ler('docs/pedagogia/tarefas-escolha/m1-u2.json'))
        self.assertEqual(d['facil']['quadro']['notas'][1], frase)
        # nos dados, só essa frase muda
        self.assertEqual(self.mudou('docs/pedagogia/tarefas-escolha/m1-u2.json'),
                         [('    "Não contam para as palavras da crónica: as respostas, as fontes e as duas linhas finais."', f'    "{frase}"')])
        enunciado, grelha = ler('tarefas/m1-u2/index.html'), ler('tarefas/m1-u2/grelha/index.html')
        self.assertEqual(enunciado, base('tarefas/m1-u2/index.html').replace('as respostas, as fontes e as duas linhas finais.', 'as respostas, a passagem copiada, as fontes e as duas linhas finais.'))
        self.assertEqual(visivel(enunciado).count(frase), 1)
        # a grelha diz o mesmo, com as mesmas palavras, e o que mais custa também
        self.assertEqual(grelha.count(frase + ' O aquecimento não conta para a nota.</p>'), 1)
        self.assertEqual(grelha.count('Contar as respostas, a passagem copiada, as fontes ou as duas linhas finais nas 160 a 200' + N + 'palavras da crónica.'), 1)
        self.assertNotIn('ficam fora da contagem', grelha)
        self.assertEqual(len(self.mudou('tarefas/m1-u2/grelha/index.html')), 1)
        # o tema A continua a pedir a passagem copiada, e os números são os de antes
        self.assertIn('Inclui uma passagem copiada exatamente do capítulo escolhido.', enunciado)
        self.assertIn('160' + N + 'a' + N + '200', enunciado)
        # a versão de correção não diz o que conta para as palavras: fica igual ao main
        correcao = ler('tarefas/m1-u2/correcao/index.html')
        self.assertEqual(correcao, base('tarefas/m1-u2/correcao/index.html'))
        self.assertNotRegex(correcao, r'contagem|[Nn]ão contam')

    def test_b_m5_u1_a_carta_de_exemplo_so_com_materia_das_licoes(self):
        d = json.loads(ler('docs/pedagogia/tarefas-escolha/m5-u1.json'))
        antes = json.loads(base('docs/pedagogia/tarefas-escolha/m5-u1.json'))
        x, xa = d['facil']['temas'][0]['material']['exemplos'][0], antes['facil']['temas'][0]['material']['exemplos'][0]
        carta = x['paragrafos'][0]['t']
        self.assertEqual(carta, 'Em casa, [dia, mês e ano]. Meu filho: hás de perguntar porque te escrevo outra vez. Escrevo porque espero a tua resposta. '
                                'Lembras-te das outras cartas? Escrevi-as, e «não recebia resposta». O teu silêncio é uma porta fechada. Deus te guarde. Tua mãe.')
        # nos dados, só muda este exemplo: a carta e mais uma linha sobre a data
        self.assertEqual(x['paragrafos'][1], xa['paragrafos'][1])
        self.assertEqual(x['paragrafos'][2:], ['A data fica entre parênteses retos porque as lições não a dão.'])
        self.assertEqual((x['titulo'], len(xa['paragrafos'])), (xa['titulo'], 2))
        x['paragrafos'] = xa['paragrafos']
        self.assertEqual(d, antes)
        # o que a carta de antes inventava já não está, nem no enunciado nem na grelha
        enunciado, grelha = ler('tarefas/m5-u1/index.html'), ler('tarefas/m5-u1/grelha/index.html')
        for fora in ('dia de Natal', 'todos os dias', 'Foram tantas', 'ainda pensa em ti', 'aqui está tudo como deixaste'):
            self.assertIn(fora, base('tarefas/m5-u1/grelha/index.html'), fora)
            for pagina in (enunciado, grelha, ler(GRELHAS)):
                self.assertNotIn(fora, pagina, fora)
        # a matéria é a da lição F17, letra a letra: a mãe escrevia, não recebia resposta e pensava que o filho não respondia
        f17 = html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler('m5/licao-m5-f17/index.html')))
        self.assertIn('«Escrevia a mãe a Simão, e não recebia resposta. Pensava ela que o filho não respondia: anos depois, vimos entre os papéis de meu pai todas as cartas que ela escrevera.', re.sub(r'\s+', ' ', f17))
        self.assertEqual(re.findall(r'«([^«»]+)»', carta), ['não recebia resposta'])
        self.assertIn('Respeitei o romance: a mãe escrevia a Simão e pensava que o filho não respondia.', x['paragrafos'][1]['t'])
        # a carta não tem números nem nomes de lugares ou de dias que as lições não deem para estas cartas
        self.assertNotRegex(carta, r'\d|Natal|Viseu|Porto|Coimbra|janeiro|março|domingo')
        # o exemplo não usa os textos da tarefa (nenhuma sequência de quatro palavras) nem as passagens reservadas do aquecimento
        blocos = re.findall(r'<section class="tt-texto[^"]*" id="texto-\d".*?</section>', enunciado, re.S)
        self.assertEqual(len(blocos), 3)
        textos = ' ' + ' '.join(re.findall(r"[\w'’-]+", html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(blocos))))).casefold() + ' '
        palavras = re.findall(r"[\w'’-]+", carta + ' ' + x['paragrafos'][1]['t'])
        for k in range(len(palavras) - 3):
            self.assertNotIn(' ' + ' '.join(palavras[k:k + 4]).casefold() + ' ', textos)
        for r in json.loads(ler('docs/pedagogia/aquecimentos/m5-u1.json'))['reservadas']:
            self.assertNotIn(r, carta, r)
        # o enunciado e a grelha usam o mesmo exemplo, e o exemplo parcial da grelha é a mesma carta, sem o que falta
        self.assertEqual(enunciado.count(carta), 1)
        self.assertEqual(grelha.count(carta), 1)
        self.assertEqual(grelha.count('A: Em casa, [dia, mês e ano]. Meu filho: escrevo-te outra vez. Deus te guarde. Tua mãe. (As marcas estão todas;'), 1)
        self.assertEqual(grelha.count('A data fica entre parênteses retos porque as lições não a dão.'), 1)
        self.assertEqual(enunciado.count('<p class="tf-p">A data fica entre parênteses retos porque as lições não a dão.</p>'), 1)
        # no enunciado, só o desdobrável do exemplo muda
        self.assertEqual(len(self.mudou('tarefas/m5-u1/index.html')), 1)
        self.assertIn('Outra voz: uma carta inventada da mãe de Simão ao filho', self.mudou('tarefas/m5-u1/index.html')[0][1])
        self.assertEqual(ler('tarefas/m5-u1/correcao/index.html'), base('tarefas/m5-u1/correcao/index.html'))

    def test_c_grelha_do_m5_os_exemplos_ja_nao_citam_os_textos_da_tarefa(self):
        g, ga = json.loads(ler(GRELHAS))['tarefas'], json.loads(base(GRELHAS))['tarefas']
        u1, u2 = ler('tarefas/m5-u1/grelha/index.html'), ler('tarefas/m5-u2/grelha/index.html')
        # m5-u1, rigor: saiu a frase do capítulo IV (um texto da tarefa) e entrou uma frase de outra obra, que a lição F16 dá
        self.assertIn('«a violencia de um pae é sempre amor» (cap.' + N + 'IV)', ga['m5-u1']['criterios'][3]['niveis']['max'][1])
        self.assertIn('a violencia de um pae é sempre amor', ler('tarefas/m5-u1/index.html'))  # o texto da tarefa continua na página
        self.assertNotIn('a violencia de um pae', u1)
        self.assertNotIn('a violência e o amor', u1)
        self.assertNotIn('a violencia de um pae', json.dumps(g['m5-u1'], ensure_ascii=False))
        rigor = g['m5-u1']['criterios'][3]['niveis']
        self.assertEqual(rigor['max'][1], 'Noutra obra: «O latim era um luxo d’erudito» (_Os Maias_, cap.' + N + 'III, lição F16): copio d’erudito como está na edição, sem o corrigir.')
        self.assertEqual(rigor['parcial'][1], 'Noutra obra: cito a frase de _Os Maias_ sobre o latim com a grafia de hoje, e sem dizer de que capítulo é.')
        self.assertEqual(rigor['0'], ga['m5-u1']['criterios'][3]['niveis']['0'])
        f16 = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>|\\n', ' ', ler('m5/licao-m5-f16/index.html'))))
        self.assertIn('No capítulo III, Brown adia o latim', f16)
        self.assertIn('«O latim era um luxo d’erudito»', f16)
        for rel in ('tarefas/m5-u1/index.html', 'tarefas/m5-u2/index.html', 'docs/pedagogia/aquecimentos/m5-u1.json', 'docs/pedagogia/aquecimentos/m5-u2.json'):
            self.assertNotIn('luxo d', ler(rel), rel)
        self.assertEqual(u1.count('Noutra obra: «O latim era um luxo d’erudito» (<i>Os Maias</i>, cap.' + N + 'III, lição F16): copio d’erudito como está na edição, sem o corrigir.'), 1)
        # m5-u2, tema A: o exemplo é o mesmo (a paragem de autocarro) e já não cita «Sole normande?»; diz o gesto com as palavras do enunciado
        self.assertIn('Imitei o «Sole normande?»: uma coisa banal', ga['m5-u2']['criterios'][2]['niveis']['max'][1])
        self.assertEqual(g['m5-u2']['criterios'][2]['niveis']['max'][1],
                         ga['m5-u2']['criterios'][2]['niveis']['max'][1].replace('Imitei o «Sole normande?»:', 'Imitei a interrupção do jantar do Hotel Central:'))
        self.assertNotIn('Sole normande', u2)
        self.assertNotIn('Sole normande', json.dumps(g['m5-u2'], ensure_ascii=False))
        self.assertEqual(u2.count('Imitei a interrupção do jantar do Hotel Central: uma coisa banal, o autocarro, corta a conversa séria e ninguém volta a ela.'), 1)
        enunciado = ler('tarefas/m5-u2/index.html')
        self.assertIn('interrompida por algo banal, como no Hotel Central', enunciado)
        self.assertIn('A interrupção está nos parágrafos', enunciado)
        self.assertEqual(enunciado, base('tarefas/m5-u2/index.html'))
        self.assertEqual(len(self.mudou('tarefas/m5-u2/grelha/index.html')), 1)
        # nenhuma citação «…» dos exemplos de qualquer das duas grelhas ocorre nos textos da sua tarefa
        for slug in ('m5-u1', 'm5-u2'):
            pagina = ler(f'tarefas/{slug}/index.html')
            textos = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(re.findall(r'<section class="tt-texto[^"]*" id="texto-\d".*?</section>', pagina, re.S))))).casefold()
            self.assertGreater(len(textos), 3000)
            exemplos = ' '.join(v[1] for c in g[slug]['criterios'] for v in c['niveis'].values())
            citacoes = re.findall(r'«([^«»]+)»', exemplos.replace('“', '«').replace('”', '»'))
            self.assertGreaterEqual(len(citacoes), 5, slug)
            for c in citacoes:
                if len(c.split()) >= 2:
                    self.assertNotIn(c.casefold().rstrip('.!?'), textos, (slug, c))
        # as versões de correção não mostram exemplos: ficam iguais ao main
        for rel in ('tarefas/m5-u1/correcao/index.html', 'tarefas/m5-u2/correcao/index.html'):
            self.assertEqual(ler(rel), base(rel))


if __name__ == '__main__':
    unittest.main()
