// Devis : lignes éditables et calcul automatique des totaux.
(function () {
  "use strict";

  var LIGNES_PAR_DEFAUT = [
    ["Couverture photo (préparation et prises de vue)", 1, 0],
    ["Sélection, retouche « cinéma » et galerie en ligne privée", 1, 0],
    ["Tirage(s) photo 10×15 cm", 1, 0],
    ["Frais de déplacement", 1, 0]
  ];
  var TAUX_TVA = 0.2;

  var tbody = document.getElementById("lines");
  var tvaBox = document.getElementById("tva");
  var pctInput = document.getElementById("pct");
  var $ = function (id) { return document.getElementById(id); };

  function euro(n) {
    return n.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
  }
  function nombre(input) {
    var v = parseFloat(input.value);
    return isFinite(v) && v > 0 ? v : 0;
  }
  function el(tag, attrs) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    return e;
  }

  function ajouterLigne(desc, qte, prix) {
    var tr = el("tr");

    var tdDesc = el("td");
    var champ = el("span", { "class": "f block", contenteditable: "", "data-ph": "Description" });
    champ.textContent = desc || "";
    tdDesc.appendChild(champ);

    var tdQte = el("td", { "class": "num" });
    var inQte = el("input", { type: "number", min: "0", step: "1", "aria-label": "Quantité" });
    inQte.value = qte == null ? 1 : qte;
    tdQte.appendChild(inQte);

    var tdPrix = el("td", { "class": "num" });
    var inPrix = el("input", { type: "number", min: "0", step: "0.01", "aria-label": "Prix unitaire en euros" });
    inPrix.value = prix ? prix : "";
    tdPrix.appendChild(inPrix);

    var tdTotal = el("td", { "class": "num total" });

    var tdSuppr = el("td", { "class": "no-print" });
    var suppr = el("button", { type: "button", "class": "del", title: "Supprimer la ligne", "aria-label": "Supprimer la ligne" });
    suppr.textContent = "×";
    suppr.addEventListener("click", function () { tr.remove(); recalculer(); });
    tdSuppr.appendChild(suppr);

    [tdDesc, tdQte, tdPrix, tdTotal, tdSuppr].forEach(function (td) { tr.appendChild(td); });
    tr.addEventListener("input", recalculer);
    tbody.appendChild(tr);
    recalculer();
  }

  function recalculer() {
    var ht = 0;
    Array.prototype.forEach.call(tbody.rows, function (tr) {
      var inputs = tr.querySelectorAll("input");
      var t = nombre(inputs[0]) * nombre(inputs[1]);
      tr.querySelector(".total").textContent = euro(t);
      ht += t;
    });
    var avecTva = tvaBox.checked;
    var tva = avecTva ? ht * TAUX_TVA : 0;
    var ttc = ht + tva;
    var pct = Math.min(100, nombre(pctInput));
    var acompte = Math.round(ttc * pct) / 100;

    $("ht").textContent = euro(ht);
    $("tvaval").textContent = euro(tva);
    $("tva-row").hidden = !avecTva;
    $("tva-mention").hidden = avecTva;
    $("ttc-label").textContent = avecTva ? "Total TTC" : "Total net";
    $("ttc").textContent = euro(ttc);
    $("acompte").textContent = euro(acompte);
    $("solde").textContent = euro(ttc - acompte);
  }

  document.querySelector('[data-action="add-row"]').addEventListener("click", function () { ajouterLigne("", 1, 0); });
  tvaBox.addEventListener("change", recalculer);
  pctInput.addEventListener("input", recalculer);
  LIGNES_PAR_DEFAUT.forEach(function (l) { ajouterLigne(l[0], l[1], l[2]); });
})();
