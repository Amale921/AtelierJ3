# ADR 0014 — Correctif : Aucune autorisation dans le service

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : application · **Propriété DICP** : C·I

## Contexte
N'importe quel appelant pouvait modifier un incident : le service ne vérifiait aucun rôle.

## Décision
Vérifier le rôle **en premier** dans le cas d'usage (`require_role`), avant d'accéder au dépôt, et compter les refus.

## Conséquences
- Positive : le contrôle est écrit une seule fois, au centre, pour tous les adaptateurs d'entrée.
- **Négative** : chaque nouveau cas d'usage doit penser à appeler le contrôle ; aucun mécanisme ne l'impose automatiquement.
