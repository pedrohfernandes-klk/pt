# Português — fase 0: baseline verificável

Data: 18 de outubro de 2026.
Repositório exclusivo: pedrohfernandes-klk/pt.
Branch de origem: main.
SHA auditado: 96cdb520fcf118ef555ef2e325ce93465836c9ea.

## Inventário

Foram encontradas 100 páginas de lição em m1–m9, pelo padrão
mN/licao-*/index.html: 12, 8, 11, 15, 11, 9, 17, 10 e 7.
Este critério não contabiliza painéis, provas, percursos ou outros recursos como lições.
O inventário JSON regista caminho, título, tamanho e SHA-256 de cada página.
Não foram encontrados testes, manifesto de dependências ou workflows na baseline.

## Verificação reproduzível

Executar `python scripts/audit_lessons.py` com Python 3.11+ e Node.js.
O comando valida contagens, correspondência do módulo, UTF-8, título,
idioma pt-PT e sintaxe dos scripts JavaScript incorporados nas 100 lições.
A contagem esperada deve ser revista explicitamente quando forem acrescentadas lições.
Os hashes são evidência de preservação nesta fase, não uma proibição de futuras melhorias.

Limites: esta verificação não executa interações nem valida respostas pedagógicas,
navegação, armazenamento, acessibilidade ou apresentação no navegador.
Testes funcionais e visuais NÃO EXECUTADOS: bloqueiam aprovação para publicação.

## Sequência proposta, sujeita aos relatórios anteriores

1. Fixar a baseline e os critérios de verificação (este PR, sem alterar o site).
2. Confrontar os relatórios anteriores com os conteúdos atuais e construir uma matriz
   de competências, exercícios, avaliação e acessibilidade por módulo.
3. Corrigir problemas confirmados em PRs pequenos; executar testes funcionais e
   visuais para cada alteração antes de a considerar pronta.
4. Introduzir lições apenas para lacunas demonstradas e com ligações no percurso,
   objetivos, prática, feedback e revisão. Cerca de 120 é uma referência, não uma quota.
5. Otimizar recursos apenas após medir duplicação e peso, preservando conteúdo,
   comportamento, variedade e caminhos existentes.

O resumo da conversa recebido não contém a auditoria detalhada nem as decisões
anteriores. Esses documentos continuam necessários para executar as fases pedagógicas
sem inventar decisões. A menor contagem de um módulo não prova uma lacuna curricular.

Não fazer merge, publicar ou alterar o repositório LENTE nesta fase.
LENTE só poderá começar após conclusão e aprovação explícita do Português.

