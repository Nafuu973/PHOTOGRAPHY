// Affiche la barre de réservation fixe (téléphone) dès que le bouton principal
// est passé au-dessus de l'écran. Sans JavaScript, la barre reste masquée.
(function () {
  "use strict";
  var heroCta = document.getElementById("cta-principal");
  var bar = document.querySelector(".cta-bar");
  if (!heroCta || !bar) return;

  var pending = false;
  function update() {
    pending = false;
    var passed = heroCta.getBoundingClientRect().bottom < 0;
    bar.classList.toggle("is-visible", passed);
    bar.setAttribute("aria-hidden", passed ? "false" : "true");
  }
  window.addEventListener("scroll", function () {
    if (!pending) { pending = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  update();
})();
