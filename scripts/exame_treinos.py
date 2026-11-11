#!/usr/bin/env python3
"""11/11/2026: gera os três treinos da preparação de exame e a sua entrada (exame/treinos/).

Os textos oficiais vêm de tests/fixtures/prova-639-2026-*.json; o texto nosso e a ordem dos passos estão em
scripts/exame_treinos_dados/. O estilo e o motor são assets/exame/treino.css e assets/exame/treino.js.

  python scripts/exame_treinos.py           escreve as quatro páginas
  python scripts/exame_treinos.py --check   confere que as páginas publicadas são as que o gerador escreve
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True

from exame_treinos_dados import interpretacao, gramatica, escrita, indice  # noqa: E402


def paginas():
    """{caminho no repositório: página}, pela ordem em que aparecem na entrada."""
    return dict(m.construir() for m in (indice, interpretacao, gramatica, escrita))


def main(argv):
    conferir = '--check' in argv
    diferentes = []
    for caminho, pagina in paginas().items():
        destino = ROOT / caminho
        if conferir:
            if not destino.is_file() or destino.read_text(encoding='utf-8') != pagina:
                diferentes.append(caminho)
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(pagina, encoding='utf-8', newline='\n')
    if diferentes:
        print('Páginas diferentes do gerador: ' + ', '.join(diferentes))
        return 1
    print('Treinos de exame: 4 páginas ' + ('conferidas' if conferir else 'escritas') + '.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
