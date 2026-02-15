NAME = src/mazegen/main.py
CONFIG_FILE = default_config.txt

# 42 Mandatory Default Rule
all: run

run:
	@python3 $(NAME) $(CONFIG_FILE)

# Added --user for cluster compatibility
install:
	@python3 -m pip install --user mlx-*.whl

debug:
	python3 -m pdb $(NAME)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Added --user for cluster compatibility
build:
	@python3 -m pip install --user --quiet --upgrade build
	@python3 -m build

clean:
	rm -vrf */__pycache__ */*/__pycache__
	rm -vrf .mypy_cache
	rm -vrf build/ dist/ *.egg-info

# 42 Mandatory Rules
fclean: clean

re: fclean all

.PHONY: all run install debug lint build clean fclean re
