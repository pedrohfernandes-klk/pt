"""Structural audit of existing Portuguese lesson banks and an editorial route.

Run: python scripts/audit_learning_progression.py [--root PATH] [--json]
The audit detects structural signals; it cannot measure student learning.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from audit_cards import lesson_cards

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'docs/pedagogia/m2-u1-progressao.json'


def audit(root):
    problems, signals = [], []
    bank = {}
    files = sorted(root.glob('m[1-9]/licao-m*-f*/index.html'))
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            cards = lesson_cards(path)
            if not cards:
                problems.append(f'{rel}: empty card bank')
            reading = sum(isinstance(c, dict) and c.get('t') == 'ler' for c in cards)
            doing = [c for c in cards if isinstance(c, dict) and c.get('t') != 'ler']
            missing = sum(not isinstance(c.get('f'), str) or not c['f'].strip() for c in doing)
            if missing:
                problems.append(f'{rel}: {missing} activities without explanatory feedback')
            bank[rel] = {
                'reading': reading, 'activities': len(doing),
                'alternative_prompts': sum(bool(c.get('p2')) for c in doing),
                'specific_feedback': sum(bool(c.get('fe')) for c in doing),
                'types': dict(Counter(c.get('t', '?') for c in doing)),
            }
        except (OSError, ValueError, TypeError) as exc:
            problems.append(f'{rel}: {exc}')
    if not files:
        problems.append('no lesson pages found')

    manifest_path = root / MANIFEST
    try:
        route = json.loads(manifest_path.read_text(encoding='utf-8'))
        if route.get('unit') != 'm2-u1':
            problems.append('manifest: unexpected unit ID')
        lessons = route.get('lessons')
        if not isinstance(lessons, list) or not lessons:
            problems.append('manifest: lessons list is missing')
            lessons = []
        seen = set()
        for pos, lesson in enumerate(lessons, 1):
            if not isinstance(lesson, dict):
                problems.append(f'manifest step {pos}: expected object')
                continue
            lid, path = lesson.get('id'), lesson.get('path')
            if not isinstance(lid, str) or lid in seen:
                problems.append(f'manifest step {pos}: duplicate or invalid ID')
            seen.add(lid)
            if not isinstance(path, str) or path not in bank or not path.startswith('m2/licao-m2-'):
                problems.append(f'manifest step {pos}: missing or invalid lesson path {path!r}')
            for key in ('goal', 'evidence', 'misconception', 'transfer', 'next_step'):
                if not isinstance(lesson.get(key), str) or not lesson[key].strip():
                    problems.append(f'manifest step {pos}: missing {key}')
            if path in bank:
                signals.append({'id': lid, 'path': path, **bank[path]})
        if len(lessons) != 3 or set(l.get('id') for l in lessons if isinstance(l, dict)) != {'m2-f01', 'm2-f02', 'm2-f07'}:
            problems.append('manifest: M2 unit 1 should reference F01, F02 and F07 once each')
    except (OSError, ValueError, TypeError) as exc:
        problems.append(f'manifest: {exc}')

    totals = {
        'lessons_read': len(bank),
        'readings': sum(x['reading'] for x in bank.values()),
        'activities': sum(x['activities'] for x in bank.values()),
        'with_specific_feedback': sum(x['specific_feedback'] for x in bank.values()),
        'with_alternative_prompt': sum(x['alternative_prompts'] for x in bank.values()),
    }
    return {'totals': totals, 'pilot': signals, 'problems': problems,
            'interpretation': 'Structural checks only: no evidence of retention, transfer or student learning.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    p.add_argument('--json', action='store_true')
    args = p.parse_args()
    report = audit(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        t = report['totals']
        print(f"{t['lessons_read']} lições | {t['readings']} leituras | {t['activities']} atividades")
        for l in report['pilot']:
            print(f"{l['id']}: {l['reading']} leituras, {l['activities']} atividades, "
                  f"{l['specific_feedback']} feedbacks específicos, {l['alternative_prompts']} perguntas alternativas")
        for error in report['problems']:
            print('ERRO:', error)
        print(report['interpretation'])
    return bool(report['problems'])


if __name__ == '__main__':
    raise SystemExit(main())
