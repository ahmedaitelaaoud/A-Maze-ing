NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt

all: run

run:
	@python3 $(NAME) $(CONFIG_FILE)

install:
	@python3 -m pip install --user --upgrade pip
	@python3 -m pip install --user flake8 mypy build

debug:
	python3 -m pdb $(NAME) $(CONFIG_FILE)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	@python3 -m build

clean:
	rm -vrf */__pycache__ */*/__pycache__
	rm -vrf .mypy_cache
	rm -vrf build/ dist/ *.egg-info

fclean: clean

re: fclean all

.PHONY: all run install debug lint build clean fclean re
