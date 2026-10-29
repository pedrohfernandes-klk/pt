# Auditoria do M7, resto do M4 e do M1: correções aplicadas (28/10/2026)

Segundo lote da auditoria de 28/10, depois do #128. Aplica todos os achados confirmados do M7, os do M4 que o #128 deixou de fora e os do M1 que não estavam no manifesto do #128. São 292 trocas literais em 54 ficheiros, todas só de texto (268 do lote e 24 da revisão de 29/10, que também acertou seis trocas do lote). As trocas estão em `scripts/auditoria_m4_m7_20261028.json`, e o script `scripts/aplicar_trocas.py` aplica-as e gera o manifesto `tests/fixtures/auditoria-m4-m7-edits-20261028.json`.

## O que mudou

**Regras de escrita**
- Saem «ficha», «folha» e «jogar» do texto visível:
  - nas tarefas da unidade 1 e da unidade 3 do M7 (descrição e entrega «em papel»);
  - no arquivo do guia do M7 («perfil» em vez de «ficha de identidade», «créditos» em vez de «ficha técnica»);
  - no portefólio do M7 («no papel», ficheiros `M7_Ux_aula_<dia-mês>`);
  - na F36 («na lição»).
- «·» dentro de frases: nos rodapés «Fontes:» de oito lições do M7 e nos cartões das tarefas do índice do M1.
- «glossário» passa a «vocabulário», como o quadro se chama, em dez enunciados do M7.
- Títulos de obras em itálico: nos guiões das aulas 4, 6, 9, 10, 11 e 13 do M1 e numa ligação da tarefa da unidade 3 do M7. No guia do M7, «Lírica pessoana», com minúscula, como no índice e no mapa.

**Factos, citações e numeração**
- A margem dos poemas do M7 passa a contar os versos de cada poema (F02, F04, F05, F06, F08, F09, F11, F34, F36). As explicações que citam «v. N» acompanham-na: «Mar Português» tem 12 versos, «Nevoeiro» 15. Nos excertos não contíguos da F36, a margem e as explicações deixam de ter números.
- F09: o retrato de D. Sebastião é anterior a Alcácer Quibir (1578). «Valete, Fratres» fica completo no texto e no vocabulário.
- F34: 1915 é o ano da publicação no *Orpheu*, não o da escrita. F06: «à parte isso» quer dizer «fora isso, tirando isso».
- F07: a lição mostra os versos que trabalha, com as fontes («Os versos da lição», no fim do cartão 2). O exemplo da causal passa a ser declarativo: «Os deuses são deuses / Porque não se pensam».
- F01: a paráfrase da carta a Casais Monteiro deixa de estar entre aspas. F35: «O rio da minha aldeia…» abre a última estrofe.
- F13 e F15: as pistas deixam de dizer o que a lição explica que o texto não autoriza. Na F13, a pista da 4.ª estrofe diz que o poeta se dirige à ceifeira e, à parte, o que diz de si («O que em mim sente está pensando»), sem pôr o verso na boca da ceifeira.
- F13, cartão 8: o enunciado chamava «antítese» ao recurso que a 1.ª lacuna pede. Passa a «Que recurso há em «Ouvi-la alegra e entristece», e que reação de quem ouve mostra?», na lição e no relâmpago k8 do painel (dados e opção). A chave não muda.
- F14: saem do Abre a página de «Tabacaria» na *Presença* e a nota que pedia desculpa por ela (achado m7 26). Ficam o símbolo e o texto de abertura.
- Página de Pessoa (obras): as lições já têm leituras de «Autopsicografia», de «O meu olhar é nítido como um girassol», de «Para ser grande, sê inteiro» (F23) e de «Chuva Oblíqua», VI (F34), e a cena-poema de «Vem sentar-te comigo, Lídia». A leitura de «Quando vier a Primavera» liga à F35, «O rio e o olhar», que a tem.
- Tarefa da unidade 1 do M7: «Ambos se voltam» (próclise). Os cartões da F14 e da F15 são indicados pelo nome, e não por números que mudam a cada tentativa.

