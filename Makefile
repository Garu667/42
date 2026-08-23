VENV	:= .venv
UV		:= uv
MAP		?= maps/easy/01_linear_path.txt

install:
	$(UV) sync

run: install
	$(UV) run python ./fly-in.py $(MAP)

debug: install
	$(UV) run python -m pdb ./fly-in.py $(MAP)

clean:
	find . -type d -name __pycache__ -exec rm -fr {} +
	rm -rf .mypy_cache $(VENV) uv.lock

lint: install
	$(UV) run flake8 . --exclude=$(VENV)
	$(UV) run mypy . --exclude $(VENV) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(UV) run flake8 . --exclude=$(VENV)
	$(UV) run mypy . --exclude $(VENV) --strict

.PHONY: install run debug clean lint lint-strict
