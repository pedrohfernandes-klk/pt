"""Aquecimentos em cartões antes das aulas de tarefa (29/10/2026, decisões do docente; piloto no M7).

Contrato: cada tarefa do M7 tem uma página própria de cartões, tarefas/<slug>/aquecimento/, gerada por
scripts/aquecimentos.py a partir de docs/pedagogia/aquecimentos/<slug>.json. A página grava só a chave
«aquecimento-<slug>» (não conta como lição, não mexe no «Continuar», não grava em projeção), o baralho passa no validador
do sítio e nas regras de escrita, as citações estão letra a letra nas lições indicadas e nenhum cartão de fazer usa as
passagens reservadas à tarefa (o aquecimento não faz a tarefa por ti). A tarefa liga ao aquecimento no cartão
«Enunciado» e o percurso tem a linha «A» logo antes da linha «T». Fica fora de audit_cards.audit() (as 109 lições).

29/10/2026: a unidade 3 do M7 deixa o «Dia Pessoa» (tarefa nova «Louco, sim», F10 reescrita como «Argumentar com
versos», página da visita como caderno de campo facultativo) e a U2 faz as apresentações em pequenos grupos.

29/10/2026 (revisão pedagógica e técnica): as citações da U3 e da F10 conferem-se só nas lições que esta camada não
escreve; o validador olha também para o título, a descrição e o menu, e não distingue maiúsculas nas passagens reservadas;
os diapositivos ligados não trazem o «Dia Pessoa»; o guia diz o mesmo que as tarefas (blocos de 90 minutos, aquecimento,
nomes de ficheiro do portefólio).
"""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs/pedagogia/aquecimentos'
SLUGS = ['m7-u1', 'm7-u2', 'm7-u3']
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards, validate_cards  # noqa: E402
# 29/10/2026 (revisão técnica, P1): as lições do M7 de onde vêm as citações da unidade 3, nenhuma escrita nesta camada.
sys.path.insert(0, str(ROOT / 'tests'))
from test_task_choice import WARM_LESSONS  # noqa: E402

_spec = importlib.util.spec_from_file_location('aquecimentos', ROOT / 'scripts/aquecimentos.py')
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
FORA = {'.git', '.github', 'tests', 'scripts', 'docs', 'tools', 'node_modules'}


def dados(slug):
    return json.loads((DADOS / f'{slug}.json').read_text('utf-8'))


def pagina(slug):
    return (ROOT / 'tarefas' / slug / 'aquecimento' / 'index.html').read_text('utf-8')


def publicados():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if p.is_file() and p.suffix in ('.html', '.js') and not (set(rel.parts) & FORA):
            yield rel.as_posix(), p.read_text('utf-8', errors='replace')


class Lista(HTMLParser):
    def __init__(self, s):
        super().__init__()
        self.li = []
        self.feed(s)

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.li.append(dict(attrs))


class Aquecimentos(unittest.TestCase):
    def test_dados_publicos_e_gerador_idempotente(self):
        self.assertEqual(sorted(p.stem for p in DADOS.glob('*.json')), SLUGS)
        for slug in SLUGS:
            d = dados(slug)
            with self.subTest(aquecimento=slug):
                self.assertEqual(d['slug'], slug)
                self.assertFalse({'grelha', 'provas', 'notas_docente', 'chave'} & set(d))
                self.assertEqual(A.validar(ROOT, d), [])
                self.assertTrue(d.get('reservadas'))
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, '-B', 'scripts/aquecimentos.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            for slug in SLUGS:
                with self.subTest(aquecimento=slug):
                    self.assertEqual((Path(tmp) / 'tarefas' / slug / 'aquecimento' / 'index.html').read_bytes(),
                                     (ROOT / 'tarefas' / slug / 'aquecimento' / 'index.html').read_bytes())

    def test_baralho_validado_e_lido_pelo_auditor(self):
        for slug in SLUGS:
            d, s = dados(slug), pagina(slug)
            cartoes = lesson_cards(ROOT / 'tarefas' / slug / 'aquecimento' / 'index.html')
            with self.subTest(aquecimento=slug):
                self.assertEqual(cartoes, d['cartoes'])
                self.assertEqual(validate_cards(cartoes), [])
                self.assertTrue(10 <= len(cartoes) <= 14, len(cartoes))
                fazer = [c for c in cartoes if c['t'] != 'ler']
                self.assertGreaterEqual(len(fazer), 10)
                self.assertEqual(cartoes[0]['t'], 'ler')
                self.assertEqual(cartoes[-1].get('rot'), 'Para levar')
                for c in fazer:
                    if c['t'] in ('escolha', 'rever'):
                        # Três opções: o motor mostra todas, e todas as explicações se veem.
                        self.assertEqual(len(c['o']), 3)
                        self.assertEqual(sum(x is None for x in c['fe']), 1)
                    else:
                        self.assertTrue(c.get('fe'))
                # rever-frase.js só quando há um cartão «rever» (o tipo não vive em jogo.js)
                self.assertEqual('rever-frase.js' in s, any(c['t'] == 'rever' for c in cartoes))
        # O auditor das 109 lições não conta estas páginas.
        self.assertEqual(len(list(ROOT.glob('m[1-9]/licao-*/index.html'))), 109)

    def test_o_validador_recusa_o_que_deve(self):
        d = dados('m7-u3')
        estragado = json.loads(json.dumps(d))
        c = estragado['cartoes'][1]
        c['pares'][0][0] = '«Valeu a pena? Tudo vale a pena / Se a alma não for pequena.»'   # citação falsa
        estragado['cartoes'][6]['fe'][1] = ''                                                 # explicação em falta
        estragado['cartoes'][4]['f'] += ' Vamos jogar.'                                       # palavra proibida
        estragado['cartoes'][5]['p'] = 'Que palavra dá força a um país?'                      # passagem reservada
        estragado['cartoes'][8]['f'] += ' Fim — e pronto.'                                    # travessão
        # 29/10/2026 (revisão técnica, P4): passagem reservada com maiúscula, e palavra proibida fora dos cartões.
        estragado['cartoes'][3]['p2'] = 'Alguém volte e resolva: liga cada oração.'
        estragado['descricao'] += ' Vamos jogar.'
        erros = ' '.join(A.validar(ROOT, estragado))
        for marca in ('não está letra a letra', 'não diz porquê', "'\\\\bjog'", 'reservada', "'—'",
                      '«alguém volte e resolva»', 'título, descrição ou menu'):
            self.assertIn(marca, erros)

    def test_chave_propria_sem_licao_nem_continuar(self):
        for slug in SLUGS:
            s = pagina(slug)
            with self.subTest(aquecimento=slug):
                self.assertIn(f'var K="aquecimento-{slug}"', s)
                self.assertEqual(s.count('chave:K'), 1)
                for proibido in ('epi-ultima', 'localStorage', 'sessionStorage', 'ntfy', 'EPISala'):
                    self.assertNotIn(proibido, s)
                # O único nome de chave na página é o do aquecimento (os menus ligam às lições, mas nada grava licao-…).
                self.assertEqual(re.findall(r'"((?:licao|percurso|desafio|epi-pt|aquecimento)-[a-z0-9-]+)"', s), [f'aquecimento-{slug}'])
                # Casca, aparência, projeção e o regresso à tarefa e à unidade.
                # 29/10/2026 (revisão pedagógica, C8): o menu diz quando se faz o aquecimento, como a tarefa e a linha A.
                self.assertIn(f'<p>Módulo 7 · {dados(slug)["momento"]}<br>Unidade {slug[-1]}</p>', s)
                for marca in ('assets/pt-lessons/casca.js', 'assets/pt-lessons/jogo.js', 'assets/appearance.css', 'assets/appearance.js',
                              'assets/projection-launcher.js', '<a class="c-marca" href="../"', '"seguinte": "../"',
                              f'data-unit-return="../../../m7/#unidade-pedagogica-{slug[-1]}"', '<a href="?projetar=1">Projetar para a turma</a>',
                              'não conta para a nota'):
                    self.assertIn(marca, s)
                self.assertEqual(s.count('<style id="casca-pc">'), 1)
                texto = re.sub(r'<[^>]+>', ' ', s.split('<body', 1)[1].split('<script>document.addEventListener', 1)[0])
                for proibido in ('jogar', 'ficha', 'folha', 'professor', '—'):
                    self.assertNotIn(proibido, texto.lower())

    def test_ligacao_no_enunciado_e_linha_a_no_percurso(self):
        indice = (ROOT / 'm7/index.html').read_text('utf-8')
        items = Lista(indice).li
        for n, slug in enumerate(SLUGS, 1):
            tarefa = (ROOT / 'tarefas' / slug / 'index.html').read_text('utf-8')
            with self.subTest(tarefa=slug):
                header = tarefa.split('<header>', 1)[1].split('</header>', 1)[0]
                self.assertIn('<p class="task-aquecer"><a href="aquecimento/">', header)
                self.assertLess(header.index('task-aquecer'), header.index('id="produzir"'))
                ids = [a.get('id') for a in items]
                a, t = ids.index(f'aquecimento-unidade-{n}'), ids.index(f'tarefa-unidade-{n}')
                self.assertEqual(a + 1, t)
                linha = items[a]
                self.assertEqual(linha.get('class'), 'aula-aquecimento')
                self.assertNotIn('data-passo', linha)
                self.assertNotIn('data-task-lesson', linha)
                self.assertIn(f'<li class="aula-aquecimento" id="aquecimento-unidade-{n}"><a href="../tarefas/{slug}/aquecimento/"><span class="n">A</span>', indice)
                self.assertTrue((ROOT / 'tarefas' / slug / 'aquecimento' / 'index.html').is_file())
        css = (ROOT / 'assets/task-90.css').read_text('utf-8')
        self.assertIn('.task-aquecer a{', css)
        self.assertIn('@media print{.task-aquecer{display:none!important}}', css)

    def test_o_aquecimento_nao_faz_a_tarefa(self):
        # Nenhum cartão de fazer usa as passagens reservadas; na U3, nenhum toma partido nos temas.
        for slug in SLUGS:
            d = dados(slug)
            for n, c in enumerate(d['cartoes'], 1):
                if c['t'] == 'ler':
                    continue
                texto = A.texto_visivel(c)
                for r in d['reservadas']:
                    with self.subTest(aquecimento=slug, cartao=n, reservada=r):
                        self.assertNotIn(r, texto)
        tarefa = json.loads((ROOT / 'docs/pedagogia/tarefas-escolha/m7-u3.json').read_text('utf-8'))
        for tema in tarefa['temas']:
            pergunta = re.sub(r'«[^»]*»', '', tema['texto']).split('?')[0]
            for c in dados('m7-u3')['cartoes'][1:-1]:
                self.assertNotIn(pergunta.strip(), A.texto_visivel(c))

    def test_u3_os_cartoes_substituem_as_maquinas(self):
        s = (ROOT / 'tarefas/m7-u3/index.html').read_text('utf-8')
        aquecer = s.split('id="aquecer"', 1)[1].split('</section>', 1)[0]
        self.assertIn('data-task-warm="cartoes"', s)
        self.assertNotIn('data-task-machine', s)
        self.assertNotIn('data-task-question="aquecer"', s)
        self.assertIn('<a href="aquecimento/">Abrir o aquecimento em cartões</a>', aquecer)
        self.assertIn('data-max="10"', aquecer)
        self.assertIn('Respostas exploradas: 0 de 1.', s)
        # Os dois exemplos resolvidos e o dossiê do tema B.
        self.assertIn('<h3 id="exemplos">Ver como se faz</h3>', s)
        self.assertEqual(s.count('<article class="task-example">'), 2)
        for marca in ('[S]', '[R]', '[M]', '[N]', 'Dossiê do tema B', '1578', '20 de fevereiro de 1933', 'sebastianismo', 'Madalena'):
            self.assertIn(marca, s)
        # 29/10/2026 (revisão pedagógica, C4): a grelha tira pontos a um facto sem data, por isso cada facto do dossiê tem
        # data; o de Garrett é a outra voz.
        tarefa = json.loads((ROOT / 'docs/pedagogia/tarefas-escolha/m7-u3.json').read_text('utf-8'))
        for facto in tarefa['dossie']:
            if 'Frei Luís de Sousa' not in facto['facto']:
                with self.subTest(facto=facto['facto']):
                    self.assertRegex(facto['facto'], r'\b1[0-9]{3}\b')
        self.assertIn('o facto que usares tem de ter data', tarefa['temas'][1]['texto'])

    def test_u2_apresentacoes_em_pequenos_grupos(self):
        # Decisão 5 do docente: a tarefa, o guia e a linha do percurso dizem o mesmo.
        tarefa = (ROOT / 'tarefas/m7-u2/index.html').read_text('utf-8')
        guia = (ROOT / 'm7/guia-da-tarefa-m7/index.html').read_text('utf-8')
        indice = (ROOT / 'm7/index.html').read_text('utf-8')
        self.assertIn('As apresentações fazem-se em pequenos grupos de 4 ou 5, todos ao mesmo tempo, com o docente a circular.', tarefa)
        self.assertIn('Apresenta a voz ao teu grupo em dois minutos', tarefa)
        self.assertIn('apresentações em pequenos grupos, ao mesmo tempo</li>', guia)
        self.assertIn('Apresenta-o ao teu grupo de 4 ou 5 colegas', guia)
        linha_t = re.search(r'<li class="aula-tarefa" data-task-lesson="2".*?</li>', indice).group(0)
        self.assertIn('apresentações em pequenos grupos ao mesmo tempo', linha_t)
        self.assertIn('aquecimento em cartões no início', linha_t)
        self.assertIn('No início da aula de tarefa', dados('m7-u2')['cartoes'][0]['html'])
        self.assertNotIn('em grupo', tarefa)
        # 29/10/2026 (revisão pedagógica): a descrição diz o mesmo (C8), e a resposta à pergunta fica registada no papel,
        # para a Apresentação ter prova com os grupos todos ao mesmo tempo (C10).
        self.assertIn('no início da aula de tarefa', dados('m7-u2')['descricao'])
        self.assertIn('Cada um regista no seu papel, numa linha, a pergunta que lhe fizeram e o que respondeu', tarefa)
        self.assertIn('responde a uma pergunta (registada numa linha no papel)', guia)

    def test_sem_dia_pessoa_e_f10_com_o_titulo_novo(self):
        falso = 'Nesse dia Pessoa escreveu'
        for rel, texto in publicados():
            with self.subTest(pagina=rel):
                self.assertIsNone(re.search(r'[Dd]ia (?:de )?(?:Fernando )?Pessoa', texto.replace(falso, '')))
                self.assertNotIn('Defender o projeto', texto)
        for rel in ('m7/licao-m7-f10/index.html', 'm7/painel-m7-f10/index.html', 'm7/index.html', 'index.html', '3/index.html',
                    '3/todos/index.html', 'm7/diapositivos/index.html', 'm7/mapa-do-modulo-m7/index.html'):
            with self.subTest(titulo=rel):
                self.assertIn('Argumentar com versos', (ROOT / rel).read_text('utf-8'))
        f10 = lesson_cards(ROOT / 'm7/licao-m7-f10/index.html')
        self.assertEqual(len(f10), 20)
        self.assertEqual([c['t'] == 'ler' for c in f10], [True] * 3 + [False] * 16 + [True])
        self.assertIn('Os seis movimentos', f10[2]['html'])
        visita = (ROOT / 'm7/visita-casa-fernando-pessoa/index.html').read_text('utf-8')
        self.assertIn('facultativo', visita)
        self.assertNotIn('Teams', visita)
        self.assertNotIn('memória descritiva', visita.lower())

    def test_citacoes_so_das_licoes_anteriores_a_camada(self):
        # 29/10/2026 (revisão técnica, P1): a F10 nova e a tarefa da U3 foram escritas nesta camada e não servem de fonte a
        # si próprias. As citações do aquecimento da U3 e da F10 reescrita conferem-se, letra a letra, nas lições do M7
        # que esta camada não toca (F07, F08, F09 e F11); a única exceção é a retoma da unidade 3, citada do percurso.
        self.assertEqual(set(dados('m7-u3')['licoes_das_citacoes']), {'m7/' + f for f in WARM_LESSONS['m7']})
        fontes = ' '.join(A.plano(ROOT, 'm7/' + f) for f in WARM_LESSONS['m7'])
        indice = (ROOT / 'm7/index.html').read_text('utf-8')
        retomas = set(re.findall(r'<li>([^<]+)</li>', ' '.join(re.findall(r'<aside class="unit-retoma">.*?</aside>', indice, re.S))))
        self.assertIn('Por quem, ou pelo quê, ainda esperamos?', retomas)

        def visivel(c):
            # Sem marcas HTML e sem espaços no lugar delas: o «Para levar» da F10 escreve a frase letra a letra, em <span>.
            t = json.dumps(c, ensure_ascii=False)
            t = json.loads(t)
            partes = []
            for k in ('p', 'p2', 'frase', 'f', 'titulo', 'html', 'trecho', 'apoio', 'cita'):
                if isinstance(t.get(k), str):
                    partes.append(t[k])
            for k in ('o', 'passos'):
                partes += [x for x in t.get(k, []) if isinstance(x, str)]
            for par in t.get('pares', []):
                partes += par
            fe = t.get('fe')
            partes += [x for x in (fe if isinstance(fe, list) else [fe]) if isinstance(x, str)]
            texto = ' '.join(partes).replace('**', '')
            texto = re.sub(r'<(?:br|/p|/li|/div|/h3|/figcaption)[^>]*>', ' ', texto)
            return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', texto))

        baralhos = {'aquecimento m7-u3': dados('m7-u3')['cartoes'], 'licao-m7-f10': lesson_cards(ROOT / 'm7/licao-m7-f10/index.html')}
        vistas = 0
        for nome, cartoes in baralhos.items():
            for n, c in enumerate(cartoes):
                for citacao in re.findall(r'«([^»]{12,})»', visivel(c)):
                    if citacao in retomas:
                        continue
                    for verso in [v.strip() for v in citacao.split(' / ')]:
                        vistas += 1
                        with self.subTest(baralho=nome, cartao=n, citacao=verso):
                            self.assertTrue(verso in fontes, f'não está letra a letra em F07, F08, F09 nem F11: «{verso}»')
        self.assertGreater(vistas, 40)

    def test_diapositivos_ligados_sem_dia_pessoa(self):
        # 29/10/2026 (revisão, G1 e G2): na página dos diapositivos, nenhuma ligação leva «projetar=1» (o lançador da
        # projeção troca-a pelo seu botão e a sessão desaparece da lista); as sessões 14 e 15 abrem a lição até o PDF e o
        # PowerPoint serem refeitos; nenhum PowerPoint da pasta traz o «Dia Pessoa» (o PDF sai das mesmas fontes).
        pasta = ROOT / 'm7/diapositivos'
        s = (pasta / 'index.html').read_text('utf-8')
        principal = s.split('<main', 1)[1].split('</main>', 1)[0]
        self.assertNotIn('projetar=1', principal)
        self.assertIn('<a href="../licao-m7-f10/">Sessão 14: Argumentar com versos<small>', principal)
        self.assertIn('<a href="../licao-m7-f11/">Sessão 15: Quantas vozes cabem num homem<small>', principal)
        for href in re.findall(r'href="([^"/]+\.(?:pdf|pptx))"', principal):
            self.assertTrue((pasta / href).is_file(), href)
        for p in sorted(pasta.glob('*.pptx')):
            with zipfile.ZipFile(p) as z:
                xml = ' '.join(z.read(n).decode('utf-8', 'replace') for n in z.namelist()
                               if n.startswith('ppt/slides/slide') and n.endswith('.xml'))
            with self.subTest(powerpoint=p.name):
                self.assertIsNone(re.search(r'[Dd]ia (?:de )?(?:Fernando )?Pessoa', re.sub(r'<[^>]+>', '', xml)))

    def test_guia_diz_o_mesmo_que_as_tarefas(self):
        # 29/10/2026 (revisão pedagógica, C8, C9, P6; técnica, P7): no arquivo do guia, os blocos somam os 90 minutos, a
        # U2 começa pelo aquecimento, os nomes de ficheiro seguem o portefólio e os títulos de obras vão em itálico.
        guia = (ROOT / 'm7/guia-da-tarefa-m7/index.html').read_text('utf-8')
        i = guia.index('BLOCOS=') + len('BLOCOS=')
        blocos, _ = json.JSONDecoder().raw_decode(guia, i)
        self.assertEqual(sum(b[0] for b in blocos), 90)
        for n, (minutos, nome, texto) in enumerate(blocos):
            self.assertIn(f'<div class="t"><b>{nome}, {minutos} min</b><span>{texto}</span></div>', guia)
        self.assertIn(f'<span class="relogio" id="relogio">{blocos[0][0]}:00</span>', guia)
        i = guia.index('T=[{') + 2
        T, _ = json.JSONDecoder().raw_decode(guia, i)
        self.assertEqual(T[0]['passos'][0], 'No início da aula, faz o aquecimento em cartões (10 a 15 minutos).')
        self.assertEqual(T[1]['passos'][0], 'No início da aula, faz o aquecimento em cartões (10 minutos).')
        ficheiros = re.findall(r'M7_[A-Za-z0-9]+_[A-Za-z]+', json.dumps(T, ensure_ascii=False))
        self.assertEqual(sorted(set(ficheiros)), ['M7_Extra_Mensagem', 'M7_Tarefa2_Heteronimo', 'M7_Tarefa3_Opiniao'])
        self.assertIn('_Mensagem_', T[1]['titulo'])
        self.assertIn('function it(s){', guia)
        self.assertIn('$("#r-titulo").innerHTML=it(atual.titulo)', guia)

    def test_f10_refeita_traz_versao(self):
        # 29/10/2026 (revisão técnica, P2): regra de 23/10 em jogo.js; o progresso guardado da F10 antiga recomeça.
        f10 = (ROOT / 'm7/licao-m7-f10/index.html').read_text('utf-8')
        self.assertEqual(f10.count('EPIJogo.montar({casca:CASCA,versao:"2026-10-29",'), 1)
        self.assertIn('var K="licao-m7-f10"', f10)

if __name__ == '__main__':
    unittest.main()
