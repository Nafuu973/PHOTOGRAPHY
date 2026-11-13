# nafuu.raw — page de liens

Page « linktree » de **Nafuu**, photographe à Agen.
*L'esthétique du cinéma appliquée à la photo.*

Site 100 % statique hébergé sur GitHub Pages : HTML, CSS, un script d'une vingtaine de lignes.
Aucune dépendance, aucun traceur, aucune ressource externe, aucun cookie.

## Organisation

```
public/                 SEUL dossier publié sur Internet
  index.html            La page de liens
  404.html              Page d'erreur
  robots.txt, sitemap.xml
  assets/
    css/                fonts.css, style.css
    js/main.js          Barre « Demander un devis » fixe sur téléphone
    fonts/              Jost et IBM Plex Mono auto-hébergées + licences (SIL OFL)
    img/                Favicon, image de partage
    img/plans/          Photos 2:1, en 1000 et 2000 px de large, sans métadonnées
tools/check.py          Contrôle automatique avant publication
.github/
  workflows/pages.yml   Vérifie, puis publie public/ sur GitHub Pages
  dependabot.yml        Met à jour les actions GitHub
  CODEOWNERS            Propriétaire des fichiers sensibles
  rulesets/main.json    Protection de la branche main (à importer, voir plus bas)
SECURITY.md, LICENSE
```

Règle : tout ce qui est dans `public/` est visible par tout le monde, et ce dépôt est public.
Les devis, contrats, QR, exports et outils sont dans un dépôt **privé** séparé : `nafuu-studio`.

## Avant chaque publication

```
python3 -I tools/check.py
```

GitHub Actions l'exécute aussi à chaque modification et **bloque la publication** s'il échoue. Il vérifie :
- `public/` : aucun script ou style inline (bloqué par la CSP), références valides, aucune ressource externe chargée,
  liens externes limités à WhatsApp, Instagram et Lydia, aucun fichier sensible (devis, contrat, PDF, clé, RAW)
  ou supérieur à 1,5 Mo, adresse du site identique partout ;
- workflows : actions épinglées par SHA, permissions déclarées, pas de `pull_request_target`,
  pas d'injection via `github.event`, identifiants de checkout non conservés.

## Modifier la page

| Quoi | Où |
|---|---|
| Textes et prix | `public/index.html`, section `<!-- Prestations -->` (prix indicatifs, « dès ») |
| Liens WhatsApp pré-remplis | `tools/build_links.py` dans `nafuu-studio`, puis coller dans `index.html` |
| Photos | `public/assets/img/plans/` : `nom-1000.jpg` et `nom-2000.jpg`, format 2:1, EXIF retirés ; texte alternatif et légende dans `index.html` |
| Couleurs, tailles | `public/assets/css/style.css`, section 1 « Variables » |
| Image de partage | `public/assets/img/partage.jpg` (1200×630) |

Toute nouvelle ressource externe (police, script, image distante) est volontairement refusée : l'héberger dans `public/assets/`.
Ne jamais assouplir la CSP (`unsafe-inline`, `*`) pour « faire marcher » un ajout : corriger l'ajout.

Flux de travail : créer une branche, ouvrir une pull request, attendre le contrôle vert, fusionner.
La fusion dans `main` publie le site.

## Mise en ligne (GitHub Pages par GitHub Actions)

1. Settings → **Pages** → Build and deployment → Source : **GitHub Actions**. L'ancien site reste en ligne jusqu'au premier déploiement.
2. Fusionner la pull request. Onglet **Actions** : les trois étapes `verifier`, `construire`, `deployer` doivent passer.
3. Ouvrir l'adresse publique et vérifier la page.

## Réglages GitHub à activer (à faire une fois)

Ces réglages ne sont pas dans le code : les faire dans l'interface GitHub.

