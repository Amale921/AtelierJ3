# Modèle de menaces — ajouts du jour 3
_À fusionner dans `docs/threat_model.md`._
DICP : **D**isponibilité, **I**ntégrité, **C**onfidentialité, **P**reuve (traçabilité).

| ID | Faille | Couche | Propriété | Correctif | Preuve / non-régression |
| --- | --- | --- | --- | --- | --- |
| M-J3-01 | Secret en dur partagé | configuration | C | ADR 0010 | `@pytest.mark.lab` puis test inversé |
| M-J3-02 | Regex à retour arrière exponentiel (ReDoS) | adaptateur | D | ADR 0011 | `@pytest.mark.lab` puis test inversé |
| M-J3-03 | Désérialisation pickle | adaptateur | I | ADR 0012 | `@pytest.mark.lab` puis test inversé |
| M-J3-04 | Requête SQL construite par f-string | persistance | I | ADR 0013 | `@pytest.mark.lab` puis test inversé |
| M-J3-05 | Aucune autorisation dans le service | application | C·I | ADR 0014 | `@pytest.mark.lab` puis test inversé |
| M-J3-06 | Services qui ne s'authentifient pas | infrastructure | I·P | ADR 0015 | `@pytest.mark.lab` puis test inversé |
| M-J3-07 | Comparaison de jeton non constante | sécurité | C | ADR 0016 | `@pytest.mark.lab` puis test inversé |

**Contrôle d'éthique** : toute exploitation se fait uniquement sur `labs/vulnerable_queenbee.py`, en local.
