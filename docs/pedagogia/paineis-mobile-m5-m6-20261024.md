# M5/M6 — instruções legíveis ao lado do QR

A regra original reservava 150px laterais para o QR. Abaixo de900px, o QR passava para o fluxo normal, mas as instruções continuavam a perder essa largura. No painel M6-F11 a360px, o texto ficava com87px.

Nos20painéis remotos de M5/M6, acrescenta-se apenas `.como{max-width:40rem}` à regra móvel existente. As instruções passam a237px a360px; o QR fica abaixo do texto. Os dois painéis editoriais M6-F12/F13 não usam este bloco e ficam intactos. Não há alteração de HTML, JavaScript, rótulos, serviços ou regras acima de900px.

## Verificação executada

- Navegador,20painéis a360px: texto com237px, QR estático abaixo das instruções, sem transbordo horizontal.
- Painel M6-F11 a320,360,390,900,901e1280px: sem transbordo; larguras do texto197,237,267,640,323e583.125px, respetivamente. O QR mantém a posição absoluta acima de900px.
- Comparação dos20ficheiros: removendo a única regra acrescentada, cada ficheiro coincide com o anterior. `git diff --check` aprovado.
- Capturas e medidas antes/depois guardadas na entrega local. Não se iniciou sala nem se enviaram respostas.

Pendências complementares: leitor de ecrã, sessão multiutilizador e ecrã inteiro nativo não executados. A contagem161de testes Python corresponde ao código pedagógico anterior deste ciclo; a correção CSS é validada pelas medições e comparação dos ficheiros, sem criar testes que apenas repitam a regra.

O padrão também existe noutros módulos, mas a propagação fica para lote próprio após confirmar o trabalho concorrente em M1/M7 (PR#80). Este lote limita-se a M5/M6.
