"""
a_maze_ing.py - Entry point for the A-Maze-ing maze generator.

Usage:
    python3 a_maze_ing.py <config.txt>
"""

import sys
from typing import List, Tuple, Optional
from src.mazegen.utils import parse_config, validate_config
from src.mazegen import MazeGenerator
from src.solver.hex_writer import HexWriter
from src.solver.maze_data import MazeData
from src.solver.pathfinder import Pathfinder
from src.display import TerminalDisplay

# from src.display import run_display


def build_maze(
    config: dict,  # type: ignore[type-arg]
) -> Tuple[List[List[int]], Optional[str]]:
    """
    Instantiate MazeGenerator, generate the maze, write output file.
    """
    seed: Optional[int] = config.get("SEED")

    generator = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        seed=seed,
    )

    grid: List[List[int]] = generator.generate()
    entry: Tuple[int, int] = config["ENTRY"]
    exit_pt: Tuple[int, int] = config["EXIT"]
    output_file: str = config["OUTPUT_FILE"]

    maze = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)

    pf = Pathfinder(maze)
    path: str = pf.solve()

    writer = HexWriter(maze, path, output_file)
    writer.write()

    print(f"Maze written to '{output_file}'.")
    return grid, path


def main() -> None:
    """Parse config, generate maze, write file, launch display."""
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py <config.txt>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_file: str = sys.argv[1]

    try:
        raw_config = parse_config(config_file)
        config = validate_config(raw_config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    entry: Tuple[int, int] = config["ENTRY"]
    exit_pt: Tuple[int, int] = config["EXIT"]

    # Initial generation
    try:
        grid, path = build_maze(config)
    except Exception as e:
        print(f"Generation error: {e}", file=sys.stderr)
        sys.exit(1)

    # Grab the 42 pattern cells for display highlighting
    from src.mazegen.generator import MazeGenerator as _MG
    _gen = _MG(width=config["WIDTH"], height=config["HEIGHT"])
    pattern_cells = _gen.patern_cells

    # def regenerate():  # type: ignore[return]
    #     """Re-generate a fresh maze (used by the display menu option 1)."""
    #     try:
    #         new_grid, new_path = build_maze({**config, "SEED": None})
    #         return new_grid, new_path
    #     except Exception as err:
    #         print(f"Re-generation error: {err}", file=sys.stderr)
    #         return grid, path

    # run_display(
    #     grid=grid,
    #     entry=entry,
    #     exit_pt=exit_pt,
    #     path=path,
    #     pattern_cells=pattern_cells,
    #     regenerate_callback=regenerate,
    # )
    maze_obj = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)

# 3. PASSI pattern_cells hna (Argument t-talet!)
    test = TerminalDisplay(maze_obj, path, pattern_cells=pattern_cells)

# 4. Render
    test.render()
    test.main_menu()
if __name__ == "__main__":
    main()
