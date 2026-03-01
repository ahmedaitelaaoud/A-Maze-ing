"""
a_maze_ing.py - Entry point for the A-Maze-ing maze generator.

Usage:
    python3 a_maze_ing.py <config.txt>
"""

import sys
import os
from typing import Any, Dict, List, Optional, Tuple

from src.mazegen.utils import parse_config, validate_config
from src.mazegen.generator import MazeGenerator
from src.solver.hex_writer import HexWriter
from src.solver.maze_data import MazeData
from src.solver.pathfinder import Pathfinder
from src.display import TerminalDisplay


def build_maze(
    config: Dict[str, Any],
) -> Tuple[List[List[int]], str, List[Tuple[int, int]]]:
    """
    Instantiate MazeGenerator, generate the maze, write output file.
    """
    # ✅ Bug 1 fixed: Use the config passed in, not a re-parsed hardcoded file
    # ✅ Bug 2 fixed: Use consistent variable name 'generator' (not 'maze')
    generator = MazeGenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        perfect=config["PERFECT"],  # ← reads PERFECT=false from your config file
        seed=config["SEED"]
    )

    # ✅ Bug 3 fixed: call generate() on 'generator', not undefined 'generator.generate()'
    grid: List[List[int]] = generator.generate()

    # ✅ Bug 4 fixed: 'maze' was being overwritten — renamed to 'maze_data' below
    pattern_cells = generator._get_42_pattern_cells()

    entry: Tuple[int, int] = config["ENTRY"]
    exit_pt: Tuple[int, int] = config["EXIT"]
    output_file: str = config["OUTPUT_FILE"]

    maze_data = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)

    pf = Pathfinder(maze_data)
    path: str = pf.solve()

    writer = HexWriter(maze_data, path, output_file)
    writer.write()

    return grid, path, pattern_cells


def main() -> None:
    """Parse config, generate maze, write file, launch display."""
    if len(sys.argv) != 2:
        print(
            "Usage: python3 a_maze_ing.py <config.txt>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_file: str = sys.argv[1]

    # Parse and Validate Configuration safely
    try:
        raw_config = parse_config(config_file)
        config = validate_config(raw_config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    entry: Tuple[int, int] = config["ENTRY"]
    exit_pt: Tuple[int, int] = config["EXIT"]

    # Initial Maze Generation
    try:
        grid, path, pattern_cells = build_maze(config)
    except Exception as e:
        print(f"Generation error: {e}", file=sys.stderr)
        sys.exit(1)

    # Launch Display
    maze_obj = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)
    display = TerminalDisplay(maze_obj, path, pattern_cells)
    display.render()

    # Interactive Loop
    try:
        while True:
            print("\n== A-Maze-ing ==")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            choice_input = input("Choice (1-4): ")

            try:
                choice = int(choice_input)
                if choice < 1 or choice > 4:
                    print("Invalid input, try again!")
                    continue
            except ValueError:
                print("Invalid input, try again!")
                continue

            if choice == 1:
                os.system('clear')
                try:
                    grid, path, pattern_cells = build_maze(config)
                except Exception as e:
                    print(f"Generation error: {e}", file=sys.stderr)
                    continue

                maze_obj = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)
                display = TerminalDisplay(maze_obj, path, pattern_cells=pattern_cells)
                display.render()

            elif choice == 2:
                display.show_path()
            elif choice == 3:
                display.render(True)
            elif choice == 4:
                print("Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nExiting gracefully. Goodbye!", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
