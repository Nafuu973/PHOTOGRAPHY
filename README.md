# nafuu.raw — page de liens

Page « linktree » de **Nafuu**, photographe à Agen.
*L'esthétique du cinéma appliquée à la photo.*

🔗 **Adresse publique :** https://nafuu973.github.io/photography/

La page met en avant les offres qui rapportent le plus : **mariage & événement**,
**shooting privé** et **carte cadeau**. Chaque bouton ouvre WhatsApp avec un
message pré-rempli. Viennent ensuite le portfolio Instagram et les albums des
événements bénévoles (participation libre sur Lydia).

## Organisation du dépôt

```
index.html              La page de liens
assets/
  css/fonts.css         Déclaration des polices
  css/style.css         Mise en forme (sections numérotées)
  js/main.js            Barre « Demander mon devis » qui apparaît au défilement
  fonts/                Polices auto-hébergées + licences (SIL OFL)
  img/                  Photo de profil, favicon, image de partage (1200×630)
  qr/                   QR codes et carte prête à publier
documents/
  devis.html            Modèle de devis (calcul automatique)
  contrat-mariage.html  Modèle de contrat de mariage
  doc.css, doc.js, devis.js
tools/
  build_links.py        Génère les liens WhatsApp pré-remplis
  partage.html          Source de l'image de partage
  carte-qr.html         Source de la carte QR
robots.txt              Empêche Google d'indexer documents/ et tools/
```

## Modifier la page

On peut tout modifier directement sur GitHub : ouvrez le fichier, cliquez sur le
crayon ✏️, puis sur **Commit changes**.

| Quoi | Où |
|---|---|
| Textes des offres | `index.html`, section `<!-- Offres -->` |
| Messages WhatsApp pré-remplis | modifier `tools/build_links.py`, le lancer, coller les liens dans `index.html` |
| Galeries Google Photos | `index.html`, décommenter le bloc `Galeries` |
| Couleurs, tailles | `assets/css/style.css`, section 1 « Variables » |
| Photo de profil | remplacer `assets/img/profil.jpg` (carrée, 480×480) |

## Sécurité

- **Aucun script externe, aucun traceur, aucune police Google** : tout est servi
  depuis le site lui-même (aucune donnée de visiteur envoyée à des tiers).
- **Content-Security-Policy** stricte : seuls les fichiers du site peuvent être
  chargés ; aucun code inline, aucun formulaire.
- La page fonctionne entièrement sans JavaScript. Le seul script (`main.js`)
  ne fait qu'afficher la barre de réservation au défilement.
- Liens externes en `rel="noopener noreferrer"`.
- Les photos publiées sont débarrassées de leurs métadonnées (EXIF, GPS).
- HTTPS forcé par GitHub Pages (cocher **Enforce HTTPS** dans Settings → Pages).

## QR code

| Fichier | Usage |
|---|---|
| `assets/qr/carte-qr.png` | Carte 1080×1350 prête à publier (story, post, impression) |
| `assets/qr/qr-nafuu-logo.png` | QR seul avec l'œil au centre |
| `assets/qr/qr-nafuu.png` / `.svg` | QR simple (le SVG s'imprime à n'importe quelle taille) |

Le QR pointe vers https://nafuu973.github.io/photography/ (correction d'erreur
maximale : il reste lisible même abîmé ou imprimé petit, 2 cm minimum).

## Mise en ligne (GitHub Pages)

1. Le dépôt doit être **public** : Settings → General → Danger Zone → Change visibility.
2. Settings → **Pages** → Source : **Deploy from a branch**.
3. Branche : celle qui contient `index.html`, dossier `/ (root)` → **Save**.
4. Cocher **Enforce HTTPS**. La page est en ligne en 1 à 2 minutes.

## Documents commerciaux

Ouvrez `documents/devis.html` ou `documents/contrat-mariage.html` dans un
navigateur, remplissez les zones orangées, puis **Imprimer / Enregistrer en PDF**.
Rien n'est enregistré ni envoyé : gardez le PDF de chaque devis et contrat signé.

> ⚠️ Ces modèles ne remplacent pas un conseil juridique : faites relire le contrat
> une fois (CCI, juriste). Adhérez à un **médiateur de la consommation**
> (obligatoire pour vendre à des particuliers) et indiquez-le dans l'article 11.
