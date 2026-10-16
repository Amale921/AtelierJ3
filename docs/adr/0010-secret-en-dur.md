# ADR 0010 — Correctif : Secret en dur partagé

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : configuration · **Propriété DICP** : C

## Contexte
Une clé écrite dans le code et partagée par tous se retrouve dans le dépôt, donc chez quiconque le lit.

## Décision
Lire la clé dans l'environnement (`.env` ignoré par Git, coffre en production), une clé par agent, échec explicite au démarrage si elle est absente ou trop courte.

## Conséquences
- Positive : la clé n'est plus dans le code ni dans l'historique du dépôt.
- **Négative** : l'ancienne clé commitée reste compromise : il faut la révoquer, la régénérer et la purger de l'historique.
