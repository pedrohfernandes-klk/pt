"""28/10/2026: correções da auditoria do M1 e do M4, autorizadas literalmente.

O manifesto tests/fixtures/auditoria-m1-m4-edits-20261028.json guarda cada troca de texto (antigo, novo,
ocorrências). Os testes que comparam páginas com um estado congelado desfazem primeiro estas trocas, e só
depois aplicam os seus próprios manifestos. Uma troca que já não se encontre tantas vezes como o manifesto
diz faz falhar o teste: nada se desfaz em silêncio.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/fixtures/auditoria-m1-m4-edits-20261028.json'
_FILES = json.loads(MANIFEST.read_text('utf-8'))['files']


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def undo(path, text):
    """Devolve o texto anterior às correções de 28/10 para este ficheiro (ou o mesmo texto, se não as tem)."""
    for edit in reversed(_FILES.get(_relative(path), {}).get('edits', [])):
        if text.count(edit['new']) != edit['occurrences']:
            raise AssertionError(f"Correção autorizada a 28/10 já não confere: {_relative(path)}: {edit['location']}")
        text = text.replace(edit['new'], edit['old'])
    return text
