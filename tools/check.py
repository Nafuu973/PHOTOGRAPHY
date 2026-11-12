"""Contrôle du dépôt avant publication (bibliothèque standard uniquement).

Usage : python3 -I tools/check.py
Code de sortie 0 si tout est conforme, 1 sinon. Exécuté automatiquement par GitHub Actions.

Vérifie :
- public/ : CSP respectée (rien d'inline), références locales valides, aucune ressource externe chargée,
  liens externes prévus uniquement, aucun fichier sensible ou trop lourd, adresse cohérente partout ;
- .github/workflows/ : actions épinglées par SHA, permissions déclarées, pas de pull_request_target,
  pas d'injection via le contexte github.event, identifiants de checkout non conservés.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

RACINE = Path(__file__).resolve().parents[1]
PUBLIC = RACINE / "public"
LIENS_EXTERNES_OK = ("https://wa.me/", "https://www.instagram.com/", "https://pots.lydia.me/")
SENSIBLE = re.compile(r"(\.env|\.git|\.pdf$|devis|contrat|\.key$|\.pem$|\.cr[23]$|\.dng$|\.zip$)", re.I)
POIDS_MAX = 1_500_000
erreurs = []


def err(msg):
    erreurs.append(msg)


def lire(chemin):
    return chemin.read_text(encoding="utf-8")


index = lire(PUBLIC / "index.html")
m = re.search(r'<link rel="canonical" href="([^"]+)"', index)
CANONIQUE = m.group(1) if m else ""
if not CANONIQUE:
    err("index.html: lien canonical absent")
BASE = urlparse(CANONIQUE).path.rstrip("/")  # "/PHOTOGRAPHY" en projet GitHub Pages, "" sur un domaine


class Page(HTMLParser):
    def __init__(self, fichier):
        super().__init__()
        self.fichier = fichier

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        nom = self.fichier.relative_to(PUBLIC)
        if tag == "script" and a.get("type") != "application/ld+json" and "src" not in a:
            err(f"{nom}: <script> inline interdit par la CSP")
        if tag == "style":
            err(f"{nom}: <style> inline interdit par la CSP")
        if "style" in a:
            err(f"{nom}: attribut style= interdit par la CSP")
        for k in a:
            if k.startswith("on"):
                err(f"{nom}: gestionnaire {k}= interdit par la CSP")
        if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
            err(f"{nom}: lien target=_blank sans rel=noopener")
        for cle in ("src", "href"):
            url = a.get(cle)
            if not url or url.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            if url.startswith(("http://", "https://")):
                canonique = tag == "link" and a.get("rel") == "canonical"
                if tag != "a" and not canonique:
                    err(f"{nom}: ressource externe chargée : {url}")
                elif tag == "a" and not url.startswith(LIENS_EXTERNES_OK):
                    err(f"{nom}: lien externe non prévu : {url}")
                continue
            if url.startswith("/"):
                if BASE and not url.startswith(BASE + "/"):
                    err(f"{nom}: chemin absolu hors de {BASE}/ : {url}")
                    continue
                cible = PUBLIC / url[len(BASE):].lstrip("/")
            else:
                cible = self.fichier.parent / url
            if not cible.resolve().exists():
                err(f"{nom}: référence cassée : {url}")


# --- public/ ---------------------------------------------------------------------------------
for page in sorted(PUBLIC.rglob("*.html")):
    texte = lire(page)
    if "Content-Security-Policy" not in texte:
        err(f"{page.relative_to(PUBLIC)}: balise meta CSP absente")
    if "frame-ancestors" in texte:
        err(f"{page.relative_to(PUBLIC)}: frame-ancestors est ignoré dans une balise meta")
    Page(page).feed(texte)

for f in PUBLIC.rglob("*"):
    if not f.is_file():
        continue
    if SENSIBLE.search(f.name):
        err(f"fichier sensible dans public/ : {f.relative_to(PUBLIC)}")
    if f.stat().st_size > POIDS_MAX:
        err(f"fichier trop lourd (> 1,5 Mo) : {f.relative_to(PUBLIC)}")

# Cohérence de l'adresse publique (là où les oublis arrivent après un changement de domaine)
if CANONIQUE:
    racine = CANONIQUE.rstrip("/")
    urls = re.findall(r'(?:og:url|og:image)" content="([^"]+)"', index)
    urls += re.findall(r'"(?:url|image)": "([^"]+)"', index)
    urls += re.findall(r"<loc>([^<]+)</loc>", lire(PUBLIC / "sitemap.xml"))
    urls += re.findall(r"^Sitemap:\s*(\S+)", lire(PUBLIC / "robots.txt"), re.M)
    for u in urls:
        if not u.startswith(racine):
            err(f"adresse incohérente avec le canonical ({racine}) : {u}")

# --- workflows -------------------------------------------------------------------------------
for wf in sorted((RACINE / ".github" / "workflows").glob("*.y*ml")):
    t, nom = lire(wf), wf.name
    if not re.search(r"^permissions:", t, re.M):
        err(f"{nom}: permissions de premier niveau absentes (mettre permissions: {{}})")
    for u in re.findall(r"^\s*-?\s*uses:\s*(\S+)", t, re.M):
        if not u.startswith("./") and not re.search(r"@[0-9a-f]{40}$", u):
            err(f"{nom}: action non épinglée par SHA : {u}")
    if "pull_request_target" in t:
        err(f"{nom}: pull_request_target interdit")
    if re.search(r"\$\{\{\s*github\.(event\.|head_ref)", t):
        err(f"{nom}: injection possible via le contexte github.event / head_ref")
    if t.count("actions/checkout") != t.count("persist-credentials: false"):
        err(f"{nom}: chaque checkout doit avoir persist-credentials: false")

if erreurs:
    print("\n".join("ERREUR " + e for e in erreurs))
    sys.exit(1)
print("OK : public/ et les workflows sont conformes.")
