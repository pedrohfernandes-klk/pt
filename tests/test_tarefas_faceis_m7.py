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
FICHEIROS = ['docs/pedagogia/tarefas-escolha/m7-u3.json', GRELHAS, 'docs/pedagogia/aquecimentos/m7-u1.json', 'docs/pedagogia/aquecimentos/m7-u3.json',
             'tarefas/m7-u1/index.html', 'tarefas/m7-u2/index.html', 'tarefas/m7-u1/aquecimento/index.html', 'tarefas/m7-u3/index.html',
             'tarefas/m7-u3/grelha/index.html', 'tarefas/m7-u3/aquecimento/index.html', 'tarefas/m7-u3/correcao/index.html', GUIA, PORTEFOLIO]
CARTOES = {'m7-u1': ['A comparação', 'Fechar e entregar', 'Rever a matéria'],
           'm7-u2': ['Parte' + N + '1: o perfil', 'Parte' + N + '2: o texto', 'Parte' + N + '3: escolhas e fontes', 'Parte' + N + '4: a apresentação', 'Fechar e entregar', 'Rever a matéria'],
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
        for slug in antes:
            if slug != 'm7-u3':
                self.assertEqual(agora[slug], antes[slug], slug)
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
                       'Quem está ao pé dele está só ao pé dele', 'a vida inventada prepara o estilo',
                       'Estes dados ajudam a caracterizar a figura, mas não explicam, por si sós, a presença de máquinas ou o verso livre',
                       'Hoje levantei catorze contentores.', 'Deus quer, o homem sonha, a obra nasce.', 'Estou hoje vencido, embora não saiba a verdade',
                       'Artificial, sim, artificial, porque escolheu cada pausa em vez de a deixar ao acaso.'):
            self.assertIn(trecho, fontes, trecho)


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
                self.assertNotRegex(visivel(pagina), r'\b60[ ' + N + r']min|\b5[ ' + N + r']min|10 a 15')
        self.assertEqual(ler('tarefas/m7-u2/index.html').count('data-max="2" data-passo="0.5" data-rotulo="Apresentação da voz"'), 1)
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
                self.assertIn('Não conta' if slug == 'm7-u2' else 'Não contam para as palavras: os versos citados ou copiados e as duas linhas finais.', texto)
                self.assertEqual(pagina.count('data-task-print'), 2)
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
        self.assertEqual(guia[guia.index('{"n":1,'):guia.index('{"n":2,')], antes[antes.index('{"n":1,'):antes.index('{"n":2,')])
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
        self.assertEqual(iguais, len(nomes) - 10)
        for rel in ('m7/index.html', 'm7/mapa-do-modulo-m7/index.html'):
            self.assertEqual(ler(rel), base(rel))


class Camada(unittest.TestCase):
    def test_no_topo_com_manifesto_e_reversivel_ate_a_base(self):
        self.assertEqual(verificar_camadas.LAYERS[0], ('tarefas_faceis_m7_20261113', 'tarefas-faceis-m7-edits-20261113'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('tarefas_faceis_m6_20261113', 'tarefas-faceis-m6-edits-20261113'))
        self.assertEqual(len(verificar_camadas.LAYERS), 51)
        self.assertEqual(MANIFESTO['base_commit'], BASE_COMMIT)
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
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
            self.assertEqual(fluxo.count(f'--desfazer-antes {m6}'), fluxo.count(f'--desfazer-antes {m7} --desfazer-antes {m6}')
                             + fluxo.count(f'tarefas_faceis_m5_20261113.json --manifesto tests/fixtures/tarefas-faceis-m5-edits-20261113.json --verificar --desfazer-antes {m7} --desfazer-antes {m6}') * 0, p.name)
            self.assertEqual(fluxo.count("'scripts/tarefas_faceis_m6_20261113.*'"), fluxo.count("'scripts/tarefas_faceis_m7_20261113.*'"), p.name)
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m6_20261113.json --manifesto {m6} --verificar --desfazer-antes {m7}\n', tarefas)
        self.assertIn(f'python scripts/aplicar_trocas.py scripts/tarefas_faceis_m7_20261113.json --manifesto {m7} --verificar\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_tarefas_faceis_m7.py' -v\n", tarefas)
        self.assertIn('run: python tests/browser_tarefas_faceis_m7.py\n', tarefas)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), 1)
        self.assertEqual(tarefas.count('timeout-minutes: 40'), base('.github/workflows/pt-tarefas-qa.yml').count('timeout-minutes: 40'))


if __name__ == '__main__':
    unittest.main()
