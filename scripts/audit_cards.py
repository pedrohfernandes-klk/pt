"""Audit embedded lesson card definitions; no browser or external dependencies.

Run: python scripts/audit_cards.py
Counts definitions in CARTOES, not the random subset shown in one attempt.
"""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'ler', 'emparelhar', 'escolha', 'completar', 'vf', 'ordenar', 'frase', 'versos', 'sublinhar', 'calcada'}


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
        if kind == 'vf' and type(card.get('v')) is not bool:
            errors.append(f'card {number}: true/false answer must be boolean')
    return errors


def audit(root=ROOT):
    counts, lessons, errors = Counter(), [], []
    for path in sorted(root.glob('m[1-9]/licao-*/index.html')):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding='utf-8')
            marker = 'CARTOES='
            start = text.index(marker) + len(marker)
            cards, _ = json.JSONDecoder().raw_decode(text[start:])
            issues = validate_cards(cards)
            errors.extend(f'{rel}: {issue}' for issue in issues)
            if isinstance(cards, list):
                kinds = Counter(c.get('t', 'unknown') for c in cards if isinstance(c, dict))
                counts.update(kinds)
                lessons.append({'path': rel, 'definitions': len(cards), 'types': dict(kinds)})
        except (ValueError, OSError) as error:
            errors.append(f'{rel}: {error}')
    if len(lessons) != 100:
        errors.append(f'Expected 100 baseline lessons, found {len(lessons)}; review inventory changes explicitly')
    return {'lessons': len(lessons), 'definitions': sum(counts.values()),
            'reading': counts['ler'], 'interactive': sum(counts.values()) - counts['ler'],
            'types': dict(counts), 'errors': errors, 'inventory': lessons}


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    sys.exit(bool(result['errors']))

