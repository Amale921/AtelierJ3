.PHONY: check lint types arch sec test lab
check: lint types arch sec test
lint:
	ruff check .
types:
	mypy
arch:
	lint-imports
sec:
	bandit -q -r src -ll
	pip-audit --skip-editable
test:
	pytest
lab:
	pytest -m lab -q
