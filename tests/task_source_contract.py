"""Validate current compact task bodies before exposing their frozen predecessors.

Historical tests describe earlier authorized products/teaching sequences, not the
current concise UI. They may use historical_task_source only after this module
has checked the real body against the literal compact manifest. Current compact
and grammar tests must continue to inspect the real files themselves.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    'm1-compact-task-edits-20261027.json',
    'm4-tasks-compact-20261027.json',
    'task-compact-m7-before-after.json',
)


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


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


def _relative(path):
    path = Path(path)
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


def _body_on(source):
    return source[source.index('<body'):]


def _authorized_markup_variants(source, path):
    """Reverse only three expressly authorized follow-up strings, never content.

    Keep variants because the independently authored M7 baseline already includes
    some of these markers. A variant must still match the original exact digest.
    Head-only cache version changes are outside the compared body by design.
    """
    variants = {source}
    reversals = [
        lambda s: s.replace('<details data-task-optional-preparation>', '<details>'),
        lambda s: re.sub(r'(<h3 id="criterios">[^<]*</h3>)<ul class="task-criteria">', r'\1<ul>', s),
    ]
    if path == 'tarefas/m1-u1/index.html':
        reversals.append(lambda s: s.replace('Com consulta durante toda a tarefa.', 'Com consulta.'))
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
    if 'after_source' in record:
        expected = record['after_source']
        if _sha(expected) != record['after_sha256']:
            raise AssertionError('Corrupt compact source snapshot: ' + relative)
        target, digest = _body_on(actual), record['after_body_sha256']
    elif 'after_body' in record:
        # M1 stores the complete main and its original full source. Rebuild the
        # authorized source to check footer/scripts as well as the main content.
        if before.count(record['before_body']) != 1:
            raise AssertionError('Invalid M1 body substitution: ' + relative)
        expected = before.replace(record['before_body'], record['after_body'])
        if _sha(expected) != record['after_sha256']:
            raise AssertionError('Corrupt compact body snapshot: ' + relative)
        target, digest = _body_on(actual), _sha(_body_on(expected))
    else:
        # M4's literal contract deliberately stores all body children only.
        match = re.search(r'<body[^>]*>([\s\S]*?)</body>', actual)
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
