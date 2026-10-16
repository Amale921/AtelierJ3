# ADR 0012 — Correctif : Désérialisation pickle

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : adaptateur · **Propriété DICP** : I

## Contexte
`pickle.loads` exécute du code arbitraire contenu dans les données reçues.

## Décision
Remplacer pickle par JSON, avec schéma strict, taille bornée et signature vérifiée avant toute lecture.

## Conséquences
- Positive : plus aucune exécution de code possible depuis une entrée.
- **Négative** : JSON ne transporte que des types simples ; les objets complexes demandent une conversion explicite à écrire.
