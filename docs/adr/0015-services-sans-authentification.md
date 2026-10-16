# ADR 0015 — Correctif : Services qui ne s'authentifient pas

- **Statut** : à confirmer après la preuve et le test inversé de votre groupe
- **Couche d'origine** : infrastructure · **Propriété DICP** : I·P

## Contexte
Un service qui accepte tout appel interne permet à un attaquant déjà présent sur le réseau de se faire passer pour un autre composant.

## Décision
Authentification mutuelle entre composants (mTLS ou jeton signé à durée courte) sur chaque flux interne de la matrice des flux.

## Conséquences
- Positive : chaque flux a une identité vérifiable et peut être révoqué.
- **Négative** : gestion de certificats ou de jetons à outiller, et risque de panne si un certificat expire sans être renouvelé.
