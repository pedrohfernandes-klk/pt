#!/usr/bin/env python3
"""12/11/2026: as «Provas em cartões» do Exame (exame/provas/) passam a apontar para os documentos oficiais e a dizer só o que eles
dizem; e as referências da moldura deixam de se partir entre linhas.

Constrói scripts/exame_provas_oficial_20261112.json, a camada literal exame_provas_oficial_20261112, sobre as seis lições das duas
provas de 2026 (exame/provas/2026-1f e 2026-2f, grupos I, II e III), a secção exame/provas/index.html e os dados de onde elas saem
(scripts/provas/dados/: os seis grupo-x.json, os dois prova.json e seccao.json). São páginas geradas por scripts/provas/gerar.py e
congeladas por camada (cuidado_exame_20261112 e, no Grupo I da 1.ª fase, conteudos_lote2_20261101): só mudam por camada literal. A
camada aplica-se com scripts/aplicar_trocas.py e o manifesto fica em tests/fixtures/exame-provas-oficial-edits-20261112.json:

  python3 scripts/exame_provas_oficial_20261112.py
  python3 scripts/aplicar_trocas.py scripts/exame_provas_oficial_20261112.json \\
      --manifesto tests/fixtures/exame-provas-oficial-edits-20261112.json \\
      --base-commit 41c77a868c3291cfafb6ac754a50565f01fa78a1 --nota "…"

Fica por cima da ligação «Treinos» na página principal do Exame (exame_ligacao_treinos_20261112, no main 41c77a86, #199), com a
qual não partilha nenhum ficheiro, e por cima da decisão 152 no Exame (cuidado_exame_20261112), com a qual partilha as seis lições
e os seis grupo-x.json.

O que muda (cada mudança está escrita em EDICOES, sobre os dados; as páginas saem do gerador):
1. Ligações (decisão do utilizador, 12/11/2026): o enunciado, os critérios de classificação e a página da imagem do Grupo III da
   1.ª fase (p. 13 do enunciado) passam a levar a eduqa.pt, que publica os documentos; antes levavam a cópias em
   examesnacionais.com.pt. Os endereços são os que a transcrição já guardava (enunciado_original_url e criterios_original_url):
   conferidos a 12/11/2026 (200, application/pdf, iguais byte a byte aos de quem conferiu a camada oficial). As transcrições
   (tests/fixtures/prova-639-2026-*.json) não mudam.
2. Autoria (camada oficial, secção 5, linha 1): sai «IAVE». O enunciado e os critérios das duas fases só trazem, na p. 1, o
   logótipo da EduQA (ao lado do da República Portuguesa); «IAVE» não aparece em nenhum dos quatro PDF.
3. Marca de água (linha 2): sai a nota sobre a cópia dos critérios com «VERSÃO DE TRABALHO». Os critérios de eduqa.pt não têm
   marca (conferido nas 16 páginas das duas fases) e as ligações já não levam à cópia.
4. «Nas oito provas de 2023 a 2026 …» e «Em cinco provas … em três …» (linha 3): o repositório só tem as duas provas de 2026. As
   seis frases dos cartões «Para levar» passam a dizer o que essas duas provas mostram, com o número do item.
5. «conectores» (linha 8): onde lemos a grelha do parâmetro C do Grupo III, fica a formulação do critério, citada: «mecanismos de
   articulação interfrásica» (critérios, p. 15, nas duas fases), sem a estreitar.
6. «os tópicos são exemplos de formulações possíveis» (linha 9): os critérios pedem que se abordem os tópicos, «ou outros
   igualmente relevantes» (em cada item); exemplos de formulações são «as expressões separadas por barras oblíquas» (p. 4).
7. Referências e números que não se partem (achado 28 da varredura do cuidado, que a camada cuidado_exame_20261112 deixou para um
   pedido próprio, e a moldura das lições): U+00A0 no espaço que os prende e U+2060 a seguir ao hífen da sigla, na secção, no
   título <h1>, na cabeça, nas migalhas e nas ligações do menu, no crédito, no fim da lição, nas ligações da imagem com direitos
   e nos títulos e rótulos nossos dos cartões. Nunca em atributos nem no <title>.

O que fica como estava, de propósito:
- os 20 rótulos «Item N da prova…» dos cartões que mostram um item tal como está na prova. É por esse rótulo, com o espaço normal,
  que os testes (OFICIAL em tests/test_provas_cartoes.py, que tests/test_cuidado_exame.py também usa para ler a camada de baixo),
  a medição das opções (scripts/provas/opcoes.py), a camada de baixo (scripts/cuidado_exame_20261112.py) e o motor
  (assets/exame/provas-licao.js: /\\bItem \\d+ da prova\\b/) reconhecem o item oficial. Prendê-los obrigava a afrouxar esses
  testes ou a mudar o motor;
- as indicações de fonte (<p class="fonte">) e as referências dos textos «como a prova os indica», que são da transcrição;
- o texto oficial (o texto e os itens da prova, as grelhas, os tópicos e as regras dos critérios) e as citações entre «»;
- versao_licao (mudá-la recomeçava o progresso de quem já fez a lição) e as versões de cache.

Como as páginas são geradas: o gerador só muda de comportamento com chaves novas nos dados («autoria.texto», «autoria.ligacoes»
e «nao_partir» em prova.json; «nao_partir» em seccao.json). Sem elas, dá byte a byte as páginas de antes: é o que a camada de
baixo (cuidado_exame_20261112) confere quando volta a gerar as páginas a partir dos dados como ela os deixou. As chaves entram
nesta camada, com os dados.

O script calcula as trocas sobre a base (cada ficheiro com esta camada desfeita pelo manifesto, quando ele já existe): pode voltar
a correr depois de a camada estar aplicada e dá o mesmo JSON. Aplica EDICOES aos dados da base, gera as páginas com
scripts/provas/gerar.py sobre esses dados (numa pasta temporária) e tira as trocas da diferença entre a base e o resultado: cada
troca leva o contexto mínimo que a torna única na base e no resultado, e confere-se como scripts/aplicar_trocas.py a vai conferir.

As camadas de baixo desfazem primeiro esta: scripts/verificar_camadas.py (LAYERS[0]), tests/auditoria_20261028.py,
scripts/desligar_sala.py e scripts/cuidado_exame_20261112.py (a base das provas em cartões).
"""
import difflib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from aplicar_trocas import processar, TrocaFalhou  # noqa: E402

