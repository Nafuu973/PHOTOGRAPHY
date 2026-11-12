# nafuu.raw — page de liens

Page « linktree » de **Nafuu**, photographe à Agen.
*L'esthétique du cinéma appliquée à la photo.*

Site 100 % statique : HTML, CSS, un script de 15 lignes. Aucun traceur, aucune ressource externe.

## Organisation

```
public/                 SEUL dossier publié sur Internet
  index.html            La page de liens
  404.html              Page d'erreur
  _headers              En-têtes de sécurité et de cache (Cloudflare)
  robots.txt, sitemap.xml
  assets/
    css/                fonts.css, style.css
    js/main.js          Barre « Demander mon devis » au défilement
    fonts/              Polices auto-hébergées + licences (SIL OFL)
    img/                Photo de profil, favicon, image de partage

studio/                 Jamais publié : outils et documents internes
  documents/            Devis et contrat de mariage (ouvrir en local)
  tools/                Générateurs (liens WhatsApp, visuels) et check.py
  instagram/            Visuels du post épinglé (exports)
  qr/                   QR codes et carte prête à publier
  google-business/      Logo et couverture de la fiche Google

wrangler.jsonc          Configuration du déploiement Cloudflare
```

Règle : tout ce qui est dans `public/` est visible par tout le monde. Tout le reste ne l'est pas.

## Avant chaque publication

```
python3 studio/tools/check.py
```

Le script échoue si `public/` contient un script ou un style inline (bloqué par la CSP), une référence cassée,
une ressource externe, un fichier sensible (devis, contrat, PDF, clé, RAW) ou si `_headers` est incomplet.

## Modifier la page

| Quoi | Où |
|---|---|
| Textes des offres | `public/index.html`, section `<!-- Offres -->` |
| Messages WhatsApp pré-remplis | `studio/tools/build_links.py` : le lancer, coller les liens dans `index.html` |
| Galeries | `public/index.html`, bloc `Galeries` à décommenter |
| Couleurs, tailles | `public/assets/css/style.css`, section 1 « Variables » |
| Photo de profil | `public/assets/img/profil.jpg` (carrée, 480×480) |

Aucune modification de `public/_headers` ne doit affaiblir la CSP sans raison. Toute nouvelle ressource externe
(police, script, image distante) est volontairement refusée : hébergez-la dans `public/assets/`.

## Déploiement sur Cloudflare (Workers, fichiers statiques)

> Ordre impératif : ne fusionner cette structure dans la branche servie par GitHub Pages qu'**après** la mise en
> ligne sur Cloudflare. GitHub Pages ne sert que la racine du dépôt ou `/docs` : avec `public/`, l'ancienne adresse tomberait en 404.

1. Dashboard Cloudflare → **Workers & Pages** → **Create** → **Import a repository** → ce dépôt.
2. Branche de production : `main`. Commande de build : vide. Commande de déploiement : `npx wrangler deploy`.
3. Le nom du Worker doit correspondre au champ `name` de `wrangler.jsonc` (`nafuu-linkpage`).
4. Tester l'adresse `*.workers.dev`, puis attacher le nom de domaine (Settings → Domains & Routes).
5. Seulement ensuite : désactiver GitHub Pages et, si souhaité, passer le dépôt en privé.

Cloudflare lit un dépôt privé : `studio/` (contrat, devis, outils) n'est alors plus exposé sur GitHub non plus.

## Changer d'adresse (nom de domaine)

L'adresse publique apparaît à 5 endroits : `index.html` (canonical, og:url, og:image, JSON-LD),
`robots.txt`, `sitemap.xml`, `studio/tools/carte-qr.html` (texte imprimé) et les QR codes de `studio/qr/`.

```
grep -rn "nafuu973.github.io/PHOTOGRAPHY" public studio
```

Remplacer partout, puis régénérer les QR codes et exporter à nouveau `studio/qr/carte-qr.png`.
Ne pas imprimer de QR avant d'avoir fixé le nom de domaine définitif.

## Sécurité

- CSP stricte (`default-src 'none'`), doublée par `_headers` : `frame-ancestors 'none'` (anti-clickjacking),
  HSTS, `nosniff`, Permissions-Policy fermée, COOP.
- Aucun formulaire, aucun cookie, aucune donnée de visiteur envoyée à un tiers.
- Liens externes en `rel="noopener noreferrer"`.
- `.gitignore` bloque `.env`, clés, PDF clients et fichiers RAW.
- Activer la double authentification sur GitHub et sur Cloudflare.
- Vérifier les photos publiées : `exiftool public/assets/img/*.jpg` ne doit montrer ni GPS ni numéro de série.
- Coordonnées publiques : le numéro et l'e-mail de la page sont lisibles par les robots. Utiliser des coordonnées dédiées à l'activité.

## Documents commerciaux

Ouvrir `studio/documents/devis.html` ou `contrat-mariage.html` dans un navigateur, remplir les zones orangées,
puis **Imprimer / Enregistrer en PDF**. Rien n'est enregistré ni envoyé. Conserver chaque PDF signé hors de ce dépôt.

> Ces modèles ne remplacent pas un conseil juridique : faire relire le contrat une fois (CCI, juriste).
> Adhérer à un médiateur de la consommation (obligatoire pour vendre à des particuliers) et l'indiquer à l'article 11.
> La clause de responsabilité limitée (article 5) est à faire valider : face à un consommateur, elle peut être jugée abusive.
