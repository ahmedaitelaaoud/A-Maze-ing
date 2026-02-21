"""
display.py - Terminal renderer for A-Maze-ing using box-drawing characters.

Uses Unicode box-drawing chars for walls and ANSI colours for highlights.
"""

import os
import sys
from typing import List, Tuple, Optional, Set, Callable

# ---------------------------------------------------------------------------
# Wall bitmask constants (must match MazeGenerator)
# ---------------------------------------------------------------------------
N: int = 1
E: int = 2
S: int = 4
W: int = 8

# ---------------------------------------------------------------------------
# ANSI colours
# ---------------------------------------------------------------------------
RESET: str = "\033[0m"

FG: dict[str, str] = {
    "black":         "\033[30m",
    "red":           "\033[31m",
    "green":         "\033[32m",
    "yellow":        "\033[33m",
    "blue":          "\033[34m",
    "magenta":       "\033[35m",
    "cyan":          "\033[36m",
    "white":         "\033[37m",
    "bright_yellow": "\033[93m",
    "bright_white":  "\033[97m",
    "bright_cyan":   "\033[96m",
    "bright_green":  "\033[92m",
    "bright_red":    "\033[91m",
}

BG: dict[str, str] = {
    "blue":    "\033[44m",
    "cyan":    "\033[46m",
    "green":   "\033[42m",
    "red":     "\033[41m",
    "yellow":  "\033[43m",
    "magenta": "\033[45m",
}

WALL_COLOURS: List[str] = [
    FG["bright_white"],
    FG["bright_yellow"],
    FG["bright_cyan"],
    FG["magenta"],
    FG["blue"],
    FG["bright_green"],
    FG["bright_red"],
]
WALL_NAMES: List[str] = [
    "White", "Yellow", "Cyan", "Magenta", "Blue", "Green", "Red"
]

# ---------------------------------------------------------------------------
# Box-drawing corner lookup
# Corners depend on which neighbours have walls. We use a 4-bit key:
# bit3=N-wall-exists, bit2=E-wall-exists, bit1=S-wall-exists, bit0=W-wall-exists
# ---------------------------------------------------------------------------
CORNER: dict[int, str] = {
    #  NESW
    0b0000: " ",
    0b0001: "╴",
    0b0010: "╶",
    0b0011: "─",
    0b0100: "╵",
    0b0101: "┘",
    0b0110: "└",
    0b0111: "┴",
    0b1000: "╷",
    0b1001: "┐",
    0b1010: "┌",
    0b1011: "┬",
    0b1100: "│",
    0b1101: "┤",
    0b1110: "├",
    0b1111: "┼",
}


def _c(text: str, colour: str) -> str:
    """Wrap text with ANSI colour and reset."""
    return f"{colour}{text}{RESET}"


def _clear() -> None:
    """Clear the terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def _path_cells(path: str, entry: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Return all cells visited along the BFS path string."""
    cells: Set[Tuple[int, int]] = {entry}
    px, py = entry
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    for letter in path:
        dx, dy = moves[letter]
        px += dx
        py += dy
        cells.add((px, py))
    return cells


def _corner_char(
    grid: List[List[int]],
    cx: int,
    cy: int,
    wall_colour: str,
) -> str:
    """
    Compute the correct box-drawing corner character at grid corner (cx, cy).

    A grid of W x H cells has (W+1) x (H+1) corners.
    Corner (cx, cy) is touched by up to 4 cells:
        top-left=(cx-1,cy-1), top-right=(cx,cy-1),
        bot-left=(cx-1,cy),   bot-right=(cx,cy)

    Args:
        grid:        2D wall bitmask grid.
        cx, cy:      Corner indices (0..W, 0..H).
        wall_colour: ANSI colour string.

    Returns:
        Coloured box-drawing character string.
    """
    h = len(grid)
    w = len(grid[0])

    def has(x: int, y: int, wall: int) -> bool:
        if 0 <= x < w and 0 <= y < h:
            return bool(grid[y][x] & wall)
        return False

    # A corner segment exists if the adjacent cell has that wall
    go_n = has(cx - 1, cy - 1, S) or has(cx, cy - 1, S)  # segment goes up
    go_e = has(cx, cy - 1, S) or has(cx, cy, N)           # segment goes right
    go_s = has(cx - 1, cy, E) or has(cx, cy, W)           # segment goes down — fixed
    go_w = has(cx - 1, cy - 1, E) or has(cx - 1, cy, E)   # segment goes left

    # Recompute properly: a corner line segment exists between two cells
    # North arm: top-left cell has S wall OR top-right cell has S wall
    arm_n = has(cx - 1, cy - 1, S) or has(cx, cy - 1, S)
    # South arm: bot-left cell has N wall OR bot-right cell has N wall  -- simpler:
    arm_s = has(cx - 1, cy, N) or has(cx, cy, N)
    # West arm: top-left has E, or bot-left has E
    arm_w = has(cx - 1, cy - 1, E) or has(cx - 1, cy, E)
    # East arm: top-right has W, or bot-right has W
    arm_e = has(cx, cy - 1, W) or has(cx, cy, W)

    key = (
        (1 if arm_n else 0) << 3
        | (1 if arm_e else 0) << 2
        | (1 if arm_s else 0) << 1
        | (1 if arm_w else 0)
    )
    ch = CORNER[key]
    if ch == " ":
        return " "
    return _c(ch, wall_colour)