1. **Compte** : Settings → Password and authentication → activer la double authentification (clé d'accès ou application),
   garder les codes de secours hors ligne. Vérifier Settings → Applications et SSH keys : supprimer ce qui n'est plus utilisé.
2. **Branche par défaut** : Settings → General → Default branch → renommer en `main`.
3. **Ruleset** : Settings → Rules → Rulesets → New ruleset → **Import a ruleset** → `.github/rulesets/main.json`.
   Effet : pas de suppression ni de réécriture de `main`, passage obligatoire par pull request et par le contrôle `verifier`.
4. **Sécurité du dépôt** : Settings → Advanced Security (ou Code security) : activer *Private vulnerability reporting*,
   *Dependabot alerts*, *Dependabot security updates*, *Secret scanning* et *Push protection*.
5. **Actions** : Settings → Actions → General :
   - Actions permissions : *Allow actions created by GitHub* ;
   - cocher *Require actions to be pinned to a full-length commit SHA* ;
   - Workflow permissions : *Read repository contents and packages permissions*, décocher *Allow GitHub Actions to create and approve pull requests* ;
   - Fork pull request workflows : exiger l'approbation pour tous les contributeurs externes.
6. **Pages** : cocher *Enforce HTTPS* si l'option est proposée.
7. **Nom de domaine** (quand il sera acheté) : vérifier le domaine au niveau du **profil** (Settings du compte → Pages → Add a domain)
   avec l'enregistrement TXT demandé, et le **laisser en place**. Jamais d'enregistrement DNS générique `*.domaine`.
   Sans cela, un tiers peut reprendre le domaine si le site est supprimé ou désactivé.

## Carte de contact (NFC et QR code)

`public/carte.html` ouvre la fiche `public/nafuu.vcf` (« Ajouter à mes contacts »). Page non indexée.
Les puces NFC et les QR codes imprimés pointent vers `https://nafuu973.github.io/PHOTOGRAPHY/carte.html`.
Après programmation d'une puce, la **verrouiller en écriture**, sinon n'importe qui peut la réécrire vers un autre site.
Changer de domaine oblige à reprogrammer les puces et à réimprimer les QR codes.

## Changer d'adresse (nom de domaine)

L'adresse publique apparaît dans `index.html` (canonical, og:url, og:image, JSON-LD), `robots.txt`, `sitemap.xml`
et `404.html` (chemin `/PHOTOGRAPHY/`). Le contrôle signale toute incohérence.

```
grep -rn "nafuu973.github.io\|/PHOTOGRAPHY/" public
```

Remplacer partout, puis régénérer les QR codes dans `nafuu-studio` avant toute impression.
Ne pas imprimer de QR avant d'avoir fixé le nom de domaine définitif.

## Limites connues

- GitHub Pages ne permet pas de définir des en-têtes HTTP. La CSP est posée par balise `meta`, qui ignore `frame-ancestors` :
  la page peut être affichée dans une iframe par un tiers (clickjacking). Risque faible : pas de connexion, pas d'action sensible.
  Seul un autre hébergeur (ou un proxy) permettrait un vrai en-tête `X-Frame-Options` / `frame-ancestors`.
- Le numéro de téléphone et l'e-mail de la page sont lisibles par des robots. Utiliser des coordonnées dédiées à l'activité.
- L'historique du dépôt reste public même après suppression d'un fichier. Ne jamais y déposer un secret, un devis ou un contrat :
  si cela arrive, changer le secret, puis seulement nettoyer l'historique.
- Mentions légales : à ajouter dès que le statut et le SIRET sont connus (obligation pour un site professionnel en France).

## Code généré par IA : garde-fous appliqués ici

Ce dépôt est rédigé avec une IA. Les études sur le code généré par IA montrent surtout des contrôles d'accès absents,
des secrets exposés, des dépendances inventées et des affirmations non vérifiées. Réponse retenue :
- **Zéro dépendance** : rien à installer, donc aucun paquet inventé ou piégé ;
- **Zéro secret** : le dépôt n'en contient pas (historique analysé), `.gitignore` et la protection au push les bloquent ;
- **Chaque affirmation est vérifiée par machine** (`tools/check.py`), pas seulement écrite dans ce README ;
- **Petites modifications relues** : une pull request, un contrôle vert, une relecture humaine avant fusion ;
- **Pas d'assouplissement silencieux** de la sécurité pour corriger un bug.
