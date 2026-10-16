# ADR 0016 — Correctif : Comparaison de jeton non constante

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : sécurité · **Propriété DICP** : C

## Contexte
Comparer deux jetons avec `==` s'arrête au premier caractère différent : le temps de réponse révèle le jeton petit à petit.

## Décision
Utiliser `hmac.compare_digest` sur des octets de même type, et ne jamais journaliser le jeton.

## Conséquences
- Positive : le temps de comparaison ne dépend plus du contenu.
- **Négative** : la protection ne vaut que si tout le chemin est en temps constant (pas de recherche en base avant la comparaison).
