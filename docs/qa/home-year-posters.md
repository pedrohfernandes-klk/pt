# Português: cartazes dos três anos

Baseline `5f91350a6b40db13becf9e9d5b8f39dd6bbd43c8`. Primeiro incremento visual restrito à página inicial e uma folha CSS exclusiva, coerente com a composição editorial do LENTE. Sem alterações às lições, exercícios ou páginas dos módulos.

## Alterações

Três cabeçalhos de ano com perguntas, desenhos tipográficos e cores papel, azul e carvão. Mantidos título, fontes, símbolos dos nove módulos, acesso direto a cada módulo, continuação, progresso e ferramentas de guardar/repor. Alturas mínimas flexíveis, sem cortar texto nem alturas máximas. Sem novas imagens, fontes, bibliotecas ou JavaScript.

Corrigido o destino «Aquecimentos de cinco minutos»: `#experimentar-aquecer` corresponde agora à coleção dos quinze aquecimentos no LENTE. A âncora anterior `#aquecimentos` identifica atualmente as oficinas. Todas as restantes ligações permanecem.

## Validação executada

- Comparação automática e revisão independente: seis scripts e nove linhas de módulos byte a byte idênticos; IDs e atributos de progresso preservados; secção de progresso idêntica; sem IDs duplicados nem ligações aninhadas. Única alteração de destino de navegação: correção dos aquecimentos acima.
- Navegador real a larguras CSS confirmadas de 320, 390, 768 e 1440 px: sem overflow; alvos de ano/módulo com pelo menos 65,9 px de altura. Inspeção visual em computador e telemóvel. Capturas antes/depois guardadas localmente.
- Estado real local comparado antes/depois: mesmas nove contagens, mesmo registo do aparelho e mesma continuação para M3-F18. Não alterado o armazenamento do utilizador no site público.
- Teclado: foco visível no acesso M7, com contorno mostarda sobre carvão. Contrastes calculados para texto/fundo: 14,69:1, 11,82:1 e 13,93:1; foco/fundo: 4,91:1, 5,72:1 e 7,94:1. Cores dos cartazes definidas explicitamente, independentes do esquema do sistema.
- Sem erros/avisos de consola no teste local. Sem alterações ao motor ou mecanismos dos exercícios.

## Pendências complementares

Não executados: leitor de ecrã real, dispositivos físicos, zoom do navegador a 200%, troca real do esquema escuro do sistema e benchmark de desempenho. Refluxo testado até 320 px, contrastes verificados, mas esses testes não são equivalentes a uma certificação completa de acessibilidade. Não repetidos integralmente os exercícios preservados nem exportação/importação do progresso, cujo código é idêntico. Verificação do deployment e navegação pública registadas no PR após publicação.
