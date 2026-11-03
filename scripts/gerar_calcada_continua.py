"""03/11/2026: três ondas independentes, sem repetição vertical, a partir das pedras existentes."""
import math
from pathlib import Path
import argparse
from gerar_calcada_mar import pedras, caminho, CLARAS, ESCURAS, ARGAMASSA
ROOT = Path(__file__).resolve().parents[1]
def assets():
    data = pedras()
    start = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" preserveAspectRatio="none">\n<!-- Grafismo gerado com recurso a IA, EPI, 2026. Derivação da calçada existente; gerar_calcada_continua.py. -->\n'
    light = start + f'<rect width="960" height="440" fill="{ARGAMASSA}"/><g stroke-width="1.5" stroke-linejoin="round">'
    for kind in ('c', 'e'):
        for tone, pts in sorted(data[kind].items()):
            light += f'<path fill="{CLARAS[tone]}" stroke="{CLARAS[tone]}" d="{caminho(pts)}"/>'
    result = {'calcada-clara.svg': light + '</g></svg>\n'}
    for band, low in enumerate((28, 172, 316), 1):
        def wave(x, y): return y + 44 * math.sin(2 * math.pi * x / 480)
        outline = [(x, wave(x, low)) for x in range(-16, 977, 8)] + [(x, wave(x, low + 72)) for x in range(976, -17, -8)]
        svg = start + f'<path fill="{ARGAMASSA}" d="{caminho([outline])}"/><g stroke-width="1.5" stroke-linejoin="round">'
        for tone, pts in sorted(data['e'].items()):
            selected = []
            for stone in pts:
                x = sum(p[0] for p in stone) / 4
                y = sum(p[1] for p in stone) / 4 - 44 * math.sin(2 * math.pi * x / 480)
                if low <= y < low + 72: selected.append(stone)
            svg += f'<path fill="{ESCURAS[tone]}" stroke="{ESCURAS[tone]}" d="{caminho(selected)}"/>'
        result[f'calcada-onda-{band}.svg'] = svg + '</g></svg>\n'
    return result
if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--verificar', action='store_true'); args = parser.parse_args()
    for name, content in assets().items():
        target = ROOT / 'assets' / name
        if args.verificar: assert target.read_text('utf-8') == content, name
        else: target.write_text(content, encoding='utf-8', newline='\n')
        print(name, len(content.encode()))
