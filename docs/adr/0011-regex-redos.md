# ADR 0011 — Correctif : Regex à retour arrière exponentiel (ReDoS)

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : adaptateur · **Propriété DICP** : D

## Contexte
Une expression régulière avec des quantificateurs imbriqués peut occuper le processeur pendant des minutes sur une ligne bien choisie.

## Décision
Borner la longueur avant d'appliquer la regex et la réécrire sans imbrication (classes de caractères simples, `fullmatch`) ; le temps devient linéaire.

## Conséquences
- Positive : une ligne hostile ne peut plus bloquer le traitement.
- **Négative** : la regex stricte rejette quelques lignes autrefois acceptées ; il faut accepter ces faux rejets, qui sont comptés.