CAMADA = ROOT / 'scripts/exame_provas_oficial_20261112.json'
MANIFESTO = ROOT / 'tests/fixtures/exame-provas-oficial-edits-20261112.json'
NBSP, WJ = '\xa0', '\u2060'
PROVAS = ('2026-1f', '2026-2f')
GRUPOS = ('grupo-i', 'grupo-ii', 'grupo-iii')
DADOS = 'scripts/provas/dados'
SECCAO_DADOS = f'{DADOS}/seccao.json'
SECCAO = 'exame/provas/index.html'
FICHEIROS_DADOS = ([f'{DADOS}/{pv}/{g}.json' for pv in PROVAS for g in GRUPOS] + [f'{DADOS}/{pv}/prova.json' for pv in PROVAS]
                   + [SECCAO_DADOS])
PAGINAS = [f'exame/provas/{pv}/{g}/index.html' for pv in PROVAS for g in GRUPOS] + [SECCAO]
# O rótulo dos cartões com o item tal como está na prova: fica com o espaço normal (ver a docstring).
ITEM_DA_PROVA = re.compile(r'\bItem \d+ da prova\b')

ACHADOS = {
    'ligacoes': ('Decisão do utilizador (12/11/2026): as ligações para o enunciado, os critérios e a página da imagem levam a '
                 'eduqa.pt, que publica os documentos (antes, a cópias em examesnacionais.com.pt). Endereços conferidos a 12/11/2026.'),
    'autoria': ('Camada oficial, secção 5, linha 1: os PDF de 2026 só trazem o logótipo da EduQA (enunciado, p. 1; critérios, p. 1). '
                'Sai «IAVE».'),
    'marca': ('Camada oficial, secção 5, linha 2: sai a nota sobre a cópia dos critérios com a marca de água «VERSÃO DE TRABALHO»; os '
              'critérios de eduqa.pt, para onde as ligações passam a levar, não têm marca.'),
    'provas': ('Camada oficial, secção 5, linha 3: «Nas oito provas de 2023 a 2026» e «Em cinco provas … em três» não têm apoio no '
               'repositório, que só tem as duas provas de 2026; a frase passa a dizer o que essas duas mostram.'),
    'articulacao': ('Camada oficial, secção 5, linha 8: «conectores» estreitava o critério; fica a formulação do parâmetro C, citada: '
                    '«mecanismos de articulação interfrásica» (critérios, p. 15).'),
    'topicos': ('Camada oficial, secção 5, linha 9: os tópicos devem ser abordados, «ou outros igualmente relevantes» (em cada item); '
                'exemplos de formulações são «as expressões separadas por barras oblíquas» (critérios, p. 4).'),
    'presas': ('Achado 28 da varredura do cuidado (decisão 152) e moldura das provas em cartões: referências e números que não se '
               'partem entre linhas (U+00A0; U+2060 a seguir ao hífen da sigla). Fora de atributos e do <title>.'),
    'chaves': ('As chaves novas dos dados com que scripts/provas/gerar.py muda de comportamento (sem elas, as páginas saem como '
               'antes): «autoria.texto», «autoria.texto_curto», «autoria.ligacoes» e «nao_partir».'),
}


