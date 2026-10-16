# A1 — Suivi de la revue de sécurité (à remplir faille par faille)

Cycle pour chaque faille (≈ 10 min) : ① preuve (`@pytest.mark.lab`) → ② correctif **dans la couche d'origine** →
③ test inversé (non-régression) → ④ `bandit` et `pip-audit` → ⑤ ADR + modèle de menaces.
Pas de « rustine » : un `try/except` qui avale l'erreur n'est pas un correctif.

| # | Faille | ① Preuve écrite | ② Corrigée | ③ Test inversé | ④ bandit / pip-audit | ⑤ ADR + menaces |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Secret en dur | ☐ | ☐ | ☐ | ☐ | ADR 0010 (brouillon) |
| 2 | ReDoS | ☐ fournie | ☐ | ☐ | ☐ | ADR 0011 (brouillon) |
| 3 | pickle | ☐ fournie | ☐ | ☐ | ☐ | ADR 0012 (brouillon) |
| 4 | SQL f-string | ☐ fournie | ☐ | ☐ | ☐ | ADR 0013 (brouillon) |
| 5 | Aucune autorisation | ☐ | ☐ | ☐ | ☐ | ADR 0014 (brouillon) |
| 6 | Services non authentifiés | ☐ | ☐ | ☐ | ☐ | ADR 0015 (brouillon) |
| 7 | Comparaison de jeton | ☐ | ☐ | ☐ | ☐ | ADR 0016 (brouillon) |
