# A-Maze-ing

A Python maze generator and terminal visualizer combining iterative DFS or randomized Prim generation with BFS pathfinding.

*Created as part of the 42 curriculum by aait-ela and yrabhi.* This is a team learning project; the contribution breakdown and AI-use disclosure are preserved below.

## Run locally

Python 3.10 or later is sufficient to run the terminal application.

```bash
git clone https://github.com/ahmedaitelaaoud/A-Maze-ing.git
cd A-Maze-ing
python3 a_maze_ing.py default_config.txt
```

The menu regenerates the maze, toggles the solution, changes wall colors, or exits. The default run has been smoke-tested. Use a terminal with ANSI support and enough space for the selected dimensions.

## Configuration

| Key | Meaning |
| --- | --- |
| `WIDTH`, `HEIGHT` | Grid dimensions, at least 3 |
| `ENTRY`, `EXIT` | Distinct coordinates written as `x,y` |
| `PERFECT` | Whether generation should avoid added loops |
| `OUTPUT_FILE` | Destination for the encoded maze and solution |
| `ALGO` | Optional `dfs` or `prim` algorithm |
| `SEED` | Optional integer for repeatable initial generation |

See [default_config.txt](default_config.txt) for a working configuration. Interactive regeneration chooses a new seed. Entry and exit must not occupy the reserved “42” pattern.

## Architecture and decisions

| Module | Responsibility |
| --- | --- |
| `src/mazegen/generator.py` | Wall-bitmask grid, reserved pattern, DFS/Prim generation |
| `src/mazegen/utils.py` | Configuration parsing and validation |
| `src/solver/maze_data.py` | Grid and endpoint representation |
| `src/solver/pathfinder.py` | BFS solution |
| `src/solver/hex_writer.py` | Encoded file output |
| `src/display.py` | Terminal rendering |
| `a_maze_ing.py` | Application orchestration and menu |

An explicit DFS stack avoids recursive call-depth limits. The “42” cells remain fully walled and are excluded from carving; statements about connectivity concern traversable cells, not those reserved cells. Imperfect mode adds loops with a check against fully open 3×3 areas.

## Output format

The output contains one hexadecimal wall mask per cell, followed by a blank line, entry coordinates, exit coordinates, and the solution as `N/E/S/W` directions. Bits 0–3 represent North, East, South, and West; a set bit means a closed wall.

## Generator usage

From the repository root:

```bash
PYTHONPATH=src python3 - <<'PYTHON'
from mazegen.generator import MazeGenerator

generator = MazeGenerator(width=20, height=15, perfect=True, seed=42)
grid = generator.generate()
print(len(grid), len(grid[0]))
PYTHON
```

Use the concrete module import above. The repository does not provide a package-level `MazeGenerator` export.

## Development and limitations

The Makefile provides `install`, `run`, `debug`, `lint`, `lint-strict`, `build`, `clean`, and `fclean` targets. Packaging is configured in `pyproject.toml`; package installation has not been verified as part of the portfolio review.

There is no committed automated test suite. Useful next checks are connectivity across seeds, reciprocal walls, BFS solution validity, pattern overlap, and parser failures. Large mazes also warrant profiling of the Prim frontier and terminal renderer.

## License

No repository-level LICENSE file is included. The packaging metadata contains an MIT classifier, but the licensing decision needs confirmation from the project authors.

---

## Resources

### References

- [Maze generation — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — jamisbuck.org](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Randomised Prim's — jamisbuck.org](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
- [Python `random` module](https://docs.python.org/3/library/random.html)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Python packaging guide](https://packaging.python.org/en/latest/)

### AI usage

AI (Claude by Anthropic) was used for:

- **Code review:** identifying the 3×3 open-area bug in `_add_loops`,
  the seed reuse bug in the re-generation loop, and `mypy` type errors
  in `display.py` (`Optional` vs bare `None` defaults, missing type
  hints on method parameters).
- **Import debugging:** resolving `ModuleNotFoundError` caused by
  `src/` not being on `sys.path` when running from the project root.
- **Docstring drafting:** generating Google-style docstrings that were
  reviewed and corrected by the team.

All AI-suggested code was read, understood, tested, and approved by the
team before inclusion.

---

## Team and Project Management

### Roles

| Member | Responsibilities |
|---|---|
| **aait-ela** | Maze generation (`generator.py`), reusable `mazegen` package, configuration parsing (`utils.py`), output file format, project structure and packaging |
| **yrabhi** | Terminal display (`display.py`), path-finding (`pathfinder.py`), interactive menu in `a_maze_ing.py`, README |

### Anticipated planning vs reality

**Initial plan:**

- Day 1–2: understand the subject, design data structures and module
  layout.
- Day 3–4: implement DFS generator and hex output writer.
- Day 5: terminal display and interactive menu.
- Day 6: Prim's algorithm, pip package, README.
- Day 7: testing, lint, polish.

**How it evolved:**

- The "42" pattern requirement took longer than expected. Pre-marking
  pattern cells as visited before generation was the key insight that
  kept the algorithms clean.
- The 3×3 open-area constraint for `PERFECT=False` was initially
  overlooked; it required adding a tentative-remove-and-rollback step.
- The `pyproject.toml` `src/` layout misconfiguration was discovered
  late during package build testing.
- The `show_path` toggle bug (path disappearing on colour rotation) was
  caught during manual testing and fixed by separating the toggle from
  the draw call.
- The `ModuleNotFoundError` on `make run` was the last issue fixed —
  adding `sys.path.insert(0, "src")` in `a_maze_ing.py`.

### What worked well

- Separating concerns into `MazeData`, `Pathfinder`, `HexWriter`, and
  `TerminalDisplay` made each part independently testable.
- The iterative DFS was clean to implement and easy to audit.
- BFS path-finding was correct on the first attempt.

### What could be improved

- Add `pytest` unit tests covering the generator, pathfinder, and
  config parser edge cases.
- The Prim frontier list can accumulate duplicate edges; deduplicating
  on insertion would improve performance on very large mazes.
- Add a `--validate` flag to run the provided validation script
  automatically after generation.

### Tools used

- **VS Code** with Python and Pylance extensions.
- **flake8** and **mypy** for linting and static type checking.
- **Git** for version control and collaboration.
- **Claude (Anthropic)** for code review (see AI usage section above).