def j(s):
    """As formas escrevem-se com {N} (U+00A0) e {J} (U+2060)."""
    return s.replace('{N}', NBSP).replace('{J}', WJ)


# ---------- as mudanças, sobre os dados ----------
# (ficheiros, antigo, novo, ocorrências em cada ficheiro, categorias de ACHADOS). O antigo e o novo são texto cru do JSON (com \"
# onde o JSON o tem). Cada uma destas mudanças fica inteira numa troca, nos dados e nas páginas.

_GI = [f'{DADOS}/{pv}/grupo-i.json' for pv in PROVAS]
_GII = [f'{DADOS}/{pv}/grupo-ii.json' for pv in PROVAS]
_GIII = [f'{DADOS}/{pv}/grupo-iii.json' for pv in PROVAS]
_PROVA = [f'{DADOS}/{pv}/prova.json' for pv in PROVAS]
_AUTORIA_ANTES = (' "autoria": {\n'
                  '  "nota": "os PDF de 2026 trazem o logótipo da EduQA, Instituto de Educação, Qualidade e Avaliação, que os publica em eduqa.pt",\n'
                  '  "originais_em": "eduqa.pt",\n'
                  '  "nota_copias": "A cópia pública dos critérios tem a marca de água «VERSÃO DE TRABALHO»; o texto é igual ao dos critérios publicados em eduqa.pt (conferido a %s/10/2026)."\n'
                  ' },\n')
_AUTORIA_DEPOIS = j(' "autoria": {\n'
                    '  "_sobre": "12/11/2026: o que os PDF dizem de quem os faz e para onde levam as ligações. «texto» vai para o crédito do menu das lições e «texto_curto» para o bloco da prova na secção. «ligacoes»: «originais» faz as ligações do enunciado, dos critérios e da página da imagem levarem a quem publica os documentos (enunciado_original_url e criterios_original_url da transcrição).",\n'
                    '  "texto": "O enunciado e os critérios de classificação trazem, na p.{N}1, o logótipo da EduQA, Instituto de Educação, Qualidade e Avaliação, que os publica em eduqa.pt.",\n'
                    '  "texto_curto": "Enunciado e critérios de classificação com o logótipo da EduQA, Instituto de Educação, Qualidade e Avaliação (p.{N}1), publicados em eduqa.pt.",\n'
                    '  "ligacoes": "originais"\n'
                    ' },\n'
                    ' "_nao_partir": "12/11/2026: com true, as referências e os números da moldura que o gerador escreve (título, menu, migalhas, crédito, fim da lição, ligações da imagem e o bloco da prova na secção) levam U+00A0 e U+2060, para não se partirem entre linhas. Nunca em atributos nem no <title>.",\n'
                    ' "nao_partir": true,\n')
_TOPICOS_ANTES = 'Os critérios não trazem uma resposta modelo: os tópicos são exemplos de formulações possíveis.</p>'
_TOPICOS_DEPOIS = ('Os critérios não trazem uma resposta modelo: indicam tópicos a abordar, «ou outros igualmente relevantes». Dentro '
                   'dos tópicos, «as expressões separadas por barras oblíquas» são «exemplos de formulações possíveis, apresentadas em '
                   'alternativa» (p. 4 dos critérios).</p>')
_GIII_COMUM = ('<p>Nas duas provas de 2026, o Grupo{N}III vale 44{N}pontos, conta sempre para a classificação e pede um texto «bem '
               'estruturado» de 200{N}a{N}350{N}palavras, classificado nos parâmetros{N}A, B e{N}C e na correção linguística. ')
