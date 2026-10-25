"""Read-only audit of teacher selectors against the current lesson banks.

This checks routing and preserves the resolved question/answer/feedback identity.
It does not certify pedagogical validity or the network classroom transport.
An optional local Git ref supplies panel files without checking out that ref.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from audit_cards import lesson_cards

ROOT = Path(__file__).resolve().parents[1]


def digest(card):
    data = json.dumps(card, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def resolve_ref(root, ref):
    result = subprocess.run(['git', 'rev-parse', '--verify', '--end-of-options', ref + '^{commit}'],
                            cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f'Invalid local panel ref: {ref}')
    return result.stdout.strip()


def read_panel(root, path, commit):
    if commit is None:
        return path.read_text('utf-8') if path.exists() else None
    rel = path.relative_to(root).as_posix()
    listing = subprocess.run(['git', 'ls-tree', '--name-only', commit, '--', rel],
                             cwd=root, capture_output=True, text=True)
    if listing.returncode:
        raise ValueError(f'Cannot inspect panel tree at {commit}')
    if rel not in listing.stdout.splitlines():
        return None
    result = subprocess.run(['git', 'show', f'{commit}:{rel}'], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError(f'Cannot read {rel} at {commit}; no fallback was used')
    return result.stdout.decode('utf-8')


def compare(cards, controls):
    expected = [{'k': i, 't': c['t'], 'p': c.get('p', '')}
                for i, c in enumerate(cards) if c['t'] != 'ler']
    rows = []
    matched = set()
    for number, control in enumerate(controls):
        row = {'selection': number, 'control': control}
        k = control.get('k')
        if type(k) is not int or not 0 <= k < len(cards):
            row['status'] = 'invalid_index'
        else:
            card = cards[k]
            row['resolved'] = {'k': k, 't': card['t'], 'p': card.get('p', ''),
                               'sha256': digest(card),
                               'answer': {key: card[key] for key in
                                          ('c', 'v', 'o', 'lacunas', 'pares', 'certas', 'passos', 'palavras', 'linhas')
                                          if key in card},
                               'feedback': {key: card[key] for key in ('f', 'fe') if key in card}}
            if card['t'] == 'ler':
                row['status'] = 'reading_target'
            elif control.get('t') != card['t'] or control.get('p') != card.get('p', ''):
                row['status'] = 'different_question'
            else:
                row['status'] = 'matched'
                matched.add(k)
        rows.append(row)
    return {'exact_bank': controls == expected, 'expected_controls': len(expected),
            'controls': len(controls), 'statuses': dict(Counter(r['status'] for r in rows)),
            'uncovered_current': [x for x in expected if x['k'] not in matched], 'rows': rows}


def audit(root=ROOT, modules=('m4',), panel_ref=None):
    root = Path(root)
    panel_commit = resolve_ref(root, panel_ref) if panel_ref else None
    report = {'modules': list(modules), 'panel_ref': panel_ref, 'panel_commit': panel_commit,
              'scope': 'selector routing only; semantic review and classroom transport remain separate',
              'lessons': [], 'missing_modules': []}
    for module in modules:
        paths = sorted((root / module).glob('licao-*/index.html'))
        if not paths:
            report['missing_modules'].append(module)
        for path in paths:
            cards = lesson_cards(path)
            panel = path.parent.with_name(path.parent.name.replace('licao-', 'painel-', 1)) / 'index.html'
            row = {'lesson': path.relative_to(root).as_posix(),
                   'panel': panel.relative_to(root).as_posix(), 'lesson_cards': len(cards)}
            # Missing panels need an access review; an editorial guide is not a broken selector.
            text = read_panel(root, panel, panel_commit)
            if text is None:
                row['status'] = 'missing_panel'
            elif 'CARTOES=' not in text:
                row['status'] = 'editorial_panel'
            else:
                bank = json.JSONDecoder().raw_decode(text.split('CARTOES=', 1)[1])[0]
                row.update(compare(cards, bank))
                row['status'] = 'matched' if row['exact_bank'] else 'different'
            report['lessons'].append(row)
    statuses = Counter(x['status'] for x in report['lessons'])
    controls = Counter()
    for row in report['lessons']:
        controls.update(row.get('statuses', {}))
    report['summary'] = {'lessons': len(report['lessons']), 'panels': dict(statuses),
                         'controls': dict(controls),
                         'unverified': sum(v for k, v in statuses.items() if k != 'matched') + len(report['missing_modules'])}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--modules', nargs='+', choices=[f'm{i}' for i in range(1, 10)], default=['m4'])
    parser.add_argument('--panel-ref', help='Local Git ref used only for panel files; lessons remain the checked-out snapshot')
    parser.add_argument('--output', type=Path, help='Save the detailed JSON; print a compact summary')
    args = parser.parse_args()
    result = audit(args.root, args.modules, args.panel_ref)
    data = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(data + '\n', encoding='utf-8')
        print(json.dumps(result['summary'], ensure_ascii=False))
    else:
        print(data)
    raise SystemExit(bool(result['summary']['unverified']))
