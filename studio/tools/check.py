"""Contrôle du dossier public/ avant publication.

Usage : python3 studio/tools/check.py
Code de sortie 0 si tout est conforme, 1 sinon.
Vérifie : CSP respectée (rien d'inline), références locales valides,
aucune ressource externe chargée, aucun fichier sensible publié, en-têtes présents.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / "public"
LIENS_EXTERNES_OK = ("https://wa.me/", "https://www.instagram.com/", "https://pots.lydia.me/")
SENSIBLE = re.compile(r"(\.env|\.git|\.pdf$|devis|contrat|\.key$|\.pem$|\.cr[23]$|\.dng$)", re.I)
erreurs = []


def err(msg):
    erreurs.append(msg)


class Page(HTMLParser):
    def __init__(self, fichier):
        super().__init__()
        self.fichier, self.ld = fichier, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        nom = self.fichier.relative_to(PUBLIC)
        if tag == "script":
            if a.get("type") == "application/ld+json":
                self.ld = True
            elif "src" not in a:
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
            cible = (PUBLIC / url.lstrip("/")) if url.startswith("/") else (self.fichier.parent / url)
            if not cible.resolve().exists():
                err(f"{nom}: référence cassée : {url}")

    def handle_endtag(self, tag):
        if tag == "script":
            self.ld = False


for page in sorted(PUBLIC.rglob("*.html")):
    texte = page.read_text(encoding="utf-8")
    if "Content-Security-Policy" not in texte:
        err(f"{page.relative_to(PUBLIC)}: balise meta CSP absente")
    Page(page).feed(texte)

for f in PUBLIC.rglob("*"):
    if f.is_file() and SENSIBLE.search(f.name):
        err(f"fichier sensible dans public/ : {f.relative_to(PUBLIC)}")

entetes = PUBLIC / "_headers"
if not entetes.exists():
    err("public/_headers absent")
else:
    t = entetes.read_text(encoding="utf-8")
    for requis in ("Content-Security-Policy", "frame-ancestors 'none'", "Strict-Transport-Security", "nosniff"):
        if requis not in t:
            err(f"public/_headers: {requis} manquant")

if erreurs:
    print("\n".join("ERREUR " + e for e in erreurs))
    sys.exit(1)
print("OK : public/ est conforme.")
