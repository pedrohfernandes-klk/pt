# Preparação de exame — primeiro incremento

Base: `915ac73ec5f495dd36db56a18ba3d5cc03ae2290` (Português). Branch: `codex/exame-sessoes-45`.

## Conteúdo e decisões

- 26 sessões com acesso livre por matéria e percurso sugerido: 19 de educação literária e sete de leitura, gramática, escrita e revisão.
- Cada sessão: aquecer 5 min, ler 8 min, escrever 15 ou 20 min, corrigir 12 ou 7 min, fechar 5 min. Total: 45 min. O relógio nunca muda de fase nem revela correções sozinho.
- Escrita no papel; notas, revisão e fotografias opcionais na aplicação. As três oficinas de escrita extensa incluem respostas exemplificativas; as restantes apresentam orientações de correção explicitamente identificadas. Não são classificações automáticas nem critérios oficiais.
- Reciclagem das fichas M1–M9, sobretudo da revisão integrada em M1-F19/F20, M4-F25/F26/F27 e M7-F35/F36. Os antigos endereços de `revisao-m147` são redirecionamentos. Não se criou uma segunda cópia dessas páginas.
- Perguntas que dependiam de rótulos ou instruções de outra ficha foram reformuladas. O aquecimento permite consultar a leitura; duas perguntas de um banco de três, com alternativas baralhadas e opção de renovar. A verificação final recupera uma pergunta para consolidação.
- As opções curriculares são assinaladas (por exemplo, Auto da Feira, outras prosas românticas, A Ilustre Casa de Ramires, outros contos e O Ano da Morte de Ricardo Reis). Este primeiro conjunto não é um banco exaustivo para todas as alternativas.
- Referencial consultado: Informação-Prova 639 de 2026 e AE de Português disponibilizadas pela DGE. Não se certificam regras de exame de 2027. As fontes oficiais estão ligadas na área «Programa e fontes».
- Textos protegidos não foram novamente transcritos: as sessões remetem para as leituras existentes. O dossiê conserva o enunciado, a correção e as referências; não promete conter offline todos os textos de apoio.

## Dossiê

IndexedDB própria, sem conta ou envio a um servidor. Até quatro JPEG/PNG/WebP por sessão, 8 MiB por fotografia, 64 MiB no total. Verificação de formato e assinatura. Sem OCR ou avaliação automática de manuscritos. Exportação HTML autónoma, legível, com imagens incorporadas e dados para recuperação. Importação validada e transacional, preservando registos mais recentes. Cópia exportada recomendada: apagar os dados do navegador pode eliminar os registos locais.

O modo de projeção omite notas, fotografias e acesso ao dossiê, incluindo quando se tenta abrir diretamente a sua rota. Não oferece isolamento contra alguém com acesso físico ao navegador: a proteção é de apresentação em sala.

## Executado em 19-10-2026

- Validação das 26 sessões: identificadores, alternativas, respostas e explicações, duração total, tempo de escrita, existência dos destinos locais. 104 itens contando as verificações finais de recuperação.
- Sintaxe dos dois programas partilhados; 19 testes específicos do dossiê: campos inseguros, formato de imagens, limites, preservação de fotografias, escapagem HTML/JSON, exportação/importação binária, importação inválida sem alteração parcial, datas e CSP. Os testes automatizados usam duplos de IndexedDB e DOMParser; não substituem os testes reais seguintes.
- Navegador real: abertura das 26 tarefas de escrita, relógios iniciais e revelação das 26 correções com perguntas interativas.
- Sessão 01: percurso pelas cinco fases; uma resposta certa e outra errada; feedback e respostas persistidos após recarregar; iniciar/pausar e recuperar relógio; notas guardadas e fotografia JPEG adicionada.
- Exportação real e recuperação numa origem de teste vazia (`localhost` → `127.0.0.1`), com nota, enunciado e fotografia; leitura da exportação autónoma e imagem incorporada. Rejeição real de ficheiro com extensão PNG mas assinatura JPEG.
- Pesquisa por Saramago: um resultado correto. Cartaz de entrada clicável e verificação visual em ecrã estreito (322 píxeis CSS): sem transbordo horizontal do catálogo. Mapa atualizado.
- Projeção real: sessão 19, passagem de aquecimento para escrita, QR e ligação do aluno atualizados com a fase; três controlos de tamanho selecionáveis; ausência do dossiê pessoal no modo projetado.

## Limites e verificações complementares pendentes

Não foram realizados: aula completa cronometrada com alunos; leitor de ecrã; Safari/iOS e Firefox; impressão física e paginação de todas as sessões; ensaio real com quota de armazenamento esgotada; medição formal de desempenho; leitura de QR por câmara física. A compatibilidade foi verificada no navegador disponível, não em todos os dispositivos. Não se declara o conjunto como cobertura exaustiva de todas as alternativas ou de todos os descritores gramaticais. O aprofundamento editorial de respostas exemplificativas pode continuar por pequenos lotes.

Não foram modificadas fichas dos módulos nem ficheiros do LENTE neste incremento.
