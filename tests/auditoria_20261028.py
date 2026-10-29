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
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
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


def undo_aquecimentos(path, text):
    """29/10/2026: devolve o texto anterior à camada dos aquecimentos do M7 (ou o mesmo texto, se não a tem)."""
    relative = _relative(path)
    for edit in reversed(_AQUECIMENTOS_FILES.get(relative, {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Troca autorizada a 29/10 já não confere: {relative}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo(path, text):
    """Devolve o texto anterior às correções de 28/10 para este ficheiro (ou o mesmo texto, se não as tem).

    28/10/2026: desfaz primeiro o corte da Sala (o mais recente) e depois os dois lotes da auditoria.
    29/10/2026: antes de tudo, a camada dos aquecimentos do M7. Numa página gerada de novo a 29/10 (REGENERADAS_20261029)
    não há trocas de 28/10 a desfazer: o predecessor compacto continua autorizado pelo seu manifesto literal.
    """
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