**Enunciados que pediam o que nenhum cartão mostra**
- F10: a entrega fecha-se na aula de tarefa da unidade 3. O cartão «A entrega» diz o que avalia o resultado, e os cartões 14 e 17 só perguntam o que os cartões anteriores mostram. O ordenar da memória descritiva segue os cinco pontos, e o feedback do cartão 9 diz que «o que falta» é o último dos cinco.
- F11: a defesa escrita deixa de falar de «ordem pedida» e de «120 a 160 palavras». O enunciado do cartão 11 pede um poema e um autor, como as lacunas.
- F02: o cartão 19 diz «com provas» sem ambiguidade. F04: o par «Penso com os olhos» tinha duas respostas defensáveis.
- Arquivo do índice do M7: saem as remissões para cartões que o desafio não mostra («caixa Recorda», «linha de vida», «O essencial», «Para entender»). A numeração dos versos e as cópias da F07, da F10 (incluindo o ordenar da memória descritiva, com cinco pontos) e da F11 (o ordenar da defesa, sem «ordem pedida» nem «120 a 160 palavras») ficam iguais às da lição.

**Painéis do M7**
- Em 13 painéis, o relâmpago (dados e opção do seletor) passa a dizer o mesmo que a lição. Quando divergiam, a referência foi a lição.
- Oito cabeçalhos de painel passam a ter a unidade certa.
- Paridade docente (`audit_teacher_parity.py --modules m1 m4 m7`): antes, 24 painéis iguais e 13 diferentes (32 controlos diferentes); agora, 37 iguais, nenhum diferente, 471 controlos iguais.

**Mapa, guia e portefólio do M7**
- O mapa liga às aulas de tarefa (e não às âncoras escondidas do arquivo) e fecha com a última retoma do índice.
- O portefólio lista as três tarefas individuais atuais, e o bloco «Quando» pede para cada tarefa o mesmo que a lista: as fotografias do trabalho e da síntese, ou a ligação para o objeto (saem a linha a mais e os trabalhos de grupo).

**M4**
- A tarefa da unidade 1 é individual e em papel: F10 (encomenda, entrega e pistas), guião da aula 8 e mapa. Os casos da F10 passam de «grupo» a «colega» (cartões 6, 7 e 15, e «Falou depressa» no «O que não é»), com o mesmo enunciado no painel (k7 e k15) e no guião da aula 8 (bloco 29–38 e lista dos cartões).
- Aulas 8 e 16: o arquivo do Guia da tarefa guarda a versão anterior (tarefa 1 em grupo e com PDF, Tarefa 2 = discurso, Tarefa 3 = apreciação). Na aula 8 projeta-se o exemplo «Os pegadores» que está no «Ler mais» do cartão, e o arquivo não se projeta. Na aula 16 projeta-se só o exemplo «Uma hora de silêncio», com o aviso de que o arquivo guarda a numeração e a entrega anteriores. O arquivo fica como está: o verificador do achado m4 11 deu-o como marcado como anterior.
- Numeração atual das tarefas (unidade 2, apreciação; unidade 3, discurso) na F14, na F20 e nos guiões das aulas 8, 11 e 16. O «Para casa» da aula 11 deixa de pedir a tarefa em casa, e a procura da passagem na peça inteira passa a opcional.
- Mapa, «As tarefas do Teams»: a tarefa 1 é individual, e a apreciação passa a 2 e o discurso a 3, com os mesmos critérios.
- F20: a explicação do cartão 15 diz «o que lhe acontece», como o enunciado corrigido no #128.
- Guião da aula 9, reescrito a partir de `m4/recursos/tpc-entrada.js` e do `painel-m4-f28`: 45 minutos com os blocos do painel, os 15 cartões atuais, três perguntas para discutir e a proposta de cena. O quadro de Lupi passa a um prolongamento opcional de 45 minutos.

