"""28/10/2026: correções da auditoria do M1 e do M4, autorizadas literalmente.

O manifesto tests/fixtures/auditoria-m1-m4-edits-20261028.json guarda cada troca de texto (antigo, novo,
ocorrências). Os testes que comparam páginas com um estado congelado desfazem primeiro estas trocas, e só
depois aplicam os seus próprios manifestos. Uma troca que já não se encontre tantas vezes como o manifesto
diz faz falhar o teste: nada se desfaz em silêncio.

28/10/2026: a Sala de aula em tempo real saiu das páginas publicadas (decisão do docente de 17/10/2026;
scripts/desligar_sala.py). As trocas dessa mudança estão em tests/fixtures/sala-desligada-edits-20261028.json,
no mesmo formato. São as mais recentes, por isso undo() desfaz primeiro a Sala e só depois a auditoria.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/auditoria-m1-m4-edits-20261028.json'
_FILES = json.loads(MANIFEST.read_text('utf-8'))['files']
# 28/10/2026: o manifesto da Sala desligada (gerado por scripts/desligar_sala.py) desfaz-se antes do da auditoria.
SALA_MANIFEST = ROOT / 'tests/fixtures/sala-desligada-edits-20261028.json'
_SALA_FILES = json.loads(SALA_MANIFEST.read_text('utf-8'))['files']


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def _undo(files, path, text, label):
    for edit in reversed(files.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"{label} já não confere: {_relative(path)}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text


def undo_sala(path, text):
    """28/10/2026: devolve o texto anterior ao corte da Sala para este ficheiro (ou o mesmo texto, se não o tem)."""
    return _undo(_SALA_FILES, path, text, 'Corte da Sala autorizado a 28/10')


def undo(path, text):
    """Devolve o texto anterior às mudanças de 28/10 para este ficheiro (ou o mesmo texto, se não as tem).

    28/10/2026: desfaz os dois manifestos, o mais recente primeiro: a Sala desligada e depois a auditoria.
    """
    text = undo_sala(path, text)
    return _undo(_FILES, path, text, 'Correção autorizada a 28/10')
