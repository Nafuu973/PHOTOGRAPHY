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

// Mesure d'audience anonyme (Umami Cloud), sans cookie ni identifiant stocké.
// L'identifiant du site est lu dans l'attribut data-umami de la balise <script> :
// vide = aucune mesure. Seul l'hôte autorisé par la CSP (connect-src) reçoit les données.
(function () {
  "use strict";
  var script = document.currentScript;
  var website = script && script.getAttribute("data-umami");
  if (!website || location.hostname !== "nafuu973.github.io") return;
  var nav = navigator;
  if (nav.doNotTrack === "1" || nav.globalPrivacyControl === true) return;

  var ref = document.referrer;
  if (ref.indexOf(location.origin) === 0) ref = "";

  function send(name, data) {
    var payload = {
      website: website,
      hostname: location.hostname,
      url: location.pathname + location.search,
      referrer: ref,
      title: document.title,
      language: nav.language,
      screen: screen.width + "x" + screen.height
    };
    if (name) { payload.name = name; payload.data = data; }
    try {
      fetch("https://gateway.umami.is/api/send", {
        method: "POST",
        keepalive: true,
        credentials: "omit",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "event", payload: payload })
      }).catch(function () {});
    } catch (e) { /* mesure facultative */ }
  }

  send(); // page vue

  // Clics sur les contacts : quel bouton, à quel endroit de la page.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var h = a.getAttribute("href");
    var type = /^https:\/\/wa\.me\//.test(h) ? "devis-whatsapp"
      : /^tel:/.test(h) ? "appel"
      : /^mailto:/.test(h) ? "email"
      : /instagram\.com/.test(h) ? "instagram"
      : /lydia\.me/.test(h) ? "album-lydia"
      : /\.vcf$/.test(h) ? "ajout-contact" : "";
    if (type) send(type, { position: a.getAttribute("data-ev") || "autre" });
  });

  if (!("IntersectionObserver" in window)) return;

  // Sections et formules réellement regardées, une fois chacune.
  var seen = {};
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target, h3 = el.getAttribute("data-vu") === "offre" && el.querySelector("h3");
      var key = h3 ? h3.textContent.trim() : el.getAttribute("data-vu");
      io.unobserve(el);
      if (seen[key]) return;
      seen[key] = true;
      if (h3) send("vu-formule", { formule: key });
      else send("vu-section", { section: key });
    });
  }, { rootMargin: "-35% 0px -35% 0px" }); // l'élément traverse le tiers central de l'écran
  document.querySelectorAll("[data-vu]").forEach(function (el) { io.observe(el); });

  // Profondeur de lecture : 25, 50, 75, 100 %.
  var paliers = [25, 50, 75, 100], pending = false;
  function depth() {
    pending = false;
    var d = document.documentElement;
    var pct = (window.scrollY + window.innerHeight) / d.scrollHeight * 100;
    while (paliers.length && pct >= paliers[0] - 1) send("lecture", { pourcent: paliers.shift() });
  }
  window.addEventListener("scroll", function () {
    if (!pending && paliers.length) { pending = true; window.requestAnimationFrame(depth); }
  }, { passive: true });
})();
