# M8-F01 — apresentar autores e dar sentido à leitura

Base: `02aee84e44eda2a1138285f1b623425c20397e5b` (PR #58 publicado). Correção da ficha «Três vozes, um século», do seu painel e dos desafios correspondentes. Sem alterações ao LENTE, ao motor, estilos, imagens ou chaves de progresso.

## Problema e decisões

Ângelo de Lima aparecia na cronologia, abertura, pergunta de sublinhar e fecho como eixo de uma ficha dedicada a Sena, Eugénio e Amaral. O apoio anunciado como exercício de Ângelo já tinha sido substituído por «Quatro lentes, um poema», com Pessoa. A cronologia misturava essa referência de 1915 com nascimentos e mortes, sem ligar suficientemente vida e leitura.

- Cronologia de seis estações dedicada às três vozes, com nomes/obras visíveis nos rótulos, inclusive quando os detalhes estão fechados. Datas ordenadas, obras e perguntas de leitura associadas. Retira-se a conclusão artificial de que 2022 «fecha» um século.
- Abertura, essencial, ajuda e fecho orientam para os três percursos, evitando a fórmula coletiva «depois da guerra, do exílio e da ditadura» como explicação uniforme.
- Três apresentações na mesma estrutura: autor, dado relevante, relação com a obra e pequena experiência de leitura. A biografia situa; a interpretação precisa de indícios.
- Ângelo mantém contexto opcional, com acesso ao perfil e poemas existentes no Atlas. O material não desaparece nem se transforma numa quarta voz central. Desaparece a remissão para o exercício inexistente.
- As tarefas obrigatórias e os desafios deixam de pedir a história militar/hospitalar de Ângelo e a revista de 1915. Recuperam relações entre poema/pintura e prece/oração, pseudónimo e um percurso de observação → hipótese → confirmação. Preservam-se tipos, posições das chaves nos itens reciclados e contagens.
- Adília Lopes é apresentada junto da escuta; o crédito distingue autora do poema e leitor Fernando Alvim. Cesariny é apresentado como poeta/pintor junto do seu recurso. Goya é identificado como pintor, distinguindo-o do poeta. Dickinson recebe contexto junto da referência ao trabalho de Amaral.
- Painel docente sincronizado com os interativos atuais. Critério comum de apresentação de autores acrescentado às orientações pedagógicas; a extensão ao corpus restante continua pendente.

## Fontes conferidas

- [Camões — Jorge de Sena](https://www.instituto-camoes.pt/activity/centro-virtual/bases-tematicas/figuras-da-cultura-portuguesa/jorge-de-sena): engenharia, exílio no Brasil em 1959 e percurso académico.
- [Camões — Eugénio de Andrade](https://instituto-camoes.pt/activity/centro-virtual/bases-tematicas/figuras-da-cultura-portuguesa/eugenio-de-andrade): nome civil, corpo/sentidos, linguagem, *As Mãos e os Frutos* (1948).
- [U.Porto — Ana Luísa Amaral](https://noticias.up.pt/2022/08/07/ana-luisa-amaral-uma-universidade-tem-a-obrigacao-de-ajudar-a-pensar/), [entrevista da autora](https://www.up.pt/arquivoweb/centenario.up.pt/ver_olharc836.html?id_olhar=28) e Seara Nova já conferida no PR #58: ensino, tradução, Dickinson e *Ágora* (2019).
- [Emily Dickinson Museum](https://www.emilydickinsonmuseum.org/the-museum/our-site/): a obra permaneceu praticamente inédita em vida.
- [Modernismo — Ângelo de Lima](https://modernismo.pt/index.php/a/angelo-de-lima), [editora](https://www.assirio.pt/autor/angelo-de-lima/15156) e perfil já existente no Atlas: poeta/desenhador, *Orpheu* 2 e contexto biográfico. Não se toma o internamento como explicação da poesia.
- [Editora — Adília Lopes](https://www.assirio.pt/autor/adilia-lopes/9195): identidade e nome de escrita. A autoria da escuta é coerente com os dados existentes e com o registo de atividade de [uma biblioteca escolar](https://www.aegaianascente.pt/arquivo20252026.php); a nova tentativa de abrir a página do vídeo pela ferramenta web falhou. Não houve novo visionamento/validação do áudio.
- [MNAC — Mário Cesariny](https://museuartecontemporanea.gov.pt/pt/artistas/ver/36/artists) e [RTP](https://ensina.rtp.pt/artigo/mario-cesariny-poesia/): relações entre poesia e imagem, contexto surrealista e autoria/leitura do recurso.

## Validação local e navegador

149 testes Python aprovados antes da última melhoria do rótulo da cronologia; os cinco testes novos foram repetidos e aprovados depois dessa melhoria. Sintaxe de 18 scripts dos três HTML aprovada.

Pré-visualização própria: abertura sem Ângelo como eixo; apresentação de Adília aberta por Enter, créditos visíveis sem carregar vídeo; cronologia normal com os seis nomes/obras visíveis e uma estação aberta por teclado; capturas a 320 e 1440 px. Contexto dos três autores e Ângelo opcional inspecionado em fixture com chave QA, com abertura por teclado e captura a 390 px. Sem corte horizontal visual nas capturas. Os destinos relativos da fixture não certificam a navegação do site real.

O teste remoto novo percorre tentativa normal e banco completo em 320/1440 px, verifica retoma, contexto opcional, painel e projeção. Está no workflow geral; a aprovação da execução remota e a publicação devem ser confirmadas na entrega, não presumidas da existência do teste.

## Limites e sequência

Mantêm-se 24 cartões na F01 e 94 no primeiro pool de M8; nenhuma nova lição ou requisito de conclusão. Progresso usa as mesmas chaves; o motor mantém a política existente de atualização de bancos.

Pendentes nesta verificação local: percursos completos remotos, projeção atualizada, leitor de ecrã, outros motores, todas as combinações de rotação, turma real e novo visionamento dos recursos externos. Os testes funcionais não demonstram aprendizagem.

Esta ronda aplica o critério à F01. A revisão de autores no complemento «Quatro lentes», nas restantes fichas M8 e em M1–M9 precisa de lotes próprios. A nova orientação não constitui uma certificação de que todos os autores de todas as páginas já estão apresentados.
