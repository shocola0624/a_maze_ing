PYTHON = python
PDB = pdb
PIP = pip
VENV = venv
ACTIVATE = $(VENV)/bin/activate

run:
	. $(ACTIVATE); $(PYTHON) a_maze_ing.py config.txt

install:
	python3 -m venv $(VENV)
	. $(ACTIVATE); \
	$(PIP) install --upgrade pip; \
	$(PIP) install .; \
	$(PIP) install flake8 mypy build

build:
	. $(ACTIVATE); \
	$(PYTHON) -m build

debug:
	. $(ACTIVATE); \
	$(PDB) a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__ build/ dist/ *.egg-info/ venv
	find . \( -name "__pycache__" -o -name "build" -o -name "dist" -o -name "*.egg-info" -o -name "*.pyc" -o -name "maze.txt" \) -print -exec rm -rf {} \;

lint:
	. $(ACTIVATE); \
	$(PYTHON) -m flake8 .; \
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	. $(ACTIVATE); \
	$(PYTHON) -m flake8 .; \
	$(PYTHON) -m mypy . --strict

.PHONY: install run debug build clean lint lint-strict
