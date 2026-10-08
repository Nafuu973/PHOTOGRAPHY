# nafuu.raw — page de liens

Page « linktree » de **Nafuu**, photographe à Agen.
*L'esthétique du cinéma appliquée à la photo.*

La page met en avant les offres qui rapportent le plus :

1. **Shooting privé** : portrait, couple, véhicule, animaux
2. **Mariage & événement**
3. **Carte cadeau** (offrir un shooting)

Chaque bouton ouvre WhatsApp avec un message pré-rempli adapté (type de séance,
date, lieu…), pour que le client n'ait plus qu'à compléter.
Viennent ensuite le portfolio Instagram et les albums des événements bénévoles
(accès à l'album complet contre une participation libre sur Lydia).

## Modifier la page

Tout est dans `index.html`, et on peut le modifier directement sur GitHub :
ouvrez le fichier, cliquez sur le crayon ✏️, puis sur **Commit changes**.

| Quoi | Où chercher dans `index.html` |
|---|---|
| Texte d'une offre | `<!-- Offre 1 …` et `<!-- Offre 2 …` |
| Numéro WhatsApp / téléphone | `33786887651` (dans les liens `wa.me`, `tel:` et le script en bas) |
| Message pré-rempli d'un bouton | l'attribut `data-wa="…"` du bouton (`&#10;` = retour à la ligne) |
| Galeries (albums Google Photos) | la liste `GALERIES` dans le script en bas de page |
| E-mail | `nafuu.raw@gmail.com` |
| Lien de la cagnotte | `https://pots.lydia.me/…` |
| Photo de profil | remplacez le fichier `images/profil.jpg` (image carrée) |

## Mettre la page en ligne (gratuit, avec GitHub Pages)

1. Sur GitHub : **Settings** → **Pages**.
2. Dans **Source**, choisissez **Deploy from a branch**.
3. Sélectionnez la branche qui contient `index.html` et le dossier `/ (root)`, puis cliquez sur **Save**.
4. Après une ou deux minutes, la page est disponible à l'adresse
   `https://nafuu973.github.io/photography/`.

Collez cette adresse dans la bio Instagram, à la place du lien WhatsApp ou à côté.

> GitHub Pages n'est gratuit que pour les dépôts **publics** (sauf avec un abonnement GitHub Pro).
