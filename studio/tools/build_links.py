"""Affiche les liens WhatsApp pré-remplis à coller dans index.html.

Usage : python3 tools/build_links.py
Modifiez les messages ci-dessous puis remplacez les href correspondants.
"""
from urllib.parse import quote

NUMERO = "33786887651"

MESSAGES = {
    "contact": "Bonjour Nafuu ! Je vous contacte depuis votre page.",
    "devis": "Bonjour Nafuu ! J'aimerais un devis.\nPrestation (mariage, shooting…) : \nDate : \nLieu : ",
    "mariage": "Bonjour Nafuu ! Nous aimerions un devis pour notre mariage.\nDate : \nLieu : \nNombre d'invités (environ) : ",
    "shooting": "Bonjour Nafuu ! Je souhaite réserver un shooting privé.\nType de séance (portrait, couple, véhicule, animal) : \nDate souhaitée : \nLieu : ",
    "cadeau": "Bonjour Nafuu ! Je souhaite offrir un shooting en carte cadeau.\nPour qui / quelle occasion : ",
}

if __name__ == "__main__":
    for nom, texte in MESSAGES.items():
        print(f"{nom}: https://wa.me/{NUMERO}?text={quote(texte, safe='')}")