**Respostas e chaves que mudam, porque o achado o pede**
- F07: `CARTOES[9].certas` passa de `[3]` a `[4]` (na frase nova, «porque» é a 5.ª palavra), também na cópia do arquivo; `CARTOES[3].pares[1]` com o exemplo novo.
- F04: `CARTOES[17].pares[2]` passa a «Porque o vejo».
- F10: `CARTOES[6].passos` passa de quatro para cinco, também na cópia do arquivo do índice (é o mesmo cartão, com o mesmo enunciado e a mesma explicação; o achado m7 50 pede os cinco pontos, como na F07 a cópia acompanhou `certas`); `CARTOES[17].pares` com memória e defesa.
- Painel da F02, relâmpago 19: o tipo passa de «vf» a «escolha», como o cartão 19 da lição.

## Como os testes o aceitam

As lições, as tarefas e os índices estão congelados por hash. `tests/auditoria_20261028.py` desfaz agora os dois manifestos, o mais recente primeiro (este, depois o do #128). As cinco ligações que já existiam passam assim a desfazer os dois: `test_task_routes_closure` (com o manifesto novo à frente em `original_lesson_text`), `task_source_contract`, `test_m1_grammar_pilot`, `test_module_layout` e `test_task_90`. Mais quatro testes desfazem as trocas antes de comparar com o estado congelado, cada um com comentário datado:
- `test_task_routes_closure`: o hash dos bancos do arquivo;
- `test_apoios_tabelas`: o hash da F15 depois das tabelas;
- `test_task_compact_m7`: as três tarefas do M7;
- `test_m7_u2_task`: o arquivo do guia.

Um teste afirmava o texto antigo e muda, com comentário datado: `test_m7_sonho_memoria` exigia a nota «Não é uma reprodução do poema» no Abre da F14; passa a afirmar que o Abre já não tem a figura de «Tabacaria» e mantém o texto de abertura.

Sem a camada nova, 13 testes falham. Com ela, passam os 262.

## O que ficou de fora, e porquê

**Fora deste trabalho**
- Painéis novos: M1 F19 e F20 (achado m1 4) e M7 F35 e F36.
- A Sala em tempo real (código da sala, placar e o rótulo da Sala nos cabeçalhos dos painéis do M4 e do M7, achado m4 32): há outro PR a tirá-la destas páginas. As trocas de cabeçalho só tocam no número da unidade.
- O pedido projetado dos 15 painéis do M7 mostra os sublinhados em bruto. A correção é no código de envio da Sala, e não há achado confirmado no M7.

**Já resolvido pelo #128** (está no manifesto e confere no ficheiro): m7 0, 3 e 8; m4 0 a 10, 14, 16, 18 a 31 e 33; m1 0 a 3, 5 a 10, 12, 14 a 16 e 18; m1 11 (o «2.»); m1 13 (F04 e aula 1).

**Resolvido pelo #128 no sentido contrário**: m4 34 e m7 56. As legendas dizem todas «Morte do Conde Andeiro», a forma maioritária do módulo.

**Já não se confirma**: m1 11 («0 de 2»). O aquecimento também conta como pergunta.

**À espera de confirmação na fonte**: m7 33, na F13 («'stá pensando», «pra» ou «p'ra cantar»). O Arquivo Pessoa não abriu nesta sessão, e a grafia tem de ser confirmada na edição da Ática (1942). As trocas condicionais (lição, painel k9 e k12, arquivo) estão prontas.

**Pede decisão do docente**
- m4 15, «Como se avalia»: o verificador mandou esperar que o docente confirme o peso das provas rápidas, que é igual nos mapas do M1 e do M7. Só entra o bloco «As tarefas do Teams».
- m7 5, segunda parte: os nomes `_aula_` nos portefólios dos outros módulos, que os alunos já usam. O portefólio do M4 tem os mesmos problemas, mas sem achado confirmado.
- «glossário» no arquivo do índice (m7-f02 e m7-f14): obrigaria a uma redação nova.
- Sem achado confirmado: o «·» nos cartões de tarefa dos índices do M4 e do M7; o fecho dos guiões das aulas 8 e 15 do M4; o itálico de *Painéis de São Vicente* no gancho da F20 do M1.
- Arquivo do índice do M4: o desafio da F10 «Quanto dura a apresentação e quantos a fazem?» tem como resposta certa «Três a quatro minutos, em grupos de dois ou três». É um desafio arquivado, que não copia nenhum cartão atual, e mudá-lo mudaria a resposta certa sem achado.

**Fora do lote**
- m7 55 também nos títulos das provas A, B e C e dos questionários do M7. Só se trocou o guia.
- O mapa do M1 tem as mesmas ligações para `#desafio-N` escondidos (o defeito do m7 40). Fica registado para o M1.
- m7 27 na variante com um cartão novo: obrigaria a ressincronizar o painel inteiro. Seguiu-se a correção final, sem mudar índices.
- F15, pistas[2]: o verificador deixou ficar.
- Binários: os diapositivos das aulas 8, 9, 11 e 16 do M4 (o da aula 8 tem «Um grupo liga o roncador») e `m4/aulas/guioes-m4.pdf` podem repetir o texto antigo. Têm de ser regenerados no repositório das fontes.

**Rejeitadas**: nenhuma.

## Como voltar a correr o script

```
python3 scripts/aplicar_trocas.py               # aplica o que faltar e regenera o manifesto
python3 scripts/aplicar_trocas.py --verificar   # só confere (1 se faltar algo; 2 se algum ficheiro não conferir)
python3 -m unittest discover -s tests -p 'test_*.py'
```

O script é idempotente: reconhece as trocas já aplicadas e só aplica as que faltam. Cada ficheiro é independente. Se um texto antigo não aparecer o número certo de vezes, esse ficheiro fica como estava, sai do manifesto e é listado no fim (o script sai com 2); os outros aplicam-se. Sobre `origin/main` (que já tem os PR #123 e #125, do exame, sem ficheiros em comum com este lote), as 292 trocas aplicam-se todas.

**Ordem com o PR que tira a Sala (`work/sala-desligada-20261028`).** Funde-se este PR primeiro. Depois:
1. rebaseia-se a Sala sobre o `main` com este lote; nos HTML em conflito fica a versão do `main`;
2. volta-se a correr `python3 scripts/desligar_sala.py`, que corta a Sala sobre as lições já corrigidas e refaz o relâmpago e o MATERIAL dos painéis a partir delas (por exemplo, o MATERIAL do cartão 17 do painel-m7-f04 passa a ter «Porque o vejo», e o do cartão 6 do painel-m7-f10 os cinco pontos);
3. corre-se `python3 scripts/aplicar_trocas.py`: as 292 trocas já lá estão, e só os hashes do manifesto mudam;
4. em `tests/auditoria_20261028.py`, `undo()` desfaz os três manifestos, o mais recente primeiro: a Sala, depois este lote, depois o #128 (e `undo_sala()` continua a desfazer só a Sala); em `test_task_routes_closure`, `original_lesson_text` usa a mesma ordem (Sala, este lote, #128, Reis, tabelas, gramática, instruções); `test_apoios_tabelas` passa a usar `undo()`.

Esta ordem foi ensaiada numa cópia de trabalho (29/10): a árvore deste lote, com o `desligar_sala.py` do ramo da Sala corrido por cima e os testes dos dois ramos juntos como no ponto 4, dá as 292 trocas como aplicadas, o `desligar_sala.py --verificar` sem nada a mudar e 276 testes unitários a passar (os 262 deste ramo e os 14 da Sala).

**Na ordem inversa não funciona sem trabalho à mão.** Na árvore da Sala (`20ce3ef0`), o `desligar_sala.py` já refez o relâmpago de 15 painéis do M7 a partir das lições antigas (enunciado inteiro, sem «_»), e não volta a mexer em páginas já cortadas. O script aplica as trocas em 45 ficheiros e deixa por resolver os 9 painéis cujo relâmpago este lote corrige (f02, f04, f05, f07, f10, f11, f13, f23 e f34); o relâmpago e o MATERIAL desses painéis teriam de ser refeitos a partir das lições corrigidas.
