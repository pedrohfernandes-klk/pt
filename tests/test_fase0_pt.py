"""Fase 0 do plano de melhoria (23/10/2026): imagens próprias no «Abre», marca do canto que não tapa o «Para levar»
e ligações dos cartões no estilo do sítio."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_cards import lesson_cards

RESERVA = '.jogo .cartao.escuro:has(.azulejo.canto){padding-bottom:84px}'
LIGACOES = '.jogo .ler a:not([class]){color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}'
# 23/10/2026: M4-F01 está a ser refeita noutro ramo (piloto das aulas claras) e ficou fora desta correção de CSS;
# quando esse ramo entrar, a lição tem de receber as duas regras (ou ligar assets/pt-lessons/lesson.css).
FORA = {'m4/licao-m4-f01/index.html'}


def css_da_licao(path):
    s = path.read_text('utf-8')
    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
    if 'pt-lessons/lesson.css' in s:
        css += (ROOT / 'assets/pt-lessons/lesson.css').read_text('utf-8')
    return css


class Fase0(unittest.TestCase):
    def test_abre_has_its_own_image(self):
        esperado = {
            'm1/licao-m1-f02': 'san-simon-ria-vigo.jpg',
            'm5/licao-m5-f10': 'os-maias-1888.jpg',
            'm5/licao-m5-f11': 'hotel-central-1910.jpg',
            'm4/licao-m4-f07': 'garrett-malhoa-1881.jpg',
            'm4/licao-m4-f08': 'joao-de-portugal-lupi.jpg',
        }
        for licao, img in esperado.items():
            with self.subTest(licao=licao):
                path = ROOT / licao / 'index.html'
                abre = lesson_cards(path)[0]
                self.assertEqual('Abre', abre['rot'])
                self.assertIn('src="../../img/fontes/' + img, abre['html'])
                self.assertTrue((ROOT / 'img/fontes' / img).is_file())
                # sem base64, o motor só põe a imagem no cartão do fim se a receber em «imagem»
                self.assertIn('EPIJogo.montar({imagem:"../../img/fontes/' + img, path.read_text('utf-8'))
        # o quadro de Lupi não volta à lição do incêndio (o cartão 12 corrige justamente essa confusão)
        self.assertNotIn('Lupi', lesson_cards(ROOT / 'm4/licao-m4-f07/index.html')[0]['html'])

    def test_synthesis_migration_reads_the_same_key_as_the_route(self):
        # 23/10/2026: sem a caixa de notas, unit-synthesis.js lê o texto antigo diretamente do localStorage;
        # data-notas tem de ser a chave que resp(n) lê nessa página (percurso-v2-M1-u… ou percurso-M4-u…).
        for m in range(1, 10):
            with self.subTest(modulo=m):
                s = (ROOT / f'm{m}/index.html').read_text('utf-8')
                # 26/10: closure lessons read historic notes without migrating or evaluating tasks.
                # 27/10/2026 (passagem do GPT, tarefas por unidade): o M2 passa ao mesmo modelo, com duas aulas de tarefa.
                if m in (1,2,4,7):
                    self.assertIn('unit-task-route.js',s)
                    adapter=(ROOT/'assets/unit-task-route.js').read_text('utf-8')
                    for key in ('percurso-v2-','percurso-','percurso-sintese-'):
                        self.assertIn(key,adapter)
                    self.assertNotIn('localStorage.setItem',adapter)
                    continue
                resp = re.search(r'function resp\(n\)\{try\{return localStorage\.getItem\("([^"]*)"\+M\+"-u"\+n\)', s)
                tag = re.search(r'<script defer src="\.\./assets/unit-synthesis\.js[^"]*" data-module="M(\d)" data-notas="([^"]+)">', s)
                self.assertTrue(resp and tag)
                self.assertEqual(str(m), tag.group(1))
                self.assertEqual(f'{resp.group(1)}M{m}-u', tag.group(2))

    def test_corner_mark_space_and_card_links_in_every_lesson(self):
        # 23/10/2026 (verificação): as lições que ligam lesson.css têm ligações sem classe no «depois» do ecrã final
        # («Voltar ao percurso», «Notas para a aula»); também deixam de ficar no azul do navegador.
        self.assertIn('.jogo .depois a:not([class]){color:inherit;',
                      (ROOT / 'assets/pt-lessons/lesson.css').read_text('utf-8'))
        for path in sorted(ROOT.glob('m[1-9]/licao-*/index.html')):
            rel = path.relative_to(ROOT).as_posix()
            if rel in FORA:
                continue
            with self.subTest(licao=rel):
                css = css_da_licao(path)
                self.assertIn(RESERVA, css)
                self.assertIn(LIGACOES, css)


if __name__ == '__main__':
    unittest.main()
