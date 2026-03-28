PYTHON = venv/bin/python
PIP = venv/bin/pip

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install .
	$(PIP) install flake8 mypy build

run:
	$(PYTHON) a_maze_ing.py config.txt

build:
	$(PYTHON) -m build

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__ build/ dist/ *.egg-info/ venv

lint:
	venv/bin/flake8 .
	venv/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	venv/bin/flake8 .
	venv/bin/mypy . --strict

.PHONY: install run debug build clean lint lint-strict