"""01/11/2026: âmbito, reversibilidade e integridade da revisão editorial."""
from pathlib import Path
import hashlib
import json
import re
import unittest
from auditoria_20261028 import undo_varredura, undo_conteudos_lote2

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT/'docs/qa/varredura-formatacao-20261101.json').read_text('utf-8'))
MANIFEST = json.loads((ROOT/'tests/fixtures/varredura-formatacao-edits-20261101.json').read_text('utf-8'))


class Varredura(unittest.TestCase):
    def test_todos_os_pontos_tem_destino(self):
        rows = LEDGER['achados']
        self.assertEqual(len(rows), 361)
        self.assertEqual(len({r['id'] for r in rows}), 361)
        self.assertEqual(sum(r['estado']=='adiado' for r in rows), 109)
        self.assertEqual(sum(r['estado']=='conforme' for r in rows), 13)
        self.assertEqual(sum(r['estado']=='corrigido' for r in rows), 239)

    def test_nao_toca_nos_ficheiros_editoriais_em_revisao(self):
        protected = {f for p in LEDGER['pedidos'] for f in p['ficheiros']}
        self.assertEqual(set(MANIFEST['files']) & protected, set())
        for r in LEDGER['achados']:
            expected = [p['numero'] for p in LEDGER['pedidos'] if r['file'] in p['ficheiros']]
            self.assertEqual(r['depois'], expected, r['id'])

    def test_camada_reversivel_e_cabecalhos_intactos(self):
        for rel, record in MANIFEST['files'].items():
            with self.subTest(file=rel):
                current = (ROOT/rel).read_text('utf-8')
                original = undo_varredura(rel, current)
                # 02/11/2026: conferir o hash histórico após desfazer estritamente apenas o lote 2 posterior.
                current = undo_conteudos_lote2(rel, current)
                self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), record['base_sha256_lf'])
                self.assertEqual(hashlib.sha256(current.encode()).hexdigest(), record['after_sha256_lf'])
                for edit in record['edits']:
                    self.assertEqual(current.count(edit['new']), 1)
                if rel.endswith('.html'):
                    # 01/11/2026: apenas os estilos explícitos da revisão podem entrar no cabeçalho.
                    before=re.search(r'<head>.*?</head>',original,re.S)[0]
                    after=re.search(r'<head>.*?</head>',current,re.S)[0]
                    credits='.tabela{display:block;margin-top:4px;font:.8125rem/1.4 Arial,Helvetica,sans-serif;color:var(--suave)}.tabela a{color:inherit}'
                    verse='.verso .vl{display:block;padding-left:1.4em;text-indent:-1.4em}.verso:has(>b:first-child){padding-left:1.6em}.verso>b:first-child{float:left;width:1.6em;margin-left:-1.6em}'
                    for css in (credits,verse):
                        after=after.replace('<style>'+css+'</style>','')
                    self.assertEqual(before,after)
                    self.assertIn('<html lang="pt-PT"', current)

    def test_lugar_familia_e_poema_nao_passam_a_titulos_de_livro(self):
        for rel in MANIFEST['files']:
            if not rel.endswith('.html'):
                continue
            s=(ROOT/rel).read_text('utf-8')
            self.assertNotIn('Largo <i>Amor de Perdição', s)
            self.assertNotIn('<i>Os Maias</i> «vieram habitar»', s)
            self.assertNotIn('<i>O Sentimento dum Ocidental</i>', s)

    def test_creditos_declaram_as_lacunas_da_fonte(self):
        for slug in ('licao-m7-f01', 'licao-m7-f05', 'mapa-do-modulo-m7'):
            s=(ROOT/f'm7/{slug}/index.html').read_text('utf-8').replace('\\"', '"')
            # 01/11/2026: crédito visível na peça .tabela, sem controlo de abertura.
            # 05/11/2026: decisão 153 (docente: «não quero tanto texto, prefiro um botão com um "i" que o user possa abrir»)
            # substitui a regra de 01/11: os seis campos do crédito continuam todos, letra a letra, agora dentro do «i»
            # (details.info-i, família P10 do plano dos créditos), e nenhum fica fora dele; o rótulo «Fernando Pessoa, cerca de
            # 1914.» fica à vista.
            blocos=[b for b in re.findall(r'<details class="info-i[^"]*" name="info-i">(?:(?!</details>).)*</details>',s)
                    if 'PessoaChapeu' in b]
            self.assertEqual(len(blocos),1,slug)
            fora=s.replace(blocos[0],'')
            for field in ('Fotógrafo não identificado;', 'retrato de Fernando Pessoa com chapéu;',
                          'cerca de 1914 (data incerta);', 'original sem instituição indicada;',
                          'domínio público', 'File:PessoaChapeu.jpg'):
                self.assertIn(field,blocos[0])
                self.assertNotIn(field,fora)
            self.assertIn('<figcaption>Fernando Pessoa, cerca de 1914.',fora)
            self.assertNotIn('class="tabela"',s)
            self.assertNotIn('credito-imagem',s)
            self.assertIn('alt="Fernando Pessoa de chapéu e óculos, cerca de 1914"',s)
        mapa=(ROOT/'m7/mapa-do-modulo-m7/index.html').read_text('utf-8')
        # 05/11/2026: a ligação «Lição M7-F01» fica à vista, na legenda, fora do «i» e logo depois dele.
        # 11/11/2026: decisão 152 no M7 (achado 36): a sigla da ligação leva a junção (U+2060) depois do hífen, para não se partir.
        self.assertRegex(mapa,r'</details><figcaption>Fernando Pessoa, cerca de 1914\. <a href="[^"]*licao-m7-f01/">Lição M7-\u2060F01</a></figcaption>')

    # 01/11/2026: o motor de palavras formata cada peça isoladamente.
    def test_marcadores_de_italico_fecham_em_cada_palavra(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        from audit_cards import lesson_cards
        checked=0
        for path in ROOT.glob('m*/licao-*/index.html'):
            for card in lesson_cards(path):
                if card['t'] not in ('sublinhar','riscar'):continue
                for token in card['frase'].split():
                    self.assertEqual(token.count('_')%2,0,(str(path),token))
                checked+=1
        self.assertGreater(checked,0)


    # 02/11/2026: rótulos A./B./C., II./IV. sem travessão nem dois pontos encadeados (volta de confirmação, achados F2 e F7).
    def test_rotulos_com_ponto_e_sem_travessao(self):
        rotulados=('m1/guilhade-dona-fea','m1/lisboa-cercada','m3/arte-estima','m3/bicho-da-terra','m3/camoes-desconcerto',
                   'm3/espada-pena','m5/eca-ramalhete','m6/antero-deus','m6/cesario-noite','m7/campos-maquina')
        for slug in rotulados:
            s=(ROOT/slug/'index.html').read_text('utf-8')
            with self.subTest(slug=slug):
                self.assertNotIn('</b> — ',s)
                self.assertRegex(s,r'<b>(?:[A-D]|II|IV)\.</b> ')
        for rel in MANIFEST['files']:
            if rel.endswith('.html'):
                with self.subTest(file=rel):
                    self.assertIsNone(re.search(r'<b>[A-Z]{1,3}</b>(?: —|:)',(ROOT/rel).read_text('utf-8')))

    # 02/11/2026: o «Depois» de cada ponto corrigido existe no texto visível do ficheiro, pela ordem do relatório
    # (sem os asteriscos do itálico; ↵ marca a quebra de linha).
    def test_relatorio_coincide_com_o_texto_visivel(self):
        import html as H
        def visivel(s):
            s=s.replace('\\"','"').replace('\\/','/').replace('\\n','\n')
            s=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),s)
            s=re.sub(r'<br\s*/?>','\n',s)
            s=re.sub(r'</(p|li|dt|dd|div|h\d|figcaption|tr)>','\n',s)
            s=H.unescape(re.sub(r'<[^>]+>','',s))
            s=re.sub(r'(?<![\w/])_([^_\n]+?)_(?!\w)',r'\1',s).replace('**','')
            return re.sub(r'\s+',' ',s)
        cache={}
        corrigidos=[r for r in LEDGER['achados'] if r['estado']=='corrigido']
        self.assertEqual(len(corrigidos),239)
        for r in corrigidos:
            if r['file'] not in cache:
                # 02/11/2026: o relatório descreve a varredura publicada, anterior ao lote 2.
                cache[r['file']]=visivel(undo_conteudos_lote2(r['file'],(ROOT/r['file']).read_text('utf-8')))
            texto=cache[r['file']]
            segmentos=[re.sub(r'\s+',' ',x).strip() for x in r['resultado'].replace('*','').split('↵') if x.strip()]
            self.assertTrue(segmentos,r['id'])
            pos=texto.find(segmentos[0])
            self.assertNotEqual(pos,-1,(r['id'],segmentos[0][:120]))
            for seg in segmentos[1:]:
                nxt=texto.find(seg,pos)
                self.assertNotEqual(nxt,-1,(r['id'],seg[:120]))
                pos=nxt

    # 02/11/2026: uma nota que explica as barras dos versos só fica onde ainda há barras entre versos
    # (a M2-F12 ficou com a nota depois de perder as barras; visto no sítio público, depois do #152).
    def test_nota_da_barra_so_onde_ha_barras(self):
        self.assertNotIn('barra marca mudança de verso', (ROOT/'m2/licao-m2-f12/index.html').read_text('utf-8'))
        for rel in MANIFEST['files']:
            if rel.endswith('.html'):
                s=(ROOT/rel).read_text('utf-8')
                if 'barra marca mudança de verso' in s:
                    with self.subTest(file=rel):
                        self.assertRegex(s,r'class=\\?"verso\\?"[^>]*>(?:(?!</p>).)*? / ')


if __name__ == '__main__':
    unittest.main()
