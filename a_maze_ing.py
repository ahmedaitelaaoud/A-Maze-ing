"""
a_maze_ing.py - Entry point for the A-Maze-ing maze generator.

Usage:
    python3 a_maze_ing.py <config.txt>
"""

import sys
import os
from typing import List, Tuple, Optional
from src.mazegen.utils import parse_config, validate_config
from src.mazegen import MazeGenerator
from src.solver.hex_writer import HexWriter
from src.solver.maze_data import MazeData
from src.solver.pathfinder import Pathfinder
from src.display import TerminalDisplay


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

    try:
        grid, path = build_maze(config)
    except Exception as e:
        print(f"Generation error: {e}", file=sys.stderr)
        sys.exit(1)

    from src.mazegen.generator import MazeGenerator as _MG
    _gen = _MG(width=config["WIDTH"], height=config["HEIGHT"])
    pattern_cells = _gen.patern_cells

    maze_obj = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)
    test = TerminalDisplay(maze_obj, path, pattern_cells=pattern_cells)

    test.render()
    # test.main_menu()

    try:
            while True:
                print("==A-Maze-ing==")
                print("1. Re-generate a new maze")
                print("2. Show/hide path from entry to exit")
                print("3. Rotate maze colors")
                print("4. Quit")

                choice = input("Choice (1-4): ")

                try:
                    choice = int(choice)
                    if choice < 1 or choice > 4:
                        print("Invalid input try again!")
                        continue
                except ValueError:
                    print("Invalid input try again!")
                    continue
                if choice == 1:
                    os.system('clear')


                    try:
                        grid, path = build_maze(config)
                    except Exception as e:
                        print(f"Generation error: {e}", file=sys.stderr)
                        sys.exit(1)

                    from src.mazegen.generator import MazeGenerator as _MG
                    _gen = _MG(width=config["WIDTH"], height=config["HEIGHT"])
                    pattern_cells = _gen.patern_cells

                    maze_obj = MazeData(grid, config["WIDTH"], config["HEIGHT"], entry, exit_pt)
                    test = TerminalDisplay(maze_obj, path, pattern_cells=pattern_cells)
                    test.render()

                elif choice == 2:
                    test.show_path()
                elif choice == 3:
                    test.render(True)
                elif choice == 4:
                    print("Goodbye!")
                    break
    except BaseException:
        pass

if __name__ == "__main__":
    main()
