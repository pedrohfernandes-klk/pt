#!/usr/bin/env python3
"""Gera apenas as novas lições; os percursos existentes usam a camada literal."""
from html import escape
from pathlib import Path
import argparse
import json
from licoes_20261101 import ROOT, LESSONS


def sequences():
    plan = json.loads((ROOT / 'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
    units = {(f"m{m['module']}", u['number']): list(u['lessons']) for m in plan for u in m['units']}
    pending = list(LESSONS)
    while pending:
        before = len(pending)
        for item in pending[:]:
            route = units[(item['id'].split('-')[0], item['unit'])]
            if item['id'] in route:
                pending.remove(item)
            elif item['after'] in route:
                route.insert(route.index(item['after']) + 1, item['id'])
                pending.remove(item)
        if len(pending) == before:
            raise ValueError(f'Não foi possível localizar as lições: {pending}')
    return units


def render(item, units):
    module = item['id'].split('-')[0]
    route = units[(module, item['unit'])]
    i = route.index(item['id'])
    previous = '../licao-' + route[i-1] + '/' if i else '../'
    following = '../licao-' + route[i+1] + '/' if i+1 < len(route) else '../../tarefas/' + module + '-u' + str(item['unit']) + '/'
    values = dict(TITLE=escape(item['title']), UNIT=str(item['unit']), NUMBER=module[1:],
                  MODULE=module.upper(), ID=item['id'], PREVIOUS=previous, NEXT=following,
                  JSON_TITLE=json.dumps(item['title'], ensure_ascii=False),
                  CARDS=json.dumps(item['cards'], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
    text = (ROOT / 'scripts/templates/licao-20261101.html').read_text('utf-8')
    for key, value in values.items():
        text = text.replace('@@' + key + '@@', value)
    if '@@' in text:
        raise ValueError('Campo do molde por preencher')
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verificar', action='store_true')
    args = parser.parse_args()
    units = sequences()
    for item in LESSONS:
        path = ROOT / item['id'].split('-')[0] / ('licao-' + item['id']) / 'index.html'
        text = render(item, units)
        if args.verificar:
            assert path.read_text('utf-8') == text, str(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, 'utf-8', newline='\n')
        print(('Conferida: ' if args.verificar else 'Gerada: ') + item['id'])


if __name__ == '__main__':
    main()
