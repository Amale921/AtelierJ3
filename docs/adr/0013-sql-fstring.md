# ADR 0013 — Correctif : Requête SQL construite par f-string

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : persistance · **Propriété DICP** : I

## Contexte
Une valeur concaténée dans la requête permet d'en changer le sens (injection SQL).

## Décision
Requêtes paramétrées (`?`) dans l'adaptateur de persistance, uniquement ; le domaine valide aussi ses entrées.

## Conséquences
- Positive : les données ne peuvent plus être interprétées comme du SQL.
- **Négative** : les noms de tables ou de colonnes ne se paramètrent pas : ils doivent venir d'une liste blanche écrite dans le code.
