"""Opções equilibradas nas escolhas múltiplas (pedido do docente de 29/10/2026).

«Ainda há demasiadas escolhas múltiplas em que a resposta certa é claramente a de maior dimensão. Não pode ser.» A medição
é a de scripts/medir_opcoes.py (caracteres visíveis, sem etiquetas HTML nem _ e *), em toda a árvore publicada.

30/10/2026, primeira fase (opções denunciadoras): nenhuma pergunta com a certa pelo menos 1,25 × a maior errada e pelo menos
5 caracteres acima dela. As trocas estão na camada literal tests/fixtures/opcoes-denunciadoras-edits-20261030.json (gerada
por scripts/aplicar_trocas.py a partir de scripts/opcoes_denunciadoras_20261030.json). Ficam fora da regra as opções oficiais
das provas do IAVE e as páginas com testes de opções próprios (medir_opcoes.na_regra()): as provas em cartões, exame/provas/
(tests/test_provas_cartoes.py, catraca em prova.json), e os aquecimentos em cartões, tarefas/*/aquecimento/
(tests/test_aquecimentos_m*_opcoes.py).

30/10/2026: catraca para a fase seguinte (amplitude, módulo a módulo). Por pasta, as perguntas fora dos 20 % (a mais longa
mais de 1,20 × a mais curta, com 8 ou mais caracteres de diferença) e as perguntas em que a certa é estritamente a mais
longa não podem subir. Quando descerem, baixa-se a catraca com python3 scripts/medir_opcoes.py --catraca.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import medir_opcoes as M  # noqa: E402

# 30/10/2026: os números depois das opções denunciadoras (2848 perguntas na regra; 730 fora dos 20 %, 741 com a certa a
# mais longa). Não podem subir; uma pasta que não esteja aqui não tem margem nenhuma.
CATRACA = {
    'assets': {'fora20': 3, 'certa_mais_longa': 1},
    'atlas': {'fora20': 4, 'certa_mais_longa': 4},
    'c': {'fora20': 28, 'certa_mais_longa': 33},
    'm1': {'fora20': 97, 'certa_mais_longa': 79},
    'm2': {'fora20': 53, 'certa_mais_longa': 40},
    'm3': {'fora20': 63, 'certa_mais_longa': 125},
    'm4': {'fora20': 133, 'certa_mais_longa': 89},
    'm5': {'fora20': 77, 'certa_mais_longa': 109},
    'm6': {'fora20': 49, 'certa_mais_longa': 55},
    'm7': {'fora20': 92, 'certa_mais_longa': 106},
    'm8': {'fora20': 68, 'certa_mais_longa': 51},
    'm9': {'fora20': 63, 'certa_mais_longa': 49},
}

# 30/10/2026: os aquecimentos do M7 ficaram fora desta passagem (gerados por scripts/aquecimentos.py, ainda sem teste de
# opções próprio) com 6 denunciadoras. Este número só pode descer.
AQUECIMENTOS_PENDENTES = {
    'tarefas/m7-u1/aquecimento/index.html': 3,
    'tarefas/m7-u2/aquecimento/index.html': 3,
}

_MEDICAO = None


def medicao():
    global _MEDICAO
    if _MEDICAO is None:
        _MEDICAO = M.medir(ROOT)
    return _MEDICAO


class OpcoesEquilibradas(unittest.TestCase):
    def test_medicao_encontra_as_perguntas(self):
        na_regra = [r for r in medicao() if M.na_regra(r['ficheiro'])]
        self.assertGreater(len(na_regra), 2500, 'a medição deixou de encontrar as escolhas múltiplas das lições')
        self.assertTrue({f'm{n}' for n in range(1, 10)} <= {M.pasta(r['ficheiro']) for r in na_regra})

    def test_zero_denunciadoras(self):
        """30/10/2026: a certa nunca destacadamente a mais longa (1,25 × a maior errada e 5 caracteres acima)."""
        den = [r for r in medicao() if M.na_regra(r['ficheiro']) and r['denunciadora']]
        self.assertEqual([], [f"{r['ficheiro']}: «{r['pergunta'][:60]}» {r['opcoes']} (certas {r['certas']})" for r in den])

    def test_aquecimentos_sem_denunciadoras_novas(self):
        """30/10/2026: nos aquecimentos (fora da regra acima), as denunciadoras que ficaram não podem crescer."""
        contagem = {}
        for r in medicao():
            if r['ficheiro'].startswith('tarefas/') and not M.na_regra(r['ficheiro']) and r['denunciadora']:
                contagem[r['ficheiro']] = contagem.get(r['ficheiro'], 0) + 1
        for ficheiro, n in sorted(contagem.items()):
            with self.subTest(ficheiro=ficheiro):
                self.assertLessEqual(n, AQUECIMENTOS_PENDENTES.get(ficheiro, 0))

    def test_catraca_por_pasta(self):
        """30/10/2026: fora dos 20 % e certa a mais longa, por pasta, não sobem."""
        atual = M.catraca(medicao())
        for pasta, numeros in sorted(atual.items()):
            limite = CATRACA.get(pasta, {'fora20': 0, 'certa_mais_longa': 0})
            for chave in ('fora20', 'certa_mais_longa'):
                with self.subTest(pasta=pasta, medida=chave):
                    self.assertLessEqual(numeros[chave], limite[chave],
                                         f'{pasta}: {chave} subiu de {limite[chave]} para {numeros[chave]}')

    def test_regra_da_medicao(self):
        """A regra com os pisos: 25 % e 5 caracteres para a denunciadora, 20 % e 8 caracteres para a amplitude."""
        self.assertTrue(M.avalia(['a' * 30, 'b' * 20, 'c' * 20], [0])['denunciadora'])
        self.assertFalse(M.avalia(['a' * 24, 'b' * 20, 'c' * 20], [0])['denunciadora'])
        self.assertFalse(M.avalia(['heterónimo', 'ortónimo', 'fingidor'], [0])['denunciadora'])  # 2 letras não denunciam
        self.assertTrue(M.avalia(['a' * 20, 'b' * 30, 'c' * 25], [0])['fora20'])
        self.assertFalse(M.avalia(['a' * 20, 'b' * 26, 'c' * 25], [0])['fora20'])
        self.assertEqual(M.limpa('<i>Os Lusíadas</i>, _Mensagem_ e **negrito**'), 'Os Lusíadas, Mensagem e negrito')
        # As opções oficiais das provas (cartões de tipo «item») não se medem.
        self.assertEqual([], list(M.itens({'t': 'item', 'o': ['a' * 40, 'b', 'c'], 'c': 0})))
        self.assertEqual(1, len(list(M.itens({'t': 'escolha', 'o': ['a' * 40, 'b', 'c'], 'c': 0}))))
        self.assertFalse(M.na_regra('exame/provas/2026-1f/grupo-i/index.html'))
        self.assertFalse(M.na_regra('tarefas/m7-u1/aquecimento/index.html'))
        self.assertTrue(M.na_regra('tarefas/m7-u1/index.html'))
        self.assertTrue(M.na_regra('m7/licao-m7-f01/index.html'))


if __name__ == '__main__':
    unittest.main()
