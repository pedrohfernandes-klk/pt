"""Validate current compact task bodies before exposing their frozen predecessors.

Historical tests describe earlier authorized products/teaching sequences, not the
current concise UI. They may use historical_task_source only after this module
has checked the real body against the literal compact manifest. Current compact
and grammar tests must continue to inspect the real files themselves.

28/10/2026: a task that left the compact format (M1, now in the choice format) is
checked against its own literal successor manifest before any snapshot is exposed;
compact_task_source then returns the compact page authorized on 27/10.
"""
from pathlib import Path
import hashlib
import json
import re

from auditoria_20261028 import undo as undo_audit_20261028

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    'm1-compact-task-edits-20261027.json',
    'm4-tasks-compact-20261027.json',
    'task-compact-m7-before-after.json',
)


# 28/10/2026 (decisão do docente, PR #122): as duas tarefas do M1 deixam o formato compacto e passam ao
# formato com aquecimento e tema à escolha (scripts/tarefas_escolha.py). O manifesto compacto de 27/10 fica
# como está, e continua a guardar o predecessor; este segundo manifesto autoriza, literalmente, o corpo novo
# de cada página e os dados públicos de onde é gerado, encadeado no corpo compacto que substitui.
CHOICE_SUCCESSORS = 'm1-choice-tasks-20261028.json'


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _choice_successors():
    manifest = json.loads((ROOT / 'tests/fixtures' / CHOICE_SUCCESSORS).read_text('utf-8'))
    return manifest['files']


def _records():
    records = {}
    for filename in MANIFESTS:
        manifest = json.loads((ROOT / 'tests/fixtures' / filename).read_text('utf-8'))
        files = manifest['files']
        items = files.items() if isinstance(files, dict) else ((x['path'], x) for x in files)
        for path, record in items:
            if path in records:
                raise AssertionError('Duplicate compact task authorization: ' + path)
            records[path] = record
    if len(records) != 8:
        raise AssertionError('Expected eight individually authorized compact tasks')
    return records


# 27/10/2026 (pedido do docente): o relógio do aluno entra nas aulas de tarefa. Só estas marcas,
# sempre com a mesma forma, ficam autorizadas por cima dos manifestos literais; o conteúdo não muda.
TIMER_MARKUP = (
    re.compile(r'<link rel="stylesheet" href="\.\./\.\./assets/relogio\.css\?v=[0-9a-z.-]+">'),
    re.compile(r'<script defer src="\.\./\.\./assets/relogio\.js\?v=[0-9a-z.-]+"></script>'),
    re.compile(r'<div class="task-relogio" data-relogio data-max="[0-9.]+" data-passo="[0-9.]+" data-rotulo="[^"<>]+" data-chave="pt-relogio:tarefas/[a-z0-9-]+:(?:producao|apresentacao)"></div>'),
)


def without_timer(source):
    for pattern in TIMER_MARKUP:
        source = pattern.sub('', source)
    return source


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def _body_on(source):
    return source[source.index('<body'):]


def _authorized_markup_variants(source, path):
    """Reverse only four expressly authorized follow-up strings, never content.

    Keep variants because the independently authored M7 baseline already includes
    some of these markers. A variant must still match the original exact digest.
    Head-only cache version changes are outside the compared body by design.
    """
    variants = {source}
    reversals = [
        without_timer,
        lambda s: s.replace('<details data-task-optional-preparation>', '<details>'),
        lambda s: re.sub(r'(<h3 id="criterios">[^<]*</h3>)<ul class="task-criteria">', r'\1<ul>', s),
    ]
    if path == 'tarefas/m1-u1/index.html':
        reversals.append(lambda s: s.replace('Com consulta durante toda a tarefa.', 'Com consulta.'))
    # 27/10/2026, grelhas /20 (decisão do docente): uma linha com a ligação à grelha da tarefa, em
    # «Verificar e entregar», escrita por scripts/grelhas_tarefas.py. Só essa linha, literal, é revertida.
    reversals.append(lambda s: s.replace('<p class="task-grelha"><a href="grelha/">Grelha /20: como é avaliado e autoavaliação</a></p>\n', ''))
    for reversal in reversals:
        variants.update(reversal(item) for item in tuple(variants))
    return variants


