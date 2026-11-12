// Affiche la barre de réservation fixe uniquement quand le bouton principal
// n'est plus visible à l'écran. Sans JavaScript, la barre reste masquée.
(function () {
  "use strict";
  var heroCta = document.getElementById("cta-principal");
  var bar = document.querySelector(".cta-bar");
  if (!heroCta || !bar || !("IntersectionObserver" in window)) return;

  new IntersectionObserver(function (entries) {
    var hidden = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
    bar.classList.toggle("is-visible", hidden);
    bar.setAttribute("aria-hidden", hidden ? "false" : "true");
  }).observe(heroCta);
})();
