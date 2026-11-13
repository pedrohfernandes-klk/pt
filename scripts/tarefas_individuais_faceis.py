#!/usr/bin/env python3
"""13/11/2026: as tarefas individuais sem temas A e B no molde «mais fácil de fazer» (a m7-u1 e a m7-u2; camada tarefas_faceis_m7_20261113).

Estas duas páginas eram escritas à mão. Passam a sair de dados (docs/pedagogia/tarefas-individuais/<slug>.json), pelo mesmo molde das
tarefas de escolha (scripts/tarefa_facil.py, pagina_individual): o primeiro cartão com o que se faz, o que se entrega e o quadro
10/10/55/15; cada parte com um pedido por alínea, os exemplos com outro caso em desdobrável e os textos das lições, completos; a
verificação em perguntas de sim ou não; as duas perguntas opcionais de sempre. A tarefa é a mesma.

Idempotente. Uso: python3 scripts/tarefas_individuais_faceis.py [--saida PASTA] [slug ...]
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / 'docs/pedagogia/tarefas-individuais'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tarefa_facil  # noqa: E402


def main(args=None):
    args, raiz = list(sys.argv[1:] if args is None else args), ROOT
    if '--saida' in args:
        i = args.index('--saida')
        raiz = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    feitos = []
    for p in sorted(DADOS.glob('*.json')):
        d = json.loads(p.read_text('utf-8'))
        assert p.stem == d['slug'], p
        # Só o que é público: nenhuma chave de correção vive nestes dados.
        assert not {'grelha', 'provas', 'notas_docente', 'chave'} & set(d), p
        if args and d['slug'] not in args:
            continue
        html = tarefa_facil.pagina_individual(d)
        destino = raiz / 'tarefas' / d['slug'] / 'index.html'
        destino.parent.mkdir(parents=True, exist_ok=True)
        if not destino.exists() or destino.read_bytes() != html.encode('utf-8'):
            destino.write_text(html, 'utf-8', newline='\n')
        feitos.append(d['slug'])
    print('Tarefas individuais no molde novo: ' + ', '.join(feitos))


if __name__ == '__main__':
    main()
