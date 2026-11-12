"""Reconstitui o texto anterior à revisão dos enunciados para os contratos históricos."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
FILES = json.loads((ROOT / 'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']
# 11/11/2026: a decisão 152 no M6 (cuidado_m6_20261108) fica por cima desta revisão e repõe, nos enunciados novos, os espaços que
# não quebram que a revisão tinha tirado às tarefas do M1, do M3, do M4 e do M5. Quando o texto recebido é a página como essa
# camada a deixou (o hash «after» do seu manifesto), desfaz-se primeiro essa camada, com contagem estrita; quem já a desfez
# (tests/auditoria_20261028.py) entrega outro texto e nada se desfaz duas vezes.
CUIDADO_M6 = json.loads((ROOT / 'tests/fixtures/cuidado-m6-edits-20261108.json').read_text('utf-8'))['files']
def _sha_lf(text):
    return hashlib.sha256(text.replace('\r\n', '\n').encode()).hexdigest()
def desfazer(path, text):
    p = Path(path)
    rel = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
    entry = FILES.get(rel)
    if not entry:
        return text
    por_cima = CUIDADO_M6.get(rel)
    if por_cima and _sha_lf(text) == por_cima['after_sha256_lf']:
        for edit in reversed(por_cima['edits']):
            assert text.count(edit['new']) == edit['occurrences'], f'Decisão 152 no M6 não confere: {rel}'
            text = text.replace(edit['new'], edit['old'])
    if _sha_lf(text) == entry['base_sha256_lf']:
        return text
    for edit in reversed(entry['edits']):
        assert text.count(edit['new']) == edit['occurrences'], f'Enunciado revisto não confere: {rel}'
        text = text.replace(edit['new'], edit['old'])
    return text
