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
    # 01/11/2026: segue os passos completos, incluindo exercícios entre as lições.
    plan=json.loads((ROOT/'docs/pedagogia/percursos-unidades-20261020.json').read_text('utf-8'))
    steps=list(plan[int(module[1:])-1]['units'][item['unit']-1]['steps'])
    for new in sorted((x for x in LESSONS if x['id'].startswith(module+'-') and x['unit']==item['unit']),key=lambda x:route.index(x['id'])):
        if new['id'] not in steps:steps.insert(steps.index(new['after'])+1,new['id'])
    position=steps.index(item['id'])
    if position+1<len(steps):
        target=steps[position+1]
        following='../'+('licao-' if target in route else '')+target+'/'
    else:following='../../tarefas/'+module+'-u'+str(item['unit'])+'/' 
    values = dict(TITLE=escape(item['title']), UNIT=str(item['unit']), NUMBER=module[1:],
                  MODULE=module.upper(), ID=item['id'], PREVIOUS=previous, NEXT=following,
                  JSON_TITLE=json.dumps(item['title'], ensure_ascii=False),
                  CARDS=json.dumps(item['cards'], ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
    text = (ROOT / 'scripts/templates/licao-20261101.html.tpl').read_text('utf-8')
    for key, value in values.items():
        text = text.replace('@@' + key + '@@', value)
    if '@@' in text:
        raise ValueError('Campo do molde por preencher')
    # 02/11/2026: os três documentos do pedido B usam o ampliador comum, com foco e zoom.
    if item['id'] in ('m3-f19','m5-f17','m6-f14'):
        text=text.replace('</head>','<link rel="stylesheet" href="../../assets/ampliar-documentos.css"></head>')
        text=text.replace('</body>','<script src="../../assets/ampliar-documentos.js"></script></body>')
    return text


def render_notes(item):
    """01/11/2026: notas editoriais pelo molde já usado na M6-F12/F13."""
    module=item['id'].split('-')[0]
    enquadramento=''
    if item['id']=='m2-f16':
        guia=(ROOT/'docs/pedagogia/guia-docente-licoes-20261101.md').read_text('utf-8')
        linha=next(x for x in guia.splitlines() if x.startswith('O relato de Lianor'))
        enquadramento='<section aria-labelledby="enquadramento"><h2 id="enquadramento">Enquadramento para o docente</h2><p>'+escape(linha)+'</p></section>'
    perguntas=[]
    for card in item['cards']:
        if card['t']=='ler':continue
        feedback='<p>'+escape(card['f'])+'</p>'
        # 02/11/2026: o retorno de erro é uma lista por opção nas escolhas e um texto único nos outros cartões de fazer.
        if isinstance(card.get('fe'),str):
            feedback+='<ul><li>'+escape(card['fe'])+'</li></ul>'
        elif card.get('fe'):
            feedback+='<ul>'+''.join('<li>'+escape(f)+'</li>' for i,f in enumerate(card['fe']) if i!=card['c'])+'</ul>'
        perguntas.append('<li><p>'+escape(card['p'])+'</p><details><summary>Indícios e retorno</summary>'+feedback+'</details></li>')
    values=dict(TITLE=escape(item['title']),NUMBER=module[1:],ID=item['id'],QUESTION=escape(item['question']),CONTEXT=enquadramento,CARDS=''.join(perguntas))
    text=(ROOT/'scripts/templates/notas-licoes-20261101.html.tpl').read_text('utf-8')
    for key,value in values.items():text=text.replace('@@'+key+'@@',value)
    assert '@@' not in text
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
        notes=ROOT/item['id'].split('-')[0]/('painel-'+item['id'])/'index.html'
        if args.verificar:
            assert notes.read_text('utf-8')==render_notes(item),str(notes)
        else:
            notes.parent.mkdir(parents=True,exist_ok=True)
            notes.write_text(render_notes(item),'utf-8',newline='\n')
        print(('Conferida: ' if args.verificar else 'Gerada: ') + item['id'])


if __name__ == '__main__':
    main()