def render_maze(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pt: Tuple[int, int],
    path: Optional[str],
    show_path: bool,
    wall_colour: str,
    pattern_cells: Optional[Set[Tuple[int, int]]] = None,
) -> None:
    """
    Render the maze in the terminal using box-drawing wall characters.

    Layout per cell row:
        corner ─ corner ─ ... corner   (top border of row)
        │  cell  │  cell  │ ...  │     (cell bodies)

    Args:
        grid:          2D wall bitmask grid (height x width).
        entry:         (x, y) entry cell.
        exit_pt:       (x, y) exit cell.
        path:          BFS path string or None.
        show_path:     Whether to display the solution path.
        wall_colour:   ANSI colour for wall characters.
        pattern_cells: Set of '42' pattern cell coordinates.
    """
    height = len(grid)
    width  = len(grid[0])

    visited: Set[Tuple[int, int]] = set()
    if show_path and path:
        visited = _path_cells(path, entry)

    pat: Set[Tuple[int, int]] = pattern_cells or set()

    for y in range(height):
        top = ""
        mid = ""

        for x in range(width):
            cell = grid[y][x]

            # ── Top border: corner + horizontal segment ──────────────────
            top += _corner_char(grid, x, y, wall_colour)
            if cell & N:
                top += _c("──", wall_colour)
            else:
                top += "  "

        # Close the right corner of this top row
        top += _corner_char(grid, width, y, wall_colour)

        # ── Cell body: left wall + interior ──────────────────────────────
        for x in range(width):
            cell = grid[y][x]

            # Left vertical wall
            if cell & W:
                mid += _c("│", wall_colour)
            else:
                mid += " "

            # Cell interior
            if (x, y) == entry:
                mid += _c("▶▶", FG["bright_green"])
            elif (x, y) == exit_pt:
                mid += _c("★★", FG["bright_red"])
            elif show_path and (x, y) in visited:
                mid += _c("··", FG["bright_cyan"])
            elif (x, y) in pat:
                mid += _c("░░", FG["bright_yellow"])
            else:
                mid += "  "

        # Close right edge wall
        if grid[y][width - 1] & E:
            mid += _c("│", wall_colour)
        else:
            mid += " "

        print(top)
        print(mid)

    # Final bottom border
    bot = ""
    for x in range(width):
        bot += _corner_char(grid, x, height, wall_colour)
        if grid[height - 1][x] & S:
            bot += _c("──", wall_colour)
        else:
            bot += "  "
    bot += _corner_char(grid, width, height, wall_colour)
    print(bot)


def _print_menu(show_path: bool, wall_name: str) -> None:
    """Render the interactive menu."""
    toggle = "🙈 Hide path" if show_path else "🧭 Show path"
    print()
    print(_c("╔══════════════════════╗", FG["bright_white"]))
    print(_c("║  ", FG["bright_white"]) +
          _c("  A-Maze-ing  🏰  ", FG["bright_yellow"]) +
          _c("  ║", FG["bright_white"]))
    print(_c("╠══════════════════════╣", FG["bright_white"]))
    print(_c("║", FG["bright_white"]) +
          "  1. 🔀 New maze          " +
          _c("║", FG["bright_white"]))
    print(_c("║", FG["bright_white"]) +
          f"  2. {toggle:<22}" +
          _c("║", FG["bright_white"]))
    print(_c("║", FG["bright_white"]) +
          f"  3. 🎨 Colour: {wall_name:<10}" +
          _c("║", FG["bright_white"]))
    print(_c("║", FG["bright_white"]) +
          "  4. 🚪 Quit              " +
          _c("║", FG["bright_white"]))
    print(_c("╚══════════════════════╝", FG["bright_white"]))
    print()


def run_display(
    grid: List[List[int]],
    entry: Tuple[int, int],
    exit_pt: Tuple[int, int],
    path: Optional[str],
    pattern_cells: Optional[Set[Tuple[int, int]]],
    regenerate_callback: object,
) -> None:
    """
    Launch the interactive terminal display loop.

    Args:
        grid:                 Initial maze grid.
        entry:                Entry (x, y).
        exit_pt:              Exit (x, y).
        path:                 BFS path string or None.
        pattern_cells:        '42' pattern cells.
        regenerate_callback:  Callable() -> (new_grid, new_path).
    """
    cb: Callable[[], Tuple[List[List[int]], Optional[str]]] = (
        regenerate_callback  # type: ignore[assignment]
    )

    show_path:    bool = False
    colour_index: int  = 0
    current_grid: List[List[int]] = grid
    current_path: Optional[str]   = path

    while True:
        _clear()
        render_maze(
            grid=current_grid,
            entry=entry,
            exit_pt=exit_pt,
            path=current_path,
            show_path=show_path,
            wall_colour=WALL_COLOURS[colour_index],
            pattern_cells=pattern_cells,
        )
        _print_menu(show_path, WALL_NAMES[colour_index])

        try:
            choice = input("Choice (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            sys.exit(0)

        if choice == "1":
            current_grid, current_path = cb()
            show_path = False
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            colour_index = (colour_index + 1) % len(WALL_COLOURS)
        elif choice == "4":
            print("Goodbye! 👋")
            sys.exit(0)
