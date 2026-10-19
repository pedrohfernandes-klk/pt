# Português — arquitetura de aprendizagem real

**Estado:** especificação editorial e piloto estrutural. **Âmbito:** nove módulos; primeira concretização documentada na Unidade 1 do M2. Não constitui avaliação de eficácia, reconstrução dos motores ou aprovação de publicação.

## 1. Contrato de aprendizagem

Cada lição continua a ser uma lição normal, com identidade, leitura e exercícios próprios. A ligação à seguinte nasce do **conhecimento necessário**, não de um separador «ponte». A unidade tem uma pergunta orientadora; cada ficha resolve uma parte dessa pergunta, conserva o seu objeto e deixa uma questão pronta para a próxima.

Uma lição pode combinar oito ou nove **momentos didáticos** (não oito ou nove ecrãs obrigatórios):

1. **Situar:** um problema reconhecível, uma passagem ou um objeto; introduzir o vocabulário indispensável.
2. **Observar:** encontrar indícios no texto, na imagem ou na fala; distinguir observar de concluir.
3. **Arriscar uma hipótese:** responder antes de receber a explicação completa, quando a dificuldade o permite.
4. **Ler com apoio:** disponibilizar excerto, contexto e esclarecimentos para rever a primeira hipótese.
5. **Relacionar:** pôr em contacto elementos do mesmo texto ou de textos diferentes.
6. **Testar:** exercício com alternativas plausíveis, não apenas eliminação de absurdos.
7. **Explicar e corrigir:** feedback que aponta o indício relevante, a confusão e o caminho de revisão.
8. **Transferir:** pequeno caso novo, reescrita, comparação ou aplicação fora do exemplo treinado.
9. **Retomar:** síntese curta e pergunta que reaparece numa lição posterior.

A ordem varia conforme a obra e o objetivo. Os momentos podem fundir-se; a leitura pode ser o centro da lição. Evitar ecrãs adicionais só para «cumprir etapas». Nem todas as respostas têm de ser fechadas, nem todo o progresso tem de ocorrer no dispositivo.

## 2. Quatro níveis distintos de evidência

- **Exposição:** o aluno viu ou leu o conteúdo. Nunca equivale, por si só, a aprendizagem.
- **Execução:** o aluno resolveu uma tarefa; um acerto automático comprova apenas o acerto nessa tarefa.
- **Compreensão fundamentada:** o aluno explica uma relação e indica um indício pertinente. Pode exigir observação do professor ou resposta não automatizada.
- **Transferência e retenção:** o aluno aplica a ideia a outro material e volta a mobilizá-la mais tarde, sem repetir mecanicamente o mesmo exemplo.

**Não converter estes níveis numa classificação automática.** Manter pontuação, selos e progresso existentes como indicadores operacionais; nunca lhes chamar «domínio adquirido» sem evidência independente. O professor pode observar discussão, leitura oral, produção em papel A6 ou escrita no portefólio. O aluno pode rever autonomamente no telemóvel sem ficar obrigado a escrever no ecrã.

## 3. Feedback e variedade que ensinam

Um bom erro revela uma hipótese plausível: troca de narrador e autor, de opinião e facto, de causa e consequência, de forma e função. O feedback deve dizer **o que observar**, **por que a resposta falhou** e, quando adequado, **o que mudar**. Usar o campo «fe» do motor atual para erros específicos em escolhas pertinentes; preservar «f» como explicação geral. Evitar repetir uma definição ou oferecer logo a resposta antes da nova tentativa.

A variação entre tentativas deve manter o **mesmo objetivo cognitivo** e pré-requisitos equivalentes. Uma pergunta alternativa «p2» que só muda palavras não demonstra variedade efetiva. O historial serve para evitar repetições inúteis; o tempo decorrido, os cliques, os pontos e a conclusão não servem como medida isolada de compreensão.

## 4. Unidade 1 do Módulo 2 — piloto sem fichas novas

A unidade já contém três fichas (m2-f01, m2-f02, m2-f07). O mapa editorial verificável encontra-se em docs/pedagogia/m2-u1-progressao.json.

| Lição | O aluno parte de… | Deve passar a conseguir… | Prepara… |
| --- | --- | --- | --- |
| F01, *Deram-lhe um provérbio* | uma rubrica e o provérbio | separar representação, ação, fala e didascália; identificar um indício da encomenda | compreender quem fala e de quem se fala |
| F02, *Inês, como panela sem asa* | o monólogo e o diálogo com a Mãe | interpretar imagens e conflito sem confundir acusação da Mãe com facto textual | analisar como as falas organizam relações |
| F07, *Orações em cena* | frases de cenas já lidas | distinguir relações entre orações no contexto e justificar a classificação | ler escolhas e consequências no desenvolvimento da farsa |

**Intervenção editorial futura, e não executada neste lote:** incorporar uma pergunta curta de retoma no início de F02 e F07, uma transferência num excerto novo no fim de F07 e feedback específico para distratores plausíveis de F01/F02. Não acrescentar lições por quota; rever primeiro a qualidade e distribuição de tarefas existentes. Preservar desafios, URLs, chaves de progresso, imagens licenciadas e encaminhamentos.

## 5. Arquitetura técnica mínima

**Conteúdo → motor existente → evidência → continuidade.** Não criar um segundo renderizador, uma plataforma de conteúdos, um backend, um perfil individual ou uma base de dados central. Continuar a usar assets/pt-lessons/casca.js, jogo.js e lesson.css; dados CARTOES nas fichas atuais. O manifesto do piloto é documentação de progressão pedagógica e **não é carregado no navegador**.

A verificação «python scripts/audit_learning_progression.py» percorre os bancos atuais e identifica erros estruturais, quantidade de leituras e atividades, uso de feedback individual e formulações alternativas. Confirma ainda que as três referências do piloto existem e possuem objetivo, evidência, equívoco, transferência e continuidade. Os resultados são *sinais de revisão*, não notas de qualidade pedagógica.

## 6. Extensão aos nove módulos, por lotes pequenos

Primeiro, fechar o piloto F01→F02→F07 com revisão de enunciados e uma observação em aula. Depois, escolher **uma unidade com carência efetiva** noutro módulo e mapear a mesma cadeia: pré-requisito, objeto, indício, equívoco, aplicação, retoma. Só criar ficha quando houver uma aprendizagem relevante ausente — não quando uma subsecção tem menos cartões ou a contagem parece desigual.

Em cada alteração: registar os IDs e chaves inalterados, rever a fonte e os direitos de imagens/textos, comparar percurso e respostas antes/depois, testar teclado, mobile e projeção, confirmar feedback certo/errado e persistência. Leitor de ecrã real, Safari/iOS, aula com alunos e retenção posterior exigem validação específica; não podem ser substituídos por testes de sintaxe.

**Princípio de design:** cartazes minimalistas/brutalistas como entrada visual, mas sem ruído funcional. A hierarquia visual deve tornar visíveis pergunta, excerto, tarefa e explicação. O valor didático está na operação pedida ao aluno, não no número de animações, cliques ou componentes.
