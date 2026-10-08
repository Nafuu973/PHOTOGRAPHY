// Bouton « Imprimer / Enregistrer en PDF » commun aux documents.
(function () {
  "use strict";
  var btn = document.querySelector('[data-action="print"]');
  if (btn) btn.addEventListener("click", function () { window.print(); });
})();