EDICOES = [
    # 1 a 3: ligações, autoria e marca de água (prova.json)
    ([_PROVA[0]], _AUTORIA_ANTES % '29', _AUTORIA_DEPOIS, 1, 'ligacoes autoria marca chaves'),
    ([_PROVA[1]], _AUTORIA_ANTES % '30', _AUTORIA_DEPOIS, 1, 'ligacoes autoria marca chaves'),
    # 2: autoria, nos cartões (sempre em <p class="fonte">)
    (_GI + _GII + _GIII, '(IAVE; os PDF de 2026 trazem o logótipo da EduQA, Instituto de Educação, Qualidade e Avaliação)',
     '(os PDF trazem o logótipo da EduQA, Instituto de Educação, Qualidade e Avaliação)', 1, 'autoria'),
    ([_GI[0]], '(IAVE; PDF com o logótipo da EduQA)', '(PDF com o logótipo da EduQA)', 6, 'autoria'),
    ([_GI[1]], '(IAVE; PDF com o logótipo da EduQA)', '(PDF com o logótipo da EduQA)', 6, 'autoria'),
    (_GII, '(IAVE; PDF com o logótipo da EduQA)', '(PDF com o logótipo da EduQA)', 1, 'autoria'),
    ([_GIII[0]], '(IAVE; PDF com o logótipo da EduQA)', '(PDF com o logótipo da EduQA)', 2, 'autoria'),
    ([_GIII[1]], '(IAVE; PDF com o logótipo da EduQA)', '(PDF com o logótipo da EduQA)', 3, 'autoria'),
    # 4: só o que as duas provas de 2026 mostram
    (_GI, j('<p>Nas oito provas de 2023 a 2026 (1.ª e 2.ª{N}fases), o Grupo{N}I acaba sempre numa breve exposição, com introdução, '
            'desenvolvimento e conclusão, e tem sempre um item em que identificas afirmações.</p>'),
     j('<p>Nas duas provas de 2026 (1.ª e 2.ª{N}fases), o Grupo{N}I acaba numa breve exposição, com introdução, desenvolvimento e '
       'conclusão (item{N}7), e tem um item em que identificas afirmações (item{N}6).</p>'), 1, 'provas'),
    ([_GII[0]], j('<p>Nas oito provas de 2023 a 2026 (1.ª e 2.ª{N}fases), o Grupo{N}II tem sempre sete itens de escolha múltipla, com '
                  'quatro opções: primeiro sobre o texto, no fim de gramática.</p>'),
     j('<p>Nas duas provas de 2026 (1.ª e 2.ª{N}fases), o Grupo{N}II tem sete itens de escolha múltipla, com quatro opções: os '
       'itens{N}1 a{N}4 sobre o texto e os itens{N}5 a{N}7 de gramática (leitura nossa).</p>'), 1, 'provas'),
    ([_GII[1]], j('<p>Nas oito provas de 2023 a 2026 (1.ª e 2.ª{N}fases), o Grupo{N}II tem sempre sete itens de escolha múltipla, com '
                  'quatro opções: primeiro sobre o texto, no fim de gramática (leitura nossa).</p>'),
     j('<p>Nas duas provas de 2026 (1.ª e 2.ª{N}fases), o Grupo{N}II tem sete itens de escolha múltipla, com quatro opções: os '
       'itens{N}1 a{N}4 sobre o texto e os itens{N}5 a{N}7 de gramática (leitura nossa).</p>'), 1, 'provas'),
    ([_GIII[0]], j('<p>Nas oito provas de 2023 a 2026 (1.ª e 2.ª{N}fases), o Grupo{N}III vale sempre 44{N}pontos, conta sempre e pede '
                   'sempre um texto «bem estruturado» de 200{N}a{N}350{N}palavras, classificado nos parâmetros{N}A, B e{N}C e na '
                   'correção linguística. Em cinco provas, o género é o texto de opinião; em três (2.ª{N}fase de 2023 e de 2025, '
                   '1.ª{N}fase de 2026), a apreciação crítica de uma imagem, com descrição, comentário em pelo menos três aspetos e '
                   'conclusão. Nos dois géneros, pede-se um discurso valorativo.</p>'),
     j(_GIII_COMUM + 'Na 1.ª{N}fase, o género é a apreciação crítica de uma imagem, com descrição, comentário em pelo menos três '
       'aspetos e conclusão; na 2.ª{N}fase, o texto de opinião. Nos dois géneros, pede-se um discurso valorativo.</p>'), 1, 'provas'),
    ([_GIII[1]], j('<p>Nas oito provas de 2023 a 2026 (1.ª e 2.ª{N}fases), o Grupo{N}III vale sempre 44{N}pontos, conta sempre e pede '
                   'sempre um texto «bem estruturado» de 200{N}a{N}350{N}palavras, classificado nos parâmetros{N}A, B e{N}C e na '
                   'correção linguística. Em cinco provas, o género é o texto de opinião (1.ª{N}fase de 2023, 2024 e 2025; '
                   '2.ª{N}fase de 2024 e de 2026), sempre com o ponto de vista, dois argumentos, cada um com um exemplo '
                   'significativo, e um discurso valorativo; em três, a apreciação crítica de uma imagem.</p>'),
     j(_GIII_COMUM + 'Na 2.ª{N}fase, o género é o texto de opinião, com o ponto de vista, dois argumentos, cada um com um exemplo '
       'significativo, e um discurso valorativo; na 1.ª{N}fase, a apreciação crítica de uma imagem.</p>'), 1, 'provas'),
    # 5: a formulação do critério (parâmetro C, p. 15)
    (_GIII, '>Marquei os parágrafos, com partes proporcionadas e ligadas por conectores?</td>',
     '>Marquei os parágrafos, com partes proporcionadas e articuladas entre si, e usei «mecanismos de articulação interfrásica»?</td>', 1, 'articulacao'),
    (_GIII, '<li><b>A forma também conta.</b> Parágrafos proporcionados, conectores pela relação certa, retomas sem repetição, pessoa '
            'e tempo verbal coerentes.</li>',
     '<li><b>A forma também conta.</b> Partes proporcionadas, parágrafos marcados, «mecanismos de articulação interfrásica» usados '
     'com adequação, retomas sem repetição, pessoa e tempo verbal coerentes.</li>', 1, 'articulacao'),
    ([_GIII[1]], '<li><b>10:</b> com partes proporcionadas, parágrafos marcados, conectores, retomas sem repetições e pessoa e tempo '
                 'coerentes.</li>',
     '<li><b>10:</b> com partes proporcionadas, parágrafos marcados, «mecanismos de articulação interfrásica», retomas sem '
     'repetições e pessoa e tempo coerentes.</li>', 1, 'articulacao'),
    # 6: os tópicos
    (_GI, _TOPICOS_ANTES, _TOPICOS_DEPOIS, 5, 'topicos'),
    # 7: referências presas nos dados da secção e da moldura (os títulos e os rótulos dos cartões prendem-se em prender_cartoes)
    (_PROVA, ', de 200 a 350 palavras', j(', de 200{N}a{N}350{N}palavras'), 1, 'presas'),
    (_PROVA, '"aprendes": "Aprendes a desmontar os itens de resposta escrita do Grupo I:',
     j('"aprendes": "Aprendes a desmontar os itens de resposta escrita do Grupo{N}I:'), 1, 'presas'),
    ([_PROVA[0]], 'A imagem está no PDF da prova, p. 13: cada cartão', j('A imagem está no PDF da prova, p.{N}13: cada cartão'), 1, 'presas'),
    ([SECCAO_DADOS], ' "seguir": "', ' "_nao_partir": "12/11/2026: com true, as referências do que é da secção inteira («Prova 639, 12.º ano» e '
     '«O que vem a seguir») levam U+00A0, para não se partirem entre linhas.",\n "nao_partir": true,\n "seguir": "', 1, 'chaves'),
]

# Títulos e rótulos nossos dos cartões, e o «aprendes» de cada grupo: a palavra e o número (ou a letra, ou o romano) que a segue.
_REF = re.compile(r'\b(Grupo|Item|Itens|item|itens|Partes?|Textos?|Poemas?|Linhas?|linhas?|Versos?|versos?) (\d+|[IVX]+\b|[A-C]\b)')
_SEQ = re.compile(r'(?<=[\dIVXA-C]) (a|e|de) (\d)')


def prender_texto(s):
    """«Item 1 ✱» dá «Item{N}1 ✱»; «linhas 1 a 10», «linhas{N}1 a{N}10»; «Itens 5, 6 e 7», «Itens{N}5, 6 e{N}7»; «Texto 1, 1 de 2»,
    «Texto{N}1, 1 de{N}2». Só com uma referência no texto (a palavra e o número); o resto fica como está."""
    if not _REF.search(s) and not re.search(r'\d (?:a|de) \d', s):
        return s
    s = _REF.sub(lambda m: m.group(1) + NBSP + m.group(2), s)
    return _SEQ.sub(lambda m: ' ' + m.group(1) + NBSP + m.group(2), s)


_CAMPO = re.compile(r'^(\s*"(titulo|rot|aprendes)": ")((?:[^"\\]|\\.)*)(",?)$', re.M)


def prender_cartoes(texto):
    """Os «titulo» e «rot» dos cartões e o «aprendes» do grupo com as referências presas, salvo os rótulos «Item N da prova…»
    (ver a docstring) e o «titulo» do grupo (antes da lista dos cartões), que não tem referências."""
    inicio = texto.index('"cartoes": [')

    def troca(m):
        chave, valor = m.group(2), m.group(3)
        if chave == 'aprendes' and m.start() > inicio or chave != 'aprendes' and m.start() < inicio:
            return m.group(0)
        if chave == 'rot' and ITEM_DA_PROVA.search(valor):
            return m.group(0)
        return m.group(1) + prender_texto(valor) + m.group(4)
    return _CAMPO.sub(troca, texto)


# ---------- a base, os dados finais e as páginas ----------

def ler(rel):
    return (ROOT / rel).read_bytes().decode('utf-8')


def base(rel):
    """O texto do ficheiro sem esta camada (desfeita pelo manifesto, da última troca para a primeira, com contagem estrita). Se a
    camada estiver por aplicar nesse ficheiro (nenhum novo lá está e cada antigo está, as vezes que o manifesto diz), o ficheiro
    já é a base."""
    texto = ler(rel)
    if MANIFESTO.is_file():
        edits = json.loads(MANIFESTO.read_text('utf-8'))['files'].get(rel, {}).get('edits', [])
        if edits and all(texto.count(e['new']) == 0 and texto.count(e['old']) == e['occurrences'] for e in edits):
            return texto
        for e in reversed(edits):
            if texto.count(e['new']) != e['occurrences']:
                raise SystemExit(f'{rel}: o manifesto desta camada já não confere ({e["location"]})')
            texto = texto.replace(e['new'], e['old'])
    return texto


def dados_finais():
    """{ficheiro de dados: (base, final)}: EDICOES e prender_cartoes aplicados à base, com contagem estrita."""
    out = {rel: [base(rel)] * 2 for rel in FICHEIROS_DADOS}
    for ficheiros, antigo, novo, n, _ in EDICOES:
        for rel in ficheiros:
            texto = out[rel][1]
            if texto.count(antigo) != n:
                raise SystemExit(f'{rel}: «{antigo[:70]}…» aparece {texto.count(antigo)} vez(es), não {n}')
            out[rel][1] = texto.replace(antigo, novo)
    for rel in FICHEIROS_DADOS:
        if '/grupo-' in rel:
            out[rel][1] = prender_cartoes(out[rel][1])
        json.loads(out[rel][1])
    return {rel: tuple(v) for rel, v in out.items()}


def gerar_com(dados):
    """As páginas que scripts/provas/gerar.py dá com estes dados ({ficheiro de dados: texto}), sem tocar na árvore."""
    spec = importlib.util.spec_from_file_location('provas_gerar_oficial', ROOT / 'scripts/provas/gerar.py')
    gerar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gerar)
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp) / 'dados'
        shutil.copytree(ROOT / DADOS, pasta)
        for rel, texto in dados.items():
            (pasta / rel.removeprefix(DADOS + '/')).write_bytes(texto.encode('utf-8'))
        gerar.DADOS = pasta
        try:
            saida, _ = gerar.gerar()
        except gerar.Falha as erro:
            raise SystemExit(f'o gerador das provas falhou: {erro}')
    return {rel: conteudo for rel, (conteudo, _) in saida.items()}


# ---------- da diferença às trocas ----------

_PEDACOS = re.compile(r'<[^<>]*>|[^<>\s]+\s*|\s+|.', re.S)


def diferencas(a, b):
    """Os intervalos que mudam, [(a0, a1, b0, b1)], apertados letra a letra, pela ordem do texto."""
    pa, pb = _PEDACOS.findall(a), _PEDACOS.findall(b)
    assert ''.join(pa) == a and ''.join(pb) == b
    ia, ib = [0], [0]
    for x in pa:
        ia.append(ia[-1] + len(x))
    for x in pb:
        ib.append(ib[-1] + len(x))
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        a0, a1, b0, b1 = ia[i1], ia[i2], ib[j1], ib[j2]
        while a0 < a1 and b0 < b1 and a[a0] == b[b0]:
            a0, b0 = a0 + 1, b0 + 1
        while a1 > a0 and b1 > b0 and a[a1 - 1] == b[b1 - 1]:
            a1, b1 = a1 - 1, b1 - 1
        out.append((a0, a1, b0, b1))
    return out


_FRONTEIRA = ' \n<>"'


class Intervalos:
    """Os intervalos das trocas, no texto antigo: cada diferença alargada (até à fronteira seguinte de palavra ou de etiqueta, dos
    dois lados) até ser única na base e no resultado, sem se sobrepor a outra. A posição no texto novo sai das diferenças: fora
    delas, os dois textos são iguais."""

    def __init__(self, a, b, sementes=()):
        """sementes: [(início, fim, categorias)] no texto antigo, os pedaços que ficam inteiros numa troca."""
        self.a, self.b, self.difs, self.sementes = a, b, diferencas(a, b), list(sementes)

    def esquerda(self, pos):
        """O início de um intervalo em pos: (posição no antigo, posição no novo). Nunca a meio de uma diferença."""
        delta = 0
        for a0, a1, b0, b1 in self.difs:
            if a0 < pos < a1 or (a0 == a1 == pos):
                return a0, b0
            if a1 <= pos:
                delta = b1 - a1
            else:
                break
        return pos, pos + delta

    def direita(self, pos):
        delta = 0
        for a0, a1, b0, b1 in self.difs:
            if a0 < pos < a1 or (a0 == a1 == pos):
                return a1, b1
            if a1 <= pos:
                delta = b1 - a1
            else:
                break
        return pos, pos + delta

    def alargar(self, h):
        a, (a0, a1) = self.a, h
        k = 1
        while a0 - k > 0 and a[a0 - k] not in _FRONTEIRA:
            k += 1
        a0 = self.esquerda(max(0, a0 - k))[0]
        k = 1
        while a1 + k < len(a) and a[a1 + k - 1] not in _FRONTEIRA:
            k += 1
        a1 = self.direita(min(len(a), a1 + k))[0]
        return a0, a1

    def textos(self, h):
        return self.a[h[0]:h[1]], self.b[self.esquerda(h[0])[1]:self.direita(h[1])[1]]

    def serve(self, h):
        a, b = self.a, self.b
        antigo, novo = self.textos(h)
        return (bool(antigo) and bool(novo) and a.count(antigo) == 1 and a.count(novo) == 0 and b.count(novo) == 1
                and b.replace(novo, '\0').count(antigo) == 0)

    @staticmethod
    def juntar(hs):
        out = []
        for h in sorted(hs):
            if out and h[0] <= out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], h[1]))
            else:
                out.append(h)
        return out

    def calcular(self):
        hs = [self.alargar((a0, a1)) for a0, a1, _, _ in self.difs]
        hs += [(self.esquerda(x)[0], self.direita(y)[0]) for x, y, _ in self.sementes]
        for _ in range(400):
            hs = self.juntar(hs)
            maus = [k for k, h in enumerate(hs) if not self.serve(h)]
            if not maus:
                return [self.textos(h) + (sorted({c for x, y, cs in self.sementes if h[0] <= x and y <= h[1] for c in cs.split()}),)
                        for h in hs]
            for k in maus:
                hs[k] = self.alargar(hs[k])
        raise SystemExit('não encontrei contexto que torne as trocas únicas')


def _visivel(s):
    s = s.replace('\\"', '"').replace('<\\/', '</').replace('\\n', ' ')
    s = re.sub(r'^[^<>]*>|<[^<>]*$', ' ', s)   # o resto de uma etiqueta cortada pelo contexto
    s = re.sub(r'<[^<>]*>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


ORDEM = list(ACHADOS)
# Nas páginas, o crédito (o menu das lições e o bloco da prova na secção) muda inteiro: autoria, ligações e, nas lições, a nota
# da marca de água.
CREDITO_LICAO = re.compile(r'Autor da prova e dos critérios de classificação: IAVE.*?\(conferido a \d\d/10/2026\)\.', re.S)
CREDITO_SECCAO = re.compile(r'Autor: IAVE.*?Originais: .*?critérios \(PDF\)</a>\.', re.S)


def sementes(rel, a):
    """Os pedaços do texto antigo que ficam inteiros numa troca: as mudanças de EDICOES (nos dados e, com o fecho das etiquetas escrito como nas páginas, nas páginas) e o
    crédito das páginas."""
    out = []
    pagina = rel.startswith('exame/')
    for ficheiros, antigo, _, n, cs in EDICOES:
        if pagina:
            if SECCAO_DADOS in ficheiros or any(f.endswith('prova.json') for f in ficheiros):
                continue
            if rel == SECCAO or rel.replace('exame/provas/', DADOS + '/').replace('/index.html', '.json') not in ficheiros:
                continue
            antigo = antigo.replace('</', '<\\/')
        elif rel not in ficheiros:
            continue
        ps = [m.start() for m in re.finditer(re.escape(antigo), a)]
        if len(ps) != n:
            raise SystemExit(f'{rel}: «{antigo[:70]}…» aparece {len(ps)} vez(es), não {n}')
        out += [(x, x + len(antigo), cs) for x in ps]
    if pagina:
        ms = list((CREDITO_SECCAO if rel == SECCAO else CREDITO_LICAO).finditer(a))
        if len(ms) != (2 if rel == SECCAO else 1):
            raise SystemExit(f'{rel}: o crédito não está onde se esperava')
        out += [(m.start(), m.end(), 'autoria ligacoes' + ('' if rel == SECCAO else ' marca')) for m in ms]
    return out


def categorias(antigo, novo, cs):
    """As categorias de uma troca: as das mudanças inteiras que ela leva e, pelo que muda, as ligações e as referências presas."""
    cs = set(cs)
    if 'examesnacionais' in antigo:
        cs.add('ligacoes')
    solto = lambda t: t.replace(NBSP, ' ').replace(WJ, '')
    if not cs and solto(antigo) != solto(novo):
        raise SystemExit(f'troca sem categoria: «{antigo[:120]}» para «{novo[:120]}»')
    if novo.count(NBSP) + novo.count(WJ) > antigo.count(NBSP) + antigo.count(WJ) and not cs & {'provas', 'chaves'}:
        cs.add('presas')
    return [c for c in ORDEM if c in cs]


def nome(rel):
    m = re.match(r'(?:exame/provas|scripts/provas/dados)/(\d{4})-(\d)f/(grupo-(i+)|prova)', rel)
    if rel == SECCAO:
        return 'Provas em cartões, a secção (exame/provas/index.html)'
    if rel == SECCAO_DADOS:
        return 'Provas em cartões, os dados da secção (seccao.json)'
    oque = 'os parâmetros (prova.json)' if m.group(3) == 'prova' else f'Grupo {m.group(4).upper()}'
    tipo = 'dados' if rel.startswith('scripts/') else 'lição'
    return f'Provas em cartões, Prova 639, {m.group(2)}.ª fase, {m.group(1)}, {oque} ({tipo})'


def trocas_do_ficheiro(rel, a, b):
    trocas = []
    for antigo, novo, cs in Intervalos(a, b, sementes(rel, a)).calcular():
        cs = categorias(antigo, novo, cs)
        trecho = _visivel(novo)
        trecho = trecho if len(trecho) <= 90 else trecho[:88].rstrip() + '…'
        trocas.append({'ficheiro': rel, 'local': f'{nome(rel)}: «{trecho}»', 'antigo': antigo, 'novo': novo, 'ocorrencias': 1,
                       'achado': '12/11/2026: ' + ' '.join(ACHADOS[c] for c in cs)})
    return trocas


def construir():
    """Devolve (trocas, {ficheiro: (base, final)}). Confere que o gerador, com os dados de antes, dá as páginas de antes (as chaves
    novas é que mudam as páginas), e cada ficheiro como o aplicar_trocas.py o vai conferir: a partir da base, e com tudo aplicado."""
    dados = dados_finais()
    antes = gerar_com({rel: v[0] for rel, v in dados.items()})
    depois = gerar_com({rel: v[1] for rel, v in dados.items()})
    if sorted(antes) != sorted(PAGINAS) or sorted(depois) != sorted(PAGINAS):
        raise SystemExit('o gerador das provas dá outras páginas')
    finais = dict(dados)
    for rel in PAGINAS:
        if antes[rel] != base(rel):
            raise SystemExit(f'{rel}: com os dados de antes, o gerador não dá a página de antes')
        finais[rel] = (antes[rel], depois[rel])
    todas = []
    for rel in FICHEIROS_DADOS + PAGINAS:
        a, b = finais[rel]
        if a == b:
            raise SystemExit(f'{rel}: nada muda')
        trocas = trocas_do_ficheiro(rel, a, b)
        lista = list(enumerate(trocas, 1))
        try:
            for texto in (a, b):
                x, y, _ = processar(rel, lista, texto)
                assert x == a and y == b
        except (TrocaFalhou, AssertionError) as erro:
            raise SystemExit(f'{rel}: as trocas não conferem: {erro}')
        todas += trocas
    return todas, finais


def main():
    todas, finais = construir()
    CAMADA.write_text(json.dumps(todas, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(f'{len(todas)} trocas em {len(finais)} ficheiros: {CAMADA.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
