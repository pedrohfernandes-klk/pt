"""Reconstitui o texto anterior à revisão dos enunciados para os contratos históricos."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
FILES = json.loads((ROOT / 'tests/fixtures/tarefas-claras-edits-20261110.json').read_text('utf-8'))['files']
def desfazer(path, text):
    p = Path(path)
    rel = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
    entry = FILES.get(rel)
    if not entry:
        return text
    if hashlib.sha256(text.replace('\r\n', '\n').encode()).hexdigest() == entry['base_sha256_lf']:
        return text
    for edit in reversed(entry['edits']):
        assert text.count(edit['new']) == edit['occurrences'], f'Enunciado revisto não confere: {rel}'
        text = text.replace(edit['new'], edit['old'])
    return text
