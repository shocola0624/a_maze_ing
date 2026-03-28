PYTHON = python
PDB = pdb3
PIP = pip
VENV = venv
ACTIVATE = $(VENV)/bin/activate

run: $(VENV)
	. $(ACTIVATE); $(PYTHON) a_maze_ing.py config.txt

$(VENV):
	python3 -m venv $(VENV)
	. $(ACTIVATE); \
	$(PIP) install --upgrade pip; \
	$(PIP) install .; \
	$(PIP) install flake8 mypy build

install: $(VENV)

build: $(VENV)
	. $(ACTIVATE); \
	$(PYTHON) -m build

debug: $(VENV)
	. $(ACTIVATE); \
	$(PDB) a_maze_ing.py config.txt

clean:
	-rm -rf venv
	-find . \( -name "__pycache__" -o -name "build" -o -name "dist" -o -name "*.egg-info" -o -name "*.pyc" -o -name "maze.txt" \) -print -exec rm -rf {} \;

lint: $(VENV)
	. $(ACTIVATE); \
	$(PYTHON) -m flake8 .; \
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)
	. $(ACTIVATE); \
	$(PYTHON) -m flake8 .; \
	$(PYTHON) -m mypy . --strict

.PHONY: install run debug build clean lint lint-strict
