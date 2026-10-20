"""Audit embedded lesson card definitions; no browser or external dependencies.

Run: python scripts/audit_cards.py
Counts definitions in CARTOES, not the random subset shown in one attempt.
"""
from collections import Counter
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'ler', 'emparelhar', 'escolha', 'completar', 'vf', 'ordenar', 'frase', 'versos', 'sublinhar', 'calcada'}
# Same card engine, with banks moved to explicit external scripts.
EXTERNAL_BANKS = {
    'm3/licao-m3-f18/index.html': '../../assets/pt-lessons/m3-f18.js',
    'm9/licao-m9-f11/index.html': '../recursos/f11.js',
    'm9/licao-m9-f12/index.html': '../recursos/f12.js',
    'm9/licao-m9-f13/index.html': '../recursos/f13.js',
}


def lesson_cards(path):
    text = path.read_text(encoding='utf-8')
    marker = 'CARTOES='
    rel = path.relative_to(path.parents[2]).as_posix()
    if marker not in text and rel in EXTERNAL_BANKS:
        src = EXTERNAL_BANKS[rel]
        if not re.search(r'<script\b[^>]*\bsrc=[\"\']' + re.escape(src) + r'(?:\?[^\"\']*)?[\"\']', text):
            raise ValueError('expected external card script is not linked')
        text = (path.parent / src).resolve().read_text(encoding='utf-8')
    if marker not in text:
        raise ValueError('CARTOES not found')
    cards, _ = json.JSONDecoder().raw_decode(text.split(marker, 1)[1].lstrip())
    if not isinstance(cards, list):
        raise ValueError('CARTOES is not an array')
    return cards


def validate_cards(cards):
    errors = []
    if not isinstance(cards, list):
        return ['CARTOES must be an array']
    for number, card in enumerate(cards, 1):
        if not isinstance(card, dict):
            errors.append(f'card {number}: expected object')
            continue
        kind = card.get('t')
        if kind not in TYPES:
            errors.append(f'card {number}: unknown type {kind!r}')
        if kind != 'ler' and not (isinstance(card.get('f'), str) and card['f'].strip()):
            errors.append(f'card {number}: missing explanatory feedback field')
        checks = [card] if kind == 'escolha' else card.get('lacunas', []) if kind == 'completar' else []
        if kind == 'completar' and (not isinstance(checks, list) or not checks):
            errors.append(f'card {number}: missing gaps')
            continue
        for item in checks:
            options, correct = item.get('o'), item.get('c')
            if (not isinstance(options, list) or not options or type(correct) is not int
                    or not 0 <= correct < len(options)):
                errors.append(f'card {number}: invalid answer index/options')
            elif any(not isinstance(option, str) or not option.strip() for option in options):
                errors.append(f'card {number}: empty/non-text option')
            elif len(set(options)) != len(options):
                errors.append(f'card {number}: duplicate options')
        if isinstance(card.get('fe'), list) and len(card['fe']) != len(card.get('o', [])):
            errors.append(f'card {number}: feedback/options length mismatch')
        if kind == 'sublinhar':
            words = str(card.get('frase', '')).split()
            indexes = card.get('certas')
            if (not isinstance(indexes, list) or not indexes
                    or any(type(i) is not int or not 0 <= i < len(words) for i in indexes)):
                errors.append(f'card {number}: invalid word indexes')
        if kind == 'completar' and isinstance(card.get('frase'), str):
            placeholders = set(map(int, re.findall(r'\[(\d+)\]', card['frase'])))
            if placeholders != set(range(1, len(checks) + 1)):
                errors.append(f'card {number}: placeholders/gaps mismatch')
        if kind == 'vf' and type(card.get('v')) is not bool:
            errors.append(f'card {number}: true/false answer must be boolean')
    return errors


def audit(root=ROOT):
    counts, lessons, errors = Counter(), [], []
    for path in sorted(root.glob('m[1-9]/licao-*/index.html')):
        rel = path.relative_to(root).as_posix()
        try:
            cards = lesson_cards(path)
            issues = validate_cards(cards)
            errors.extend(f'{rel}: {issue}' for issue in issues)
            if isinstance(cards, list):
                kinds = Counter(c.get('t', 'unknown') for c in cards if isinstance(c, dict))
                counts.update(kinds)
                lessons.append({'path': rel, 'definitions': len(cards), 'types': dict(kinds)})
        except (ValueError, OSError) as error:
            errors.append(f'{rel}: {error}')
    if len(lessons) != 108:
        errors.append(f'Expected 108 card banks, found {len(lessons)}; review inventory changes explicitly')
    return {'lessons': len(lessons), 'definitions': sum(counts.values()),
            'external_banks': sorted(EXTERNAL_BANKS),
            'reading': counts['ler'], 'interactive': sum(counts.values()) - counts['ler'],
            'types': dict(counts), 'errors': errors, 'inventory': lessons}


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    sys.exit(bool(result['errors']))

