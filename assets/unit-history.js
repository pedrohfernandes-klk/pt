(function () {
  "use strict";
  var script = document.currentScript;
  if (!script) return;
  var module = script.dataset.module.toUpperCase();
  var stages = script.dataset.stages.split(",");
  var records = [];
  stages.forEach(function (stage) {
    try {
      var text = localStorage.getItem("percurso-" + module + "-u" + stage);
      var saved = localStorage.getItem("desafio-" + module + "-u" + stage);
      var challenge = saved ? JSON.parse(saved) : null;
      if ((text && text.trim()) || challenge) records.push({ stage: stage, text: text || "", challenge: challenge });
    } catch (error) { /* Storage may be unavailable; reading the page still works. */ }
  });
  if (!records.length) return;
  var box = document.createElement("details");
  box.className = "unit-previous";
  var summary = document.createElement("summary");
  summary.textContent = "As tuas respostas da organização anterior";
  box.appendChild(summary);
  var intro = document.createElement("p");
  intro.textContent = "Ficam disponíveis para retomares ideias. As novas unidades têm uma síntese e um desafio próprios; o progresso das lições mantém-se.";
  box.appendChild(intro);
  records.forEach(function (record) {
    var title = document.createElement("h3");
    title.textContent = "Registo anterior " + record.stage;
    var text = document.createElement("p");
    text.style.whiteSpace = "pre-wrap";
    text.textContent = record.text;
    box.appendChild(title);
    box.appendChild(text);
    if (record.challenge) {
      var score = document.createElement("p");
      score.textContent = "Desafio anterior: melhor " + (record.challenge.melhor || 0) +
        " de " + (record.challenge.total || 8) +
        ((record.challenge.ganho || record.challenge.vencido) ? "; selo ganho na organização anterior." : "; por concluir.");
      box.appendChild(score);
    }
  });
  var index = document.querySelector(".unit-index");
  if (index) index.insertAdjacentElement("afterend", box);
})();
