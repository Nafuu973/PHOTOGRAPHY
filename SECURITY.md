# Politique de sécurité

## Périmètre

Ce dépôt contient le site vitrine statique de Nafuu (photographe, Agen). Il n'a ni serveur, ni base de données,
ni formulaire, ni compte utilisateur, ni cookie.

## Signaler une vulnérabilité

Utiliser le signalement privé de GitHub : onglet **Security** → **Report a vulnerability**.
Ne pas ouvrir de ticket public pour une faille.

Sont notamment pertinents : fuite de données personnelles ou de secret, injection de contenu (XSS), lien malveillant,
reprise de domaine, dépendance ou action GitHub compromise.

## Limites connues

- GitHub Pages ne permet pas de définir des en-têtes HTTP. La CSP est donc posée par balise `meta`, qui ignore
  `frame-ancestors` : la page peut être affichée dans une iframe par un tiers (clickjacking). Risque jugé faible,
  la page ne contient ni connexion ni action sensible.
- Les coordonnées professionnelles (téléphone, e-mail) sont publiques et lisibles par des robots.
