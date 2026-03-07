install:
	pip install .

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__ build/ dist/ *.egg-info/

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict
