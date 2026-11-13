"""28/10/2026: correções da auditoria do M1 e do M4, autorizadas literalmente.

O manifesto tests/fixtures/auditoria-m1-m4-edits-20261028.json guarda cada troca de texto (antigo, novo,
ocorrências). Os testes que comparam páginas com um estado congelado desfazem primeiro estas trocas, e só
depois aplicam os seus próprios manifestos. Uma troca que já não se encontre tantas vezes como o manifesto
diz faz falhar o teste: nada se desfaz em silêncio.

28/10/2026 (segundo lote): o M7 inteiro, o resto do M4 e o resto do M1 entram num segundo manifesto,
tests/fixtures/auditoria-m4-m7-edits-20261028.json, gerado por scripts/aplicar_trocas.py a partir de
scripts/auditoria_m4_m7_20261028.json. As trocas desse lote foram feitas por cima das do #128, por isso
desfazem-se primeiro: os manifestos ficam em MANIFESTS do mais recente para o mais antigo, e undo() desfaz
cada um, da última troca para a primeira, por essa ordem.

28/10/2026: a Sala de aula em tempo real saiu das páginas publicadas (decisão do docente de 17/10/2026;
scripts/desligar_sala.py). As trocas dessa mudança estão em tests/fixtures/sala-desligada-edits-20261028.json,
no mesmo formato. São as mais recentes (o script corre por cima dos dois lotes da auditoria), por isso undo()
desfaz primeiro a Sala, depois o segundo lote e só depois o #128.

29/10/2026: aquecimentos em cartões antes das aulas de tarefa do M7 e unidade 3 sem «Dia Pessoa» (decisões do docente
de 29/10). As trocas literais estão em tests/fixtures/aquecimentos-m7-edits-20261029.json, geradas por
scripts/aplicar_trocas.py a partir de scripts/aquecimentos_m7_20261029.json. É a camada mais recente: undo() desfaz-a
antes da Sala. A tarefa da unidade 3 do M7 foi gerada de novo (formato com escolha, scripts/tarefas_escolha.py) e é
autorizada pelo seu manifesto sucessor (tests/fixtures/m7-u3-choice-task-20261029.json, tests/task_source_contract.py):
as trocas de 28/10 dessa página ficaram no predecessor compacto e não há nada delas a desfazer na página nova.

30/10/2026: aquecimentos em cartões antes das aulas de tarefa do M1 (mesma decisão de 29/10, ordem M7, M1, M4). As trocas
literais estão em tests/fixtures/aquecimentos-m1-edits-20261030.json, geradas por scripts/aplicar_trocas.py a partir de
scripts/aquecimentos_m1_20261030.json. É agora a camada mais recente: undo() desfá-la antes da camada do M7. As tarefas
das unidades 1 e 2 do M1 foram geradas de novo por scripts/tarefas_escolha.py; a camada guarda a diferença das páginas
e dos dados públicos, por isso, depois de a desfazer, os manifestos sucessores de 28/10 continuam a conferir.

30/10/2026 (depois do M1): aquecimentos em cartões antes das aulas de tarefa do M4 e apresentações da U1 e da U3 em pequenos
grupos. As trocas literais estão em tests/fixtures/aquecimentos-m4-edits-20261030.json, geradas por scripts/aplicar_trocas.py
a partir de scripts/aquecimentos_m4_20261030.json. É agora a camada mais recente: undo() desfá-la antes da do M1.

30/10/2026 (depois do M4): aquecimentos em cartões antes das aulas de tarefa do M2. As trocas literais estão em
tests/fixtures/aquecimentos-m2-edits-20261030.json, geradas por scripts/aplicar_trocas.py a partir de
scripts/aquecimentos_m2_20261030.json. É agora a camada mais recente: undo() desfá-la antes da do M4.
30/10/2026: texto corrido justificado (decisão do docente). Os excertos em prosa citados em blockquote nos percursos
«Pensar devagar» e a prosa dialogada escrita com <br> nos exercícios do M5 levam a classe «prosa», para que
assets/appearance.css os justifique sem justificar as estrofes, que usam a mesma marcação. As trocas literais estão em
tests/fixtures/texto-justificado-edits-20261030.json, geradas por scripts/aplicar_trocas.py a partir de
scripts/texto_justificado_20261030.json. É agora a camada mais recente: undo() desfá-la antes de todas as outras (antes da do M2).
Revisão de 30/10/2026: a mesma camada põe também a classe «verso» nos parágrafos que só trazem verso citado, «prosa» nos
três blockquote sem parágrafos de m4/recursos/tpc-entrada.js e lang="en" em dois trechos em inglês; nenhum texto muda.
30/10/2026 (depois do texto justificado): opções denunciadoras (pedido do docente de 29/10: a certa não pode ser «quase de
certeza» a mais comprida). As trocas literais estão em tests/fixtures/opcoes-denunciadoras-edits-20261030.json, geradas por
scripts/aplicar_trocas.py a partir de scripts/opcoes_denunciadoras_20261030.json: só o texto das opções e do feedback que as
cita. É agora a camada mais recente: undo() desfá-la antes de todas as outras (antes da do texto justificado).
30/10/2026 (depois das opções): perguntas em português europeu («Qual das…», «Que…», nunca «Qual» seguido de nome), os versos
12 e 14 de «Ela canta, pobre ceifeira» como na Athena, n.º 3, 1924 (M7-F13 e cópias), o aquecimento da M7-U2 fixo em 10 minutos e
os pesos do M7 no mapa. As trocas literais estão em tests/fixtures/lingua-pessoa-m7-edits-20261030.json, geradas por
scripts/aplicar_trocas.py a partir de scripts/lingua_pessoa_m7_20261030.json. É agora a camada mais recente: undo() desfá-la antes
de todas as outras (antes da das opções denunciadoras).
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
# 28/10/2026: o mais recente primeiro (o segundo lote foi aplicado por cima do #128).
MANIFESTS = (
    ROOT / 'tests/fixtures/auditoria-m4-m7-edits-20261028.json',
    ROOT / 'tests/fixtures/auditoria-m1-m4-edits-20261028.json',
)
MANIFEST = MANIFESTS[-1]  # o manifesto do #128, para quem o queira ler sozinho
_LAYERS = tuple((path.name, json.loads(path.read_text('utf-8'))['files']) for path in MANIFESTS)
# 28/10/2026: o manifesto da Sala desligada (gerado por scripts/desligar_sala.py) desfaz-se antes dos da auditoria.
SALA_MANIFEST = ROOT / 'tests/fixtures/sala-desligada-edits-20261028.json'
_SALA_FILES = json.loads(SALA_MANIFEST.read_text('utf-8'))['files']


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def undo_sala(path, text):
    """28/10/2026: devolve o texto anterior ao corte da Sala para este ficheiro (ou o mesmo texto, se não o tem)."""
    relative = _relative(path)
    for edit in reversed(_SALA_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Corte da Sala autorizado a 28/10 já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 29/10/2026: a camada dos aquecimentos e da unidade 3 do M7 (a mais recente; desfaz-se antes da Sala).
AQUECIMENTOS_MANIFEST = ROOT / 'tests/fixtures/aquecimentos-m7-edits-20261029.json'
_AQUECIMENTOS_FILES = json.loads(AQUECIMENTOS_MANIFEST.read_text('utf-8'))['files']
# 29/10/2026: páginas geradas de novo por cima das trocas de 28/10, com manifesto sucessor próprio.
REGENERADAS_20261029 = frozenset({'tarefas/m7-u3/index.html'})


# 30/10/2026: a camada dos aquecimentos do M2 (a mais recente; desfaz-se antes da do M4).
AQUECIMENTOS_M2_MANIFEST = ROOT / 'tests/fixtures/aquecimentos-m2-edits-20261030.json'
_AQUECIMENTOS_M2_FILES = json.loads(AQUECIMENTOS_M2_MANIFEST.read_text('utf-8'))['files']


def undo_aquecimentos_m2(path, text):
    """30/10/2026: devolve o texto anterior à camada dos aquecimentos do M2 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_AQUECIMENTOS_M2_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 (M2) já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 30/10/2026: a camada dos aquecimentos do M4 (desfaz-se antes da do M1).
AQUECIMENTOS_M4_MANIFEST = ROOT / 'tests/fixtures/aquecimentos-m4-edits-20261030.json'
_AQUECIMENTOS_M4_FILES = json.loads(AQUECIMENTOS_M4_MANIFEST.read_text('utf-8'))['files']


def undo_aquecimentos_m4(path, text):
    """30/10/2026: devolve o texto anterior à camada dos aquecimentos do M4 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_AQUECIMENTOS_M4_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 (M4) já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 30/10/2026: a camada dos aquecimentos do M1 (desfaz-se antes da do M7).
AQUECIMENTOS_M1_MANIFEST = ROOT / 'tests/fixtures/aquecimentos-m1-edits-20261030.json'
_AQUECIMENTOS_M1_FILES = json.loads(AQUECIMENTOS_M1_MANIFEST.read_text('utf-8'))['files']


def undo_aquecimentos_m1(path, text):
    """30/10/2026: devolve o texto anterior à camada dos aquecimentos do M1 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_AQUECIMENTOS_M1_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_aquecimentos(path, text):
    """29/10/2026: devolve o texto anterior à camada dos aquecimentos do M7 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_AQUECIMENTOS_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 29/10 já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 30/10/2026: a camada do texto justificado (a mais recente; desfaz-se antes das dos aquecimentos do M4, do M1 e do M7).
JUSTIFICADO_MANIFEST = ROOT / 'tests/fixtures/texto-justificado-edits-20261030.json'
_JUSTIFICADO_FILES = json.loads(JUSTIFICADO_MANIFEST.read_text('utf-8'))['files']


def undo_justificado(path, text):
    """30/10/2026: devolve o texto anterior à classe «prosa» do texto justificado (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_JUSTIFICADO_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 30/10/2026: a camada das opções denunciadoras (a mais recente; desfaz-se antes da do texto justificado).
OPCOES_MANIFEST = ROOT / 'tests/fixtures/opcoes-denunciadoras-edits-20261030.json'
_OPCOES_FILES = json.loads(OPCOES_MANIFEST.read_text('utf-8'))['files']


def undo_opcoes(path, text):
    """30/10/2026: devolve o texto anterior às opções denunciadoras reescritas (ou o mesmo texto, se não as tem)."""
    relative = _relative(path)
    for edit in reversed(_OPCOES_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 (opções) já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 30/10/2026: a camada da língua das perguntas, do Pessoa da F13 e dos acertos do M7 (a mais recente; desfaz-se antes da das
# opções denunciadoras).
LINGUA_MANIFEST = ROOT / 'tests/fixtures/lingua-pessoa-m7-edits-20261030.json'
_LINGUA_FILES = json.loads(LINGUA_MANIFEST.read_text('utf-8'))['files']


def undo_lingua(path, text):
    """30/10/2026: devolve o texto anterior à camada da língua, do Pessoa da F13 e do M7 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_LINGUA_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 30/10 (língua) já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 31/10/2026: camada mais recente, tarefas M3, M5 e M6.
TAREFAS_M356_MANIFEST = ROOT / 'tests/fixtures/tarefas-m356-edits-20261031.json'
_TAREFAS_M356_FILES = json.loads(TAREFAS_M356_MANIFEST.read_text('utf-8'))['files']


def undo_tarefas_m356(path, text):
    relative = _relative(path)
    for edit in reversed(_TAREFAS_M356_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca de 31/10 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 01/11/2026: camada mais recente, tarefas M8 e M9.
TAREFAS_M89_MANIFEST = ROOT / 'tests/fixtures/tarefas-m89-edits-20261101.json'
_TAREFAS_M89_FILES = json.loads(TAREFAS_M89_MANIFEST.read_text('utf-8'))['files']


# 01/11/2026: as sete lições M8/M9 são a camada mais recente, acima do #145.
LICOES_M89_MANIFEST = ROOT / 'tests/fixtures/licoes-m89-edits-20261101.json'
_LICOES_M89_FILES = json.loads(LICOES_M89_MANIFEST.read_text('utf-8'))['files']


# 01/11/2026: camada mais recente, nove lições do pedido B, acima do pedido A.
_LICOES_M16_FILES = json.loads((ROOT / 'tests/fixtures/licoes-m16-edits-20261101.json').read_text('utf-8'))['files']


def undo_licoes_m16(path, text):
    # 01/11/2026: integrar o lote de conteúdos acima dos pedidos de lições.
    text = undo_cartaz_indices(path, text)
    relative = _relative(path)
    for edit in reversed(_LICOES_M16_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Lições M1/M6 de 01/11 não conferem: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_licoes_m89(path, text):
    text = undo_licoes_m16(path, text)
    relative = _relative(path)
    for edit in reversed(_LICOES_M89_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Lições de 01/11 não conferem: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 02/11/2026: o fundo animado da entrada (pt #159 e #160) entrou no main sem camada; fica registado como camada própria,
# abaixo das lições M8/M9 (que foram juntadas por cima dele) e acima das tarefas M8/M9.
FUNDOS_MANIFEST = ROOT / 'tests/fixtures/fundos-edits-20261102.json'
_FUNDOS_FILES = json.loads(FUNDOS_MANIFEST.read_text('utf-8'))['files']


def undo_fundos(path, text):
    relative = _relative(path)
    for edit in reversed(_FUNDOS_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Fundo de 02/11 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_tarefas_m89(path, text):
    # 01/11/2026: também os contratos que desfazem só esta camada recebem a base correta.
    text = undo_licoes_m89(path, text)
    # 02/11/2026: e o fundo da entrada, que está entre as lições M8/M9 e as tarefas M8/M9.
    text = undo_fundos(path, text)
    relative = _relative(path)
    for edit in reversed(_TAREFAS_M89_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca de 01/11 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 02/11/2026: tarefas individuais (pedido do docente: não há tarefas de grupo), camada mais recente, por cima dos índices.
_TAREFAS_INDIVIDUAIS = json.loads((ROOT / 'tests/fixtures/tarefas-individuais-edits-20261102.json').read_text('utf-8'))['files']


# 02/11/2026: decisão 139, a calçada «mar largo» na entrada do Português, camada mais recente, por cima das tarefas individuais.
_CALCADA_MAR = json.loads((ROOT / 'tests/fixtures/calcada-mar-edits-20261102.json').read_text('utf-8'))['files']


# 02/11/2026: a varredura de formatação (pt #152), refeita em trocas mínimas sobre o main, é a camada mais recente,
# por cima da calçada da entrada.
VARREDURA_MANIFEST = ROOT / 'tests/fixtures/varredura-formatacao-edits-20261101.json'
_VARREDURA_FILES = json.loads(VARREDURA_MANIFEST.read_text('utf-8'))['files']


# 02/11/2026: crédito de IA por cima das camadas publicadas, com correspondência estrita.
# 03/11/2026: reversao estrita da abertura, antes dos creditos.
_CABECALHO = json.loads((ROOT/'tests/fixtures/cartaz-cabecalho-edits-20261103.json').read_text('utf-8'))['files']

# 05/11/2026: revisão de 5/11, camada mais recente: desfaz-se antes do cabeçalho, com contagem estrita.
_REVISAO_0511 = json.loads((ROOT/'tests/fixtures/revisao-edits-20261105.json').read_text('utf-8'))['files']

# 05/11/2026: tabela dos seis movimentos, camada mais recente: desfaz-se antes da revisão de 5/11, com contagem estrita.
_TABELA_0511 = json.loads((ROOT/'tests/fixtures/tabela-movimentos-edits-20261105.json').read_text('utf-8'))['files']

# 05/11/2026: Laboratório do exame (lição, não «leitura de apoio»), camada mais recente: desfaz-se antes da tabela, com contagem estrita.
_EXAME_0511 = json.loads((ROOT/'tests/fixtures/exame-licao-edits-20261105.json').read_text('utf-8'))['files']

# 05/11/2026: o texto de contexto de cada sessão do Laboratório do exame (lição e excerto, não «leitura de apoio» nem «recorte»),
# camada mais recente: desfaz-se antes da ligação e das notas do Laboratório do exame, com contagem estrita.
_CONTEXTO_0511 = json.loads((ROOT/'tests/fixtures/exame-contexto-edits-20261105.json').read_text('utf-8'))['files']

# 05/11/2026: Atlas Lusófono, lote 3 (atlas, entrada e páginas dos anos), camada mais recente: desfaz-se antes da decisão 154
# (06/11/2026: por cima dela, depois de juntar o main), com contagem estrita.
_ATLAS_LOTE3_0511 = json.loads((ROOT/'tests/fixtures/atlas-lote3-edits-20261105.json').read_text('utf-8'))['files']

# 05/11/2026: decisão 153, os créditos das imagens atrás de um «i» (pedido pt-2), camada mais recente (06/11/2026: por cima do
# lote 3 do Atlas, depois de juntar o main): desfaz-se antes do Atlas, com contagem estrita.
_CREDITOS_I_0511 = json.loads((ROOT/'tests/fixtures/creditos-i-edits-20261105.json').read_text('utf-8'))['files']

# 06/11/2026: decisão 152 (cuidado em todas as lições), módulo M1: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima dos créditos atrás de um «i»: desfaz-se antes deles, com contagem estrita. 07/11/2026 (fusão do main 29441e6b): por cima dos acertos da decisão 173.
_CUIDADO_M1_0611 = json.loads((ROOT/'tests/fixtures/cuidado-m1-edits-20261106.json').read_text('utf-8'))['files']

# 07/11/2026: decisões 153, 176 e 177, créditos atrás de um «i» na entrada, nos nove índices e no Atlas (pedido pt-1), camada mais
# recente, por cima da decisão 152 no M1: desfaz-se antes dela, com contagem estrita.
_CREDITOS_I_PT1_0711 = json.loads((ROOT/'tests/fixtures/creditos-i-pt1-edits-20261107.json').read_text('utf-8'))['files']

# 08/11/2026: cartaz «Ler a cidade» na entrada do Português e nome novo da secção nas páginas publicadas (pedido do utilizador:
# «quero que [Ler a cidade] tenha um banner em português»), camada mais recente, por cima dos créditos atrás de um «i» do pedido
# pt-1: desfaz-se antes deles, com contagem estrita.
_CIDADE_CARTAZ_0811 = json.loads((ROOT/'tests/fixtures/cidade-cartaz-edits-20261108.json').read_text('utf-8'))['files']

# 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M2: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima do cartaz «Ler a cidade» e do nome novo da secção: desfaz-se antes deles, com
# contagem estrita.
_CUIDADO_M2_0811 = json.loads((ROOT/'tests/fixtures/cuidado-m2-edits-20261108.json').read_text('utf-8'))['files']

# 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M3: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M2: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M3_0811 = json.loads((ROOT/'tests/fixtures/cuidado-m3-edits-20261108.json').read_text('utf-8'))['files']

# 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M4: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M3: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M4_0811 = json.loads((ROOT/'tests/fixtures/cuidado-m4-edits-20261108.json').read_text('utf-8'))['files']

# 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M5: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M4: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M5_0811 = json.loads((ROOT/'tests/fixtures/cuidado-m5-edits-20261108.json').read_text('utf-8'))['files']

# 08/11/2026: decisão 152 (cuidado em todas as lições), módulo M6: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M5: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M6_0811 = json.loads((ROOT/'tests/fixtures/cuidado-m6-edits-20261108.json').read_text('utf-8'))['files']

# 11/11/2026: decisão 152 (cuidado em todas as lições), módulo M7: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M6: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M7_1111 = json.loads((ROOT/'tests/fixtures/cuidado-m7-edits-20261111.json').read_text('utf-8'))['files']

# 12/11/2026: decisão 152 (cuidado em todas as lições), módulo M8: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M7: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M8_1112 = json.loads((ROOT/'tests/fixtures/cuidado-m8-edits-20261112.json').read_text('utf-8'))['files']

# 12/11/2026: decisão 152 (cuidado em todas as lições), módulo M9: tabelas onde há itens paralelos e referências e números que
# não se partem, camada mais recente, por cima da decisão 152 no M8: desfaz-se antes dela, com contagem estrita.
_CUIDADO_M9_1112 = json.loads((ROOT/'tests/fixtures/cuidado-m9-edits-20261112.json').read_text('utf-8'))['files']

# 12/11/2026: decisão 152 (cuidado em todas as lições), Exame e páginas transversais: uma tabela onde havia itens paralelos e
# referências e números que não se partem, camada mais recente, por cima da decisão 152 no M9: desfaz-se antes dela, com contagem
# estrita. Não toca nas tarefas das unidades: não precisa da exceção da revisão dos enunciados.
_CUIDADO_EXAME_1112 = json.loads((ROOT/'tests/fixtures/cuidado-exame-edits-20261112.json').read_text('utf-8'))['files']

# 12/11/2026: a ligação «Treinos» na navegação da página principal do Exame (exame/index.html), camada mais recente, por cima da
# decisão 152 no Exame e nas páginas transversais: desfaz-se antes dela, com contagem estrita. Só toca em exame/index.html.
_EXAME_LIGACAO_TREINOS_1112 = json.loads((ROOT/'tests/fixtures/exame-ligacao-treinos-edits-20261112.json').read_text('utf-8'))['files']

# 12/11/2026: as provas em cartões com os documentos oficiais (a secção exame/provas/, as seis lições das provas de 2026 e os seus
# dados), camada mais recente, por cima da ligação «Treinos» na página principal do Exame e da decisão 152 no Exame e nas páginas
# transversais (com a qual partilha as seis lições e os seis grupo-x.json): desfaz-se antes delas, com contagem estrita.
_EXAME_PROVAS_OFICIAL_1112 = json.loads((ROOT/'tests/fixtures/exame-provas-oficial-edits-20261112.json').read_text('utf-8'))['files']

# 12/11/2026: as duas tarefas do M3 «mais fáceis de fazer» e «tudo junto» no M3 (os enunciados, as grelhas, as correções e os
# aquecimentos da m3-u1 e da m3-u2, os seus dados, e o guia, o índice e o mapa do M3), camada mais recente, por cima das provas em
# cartões com os documentos oficiais (com a qual não partilha nenhum ficheiro): desfaz-se antes de todas, com contagem estrita.
_TAREFAS_FACEIS_M3_1112 = json.loads((ROOT/'tests/fixtures/tarefas-faceis-m3-edits-20261112.json').read_text('utf-8'))['files']

# 13/11/2026: as duas tarefas do M1 «mais fáceis de fazer» e «tudo junto» no M1 (os enunciados, as grelhas e as correções da m1-u1 e
# da m1-u2, os seus dados, e o guia, o índice e o portefólio do M1), camada mais recente, por cima das tarefas do M3 mais fáceis de fazer (com a
# qual partilha os dados das grelhas): desfaz-se antes de todas, com contagem estrita.
_TAREFAS_FACEIS_M1_1113 = json.loads((ROOT/'tests/fixtures/tarefas-faceis-m1-edits-20261113.json').read_text('utf-8'))['files']

# 13/11/2026: as duas tarefas do M6 «mais fáceis de fazer» e «tudo junto» no M6 (os enunciados, as grelhas, as correções e os
# aquecimentos da m6-u1 e da m6-u2, os seus dados, e o guia, o índice, o mapa e o portefólio do M6), camada mais recente, por cima
# das tarefas do M5 mais fáceis de fazer (com a qual partilha os dados das grelhas): desfaz-se antes de todas, com contagem estrita.
_TAREFAS_FACEIS_M6_1113 = json.loads((ROOT/'tests/fixtures/tarefas-faceis-m6-edits-20261113.json').read_text('utf-8'))['files']

def undo_tarefas_faceis_m6_1113(path, text):
    # Pela mesma regra das camadas do M3, do M1 e do M5: esta camada está no topo, por isso o ficheiro da árvore é exatamente a página
    # como ela a deixou (o hash «after» do manifesto, que scripts/verificar_camadas.py e tests/test_tarefas_faceis_m6.py conferem). Só
    # esse texto se desfaz, com contagem estrita; quem já a desfez (ou entrega um texto histórico) recebe o texto como o deu.
    entrada = _TAREFAS_FACEIS_M6_1113.get(_relative(path))
    if not entrada or hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() != entrada['after_sha256_lf']:
        return text
    for edit in reversed(entrada['edits']):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tarefas do M6 mais fáceis de fazer não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 13/11/2026: as duas tarefas do M5 «mais fáceis de fazer» e «tudo junto» no M5 (os enunciados, as grelhas, as correções e os
# aquecimentos da m5-u1 e da m5-u2, os seus dados, e o guia, o índice, o mapa e o portefólio do M5), com dois acertos do M3 (o
# portefólio do M3 e o tema B da m3-u2), camada mais recente, por cima das tarefas do M1 mais fáceis de fazer (com a qual partilha os
# dados das grelhas): desfaz-se antes de todas, com contagem estrita.
_TAREFAS_FACEIS_M5_1113 = json.loads((ROOT/'tests/fixtures/tarefas-faceis-m5-edits-20261113.json').read_text('utf-8'))['files']

def undo_tarefas_faceis_m5_1113(path, text):
    # 13/11/2026: primeiro as tarefas do M6 mais fáceis de fazer, que estão por cima de todas (partilham os dados das grelhas).
    text = undo_tarefas_faceis_m6_1113(path, text)
    # Pela mesma regra das camadas do M3 e do M1: esta camada está no topo, por isso o ficheiro da árvore é exatamente a página como
    # ela a deixou (o hash «after» do manifesto, que scripts/verificar_camadas.py e tests/test_tarefas_faceis_m5.py conferem). Só esse
    # texto se desfaz, com contagem estrita; quem já a desfez (ou entrega um texto histórico) recebe o texto como o deu.
    entrada = _TAREFAS_FACEIS_M5_1113.get(_relative(path))
    if not entrada or hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() != entrada['after_sha256_lf']:
        return text
    for edit in reversed(entrada['edits']):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tarefas do M5 mais fáceis de fazer não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_tarefas_faceis_m1_1113(path, text):
    # 13/11/2026: primeiro as tarefas do M5 mais fáceis de fazer, que estão por cima (partilham os dados das grelhas).
    text = undo_tarefas_faceis_m5_1113(path, text)
    # Pela mesma regra da camada do M3: esta camada está no topo, por isso o ficheiro da árvore é exatamente a página como ela a
    # deixou (o hash «after» do manifesto, que scripts/verificar_camadas.py e tests/test_tarefas_faceis_m1.py conferem). Só esse
    # texto se desfaz, com contagem estrita; quem já a desfez (ou entrega um texto histórico) recebe o texto como o deu.
    entrada = _TAREFAS_FACEIS_M1_1113.get(_relative(path))
    if not entrada or hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() != entrada['after_sha256_lf']:
        return text
    for edit in reversed(entrada['edits']):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tarefas do M1 mais fáceis de fazer não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_tarefas_faceis_m3_1112(path, text):
    # 13/11/2026: primeiro as tarefas do M1 mais fáceis de fazer, que estão por cima (partilham os dados das grelhas).
    text = undo_tarefas_faceis_m1_1113(path, text)
    # Pela regra de scripts/tarefas_claras_historico.py: esta camada está no topo, por isso o ficheiro da árvore é exatamente a página
    # como ela a deixou (o hash «after» do manifesto, que scripts/verificar_camadas.py e tests/test_tarefas_faceis_m3.py conferem).
    # Só esse texto se desfaz, com contagem estrita; quem já a desfez (ou entrega um texto histórico) recebe o texto como o deu, e
    # nada se desfaz duas vezes.
    entrada = _TAREFAS_FACEIS_M3_1112.get(_relative(path))
    if not entrada or hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() != entrada['after_sha256_lf']:
        return text
    for edit in reversed(_TAREFAS_FACEIS_M3_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tarefas do M3 mais fáceis de fazer não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_exame_provas_oficial_1112(path, text):
    # 12/11/2026: primeiro as tarefas do M3 mais fáceis de fazer, que estão por cima.
    text = undo_tarefas_faceis_m3_1112(path, text)
    for edit in reversed(_EXAME_PROVAS_OFICIAL_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Provas em cartões com os documentos oficiais não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_exame_ligacao_treinos_1112(path, text):
    # 12/11/2026: primeiro as provas em cartões com os documentos oficiais, que estão por cima.
    text = undo_exame_provas_oficial_1112(path, text)
    for edit in reversed(_EXAME_LIGACAO_TREINOS_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Ligação «Treinos» na página principal do Exame não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_exame_1112(path, text):
    # 12/11/2026: primeiro a ligação «Treinos» na página principal do Exame, que está por cima.
    text = undo_exame_ligacao_treinos_1112(path, text)
    for edit in reversed(_CUIDADO_EXAME_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no Exame e nas páginas transversais não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m9_1112(path, text):
    # 12/11/2026: primeiro a decisão 152 no Exame e nas páginas transversais, que está por cima.
    text = undo_cuidado_exame_1112(path, text)
    # 12/11/2026: a mesma exceção das camadas do M6, do M7 e do M8, pela mesma razão. As tarefas da M9-U1 e da M9-U2 (as páginas e
    # os dados) estão nesta camada e na revisão dos enunciados (#192); quem as lê como eram antes da revisão
    # (scripts/tarefas_claras_historico.py desfaz esta camada e a dos enunciados, por esta ordem) entrega exatamente a base da
    # revisão (o hash do seu manifesto): esta camada já saiu e não há nada a desfazer. Em qualquer outro caso, a contagem continua
    # estrita.
    claras = _TAREFAS_CLARAS.get(_relative(path))
    if claras and hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() == claras['base_sha256_lf']:
        return text
    for edit in reversed(_CUIDADO_M9_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M9 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m8_1112(path, text):
    # 12/11/2026: primeiro a decisão 152 no M9, que está por cima.
    text = undo_cuidado_m9_1112(path, text)
    # 12/11/2026: a mesma exceção das camadas do M6 e do M7, pela mesma razão. As tarefas da M8-U1 e da M8-U2 (as páginas e os
    # dados) estão nesta camada e na revisão dos enunciados (#192); quem as lê como eram antes da revisão
    # (scripts/tarefas_claras_historico.py desfaz esta camada e a dos enunciados, por esta ordem) entrega exatamente a base da
    # revisão (o hash do seu manifesto): esta camada já saiu e não há nada a desfazer. Em qualquer outro caso, a contagem continua
    # estrita.
    claras = _TAREFAS_CLARAS.get(_relative(path))
    if claras and hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() == claras['base_sha256_lf']:
        return text
    for edit in reversed(_CUIDADO_M8_1112.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M8 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m7_1111(path, text):
    # 12/11/2026: primeiro a decisão 152 no M8, que está por cima.
    text = undo_cuidado_m8_1112(path, text)
    # 12/11/2026 (junção do ramo do M6 49871e08 no do M7): a mesma exceção que o M6 trouxe para a sua camada, pela mesma razão. As
    # tarefas da M7-U1, da M7-U2 e da M7-U3 estão nesta camada e na revisão dos enunciados (#192); quem as lê como eram antes da
    # revisão (scripts/tarefas_claras_historico.py desfaz esta camada e a dos enunciados, por esta ordem) entrega exatamente a base
    # da revisão (o hash do seu manifesto): esta camada já saiu e não há nada a desfazer. Em qualquer outro caso, a contagem
    # continua estrita.
    claras = _TAREFAS_CLARAS.get(_relative(path))
    if claras and hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() == claras['base_sha256_lf']:
        return text
    for edit in reversed(_CUIDADO_M7_1111.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M7 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m6_0811(path, text):
    # 11/11/2026: primeiro a decisão 152 no M7, que está por cima.
    text = undo_cuidado_m7_1111(path, text)
    # 12/11/2026 (junção do ramo do M6 49871e08 no do M7): depois de desfeita a do M7, vale a exceção que o M6 trouxe.
    # 11/11/2026: a decisão 152 no M6 repõe também, por cima da revisão dos enunciados das tarefas (#192), os espaços que ela tinha
    # tirado às tarefas do M1, do M3, do M4 e do M5. Os contratos históricos do M1 ao M5 leem essas páginas já como eram antes da
    # revisão (scripts/tarefas_claras_historico.py desfaz esta camada e a dos enunciados, por esta ordem): se o texto é exatamente a
    # base da revisão (o hash do seu manifesto), esta camada já saiu e não há nada a desfazer. Em qualquer outro caso, a contagem
    # continua estrita.
    claras = _TAREFAS_CLARAS.get(_relative(path))
    if claras and hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest() == claras['base_sha256_lf']:
        return text
    for edit in reversed(_CUIDADO_M6_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M6 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


_TAREFAS_CLARAS = json.loads((ROOT/'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']

def undo_cuidado_m5_0811(path, text):
    # 08/11/2026: primeiro a decisão 152 no M6, que está por cima.
    text = undo_cuidado_m6_0811(path, text)
    # 11/11/2026 (fusão do main 4bf4a053 no pedido #191): depois a revisão dos enunciados das tarefas (#192), que fica entre as duas.
    from tarefas_claras_historico import desfazer
    text = desfazer(path, text)
    for edit in reversed(_CUIDADO_M5_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M5 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m4_0811(path, text):
    # 08/11/2026: primeiro a decisão 152 no M5, que está por cima.
    text = undo_cuidado_m5_0811(path, text)
    for edit in reversed(_CUIDADO_M4_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M4 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m3_0811(path, text):
    # 08/11/2026: primeiro a decisão 152 no M4, que está por cima.
    text = undo_cuidado_m4_0811(path, text)
    for edit in reversed(_CUIDADO_M3_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M3 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m2_0811(path, text):
    # 08/11/2026: primeiro a decisão 152 no M3, que está por cima.
    text = undo_cuidado_m3_0811(path, text)
    for edit in reversed(_CUIDADO_M2_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M2 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cidade_cartaz_0811(path, text):
    # 08/11/2026: primeiro a decisão 152 no M2, que está por cima.
    text = undo_cuidado_m2_0811(path, text)
    for edit in reversed(_CIDADE_CARTAZ_0811.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Cartaz «Ler a cidade» e nome novo da secção não conferem: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_creditos_i_pt1_0711(path, text):
    # 08/11/2026: primeiro o cartaz «Ler a cidade» e o nome novo da secção, que estão por cima.
    text = undo_cidade_cartaz_0811(path, text)
    for edit in reversed(_CREDITOS_I_PT1_0711.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Créditos atrás de um «i» (pedido pt-1) não conferem: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cuidado_m1_0611(path, text):
    # 07/11/2026: primeiro os créditos atrás de um «i» do pedido pt-1, que estão por cima.
    text = undo_creditos_i_pt1_0711(path, text)
    for edit in reversed(_CUIDADO_M1_0611.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 152 no M1 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 06/11/2026: decisão 148, o desenho do índice do M4 nos nove índices do Português, camada mais recente (por cima dos
# créditos atrás de um «i»): desfaz-se antes deles, com contagem estrita.
_CARTAZ_148_0611 = json.loads((ROOT/'tests/fixtures/cartaz-indices-148-edits-20261106.json').read_text('utf-8'))['files']

# 07/11/2026: os três acertos dos índices deixados pela decisão 173 (acesso do docente repetido no M3, no M5 e no M6, «·» nas
# contagens do M8 e do M9, menu dos materiais sem JavaScript), camada mais recente (por cima do desenho comum dos índices):
# desfaz-se antes dele, com contagem estrita.
_ACERTOS_0711 = json.loads((ROOT/'tests/fixtures/indices-acertos-edits-20261107.json').read_text('utf-8'))['files']

def undo_acertos_0711(path, text):
    # 07/11/2026 (fusão do main 29441e6b no pedido #182): primeiro a decisão 152 no M1, que está por cima.
    text = undo_cuidado_m1_0611(path, text)
    for edit in reversed(_ACERTOS_0711.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Acertos dos índices (decisão 173) não conferem: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cartaz_148_0611(path, text):
    # 07/11/2026: primeiro os acertos dos índices deixados pela decisão 173, que estão por cima.
    text = undo_acertos_0711(path, text)
    for edit in reversed(_CARTAZ_148_0611.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Desenho comum dos índices (decisão 148) não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_creditos_i_0511(path, text):
    # 06/11/2026: primeiro o desenho comum dos índices (decisão 148), que está por cima.
    text = undo_cartaz_148_0611(path, text)
    for edit in reversed(_CREDITOS_I_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Créditos atrás de um «i» não conferem: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_atlas_lote3_0511(path, text):
    # 06/11/2026: primeiro os créditos atrás de um «i», que estão por cima.
    text = undo_creditos_i_0511(path, text)
    for edit in reversed(_ATLAS_LOTE3_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Atlas, lote 3, não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 05/11/2026: decisão 154 (os exercícios fazem-se sozinho; nada no texto do aluno depende do docente nem só de um colega
# ou da turma): desfaz-se antes do contexto do Laboratório do exame, com contagem estrita.
_AUTONOMIA_0511 = json.loads((ROOT/'tests/fixtures/autonomia-154-edits-20261105.json').read_text('utf-8'))['files']

def undo_autonomia_0511(path, text):
    # 06/11/2026: primeiro o lote 3 do Atlas, que está por cima.
    text = undo_atlas_lote3_0511(path, text)
    for edit in reversed(_AUTONOMIA_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Decisão 154 (exercícios a sós) não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_contexto_0511(path, text):
    # 05/11/2026: primeiro a decisão 154 (exercícios a sós), que está por cima (e, por cima dela, o lote 3 do Atlas).
    text = undo_autonomia_0511(path, text)
    for edit in reversed(_CONTEXTO_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Contexto do Laboratório do exame não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_exame_0511(path, text):
    # 05/11/2026: primeiro o contexto de cada sessão do Laboratório do exame, que está por cima.
    text = undo_contexto_0511(path, text)
    for edit in reversed(_EXAME_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Laboratório do exame não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_tabela_0511(path, text):
    # 05/11/2026: primeiro o Laboratório do exame, que está por cima.
    text = undo_exame_0511(path, text)
    for edit in reversed(_TABELA_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tabela dos seis movimentos não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_revisao_0511(path, text):
    # 05/11/2026: primeiro a tabela dos seis movimentos, que está por cima.
    text = undo_tabela_0511(path, text)
    for edit in reversed(_REVISAO_0511.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Revisão de 5/11 não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_cabecalho(path, text):
    # 05/11/2026: primeiro a revisão de 5/11, que está por cima.
    text = undo_revisao_0511(path, text)
    for edit in reversed(_CABECALHO.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Cabeçalho não confere: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


_CREDITOS_IA = json.loads((ROOT/'tests/fixtures/creditos-grafismos-ia-edits-20261102.json').read_text('utf-8'))['files']

def undo_creditos_ia(path, text):
    for edit in reversed(_CREDITOS_IA.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Créditos de IA não conferem: {path}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


_CONTEUDOS_LOTE2_FILES = json.loads((ROOT / 'tests/fixtures/conteudos-lote2-edits-20261101.json').read_text('utf-8'))['files']


_M4_PILOTO_FILES = json.loads((ROOT / 'tests/fixtures/cartaz-m4-piloto-edits-20261102.json').read_text('utf-8'))['files']


def undo_m4_piloto(path, text):
    # 02/11/2026: desfaz só a camada visual autorizada, com contagem estrita.
    relative = _relative(path)
    for edit in reversed(_M4_PILOTO_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Piloto M4 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


_VARIEDADE_F0_FILES = json.loads((ROOT / 'tests/fixtures/variedade-f0-edits-20261102.json').read_text('utf-8'))['files']


def undo_variedade_f0(path, text):
    relative = _relative(path)
    for edit in reversed(_VARIEDADE_F0_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"F0 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_conteudos_lote2(path, text):
    # 03/11/2026: desfaz F0 e os créditos publicados, com as mesmas contagens estritas.
    # 03/11/2026: cabeçalho posterior à F0 publicada.
    text = undo_cabecalho(path, text)
    # 03/11/2026: preservar as duas camadas e as contagens estritas.
    text = undo_m4_piloto(path, text)
    text = undo_variedade_f0(path, text)
    text = undo_creditos_ia(path, text)
    relative = _relative(path)
    for edit in reversed(_CONTEUDOS_LOTE2_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Lote 2 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_varredura(path, text):
    # 02/11/2026: lote 2 por cima da varredura integrada.
    text = undo_conteudos_lote2(path, text)
    relative = _relative(path)
    for edit in reversed(_VARREDURA_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 01/11 (formatação) já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_calcada_mar(path, text):
    # 02/11/2026: a varredura, mais recente, desfaz-se antes.
    text = undo_varredura(path, text)
    relative = _relative(path)
    for edit in reversed(_CALCADA_MAR.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Calçada de 02/11 não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_tarefas_individuais(path, text):
    # 02/11/2026: a camada da calçada, mais recente, desfaz-se antes.
    text = undo_calcada_mar(path, text)
    relative = _relative(path)
    for edit in reversed(_TAREFAS_INDIVIDUAIS.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Tarefas individuais de 02/11 não conferem: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


# 01/11/2026: índices Cartaz, camada mais recente sobre as dependências integradas.
_CARTAZ_INDICES = json.loads((ROOT / 'tests/fixtures/cartaz-indices-edits-20261101.json').read_text('utf-8'))['files']

def undo_cartaz_indices(path, text):
    # 02/11/2026: a camada das tarefas individuais, mais recente, desfaz-se antes.
    text = undo_tarefas_individuais(path, text)
    relative = _relative(path)
    for edit in reversed(_CARTAZ_INDICES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Índices Cartaz não conferem: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo(path, text):
    """Devolve o texto anterior às correções de 28/10 para este ficheiro (ou o mesmo texto, se não as tem).

    28/10/2026: desfaz primeiro o corte da Sala (o mais recente) e depois os dois lotes da auditoria.
    29/10/2026: antes de tudo, a camada dos aquecimentos do M7. Numa página gerada de novo a 29/10 (REGENERADAS_20261029)
    não há trocas de 28/10 a desfazer: o predecessor compacto continua autorizado pelo seu manifesto literal.
    30/10/2026: antes ainda, a camada do texto justificado (classe «prosa»).
    30/10/2026: e antes dessa, a das opções denunciadoras.
    30/10/2026: e antes de todas, a da língua das perguntas, do Pessoa da F13 e do M7 (a mais recente).
    """
    # 30/10/2026: antes de tudo, a camada da língua (a mais recente), depois a das opções denunciadoras, a do texto
    # justificado e as dos aquecimentos do M2, do M4 e do M1.
    # 31/10/2026: desfaz primeiro as tarefas M3, M5 e M6.
    # 01/11/2026: desfaz primeiro a camada M8/M9.
    text = undo_tarefas_m89(path, text)
    text = undo_tarefas_m356(path, text)
    text = undo_lingua(path, text)
    text = undo_opcoes(path, text)
    text = undo_justificado(path, text)
    text = undo_aquecimentos_m2(path, text)
    text = undo_aquecimentos_m4(path, text)
    text = undo_aquecimentos_m1(path, text)
    text = undo_aquecimentos(path, text)
    relative = _relative(path)
    if relative in REGENERADAS_20261029:
        return text
    text = undo_sala(path, text)
    for name, files in _LAYERS:
        for edit in reversed(files.get(relative, {}).get('edits', [])):
            if text.count(edit['new']) != edit['occurrences']:
                raise AssertionError(f"Correção autorizada a 28/10 já não confere ({name}): {relative}: {edit['location']}")
            text = text.replace(edit['new'], edit['old'])
    return text
