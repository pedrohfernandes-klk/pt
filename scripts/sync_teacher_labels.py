"""Check teacher remote-control labels against lesson cards (offline).

Default: check M5/M6. Pass --write to synchronize only labels/indices.
Editorial notes without an inline CARTOES bank are reported and left intact.
"""
import argparse
import html
import json
from pathlib import Path
import re
from audit_cards import lesson_cards


def expected_cards(lesson):
    return [{'k': i, 't': c['t'], 'p': c['p']}
            for i, c in enumerate(lesson_cards(lesson)) if c['t'] != 'ler']


def synchronize(root, modules=('m5', 'm6'), write=False):
    result = {'checked': [], 'different': [], 'notes': []}
    for module in modules:
        for lesson in sorted((root / module).glob('licao-*/index.html')):
            panel = lesson.parent.with_name(lesson.parent.name.replace('licao-', 'painel-', 1)) / 'index.html'
            text = panel.read_bytes().decode('utf-8')
            rel = panel.relative_to(root).as_posix()
            if 'CARTOES=' not in text:
                result['notes'].append(rel)
                continue
            start = text.index('CARTOES=') + len('CARTOES=')
            current, end = json.JSONDecoder().raw_decode(text[start:])
            expected = expected_cards(lesson)
            select = re.search(r'(<select data-r-k>)(.*?)(</select>)', text)
            if not select:
                raise ValueError(f'{rel}: remote activity selector not found')
            options = ''.join(f'<option value="{c["k"]}">{html.escape(c["p"], quote=False)}</option>' for c in expected)
            result['checked'].append(rel)
            if current == expected and select[2] == options:
                continue
            result['different'].append(rel)
            if write:
                text = text[:start] + json.dumps(expected, ensure_ascii=False, separators=(',', ':')) + text[start + end:]
                text = re.sub(r'(<select data-r-k>).*?(</select>)',
                              lambda m: m[1] + options + m[2], text, count=1)
                panel.write_bytes(text.encode('utf-8'))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    report = synchronize(args.root, write=args.write)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report['different']) and not args.write)
