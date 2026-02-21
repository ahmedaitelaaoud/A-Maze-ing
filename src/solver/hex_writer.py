"""
hex_writer.py - Maze output file writer and BFS pathfinder.

Writes the maze grid in hexadecimal format to an output file, followed
by the entry, exit, and shortest path as N/E/S/W direction letters.
"""

import sys
from collections import deque
from typing import List, Tuple, Optional, Dict

# Wall bitmask constants (must match MazeGenerator)
N: int = 1
E: int = 2
S: int = 4
W: int = 8

# Direction metadata: wall_bit -> (dx, dy, letter)
DIRECTIONS: Dict[int, Tuple[int, int, str]] = {
    N: (0, -1, "N"),
    E: (1, 0, "E"),
    S: (0, 1, "S"),
    W: (-1, 0, "W"),
}


def solve_bfs(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pt: Tuple[int, int],
) -> Optional[str]:
    """
    Find the shortest path from entry to exit using BFS.

    Moves are only allowed through open walls (bit = 0 in cell bitmask).

    Args:
        grid: 2D list of wall bitmasks (height x width).
        entry: (x, y) starting cell.
        exit_pt: (x, y) destination cell.

    Returns:
        A string of direction letters (e.g. "NESSWN"), or None if no path.
    """
    height: int = len(grid)
    width: int = len(grid[0])

    # BFS queue holds (x, y, path_so_far)
    queue: deque[Tuple[int, int, str]] = deque()
    queue.append((entry[0], entry[1], ""))
    visited: set[Tuple[int, int]] = {entry}

    while queue:
        cx, cy, path = queue.popleft()

        if (cx, cy) == exit_pt:
            return path

        for wall_bit, (dx, dy, letter) in DIRECTIONS.items():
            # Can move only if the wall in that direction is OPEN (bit = 0)
            if grid[cy][cx] & wall_bit:
                continue

            nx, ny = cx + dx, cy + dy

            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + letter))

    return None  # No path found (maze is not connected)


def write_maze_file(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pt: Tuple[int, int],
    output_file: str,
) -> Optional[str]:
    """
    Write the maze to a file in the required hexadecimal format.

    Format:
        - One hex digit per cell, cells stored row by row (one row per line).
        - An empty line separator.
        - Entry coordinates (x,y).
        - Exit coordinates (x,y).
        - Shortest path as N/E/S/W letters.

    Args:
        grid: 2D list of wall bitmasks (height x width).
        entry: (x, y) entry cell coordinates.
        exit_pt: (x, y) exit cell coordinates.
        output_file: Path to the output file.

    Returns:
        The shortest path string, or None if unreachable.
    """
    path: Optional[str] = solve_bfs(grid, entry, exit_pt)

    if path is None:
        print(
            "Warning: No path found between entry and exit.",
            file=sys.stderr,
        )
        path = ""

    try:
        with open(output_file, "w") as f:
            # Write grid rows: one hex digit per cell
            for row in grid:
                line: str = "".join(format(cell, "X") for cell in row)
                f.write(line + "\n")

            # Empty separator line
            f.write("\n")

            # Entry coordinates
            f.write(f"{entry[0]},{entry[1]}\n")

            # Exit coordinates
            f.write(f"{exit_pt[0]},{exit_pt[1]}\n")

            # Shortest path
            f.write(path + "\n")

    except OSError as err:
        print(f"Error writing output file '{output_file}': {err}", file=sys.stderr)
        raise

    return path
