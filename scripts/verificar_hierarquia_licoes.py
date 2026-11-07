#!/usr/bin/env python3
"""01/11/2026: R1/R2/R3/R5 têm de ser zero em todas as lições novas, nas duas larguras."""
import json
import sys
from licoes_20261101 import LESSONS


def main(path):
    rows=json.loads(open(path,encoding='utf-8').read())
    wanted={x['id'].split('-')[0]+'/licao-'+x['id']+'/index.html' for x in LESSONS}
    selected=[x for x in rows if x['page'].replace('\\','/') in wanted]
    errors=[]
    for page in wanted:
        widths=[x['w'] for x in selected if x['page'].replace('\\','/')==page]
        if sorted(widths)!=[390,1366]:errors.append((page,'larguras',widths))
    for row in selected:
        if row.get('erro'):errors.append((row['page'],row['erro']))
        for rule in ('r1','r2','r3','r5'):
            if row.get(rule):errors.append((row['page'],row['w'],rule,row[rule]))
    print(json.dumps(dict(paginas=len(wanted),medicoes=len(selected),erros=errors),ensure_ascii=False,indent=2))
    return bool(errors)


if __name__=='__main__':sys.exit(main(sys.argv[1]))
