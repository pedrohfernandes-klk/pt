# M8-F04 — ouvir, experimentar e cortar com sentido

Revisão local de 21 de outubro de 2026, após publicação dos blocos anteriores pela PR #54. Base main 4752090a. Ramo work/m8-palavras-escuta-20261021. Este bloco não foi publicado.

## Integração audiovisual com tarefa

A leitura de «As Palavras», por Beatriz Batarda no programa Voz (2005), já estava selecionada através da ligação à videoteca LENTE. A fonte oficial foi conferida na RTP Ensina: https://ensina.rtp.pt/artigo/as-palavras-de-eugenio-de-andrade/ . A página identifica poema, intérprete e programa e disponibiliza texto e recurso audiovisual. Foi consultado o HTML do leitor oficial, sem descarregar o vídeo.

A ficha passa a permitir carregar a leitura opcionalmente. O leitor nativo acede ao recurso remoto usado pela RTP; não se guardou uma cópia do vídeo no repositório. Não há elemento de media antes da ação de carregar, nem reprodução automática depois de carregar. O utilizador inicia a reprodução nos controlos. Há fecho por teclado, regresso do foco e libertação da fonte ao fechar ou sair do cartão. Uma falha de reprodução mostra a alternativa de abrir a fonte ou realizar a tarefa sem vídeo.

A tarefa é concreta: dizer a abertura com dois realces diferentes, ouvir até à primeira comparação, localizar uma pausa ou realce e confrontar a observação com a previsão. A interpretação do desempenho não é classificada como certa ou errada. Sem vídeo, a abertura já citada permite leitura própria, leitura por outra pessoa ou comparação mental. Texto integral na fonte/manual; não foi copiado para a ficha. Não se atribuem à intérprete pausas ou intenções que não foram revistas.

## Ensinar o corte e a comparação

O exercício de cortes na ficha referia versões sem mostrar o modelo completo. Recuperou-se do desafio o texto didático original de 17 palavras, com versões de 13, 9 e 6 palavras. Todas resultam de supressão de palavras do texto de base, mantendo a ordem; maiúsculas e pontuação podem ser ajustadas. Cada versão parte da Base, não da anterior, para evitar que o procedimento contradiga a proibição de acrescentar palavras.

A associação deixa de pedir só contagens: pergunta o que cada versão conserva explicitamente e o que deixa por inferir. A mais curta não é automaticamente a melhor. A operação tem uma consequência de sentido que o aluno pode explicar e transferir para uma frase sua.

Corrigiu-se também o atalho «metáfora sem como». A reescrita é identificada como didática e a classificação passa pela identificação figurada; a ausência de uma palavra não basta. Desafios e painel sincronizados, incluindo variantes antigas que mantinham a formulação simplificada ou decretavam superior a versão mais curta.

## Design e preservação

Mantidos 25 cartões, tipos, ordem, imagem e cartão de abertura integralmente iguais à base; nenhum motor de exercícios foi alterado. Cartões revistos: 2,3,6,8,14,19,20,21,24 (índices a partir de zero). Sem novas fichas ou aumento de exercícios. URLs e chaves de progresso preservadas; sem necessidade de migração de índices.

O botão segue o contraste e o desenho simples do site, tem pelo menos 44 píxeis de altura e foco visível. O modelo de cortes agrupa as versões com rótulo e margem marcada; CSS restrito ao leitor e ao modelo. Os detalhes técnicos da verificação ficam neste relatório, não nas instruções ao aluno.

## Verificações efetivas

- 116 testes Python aprovados, incluindo quatro regressões novas.
- Auditorias dos 108 bancos e da sintaxe, incluindo o script externo novo; contagens preservadas: 2509 cartões, 710 de leitura e 1799 interativos.
- Chromium a 320/1440: tentativa normal, conclusão recuperada após recarregar e passagem pelos 25 cartões do banco; sem erro JavaScript ou transbordo horizontal nos cenários percorridos.
- Leitor: ausência de pedidos de media antes da ação, ausência de reprodução automática, controlos nativos, fecho e alternativa por teclado, foco recuperado e fonte libertada ao sair do cartão. Mensagem de falha exercitada com um evento de erro controlado, não confundido com falha real da RTP.
- Reprodução real após integração, em largura 320: mais de dois segundos, duração técnica de 73,566 segundos, largura de vídeo 788 píxeis e dados de áudio descodificados. Isto demonstra reprodução técnica inicial; não revisão audiovisual integral, qualidade de legendas ou compreensão do aluno.
- Capturas móveis de escuta e modelo inspecionadas; dimensão e apresentação final do botão verificadas. A última clarificação de que as versões partem da Base foi validada estaticamente depois da bateria de navegador, sem mudança de mecânica.

Teste reproduzível tests/browser_m8_palavras_escuta.py. Por defeito, a CI bloqueia o acesso ao CDN e testa a interface sem depender da disponibilidade externa; --live-media acrescenta a reprodução real inicial. A execução local utilizou essa opção. O Windows bloqueou entretanto o executável habitual do ambiente; os testes foram concluídos com o Python instalado e as bibliotecas já disponíveis, sem alterar os materiais por causa desse bloqueio.

## Limites e continuidade

Não foi feita revisão audiovisual integral, transcrição ou revisão de legendagem; não se afirma qualquer pormenor efetivo da entoação de Batarda. O recorte é indicado pela passagem textual, não por uma minutagem não conferida. Não se testaram Safari/iOS, leitor de ecrã real, projeção física ou todas as rotações. PDF/PPTX arquivados não foram revistos. Os testes não demonstram retenção ou transferência com alunos. Mantém-se o plano de beneficiações e os critérios de ensino, recuperação, aplicação, jogo e design.
