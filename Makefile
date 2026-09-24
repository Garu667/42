install:
	uv sync

run:
	uv run python -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache data/output

debug:
	uv run python -m pdb -m src

test:
	uv run python -m unittest discover -s tests -t .

lint:
	uv run python3 -m flake8 . --exclude=.venv,llm_sdk
	uv run python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude .venv --exclude llm_sdk

lint-strict:
	uv run python3 -m flake8 . --exclude=.venv,llm_sdk
	uv run python3 -m mypy . --strict --exclude .venv --exclude llm_sdk

.PHONY: install run clean debug test lint lint-strict
