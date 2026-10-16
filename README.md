# Queenbee — kit J3

    python -m venv .venv && source .venv/bin/activate    # Windows : .venv\\Scripts\\activate
    pip install -e . pytest hypothesis import-linter ruff mypy bandit pip-audit
    make check          # ruff + mypy + lint-imports + bandit + pip-audit + pytest
    make lab            # pytest -m lab : preuves de failles (labs/ uniquement, en local)
    # Windows sans make : lancer chaque commande de la cible check à la main

Le code vit dans `src/queenbee`. Secret : `.env` (ignoré par Git), jamais commité.
Avant le rendu : `gitleaks detect` doit être propre.
