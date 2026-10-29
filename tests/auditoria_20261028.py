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


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def undo(path, text):
    """Devolve o texto anterior às correções de 28/10 para este ficheiro (ou o mesmo texto, se não as tem)."""
    relative = _relative(path)
    for name, files in _LAYERS:
        for edit in reversed(files.get(relative, {}).get('edits', [])):
            if text.count(edit['new']) != edit['occurrences']:
                raise AssertionError(f"Correção autorizada a 28/10 já não confere ({name}): {relative}: {edit['location']}")
            text = text.replace(edit['new'], edit['old'])
    return text
