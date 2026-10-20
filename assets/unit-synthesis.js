(function () {
  "use strict";
  var script = document.currentScript;
  if (!script) return;
  var module = script.dataset.module;
  function read(key) {
    try { return JSON.parse(localStorage.getItem(key) || "null"); }
    catch (error) { return null; }
  }
  document.querySelectorAll("[data-sintese]").forEach(function (box) {
    var n = box.dataset.sintese;
    var key = "percurso-sintese-" + module + "-u" + n;
    var state = read(key);
    var register = box.querySelector("[data-sintese-registar]");
    var revise = box.querySelector("[data-sintese-rever]");
    var status = box.querySelector("[data-sintese-estado]");
    var choices = box.querySelectorAll('input[type="radio"]');
    var note = document.querySelector('[data-resp="' + n + '"]');
    // Preserve completion already earned under the previous writing criterion.
    // New notes never mark a synthesis complete without explicit confirmation.
    try {
      if (!state && !localStorage.getItem(key + "-inicializada")) {
        if (note && note.value.trim().split(/\s+/).filter(Boolean).length >= 80) {
          var previous = { feita: true, modo: "anterior" };
          localStorage.setItem(key, JSON.stringify(previous));
          state = previous;
        }
        localStorage.setItem(key + "-inicializada", "1");
      }
    } catch (error) { /* The optional note remains available even without storage. */ }
    function paint() {
      var done = !!(state && state.feita);
      choices.forEach(function (choice) {
        if (state && state.modo === choice.value) choice.checked = true;
        choice.disabled = done;
      });
      register.hidden = done;
      register.disabled = !box.querySelector('input[type="radio"]:checked');
      revise.hidden = !done;
      status.textContent = done ?
        (state.modo === "anterior" ? "Síntese anterior preservada. " :
          "Síntese registada: " + (state.modo === "oral" ? "oralmente. " : "no caderno. ")) +
          "Este registo não avalia a qualidade da resposta." :
        "Este registo indica a realização da atividade; não avalia a qualidade da resposta.";
    }
    function save(next) {
      try { localStorage.setItem(key, JSON.stringify(next)); }
      catch (error) {
        status.textContent = "Não foi possível guardar neste aparelho. A síntese pode ser feita na mesma; confirma o registo com o docente.";
        return;
      }
      state = next;
      paint();
      window.dispatchEvent(new Event("epi-sintese"));
      (next.feita ? revise : register).focus();
    }
    choices.forEach(function (choice) { choice.addEventListener("change", paint); });
    register.addEventListener("click", function () {
      var chosen = box.querySelector('input[type="radio"]:checked');
      if (chosen) save({ feita: true, modo: chosen.value });
    });
    revise.addEventListener("click", function () {
      save({ feita: false, modo: state ? state.modo : null });
    });
    paint();
  });
  window.dispatchEvent(new Event("epi-sintese"));
})();
