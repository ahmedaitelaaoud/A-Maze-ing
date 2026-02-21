NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt

# 42 Mandatory Default Rule
all: run

run:
	@python3 $(NAME) $(CONFIG_FILE)

# 42 Mandatory Rule: Install project dependencies.
# Since we use ASCII, our only dependencies are the tools needed for linting and building.
install:
	@python3 -m pip install --user --upgrade pip
	@python3 -m pip install --user flake8 mypy build

debug:
	python3 -m pdb $(NAME)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# 42 Optional/Custom Rule for Packaging (Student 1 Requirement)
build:
	@python3 -m build

clean:
	rm -vrf */__pycache__ */*/__pycache__
	rm -vrf .mypy_cache
	rm -vrf build/ dist/ *.egg-info

# 42 Mandatory Rules
fclean: clean

re: fclean all

.PHONY: all run install debug lint build clean fclean re
