"""15/11/2026: a revisão geral antes de publicar, camada revisao_geral_20261115 (decisões do utilizador de 15/11/2026, «decide tu mesmo
isso tudo já»), por cima da fila final (fila_final_20261115).

Confere:
- as frases novas e o que sai: «ficha» no Atlas («registo de escuta», «informação técnica», com as versões dos dois ficheiros em
  atlas/index.html); a explicação a um colega passa a trabalho individual, por escrito (M9-F12 e as notas para a aula da M9-F11 e da
  M9-F12); «tentas primeiro sozinho» passa a «tentas primeiro por ti» nas provas em cartões (a secção, as quatro lições dos Grupos I
  e II das provas de 2026 e os seus dados; a frase da secção vem de seccao.json, «entrada»); saem os retratos de José Saramago (M9-F11),
  Eugénio de Andrade (M8-F13) e Ana Luísa Amaral (M8-F14), com o crédito e a legenda, do registo das imagens, da lista fechada dos
  créditos à vista e do repositório; saem os vídeos que não são dos canais dos titulares (o trailer e o bailado da M5-F14, a RTP1 da
  M5-F15), com o que dependia só deles (o facto de 2025 do dossiê da tarefa M5-U2), e a masterclass da «Academia X» da sessão 27 do
  Exame, que fica com a alternativa em texto; os cartões ficam com o texto que já tinham;
- que não sobra nenhum dos retratos, dos vídeos, dos «sozinho», das «ficha» nem dos pares visados nas páginas, nos recursos e nos
  dados do sítio (só os registos históricos e os manifestos das camadas os guardam, de propósito);
- que as legendas «Grafismo gerado com recurso a IA, EPI, 2026.» estão onde devem (decisão d): uma vez na entrada, no «i» do fundo da
  calçada, e em nenhuma página do M2, do M3, do M6 e do M9, cujos grafismos feitos por código são só interface (ícones aria-hidden, as
  divisórias de calçada e as formas de 16 px que marcam os pares ligados), sem canvas, com os PNG embutidos só nos códigos QR;
- que as páginas geradas saem iguais dos geradores (as provas em cartões, as lições geradas e as tarefas) e que o gerador das provas,
  sem a chave nova, dá a frase de antes (as camadas de baixo voltam a gerar a secção como a deixaram);
- que a camada é fechada, reversível letra a letra até ao commit de partida (2ee5309b, o pedido #212, com a mesma árvore do main
  c1f19dd3), está no topo da pilha e que as camadas de baixo a desfazem primeiro: a auditoria, a Sala, a leitura histórica, os scripts
  das camadas que partilham ficheiros, os browser_*.cjs que desfazem camadas e as cadeias dos testes e dos fluxos; e que as 23 camadas
  de baixo que partilham ficheiros com ela conferem com ela desfeita primeiro.

A reversão lê o commit de partida com git: o fluxo que corre este teste faz o checkout com fetch-depth: 0.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import verificar_camadas  # noqa: E402
from auditoria_20261028 import undo_fila_final_1115, undo_revisao_geral_1115  # noqa: E402

CAMADA_REL = 'scripts/revisao_geral_20261115.json'
MANIFESTO_REL = 'tests/fixtures/revisao-geral-edits-20261115.json'
FILA_REL = 'tests/fixtures/fila-final-edits-20261115.json'
# O commit de partida: o pedido #212 (2ee5309b), com a mesma árvore do main c1f19dd3, onde foi publicado.
BASE = '2ee5309baa209e3d2497e8a244819b17f2c0de4f'
EDITORIAL, EXPLORAR, ATLAS = 'assets/atlas-editorial.js', 'assets/atlas-explorar.js', 'atlas/index.html'
F11, F12 = 'm9/recursos/f11.js', 'm9/recursos/f12.js'
PAINEIS = ['m9/painel-m9-f11/index.html', 'm9/painel-m9-f12/index.html']
SECCAO, SECCAO_DADOS = 'exame/provas/index.html', 'scripts/provas/dados/seccao.json'
PROVAS = [f'exame/provas/{p}/{g}/index.html' for p in ('2026-1f', '2026-2f') for g in ('grupo-i', 'grupo-ii')]
PROVAS_DADOS = [f'scripts/provas/dados/{p}/{g}.json' for p in ('2026-1f', '2026-2f') for g in ('grupo-i', 'grupo-ii')]
M8F13, M8F14 = 'm8/licao-m8-f13/index.html', 'm8/licao-m8-f14/index.html'
M5F14, M5F15 = 'm5/licao-m5-f14/index.html', 'm5/licao-m5-f15/index.html'
U2_DADOS, U2 = 'docs/pedagogia/tarefas-escolha/m5-u2.json', 'tarefas/m5-u2/index.html'
SESSOES, APP = 'assets/exame/sessoes.json', 'assets/exame/app.js'
FICHEIROS = [EDITORIAL, EXPLORAR, ATLAS, F12] + PAINEIS + [SECCAO_DADOS, SECCAO] + [x for par in zip(PROVAS_DADOS, PROVAS) for x in par] + \
    [F11, M8F13, M8F14, M5F14, M5F15, U2_DADOS, U2, SESSOES]
IMAGENS_QUE_SAEM = ['img/fontes/saramago-2005.jpg', 'img/fontes/licoes-20261101/eugenio.jpg', 'img/fontes/licoes-20261101/amaral.jpg']
VIDEOS_QUE_SAEM = ['S_hGdGKAkv8', 'UVrhS1QOQyw', 'VjSVmIj8CbI', 'Xzst0nmqtFE']
# O que não pode sobrar em nenhuma página, recurso ou dado do sítio.
VISADOS = (['saramago-2005', 'licoes-20261101/eugenio.jpg', 'licoes-20261101/amaral.jpg', 'Bottelho', 'Mattias Blomgren']
           + VIDEOS_QUE_SAEM + ['Academia X', 'canal Alexandre Oliveira', 'canal Teatro Micaelense',
                                'canal Instituto de História Contemporânea', 'o vídeo de Teresa Pinto Coelho', 'nas honras de Panteão a Eça',
                                'Eça recebe honras de Panteão',
                                'tentas primeiro sozinho', 'ficha de escuta', 'ficha técnica', 'Com um colega, prepara',
                                'explica a um colega uma escolha'])
LEGENDA = 'Grafismo gerado com recurso a IA, EPI, 2026'
NBSP = '\xa0'


def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def sha_lf(texto):
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def no_commit(rel):
    return subprocess.run(['git', 'show', f'{BASE}:{rel}'], cwd=ROOT, capture_output=True, check=True).stdout.decode('utf-8')


def cartoes(texto):
    m = re.search(r'CARTOES\s*=\s*(\[)', texto)
    return json.JSONDecoder().raw_decode(texto[m.start(1):])[0]


def sessao(dados, sid):
    return next(s for s in dados['sessions'] if s['id'] == sid)


TROCAS = json.loads(ler(CAMADA_REL))
MANIFESTO = json.loads(ler(MANIFESTO_REL))


class RevisaoGeral(unittest.TestCase):
    # ---------- as frases novas e o que sai ----------
    def test_ficha_sai_do_atlas(self):
        editorial, explorar, atlas = ler(EDITORIAL), ler(EXPLORAR), ler(ATLAS)
        self.assertEqual(editorial.count('Faz um pequeno registo de escuta com três campos e preenche apenas o que encontrares nos créditos.'), 1)
        self.assertEqual(explorar.count("['Material','Consulta a informação técnica. Distingue o que vês na reprodução do que só sabes pela "
                                        "descrição dos materiais.']"), 1)
        # A proposta «a informação técnica indica sobre os materiais» não se diz em português: fica «descreve os materiais».
        self.assertEqual(explorar.count('A reprodução não permite confirmar a textura pelo toque; a informação técnica descreve os materiais.'), 1)
        self.assertNotIn('indica sobre', explorar)
        for rel, texto in ((EDITORIAL, editorial), (EXPLORAR, explorar)):
            self.assertNotRegex(texto, r'(?i)\bficha', rel)
        # As versões dos dois ficheiros mudam, para os navegadores não usarem a cópia antiga (como na decisão 154).
        for nome in ('atlas-editorial.js', 'atlas-explorar.js'):
            self.assertEqual(atlas.count(f'{nome}?v=20261115-revisao-geral-1'), 1, nome)
            self.assertEqual(len(re.findall(re.escape(nome) + r'\?v=', atlas)), 1, nome)
        self.assertNotIn('20261105-autonomia-1', atlas)

    def test_tarefas_de_pares_passam_a_individuais(self):
        f12 = ler(F12)
        self.assertEqual(f12.count('<p>Prepara por escrito duas frases: a música acrescenta algo porque…; isso não permite concluir que… .'), 1)
        self.assertNotIn('colega', f12)
        for rel in PAINEIS:
            texto = ler(rel)
            self.assertEqual(texto.count('confere a passagem no livro e explica por escrito, em duas frases, uma escolha e o seu limite.'), 1, rel)
            self.assertNotIn('colega', texto, rel)
        # As duas lições pedem duas frases: «Testa duas frases» na F11 e «prepara duas frases» na F12.
        self.assertIn('"titulo":"Testa duas frases"', ler(F11))
        self.assertIn('duas frases', f12)

    def test_sozinho_sai_das_provas_em_cartoes(self):
        self.assertEqual(ler(SECCAO).count('Nos itens de escolha, tentas primeiro por ti e depois vês porquê.</p>'), 1)
        for rel in PROVAS + PROVAS_DADOS:
            texto = ler(rel)
            self.assertEqual(texto.count('tentas primeiro por ti'), 1, rel)
            self.assertNotIn('sozinho', texto, rel)
        self.assertNotIn('sozinho', ler(SECCAO))
        # A frase da secção vem dos dados (chave nova «entrada», documentada em «_entrada»).
        sec = json.loads(ler(SECCAO_DADOS))
        self.assertTrue(sec['entrada'].endswith('Nos itens de escolha, tentas primeiro por ti e depois vês porquê.'))
        self.assertIn('_entrada', sec)
        self.assertIn(f'<p class="of-entrada">{sec["entrada"]}</p>', ler(SECCAO))
        # Sem a chave, o gerador dá a frase de antes, byte a byte (as camadas de baixo voltam a gerar a secção a partir dos dados como as
        # deixaram): a única diferença entre as duas frases é «sozinho» → «por ti».
        spec = importlib.util.spec_from_file_location('provas_gerar_revisao', ROOT / 'scripts/provas/gerar.py')
        gerar = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gerar)
        self.assertEqual(gerar.ENTRADA_ANTES.replace('tentas primeiro sozinho', 'tentas primeiro por ti'), sec['entrada'])
        self.assertIn('{sec.get("entrada", ENTRADA_ANTES)}', ler('scripts/provas/gerar.py'))

    def test_retratos_saem(self):
        f11 = cartoes(ler(F11))
        self.assertEqual(len(f11), len(cartoes(no_commit(F11))))
        self.assertTrue(f11[0]['html'].startswith('<p class="abre">Construir, ver, procurar: as ações de uma personagem dizem mais do que um '
                                                  'retrato.'))
        self.assertNotIn('<figure', json.dumps(f11, ensure_ascii=False))
        self.assertNotIn('José Saramago em 2005', ler(F11))
        for rel, abre in ((M8F13, '<p class="abre"><strong>Como pode um poema mostrar que as palavras deixaram de chegar?</strong></p>'),
                          (M8F14, '<p class="abre"><strong>Quem decide o que merece entrar na história?</strong></p>')):
            texto = ler(rel)
            c = cartoes(texto)
            self.assertEqual(len(c), 20, rel)
            self.assertTrue(c[0]['html'].startswith(abre), rel)
            self.assertNotIn('fig documento', texto, rel)
            self.assertNotIn('Créditos da imagem', json.dumps(c[0], ensure_ascii=False), rel)
            # O resto do primeiro cartão é o de antes, letra a letra.
            self.assertEqual(c[0]['html'], cartoes(no_commit(rel))[0]['html'].split('</figure>', 1)[1], rel)
        # O registo das imagens das lições geradas (scripts/imagens_licoes_20261101.py) já não as tem nem as usa.
        spec = importlib.util.spec_from_file_location('imagens_licoes_revisao', ROOT / 'scripts/imagens_licoes_20261101.py')
        imagens = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imagens)
        self.assertNotIn('eugenio', imagens.IMAGENS)
        self.assertNotIn('amaral', imagens.IMAGENS)
        self.assertNotIn('m8-f13', imagens.USOS)
        self.assertNotIn('m8-f14', imagens.USOS)
        self.assertEqual(imagens.USOS['m9-f14'][0], 'piranesi')
        # Os ficheiros das três imagens saem do repositório; a lista fechada dos créditos à vista já não tem a M9-F11.
        for rel in IMAGENS_QUE_SAEM:
            self.assertFalse((ROOT / rel).exists(), rel)
        lista = json.loads(ler('tests/fixtures/creditos-a-vista-20261105.json'))
        self.assertNotIn(F11, [e['pagina'] for e in lista['creditos']])
        self.assertIn('15/11/2026: revisão geral', lista['_nota'])

    def test_videos_saem_da_m5(self):
        f14, f15 = ler(M5F14), ler(M5F15)
        for texto, ids in ((f14, VIDEOS_QUE_SAEM[:2]), (f15, VIDEOS_QUE_SAEM[2:3])):
            for vid in ids:
                self.assertNotIn(vid, texto)
            self.assertNotIn('class=\\"yt\\"', texto)
            self.assertNotIn('youtube.com/watch', texto)
        c14, c15 = cartoes(f14), cartoes(f15)
        self.assertEqual((len(c14), len(c15)), (21, 21))
        # Os cartões ficam com o texto que já tinham.
        self.assertIn('estreou no cinema em 2014', c14[1]['html'])
        self.assertTrue(c14[1]['html'].endswith('e o que a escolha ganha e perde.</span></li></ol>'))
        self.assertIn('<summary>Quando passares ao filme</summary>', c14[20]['html'])
        self.assertTrue(c14[20]['html'].endswith('Não uses o exemplo inventado como prova sobre o filme.</p></details>'))
        self.assertIn('«Falhámos a vida»', c15[1]['html'])
        self.assertTrue(c15[1]['html'].endswith('revês também o indireto livre e a estrutura circular.</span></li></ol>'))
        for antes, depois, i in ((cartoes(no_commit(M5F14)), c14, 1), (cartoes(no_commit(M5F14)), c14, 20), (cartoes(no_commit(M5F15)), c15, 1)):
            self.assertEqual(antes[i]['html'].split('<div class="yt"', 1)[0], depois[i]['html'], i)
        for k in set(range(21)) - {1, 20}:
            self.assertEqual(c14[k], cartoes(no_commit(M5F14))[k], k)
        for k in set(range(21)) - {1}:
            self.assertEqual(c15[k], cartoes(no_commit(M5F15))[k], k)
        # A tarefa M5-U2: o dossiê do tema B fica com quatro factos datados (sai o de 2025, cuja única fonte era o vídeo que saiu).
        dados = json.loads(ler(U2_DADOS))
        self.assertEqual(len(dados['dossie']), 4)
        self.assertEqual([x['href'] for x in dados['dossie']], ['../../m5/licao-m5-f10/', '../../m5/licao-m5-f11/', '../../m5/licao-m5-f14/',
                                                                 '../../m5/licao-m5-f10/'])
        self.assertEqual(len(json.loads(no_commit(U2_DADOS))['dossie']), 5)
        pagina = ler(U2)
        dossie = re.search(r'<section class="task-dossier tf-dossie".*?</section>', pagina, re.S).group(0)
        self.assertEqual(dossie.count('<li>'), 4)
        self.assertNotIn('2025', dossie)
        self.assertIn('Usa um facto datado do <a href="#dossie">dossiê</a>, ligado à tua posição.', pagina)

    def test_sessao_27_sem_video(self):
        dados, antes = json.loads(ler(SESSOES)), json.loads(no_commit(SESSOES))
        s, s0 = sessao(dados, 's27'), sessao(antes, 's27')
        self.assertNotIn('video', s)
        self.assertFalse([x['id'] for x in dados['sessions'] if 'video' in x])
        self.assertEqual(s['tags'], ['método de estudo', 'revisão'])
        # A alternativa em texto: o antigo video.fallback, palavra por palavra, abre o contexto, antes dos dois casos.
        self.assertEqual(s['source']['context'], s0['video']['fallback'] + ' ' + s0['source']['context'])
        self.assertEqual(s['source']['note'], 'Casos fictícios. A proposta de estudo não é uma previsão do exame. Para a estrutura, a duração e '
                         'as regras da prova, consulta a Informação-Prova da tua época em «Programa e fontes».')
        self.assertTrue(s0['video']['note'].endswith('Para a estrutura, a duração e as regras da prova, consulta a Informação-Prova da tua época '
                                                     'em «Programa e fontes».'))
        self.assertEqual(s['writing']['instructions'][0], 'Consulta os casos e volta à proposta de estudo quando precisares.')
        self.assertEqual(s['writing']['criteria'][2], 'Usei uma ideia da proposta de estudo, sem a tomar como garantia de resultado.')
        texto = json.dumps(s, ensure_ascii=False)
        for velho in ('trechos', 'alternativa em texto', 'masterclass', 'Academia X', 'YouTube', 'O vídeo é'):
            self.assertNotIn(velho, texto)
        # O resto da sessão fica como estava: o aquecimento, a escrita (salvo a instrução e o critério), a correção e a saída.
        for chave in ('id', 'order', 'durationMinutes', 'title', 'group', 'module', 'focus', 'resources', 'warmup', 'correction', 'exit',
                      'alternatives'):
            self.assertEqual(s[chave], s0[chave], chave)
        self.assertEqual({k: v for k, v in s['writing'].items() if k not in ('instructions', 'criteria')},
                         {k: v for k, v in s0['writing'].items() if k not in ('instructions', 'criteria')})
        self.assertEqual({k: v for k, v in s['source'].items() if k not in ('context', 'note')},
                         {k: v for k, v in s0['source'].items() if k not in ('context', 'note')})
        # As outras 26 sessões não mudam.
        self.assertEqual([x for x in dados['sessions'] if x['id'] != 's27'], [x for x in antes['sessions'] if x['id'] != 's27'])
        ids = [q['id'] for x in dados['sessions'] for q in x['warmup'] + [x['correction']['check']]]
        self.assertEqual(len(ids), len(set(ids)))
        # O motor já tratava o vídeo como opcional: a s27 segue o caminho das outras sessões (a fase «Ler», com o contexto).
        app = ler(APP)
        self.assertEqual(app, no_commit(APP))
        self.assertIn("function phaseLabel(i){return session&&session.video&&i===1?'Ver e aplicar':phaseNames[i];}", app)
        self.assertIn('function currentQuestions(){if(phase===1&&session.video)return session.video.questions;', app)
        self.assertIn('if(phase===1&&session.video)return videoLesson();', app)
        self.assertIn('<p class="context">\'+e(s.source.context)+\'</p>', app)

    # ---------- nada sobra ----------
    def test_nada_sobra_dos_visados(self):
        listados = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\n')
        # As páginas, os recursos e os dados do sítio; fora ficam os registos históricos (docs/, menos os dados dos geradores), os testes e
        # os manifestos das camadas, que guardam os textos antigos de propósito, e o molde do gerador das provas, que guarda a frase de
        # antes para as camadas de baixo (ENTRADA_ANTES, conferida acima).
        incluidos = {'scripts/imagens_licoes_20261101.py', 'tests/fixtures/creditos-a-vista-20261105.json'}
        sitio = [r for r in listados if r and Path(r).suffix in ('.html', '.js', '.json', '.css', '.mjs')
                 and (r in incluidos or r.startswith(('scripts/provas/dados/', 'docs/pedagogia/tarefas-escolha/', 'docs/pedagogia/aquecimentos/'))
                      or not r.startswith(('docs/', 'tests/', 'scripts/', 'tools/', '.github/')))]
        self.assertGreater(len(sitio), 500)
        achados = {}
        for rel in sitio + sorted(incluidos):
            caminho = ROOT / rel
            if not caminho.is_file():
                continue
            texto = caminho.read_bytes().decode('utf-8', errors='replace')
            for v in VISADOS:
                if v in texto:
                    achados.setdefault(v, []).append(rel)
        self.assertEqual(achados, {})

    # ---------- as legendas ----------
    def test_legendas_onde_devem(self):
        # Uma vez por página, no padrão do sítio: a entrada tem-na no «i» do fundo da calçada.
        entrada = ler('index.html')
        self.assertEqual(entrada.count(LEGENDA), 1)
        self.assertRegex(entrada, r'<details class="info-i info-i--linha" name="info-i"><summary aria-label="Créditos do desenho"><span '
                                  r'aria-hidden="true">i</span></summary><p class="info-i-texto">' + re.escape(LEGENDA))
        svg = re.compile(r'<svg\b([^>]*)>(.*?)</svg>', re.S | re.I)
        paginas, interface = 0, {'aria-hidden': 0, 'marca-par': 0}
        for modulo in ('m2', 'm3', 'm6', 'm9'):
            for p in sorted((ROOT / modulo).rglob('*.html')):
                rel = p.relative_to(ROOT).as_posix()
                texto = p.read_text('utf-8')
                paginas += 1
                with self.subTest(pagina=rel):
                    # Nenhum grafismo ilustrativo feito por código: os SVG (também os das cadeias dos cartões) são ícones aria-hidden
                    # (as divisórias de calçada incluídas) ou as formas de 16 px que marcam os pares ligados; não há canvas.
                    t = texto.replace('\\"', '"').replace('<\\/', '</')
                    for m in svg.finditer(t):
                        a = m.group(1)
                        if re.search(r'aria-hidden\s*=\s*"true"', a):
                            interface['aria-hidden'] += 1
                        elif 'marca-par' in t[max(0, m.start() - 80):m.start()] and re.fullmatch(r'\s*viewBox="0 0 16 16"\s*', a):
                            interface['marca-par'] += 1
                        else:
                            self.fail(f'{rel}: grafismo por código sem legenda: {t[m.start():m.start() + 120]}')
                    for m in re.finditer(r'createElementNS\([^,]+,\s*["\']svg["\']\)', texto):
                        self.assertIn('aria-hidden', texto[m.end():m.end() + 400])
                    self.assertNotRegex(texto, r'<canvas\b|getContext\(')
                    # Os PNG embutidos são códigos QR (excluídos da legenda).
                    for m in re.finditer(r'data:image/png', texto):
                        self.assertRegex(texto[max(0, m.start() - 300):m.start()], r'class=\\?"qr\\?"')
                    # Por isso, nenhuma página destes módulos leva a legenda.
                    self.assertNotIn(LEGENDA, texto)
        self.assertGreater(paginas, 150)
        self.assertGreater(interface['aria-hidden'], 1000)
        self.assertEqual(interface['marca-par'], 16)

    # ---------- as páginas geradas ----------
    def test_paginas_geradas_saem_iguais_dos_geradores(self):
        r = subprocess.run([sys.executable, '-B', 'scripts/provas/gerar.py', '--verificar'], cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Tudo igual ao que está na árvore.', r.stdout)
        r = subprocess.run([sys.executable, '-B', 'scripts/gerar_licoes_20261101.py', '--verificar'], cwd=ROOT, capture_output=True,
                           text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Conferida: m8-f13', r.stdout)
        self.assertIn('Conferida: m8-f14', r.stdout)
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, '-B', 'scripts/tarefas_escolha.py', '--saida', tmp], cwd=ROOT, capture_output=True, text=True,
                               encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual((Path(tmp) / U2).read_bytes(), (ROOT / U2).read_bytes())

    # ---------- a camada ----------
    def test_camada_fechada(self):
        self.assertEqual(sorted({t['ficheiro'] for t in TROCAS}), sorted(FICHEIROS))
        self.assertEqual(sorted(MANIFESTO['files']), sorted(FICHEIROS))
        self.assertEqual(len(TROCAS), 32)
        self.assertEqual(MANIFESTO['base_commit'], BASE)
        self.assertTrue(MANIFESTO['_nota'].startswith('15/11/2026: revisão geral antes de publicar'))
        for t in TROCAS:
            self.assertEqual(t['ocorrencias'], 1)
            self.assertTrue(t['achado'].startswith('15/11/2026: revisão geral'))
            self.assertNotIn(t['novo'], t['antigo'])
            for palavra in ('professor', 'jogar', 'jogo', 'ficha', 'folha', '—', 'colega', 'sozinho', 'docente'):
                self.assertNotIn(palavra, t['novo'].replace('nao_partir', '').lower(), t['local'])
        for rel in FICHEIROS:
            mine = [(t['antigo'], t['novo']) for t in TROCAS if t['ficheiro'] == rel]
            self.assertEqual([(e['old'], e['new']) for e in MANIFESTO['files'][rel]['edits']], mine, rel)
            self.assertTrue(all(e['occurrences'] == 1 for e in MANIFESTO['files'][rel]['edits']))
            self.assertEqual(sha_lf(ler(rel)), MANIFESTO['files'][rel]['after_sha256_lf'], rel)
        for rel in (SESSOES, SECCAO_DADOS, U2_DADOS) + tuple(PROVAS_DADOS):
            json.loads(ler(rel))

    def test_reversivel_ate_ao_commit_de_partida(self):
        for rel in FICHEIROS:
            texto = ler(rel)
            for e in reversed(MANIFESTO['files'][rel]['edits']):
                self.assertEqual(texto.count(e['new']), e['occurrences'], rel)
                texto = texto.replace(e['new'], e['old'])
            base = no_commit(rel)
            self.assertEqual(texto, base, rel)
            self.assertEqual(sha_lf(base), MANIFESTO['files'][rel]['base_sha256_lf'], rel)
            self.assertEqual(undo_revisao_geral_1115(rel, ler(rel)), base, rel)
            self.assertEqual(undo_revisao_geral_1115(rel, base), base, rel)
        # A sessão 27, sessoes.json inteiro: com esta camada desfeita, é o ficheiro como a fila final o deixou.
        fila = json.loads(ler(FILA_REL))['files'][SESSOES]
        self.assertEqual(sha_lf(undo_revisao_geral_1115(SESSOES, ler(SESSOES))), fila['after_sha256_lf'])

    def test_o_script_da_o_mesmo_json(self):
        spec = importlib.util.spec_from_file_location('revisao_geral_20261115', ROOT / 'scripts/revisao_geral_20261115.py')
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        self.assertEqual(modulo.trocas(), TROCAS)
        self.assertEqual(json.dumps(modulo.trocas(), ensure_ascii=False, indent=1) + '\n', ler(CAMADA_REL))

    def test_aplicar_trocas_verifica_esta_e_as_de_baixo_que_partilham_ficheiros(self):
        r = subprocess.run([sys.executable, 'scripts/aplicar_trocas.py', CAMADA_REL, '--manifesto', MANIFESTO_REL, '--verificar'],
                           cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('32 trocas em 24 ficheiros: 32 aplicadas, 0 por aplicar; manifesto em dia.', r.stdout)
        # Cada camada de baixo que partilha um ficheiro com esta confere-se com as de cima desfeitas, esta primeiro.
        meus = set(MANIFESTO['files'])
        partilham = []
        for i, (camada, manifesto) in enumerate(verificar_camadas.LAYERS):
            if i == 0:
                continue
            if not meus & set(json.loads(ler(f'tests/fixtures/{manifesto}.json'))['files']):
                continue
            partilham.append(camada)
            comando = [sys.executable, 'scripts/aplicar_trocas.py', f'scripts/{camada}.json', '--manifesto', f'tests/fixtures/{manifesto}.json',
                       '--verificar']
            for _, acima in verificar_camadas.LAYERS[:i]:
                comando += ['--desfazer-antes', f'tests/fixtures/{acima}.json']
            if camada == 'auditoria_m4_m7_20261028':
                comando += ['--fora', 'tarefas/m7-u3/index.html']
            with self.subTest(camada=camada):
                r = subprocess.run(comando, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                self.assertIn('0 por aplicar; manifesto em dia.', r.stdout)
        self.assertEqual(len(partilham), 23)
        for camada in ('fila_final_20261115', 'exame_provas_oficial_20261112', 'cuidado_exame_20261112', 'cuidado_m5_20261108',
                       'cuidado_m8_20261112', 'cuidado_m9_20261112', 'autonomia_154_20261105', 'tarefas_faceis_m5_20261113'):
            self.assertIn(camada, partilham)

    def test_no_topo_da_pilha(self):
        self.assertEqual(verificar_camadas.LAYERS[0], ('revisao_geral_20261115', 'revisao-geral-edits-20261115'))
        self.assertEqual(verificar_camadas.LAYERS[1], ('fila_final_20261115', 'fila-final-edits-20261115'))
        self.assertEqual(len(verificar_camadas.LAYERS), 57)
        self.assertEqual(len(set(verificar_camadas.LAYERS)), len(verificar_camadas.LAYERS))

    def test_as_camadas_de_baixo_a_desfazem_primeiro(self):
        auditoria = ler('tests/auditoria_20261028.py')
        self.assertRegex(auditoria, r'def undo_fila_final_1115\(path, text\):\n(?:    #[^\n]*\n)*    text = undo_revisao_geral_1115\(path, text\)\n')
        # Desfeita a partir da árvore, a fila final tira primeiro esta camada: sessoes.json volta à base da fila final, letra a letra.
        fila = json.loads(ler(FILA_REL))['files'][SESSOES]
        self.assertEqual(sha_lf(undo_fila_final_1115(SESSOES, ler(SESSOES))), fila['base_sha256_lf'])
        sala = ler('scripts/desligar_sala.py')
        self.assertLess(sala.index('revisao-geral-edits-20261115.json'), sala.index('fila-final-edits-20261115.json'))
        historico = ler('scripts/tarefas_claras_historico.py')
        self.assertLess(historico.index('por_cima = REVISAO_GERAL.get(rel)'), historico.index('por_cima = FILA_FINAL.get(rel)'))
        # Os scripts das camadas que partilham ficheiros com esta leem-nos com ela desfeita primeiro (os do cuidado do M5, do M6, do M8 e
        # do M9 leem pela leitura histórica, acima).
        for nome in ('fila_final_20261115', 'tarefas_faceis_m5_20261113', 'exame_provas_oficial_20261112', 'cuidado_exame_20261112',
                     'cidade_cartaz_20261108', 'creditos_i_pt1_20261107'):
            self.assertIn("ROOT / 'tests/fixtures/revisao-geral-edits-20261115.json'", ler(f'scripts/{nome}.py'), nome)
        # Nos que também desfazem a fila final, esta vem primeiro.
        for nome in ('tarefas_faceis_m5_20261113', 'cuidado_exame_20261112', 'cidade_cartaz_20261108'):
            leitura = ler(f'scripts/{nome}.py')
            self.assertLess(leitura.index("ROOT / 'tests/fixtures/revisao-geral-edits-20261115.json'"),
                            leitura.index("ROOT / 'tests/fixtures/fila-final-edits-20261115.json'"), nome)
        for nome in ('cuidado_m5_20261108', 'cuidado_m6_20261108', 'cuidado_m8_20261112', 'cuidado_m9_20261112'):
            self.assertIn('tarefas_claras_historico', ler(f'scripts/{nome}.py'), nome)
        # Os browser_*.cjs que desfazem a fila final desfazem esta antes.
        for nome in ('browser_cartaz_indices.cjs', 'browser_cartaz_m4_piloto.cjs', 'browser_creditos_i_pt1.cjs'):
            texto = ler(f'tests/{nome}')
            self.assertIn("const revisaoGeral=JSON.parse(fs.readFileSync(path.join(root,'tests/fixtures/revisao-geral-edits-20261115.json')", texto)
            self.assertLess(texto.index('(revisaoGeral['), texto.index('(filaFinal['), nome)
        # Nas cadeias de --desfazer-antes dos testes e dos fluxos, esta camada vem logo antes da fila final, sem nada pelo meio.
        cadeia = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/fila-final-edits-20261115\.json')
        junta = re.compile(r'--desfazer-antes[ \',]+tests/fixtures/revisao-geral-edits-20261115\.json[ \',]+'
                           r'--desfazer-antes[ \',]+tests/fixtures/fila-final-edits-20261115\.json')
        for p in sorted((ROOT / '.github/workflows').glob('*.yml')) + sorted((ROOT / 'tests').glob('test_*.py')):
            if p.name == 'test_revisao_geral_20261115.py':
                continue
            texto = p.read_text('utf-8')
            self.assertEqual(len(cadeia.findall(texto)), len(junta.findall(texto)), p.name)
        # A conferência da fila final no fluxo desfaz esta antes; e esta confere-se sem nada por cima, com o seu teste.
        tarefas = ler('.github/workflows/pt-tarefas-qa.yml')
        self.assertIn('python scripts/aplicar_trocas.py scripts/fila_final_20261115.json --manifesto tests/fixtures/fila-final-edits-20261115.json '
                      '--verificar --desfazer-antes tests/fixtures/revisao-geral-edits-20261115.json\n', tarefas)
        self.assertIn('python scripts/aplicar_trocas.py scripts/revisao_geral_20261115.json --manifesto tests/fixtures/revisao-geral-edits-20261115.json '
                      '--verificar\n', tarefas)
        self.assertIn("python -m unittest discover -s tests -p 'test_revisao_geral_20261115.py' -v", tarefas)

    def test_os_fluxos_correm_quando_muda_o_que_a_camada_muda(self):
        def padrao(glob):
            partes = re.split(r'(\*\*|\*|\[[^\]]+\])', glob)
            return re.compile(''.join('.*' if x == '**' else '[^/]*' if x == '*' else x if x.startswith('[') else re.escape(x)
                                      for x in partes) + '$')
        da_camada = FICHEIROS + [CAMADA_REL, MANIFESTO_REL, 'scripts/revisao_geral_20261115.py', 'tests/test_revisao_geral_20261115.py',
                                 'scripts/provas/gerar.py', 'scripts/imagens_licoes_20261101.py', 'tests/fixtures/creditos-a-vista-20261105.json']
        for nome in ('pt-tarefas-qa.yml', 'pt-exame-laboratorio-qa.yml', 'pt-apoios-qa.yml'):
            texto = ler(f'.github/workflows/{nome}')
            cabeca = texto[texto.index('  pull_request:\n    paths:\n'):texto.index('\npermissions:')]
            padroes = [padrao(g) for g in re.findall(r"^      - '([^']+)'$", cabeca, re.M)]
            for rel in da_camada:
                self.assertTrue(any(q.match(rel) for q in padroes), (nome, rel))
        cartaz = ler('.github/workflows/cartaz-qa.yml')
        blocos = re.findall(r'^    paths: (\[.*\])$', cartaz, re.M)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0], blocos[1])
        self.assertIn("'tests/fixtures/fila-final-edits-20261115.json', 'scripts/revisao_geral_20261115.*', "
                      "'tests/fixtures/revisao-geral-edits-20261115.json'", blocos[0])


if __name__ == '__main__':
    unittest.main()
