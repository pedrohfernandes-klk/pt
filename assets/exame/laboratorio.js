/* Laboratório de respostas (Oficina da palavra): quatro máquinas de treino formativo.
   Estado em memória enquanto a página está aberta; nada é guardado no aparelho.
   O relógio é estado de cada exercício: revelar apoios não o reinicia; mudar de máquina põe-no em pausa. */
(function () {
  'use strict';

  const TEXTS = [
    {
      title: 'A biblioteca aberta',
      lines: ['A biblioteca passou a fechar duas horas mais tarde.', 'No primeiro mês, as mesas encheram-se de alunos que antes estudavam no corredor.', 'O edifício manteve a fachada azul.', 'A direção decidiu prolongar a experiência por mais um período.'],
      prompt: 'Explica de que modo o alargamento do horário respondeu a uma necessidade dos alunos, fundamentando a resposta no texto.',
      parts: [['verbo', 'Explica'], ['objeto', 'de que modo o alargamento do horário respondeu a uma necessidade dos alunos'], ['condicao', 'fundamentando a resposta no texto']],
      command: ['Explicar a relação entre a medida e a necessidade, apoiando-a no texto.', 'Enumerar as cores do edifício.', 'Dar uma opinião sobre todas as bibliotecas.'],
      evidence: 1,
      why: 'A linha 2 mostra a utilização das mesas por alunos que antes estudavam no corredor: é uma consequência concreta da medida. A cor da fachada não explica a necessidade.',
      hint: 'Procura uma mudança nas condições de estudo, e não apenas uma informação verdadeira.',
      model: 'O alargamento do horário deu aos alunos acesso a um espaço adequado para estudar durante mais tempo. As mesas passaram a ser ocupadas por quem antes estudava no corredor (linha 2), o que mostra a necessidade de espaço e de acesso à biblioteca.',
      weak: 'A biblioteca era azul e ficou aberta. Eu gosto de bibliotecas porque têm muitos livros.',
      marks: [['A biblioteca era azul', 'verdadeiro, mas irrelevante para a necessidade'], ['Eu gosto de bibliotecas porque têm muitos livros.', 'opinião pessoal: desvia do pedido']],
      missing: 'Falta a informação decisiva da linha 2.',
      review: 'A resposta menciona a medida, mas não explica a necessidade dos alunos nem mobiliza a informação decisiva da linha 2. A opinião pessoal e a cor da fachada desviam o foco. Uma redação sem erros não compensa esta insuficiência de conteúdo.',
      reviewCED: 'Não explica a necessidade dos alunos nem usa a linha 2; a opinião e a cor da fachada desviam o foco.',
      reviewCL: 'Sem erros relevantes. Uma redação correta não compensa a insuficiência de conteúdo.',
      targets: ['Explicar o acesso a um espaço adequado durante mais tempo.', 'Relacionar a ocupação das mesas com o estudo anterior no corredor (linha 2).']
    },
    {
      title: 'O regresso',
      lines: ['Ao chegar à aldeia, Leonor abrandou o passo diante da antiga escola.', 'Trazia na mala o contrato de trabalho que a levaria para longe na manhã seguinte.', 'A porta estava fechada; no vidro, reconheceu a marca que deixara em criança.', 'Sorriu, mas demorou a afastar a mão da maçaneta.'],
      prompt: 'Explica a ambivalência de Leonor no momento do regresso, relacionando dois elementos do texto.',
      parts: [['verbo', 'Explica'], ['objeto', 'a ambivalência de Leonor no momento do regresso'], ['condicao', 'relacionando dois elementos do texto']],
      command: ['Explicar sentimentos em tensão, relacionando dois elementos do texto.', 'Recontar a infância de Leonor sem recorrer ao texto.', 'Identificar apenas o local da ação.'],
      evidence: 3,
      why: 'O sorriso e a demora em afastar a mão (linha 4) sustentam uma leitura de afeto e dificuldade em partir. O contrato (linha 2) permite relacionar essa ligação ao passado com a partida iminente. A porta fechada, isoladamente, não prova rejeição.',
      hint: 'Relaciona a partida anunciada com os gestos finais; evita inventar acontecimentos da infância.',
      model: 'Leonor manifesta afeto pelo lugar da infância, visível no sorriso ao reconhecer a sua marca na escola. Ao mesmo tempo, a demora em afastar a mão sugere dificuldade em se despedir, num momento em que o contrato de trabalho anuncia uma partida iminente (linhas 2–4).',
      weak: 'Leonor voltou para a aldeia porque perdeu o emprego. A escola recusou a sua entrada e ela ficou zangada.',
      marks: [['porque perdeu o emprego', 'inventado: o texto fala de um contrato de trabalho'], ['A escola recusou a sua entrada', 'inventado: a porta fechada não prova recusa'], ['ela ficou zangada', 'sem apoio: o texto mostra um sorriso']],
      missing: 'Falta o afeto e a dificuldade da despedida (linhas 2 a 4).',
      review: 'A resposta inventa a perda do emprego e a recusa da escola. O texto anuncia um contrato e não sustenta a zanga. É necessário reconhecer o afeto e a dificuldade da despedida, relacionando os gestos finais com a partida.',
      reviewCED: 'Inventa a perda do emprego e a recusa da escola; não reconhece o afeto nem a dificuldade da despedida.',
      reviewCL: 'A redação está correta: o problema é de conteúdo, não de língua.',
      targets: ['Reconhecer o afeto pela escola e a dificuldade da despedida nos gestos de Leonor.', 'Relacionar esses gestos com a partida iminente anunciada pelo contrato (linhas 2–4).']
    }
  ];

  const MACHINES = [
    { name: 'Descobre o que te pedem', verb: 'Pensa', operation: 'Lê a instrução antes de responder: o que fazer, sobre quê e em que condição.' },
    { name: 'Prova ou distração?', verb: 'Prova', operation: 'Uma frase verdadeira pode não provar nada. Escolhe a que sustenta a leitura.' },
    { name: 'Responde em quatro linhas', verb: 'Responde', operation: 'Responde com o essencial. Quatro linhas são uma meta de treino, não uma regra do exame.' },
    { name: 'Sê o corretor', verb: 'Revê', operation: 'Lê uma resposta como quem corrige: o que falha, porquê e como melhorar.' }
  ];
  const PART_LABEL = { verbo: 'verbo de comando', objeto: 'objeto', condicao: 'condição' };
  const REVEAL_LABEL = ['Revelar pista', 'Revelar proposta de resposta', 'Revelar critérios de revisão', 'Apoios revelados'];
  const SUPPORT_TITLE = ['Pista', 'Uma resposta possível', 'Autoavaliação · adaptação didática de C-ED e CL'];
  const TIME = 120;

  const host = document.querySelector('#exercise');
  const select = document.querySelector('#texto');
  const notice = document.querySelector('#of-aviso');
  let machine = 0;
  let projection = new URL(location.href).searchParams.get('projetar') === '1';
  let ticker = null;

  const fresh = () => ({ answer: '', selected: null, checked: [], stage: 0, feedback: false, rest: TIME, end: null });
  const states = TEXTS.map(() => MACHINES.map(fresh));

  const esc = v => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const text = () => TEXTS[Number(select.value)];
  const state = () => states[Number(select.value)][machine];
  const correctAnswer = () => (machine === 0 ? 0 : machine === 1 ? text().evidence : 1);
  const say = message => { notice.textContent = ''; window.setTimeout(() => { notice.textContent = message; }, 30); };

  /* ---------- relógio: estado do exercício ---------- */
  const remaining = s => (s.end ? Math.max(0, Math.ceil((s.end - Date.now()) / 1000)) : s.rest);
  const clockText = seconds => String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(seconds % 60).padStart(2, '0');
  function pauseClock(s, announce) {
    if (!s.end) return;
    s.rest = remaining(s);
    s.end = null;
    if (announce) say('Relógio em pausa: ' + clockText(s.rest) + '.');
  }
  function paintClock() {
    const s = state(), clock = host.querySelector('#clock'), button = host.querySelector('#timer');
    if (!clock) return;
    const seconds = remaining(s);
    clock.textContent = clockText(seconds);
    clock.classList.toggle('of-relogio-fim', seconds === 0);
    if (button) button.textContent = s.end ? 'Pausar' : (s.rest < TIME && s.rest > 0 ? 'Continuar' : 'Iniciar');
    if (s.end && seconds === 0) { s.rest = 0; s.end = null; say('Terminou o tempo de treino.'); paintClock(); }
  }
  function startTicker() {
    window.clearInterval(ticker);
    ticker = window.setInterval(paintClock, 250);
  }

  /* ---------- peças de composição ---------- */
  function promptHTML(t, annotated) {
    let html = esc(t.prompt);
    if (!annotated) return html;
    t.parts.forEach(([kind, piece]) => {
      html = html.replace(esc(piece), '<span class="of-parte" data-parte="' + kind + '"><span class="of-parte-rotulo">' + PART_LABEL[kind] + '</span>' + esc(piece) + '<span class="of-so-leitor"> (' + PART_LABEL[kind] + ')</span></span>');
    });
    return html;
  }
  function instruction(t, annotated) {
    return '<div class="of-instrucao"><p class="of-rotulo">Instrução</p><p class="writing-task" id="of-pedido-texto">' + promptHTML(t, annotated) + '</p></div>';
  }
  function heading(t) {
    return '<p class="of-estatuto">Formativo · texto e tarefas autorais · PT, 2026</p><h3 class="of-texto-titulo">' + esc(t.title) + '</h3>';
  }
  function reading(t, s, after) {
    if (machine === 1) {
      return '<section class="of-leitura" aria-label="Texto: escolhe a linha que prova">' + heading(t) + '<div class="choices of-linhas" role="group" aria-label="Linhas do texto">' +
        t.lines.map((l, i) => '<button class="choice of-linha" data-answer="' + i + '" aria-pressed="' + (s.selected === i) + '"><span class="of-ref">L' + (i + 1) + '</span><span class="of-linha-texto">' + esc(l) + '</span></button>').join('') + '</div>' + after + '</section>';
    }
    let html = '<section class="of-leitura" aria-label="Texto">' + heading(t) + '<ol class="lab-text of-linhas">' + t.lines.map((l, i) => '<li><span class="of-ref" aria-hidden="true">L' + (i + 1) + '</span><span class="of-linha-texto">' + esc(l) + '</span></li>').join('') + '</ol>';
    if (machine === 3) html += '<div class="of-prova"><p class="of-rotulo">Resposta em revisão <span>(inventada para treino)</span></p><blockquote class="model of-prova-texto" id="of-prova">' + weakHTML(t, s.feedback) + '</blockquote></div>';
    return html + '</section>';
  }
  function weakHTML(t, marked) {
    let html = esc(t.weak);
    if (!marked) return html;
    t.marks.forEach(([piece, note], i) => {
      html = html.replace(esc(piece), '<mark class="of-marca">' + esc(piece) + '</mark><span class="of-nota" data-n="' + (i + 1) + '"><span class="of-so-leitor">Nota de revisão: </span>' + esc(note) + '</span>');
    });
    return html + '<span class="of-falta">' + esc(t.missing) + '</span>';
  }
  function choicesHTML(options, s) {
    return '<div class="choices of-escolhas">' + options.map((v, i) => '<button class="choice" data-answer="' + i + '" aria-pressed="' + (s.selected === i) + '"><span class="of-letra" aria-hidden="true">' + 'ABC'[i] + '</span><span>' + esc(v) + '</span></button>').join('') + '</div>';
  }
  function checks(t) {
    return t.targets.map(x => 'C-ED · ' + x).concat(['C-ED · Encadeei as ideias com clareza e sem informação irrelevante.', 'CL · Revi sintaxe, léxico, pontuação, ortografia e referências ao texto.']);
  }
  function checksHTML(t, s) {
    return '<div class="lab-checks">' + checks(t).map((c, i) => '<label><input type="checkbox" data-check="' + i + '"' + (s.checked.includes(i) ? ' checked' : '') + '><span>' + esc(c) + '</span></label>').join('') + '</div>';
  }
  function feedbackHTML() {
    const t = text(), s = state();
    if (s.selected === null) return '';
    const right = s.selected === correctAnswer();
    const head = '<p class="of-veredito"><span class="of-sinal" aria-hidden="true">' + (right ? '✓' : '↺') + '</span>' + (right ? 'Escolha adequada. ' : 'Revê a escolha. ') + '</p>';
    if (machine === 0) return head + '<p>O verbo exige explicar: relaciona os elementos pedidos e fundamenta a interpretação. Não basta localizar informação.</p><p class="of-nota-instrucao">A instrução ficou anotada: verbo de comando, objeto e condição.</p>';
    if (machine === 1) return head + '<p>' + esc(t.why) + '</p>';
    return head + '<p>' + esc(t.review) + '</p><dl class="of-eixos"><div><dt>Conteúdo · C-ED</dt><dd>' + esc(t.reviewCED) + '</dd></div><div><dt>Língua · CL</dt><dd>' + esc(t.reviewCL) + '</dd></div></dl>';
  }
  function responseHTML(t, s) {
    if (machine === 0) return '<p class="of-pergunta">Qual é o trabalho que a instrução exige?</p>' + choicesHTML(t.command, s);
    if (machine === 1) return '<p class="of-pergunta">Escolhe, no texto, a linha que dá apoio mais direto à interpretação pedida. Depois explica oralmente a ligação.</p>';
    if (machine === 2) {
      return '<p class="of-pergunta">Escreve uma resposta breve, em papel ou no campo abaixo. Quatro linhas são uma meta de concisão; o campo não limita a extensão.</p>' +
        '<div class="lab-actions of-relogio"><div><span class="of-rotulo">Tempo de treino</span><output class="lab-timer" id="clock" aria-label="Tempo restante">' + clockText(remaining(s)) + '</output></div><button id="timer">Iniciar</button><button id="reset">Repor tempo</button></div>' +
        '<label class="field-label personal" for="answer">A tua resposta · fica apenas nesta página enquanto estiver aberta</label><textarea id="answer" class="of-caderno" maxlength="6000" rows="6">' + esc(s.answer) + '</textarea>' +
        '<p class="small personal">Não há classificação automática. Compara a tua resposta com os critérios e revê-a.</p>' +
        '<section class="of-revisao" data-apoio-local="3"' + (s.stage < 3 ? ' hidden' : '') + '><h3 tabindex="-1">' + SUPPORT_TITLE[2] + '</h3><p>Assinala apenas o que consegues demonstrar na tua resposta; reescreve o que falta. Esta lista não produz uma nota de exame.</p>' + checksHTML(t, s) + '<a href="#fontes">Consultar a fundamentação oficial</a></section>';
    }
    return '<p class="of-pergunta">Avalia a resposta em revisão antes de consultar o comentário.</p>' +
      choicesHTML(['Cumpre o pedido e fundamenta a interpretação.', 'Precisa de revisão do conteúdo e da fundamentação.'], s) +
      '<label class="field-label personal" for="answer">Justifica a tua decisão e propõe uma melhoria.</label><textarea id="answer" maxlength="6000" rows="5">' + esc(s.answer) + '</textarea>';
  }
  function supportsHTML(t, s) {
    const steps = [0, 1, 2].map(i => '<span class="of-passo' + (s.stage > i ? ' feito' : '') + '"></span>').join('');
    let html = '<section class="of-apoios" aria-label="Apoios"><div class="lab-actions of-apoios-barra"><button id="reveal"' + (s.stage === 3 ? ' disabled' : '') + '>' + REVEAL_LABEL[s.stage] + '</button><span class="of-passos" aria-hidden="true">' + steps + '</span><span class="of-so-leitor" id="of-passos-texto">' + s.stage + ' de 3 apoios revelados</span><button id="restart" class="of-discreto">Recomeçar esta máquina</button></div>';
    html += '<div class="of-apoios-grelha"><section class="lab-hint" data-apoio="1"' + (s.stage < 1 ? ' hidden' : '') + '><h3 tabindex="-1">Pista</h3><p>' + esc(t.hint) + '</p></section>';
    html += '<section data-apoio="2"' + (s.stage < 2 ? ' hidden' : '') + '><h3 tabindex="-1">Uma resposta possível</h3><p class="model">' + esc(t.model) + '</p><p class="small">Outras formulações válidas são possíveis. Confirma o conteúdo no texto.</p></section>';
    if (machine !== 2) html += '<section data-apoio="3"' + (s.stage < 3 ? ' hidden' : '') + '><h3 tabindex="-1">' + SUPPORT_TITLE[2] + '</h3><p>Assinala apenas o que consegues demonstrar na tua resposta; reescreve o que falta. Esta lista não produz uma nota de exame.</p>' + checksHTML(t, s) + '<a href="#fontes">Consultar a fundamentação oficial</a></section>';
    return html + '</div></section>';
  }

  /* ---------- composição completa (só ao mudar de texto ou de máquina, ou ao recomeçar) ---------- */
  function render(focus) {
    const t = text(), s = state(), m = MACHINES[machine];
    document.body.dataset.maquina = String(machine);
    document.querySelectorAll('[data-machine]').forEach(b => {
      if (Number(b.dataset.machine) === machine) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
    });
    const verify = machine !== 2 ? '<div class="lab-actions"><button id="verify" class="of-primario"' + (s.selected === null ? ' disabled' : '') + '>Verificar escolha</button></div>' : '';
    const feedback = '<div id="feedback" class="lab-feedback" role="status"' + (s.feedback ? '' : ' hidden') + '>' + (s.feedback ? feedbackHTML() : '') + '</div>';
    host.innerHTML =
      '<header class="of-ex-cabeca"><p class="of-ex-num" aria-hidden="true"><span>Nº</span>0' + (machine + 1) + '</p><div><h2 tabindex="-1">' + m.name + '</h2><p class="of-operacao">' + m.operation + '</p></div></header>' +
      '<div class="of-mesa" data-maquina="' + machine + '">' + reading(t, s, machine === 1 ? '<div class="of-resposta">' + verify + feedback + '</div>' : '') +
      '<section class="of-acao" aria-label="Tarefa">' + instruction(t, machine === 0 && s.feedback) + '<div class="of-resposta">' + responseHTML(t, s) + (machine === 1 ? '' : verify + feedback) +
      '</div></section></div>' +
      supportsHTML(t, s);
    bind();
    paintClock();
    if (focus) host.querySelector('h2').focus();
  }

  /* ---------- atualizações parciais: não apagam texto, tempo nem foco ---------- */
  function updateSelection() {
    const s = state();
    host.querySelectorAll('[data-answer]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.answer) === s.selected)));
    const verify = host.querySelector('#verify');
    if (verify) verify.disabled = s.selected === null;
    s.feedback = false;
    const f = host.querySelector('#feedback');
    f.hidden = true; f.innerHTML = '';
    host.querySelectorAll('[data-answer]').forEach(b => b.classList.remove('correct', 'incorrect'));
    if (machine === 0) host.querySelector('#of-pedido-texto').innerHTML = promptHTML(text(), false);
    if (machine === 3) host.querySelector('#of-prova').innerHTML = weakHTML(text(), false);
  }
  function showFeedback() {
    const s = state(), t = text();
    s.feedback = true;
    const f = host.querySelector('#feedback');
    f.innerHTML = feedbackHTML();
    f.hidden = false;
    const chosen = host.querySelector('[data-answer="' + s.selected + '"]');
    if (chosen) chosen.classList.add(s.selected === correctAnswer() ? 'correct' : 'incorrect');
    if (machine === 0) host.querySelector('#of-pedido-texto').innerHTML = promptHTML(t, true);
    if (machine === 3) host.querySelector('#of-prova').innerHTML = weakHTML(t, true);
  }
  function reveal() {
    const s = state();
    if (s.stage >= 3) return;
    s.stage++;
    const target = host.querySelector('[data-apoio="' + s.stage + '"]') || host.querySelector('[data-apoio-local="' + s.stage + '"]');
    target.hidden = false;
    const button = host.querySelector('#reveal');
    button.textContent = REVEAL_LABEL[s.stage];
    host.querySelectorAll('.of-passo').forEach((p, i) => p.classList.toggle('feito', s.stage > i));
    host.querySelector('#of-passos-texto').textContent = s.stage + ' de 3 apoios revelados';
    if (s.stage === 3) { button.disabled = true; }
    target.querySelector('h3').focus();
  }

  function bind() {
    const s = state();
    host.querySelectorAll('[data-answer]').forEach(b => { b.onclick = () => { s.selected = Number(b.dataset.answer); updateSelection(); }; });
    const answer = host.querySelector('#answer');
    if (answer) answer.oninput = () => { s.answer = answer.value; };
    const verify = host.querySelector('#verify');
    if (verify) verify.onclick = showFeedback;
    host.querySelector('#reveal').onclick = reveal;
    host.querySelector('#restart').onclick = () => {
      Object.assign(s, fresh());
      render(true);
      say('Máquina recomeçada: escolhas, apoios e relógio repostos.');
    };
    host.querySelectorAll('[data-check]').forEach(c => {
      c.onchange = () => {
        const i = Number(c.dataset.check);
        s.checked = s.checked.filter(x => x !== i);
        if (c.checked) s.checked.push(i);
      };
    });
    const timer = host.querySelector('#timer');
    if (timer) {
      timer.onclick = () => {
        if (s.end) { pauseClock(s, false); }
        else {
          if (s.rest === 0) s.rest = TIME;
          s.end = Date.now() + s.rest * 1000;
        }
        paintClock();
      };
      host.querySelector('#reset').onclick = () => { s.end = null; s.rest = TIME; paintClock(); };
    }
  }

  function leave() { pauseClock(state(), true); }

  /* ---------- projeção ---------- */
  function project() {
    document.body.classList.toggle('projected', projection);
    document.querySelector('#projetar').setAttribute('aria-pressed', String(projection));
  }
  project();
  document.querySelector('#projetar').onclick = () => { projection = !projection; project(); };

  select.onchange = () => {
    const previous = states[select.dataset.anterior ? Number(select.dataset.anterior) : 0][machine];
    pauseClock(previous, true);
    select.dataset.anterior = select.value;
    render(true);
  };
  select.dataset.anterior = select.value;
  document.querySelectorAll('[data-machine]').forEach(b => {
    b.onclick = () => {
      const next = Number(b.dataset.machine);
      if (next === machine) return;
      leave();
      machine = next;
      render(true);
    };
  });

  /* ---------- papel ---------- */
  function print(correction) {
    const t = text(), s = state(), m = MACHINES[machine];
    const task = machine === 0 ? '<p class="of-p-pedido">Qual é o trabalho que a instrução exige? Assinala e justifica.</p><ol type="A">' + t.command.map(c => '<li>' + esc(c) + '</li>').join('') + '</ol>'
      : machine === 1 ? '<p class="of-p-pedido">Escolhe a linha que melhor sustenta a interpretação e justifica.</p>'
        : machine === 3 ? '<p class="of-p-rotulo">Resposta em revisão (inventada para treino)</p><blockquote>' + esc(t.weak) + '</blockquote><p class="of-p-pedido">Avalia o conteúdo e a fundamentação. Justifica e melhora.</p>'
          : '<p class="of-p-pedido">Produz uma resposta breve. Quatro linhas são uma meta de treino.</p>';
    const supports = correction ? (s.feedback ? '<h2>Comentário à escolha</h2><p>' + esc(feedbackHTML().replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()) + '</p>' : '') +
      (s.stage >= 1 ? '<h2>Pista</h2><p>' + esc(t.hint) + '</p>' : '') +
      (s.stage >= 2 ? '<h2>Uma resposta possível</h2><p>' + esc(t.model) + '</p>' : '') +
      (s.stage >= 3 ? '<h2>Revisão formativa</h2><ul>' + checks(t).map(c => '<li>' + esc(c) + '</li>').join('') + '</ul>' : '') : '';
    document.querySelector('#print-sheet').innerHTML =
      '<header class="of-p-cabeca"><p>Laboratório de respostas · Português · treino formativo</p><p class="of-p-num">Nº 0' + (machine + 1) + '</p></header>' +
      '<h1>' + m.name + '</h1><p class="of-p-operacao">' + m.operation + '</p>' +
      '<section class="of-p-texto"><p class="of-p-rotulo">Texto · ' + esc(t.title) + '</p><ol>' + t.lines.map((l, i) => '<li><b>L' + (i + 1) + '</b>' + esc(l) + '</li>').join('') + '</ol></section>' +
      '<section class="of-p-instrucao"><p class="of-p-rotulo">Instrução</p><p>' + esc(t.prompt) + '</p></section>' + task +
      '<div class="answer-lines" aria-hidden="true"></div><p class="of-p-nome">Nome ______________________ Data ____ / ____</p>' + supports +
      '<p class="print-meta">Treino autoral (formativo). Referência: Prova 639, 2026, 1.ª fase, critérios definitivos, pp. 1–3. https://eduqa.pt/wp-content/uploads/2026/07/portugues_prova_639_cc.pdf</p>';
    window.print();
  }
  document.querySelector('#papel').onclick = () => print(false);
  document.querySelector('#solucoes').onclick = () => print(true);

  render(false);
  startTicker();
}());