def validate_task_source(path, source=None):
    """Return the real source only if its body has an explicit compact contract."""
    relative = _relative(path)
    records = _records()
    if relative not in records:
        raise AssertionError('No compact manifest for task: ' + relative)
    record = records[relative]
    before = record['before_source']
    before_digest = record.get('before_sha256', record.get('before_sha256_lf'))
    if _sha(before) != before_digest:
        raise AssertionError('Corrupt frozen predecessor: ' + relative)
    actual = (ROOT / relative).read_text('utf-8') if source is None else source
    # 28/10/2026: as correções literais da auditoria do M1 e do M4 desfazem-se antes de comparar; a página
    # devolvida continua a ser a real. 28/10/2026 (segundo lote): o undo desfaz também, e antes, o manifesto do
    # M7 e do resto do M4 e do M1 (tarefas do M7: sem «folhas», cartões pelo nome, próclise, título, itálico).
    checked = undo_audit_20261028(relative, actual)
    successors = _choice_successors()
    if relative in successors:
        successor = successors[relative]
        # The chain is explicit: the successor names the compact body it replaces.
        if successor['replaces_after_body_sha256'] != record['after_body_sha256']:
            raise AssertionError('Choice successor does not replace the authorized compact body: ' + relative)
        data = undo_audit_20261028(successor['data'], (ROOT / successor['data']).read_text('utf-8'))
        if _sha(data) != successor['data_sha256']:
            raise AssertionError('Public task data differs from its authorization: ' + successor['data'])
        if _sha(_body_on(checked)) != successor['after_body_sha256']:
            raise AssertionError('Current choice body differs from its authorization: ' + relative)
        return actual
    if 'after_source' in record:
        expected = record['after_source']
        if _sha(expected) != record['after_sha256']:
            raise AssertionError('Corrupt compact source snapshot: ' + relative)
        target, digest = _body_on(checked), record['after_body_sha256']
    elif 'after_body' in record:
        # M1 stores the complete main and its original full source. Rebuild the
        # authorized source to check footer/scripts as well as the main content.
        if before.count(record['before_body']) != 1:
            raise AssertionError('Invalid M1 body substitution: ' + relative)
        expected = before.replace(record['before_body'], record['after_body'])
        if _sha(expected) != record['after_sha256']:
            raise AssertionError('Corrupt compact body snapshot: ' + relative)
        target, digest = _body_on(checked), _sha(_body_on(expected))
    else:
        # M4's literal contract deliberately stores all body children only.
        match = re.search(r'<body[^>]*>([\s\S]*?)</body>', checked)
        if match is None:
            raise AssertionError('Missing task body: ' + relative)
        target, digest = match[1], record['after_body_sha256_lf']
    if not any(_sha(candidate) == digest for candidate in _authorized_markup_variants(target, relative)):
        raise AssertionError('Current compact body differs from its authorization: ' + relative)
    return actual


def historical_task_source(path):
    """Validated predecessor for historical contracts; never a silent fallback."""
    validate_task_source(path)
    return _records()[_relative(path)]['before_source']


def compact_task_source(path):
    """Validated compact snapshot of a task that has since moved on (28/10/2026: M1 to the choice format).

    Compact contracts written on 27/10 keep reading the exact page they authorized, rebuilt from the
    literal manifest, after the current page has been validated against its own authorization.
    """
    relative = _relative(path)
    validate_task_source(path)
    if relative not in _choice_successors():
        raise AssertionError('Task is still live in the compact format; read the real file: ' + relative)
    record = _records()[relative]
    expected = record['before_source'].replace(record['before_body'], record['after_body'])
    if _sha(expected) != record['after_sha256']:
        raise AssertionError('Corrupt compact body snapshot: ' + relative)
    return expected
