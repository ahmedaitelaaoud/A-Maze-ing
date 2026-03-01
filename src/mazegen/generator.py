import random
import sys
from typing import Optional, List, Set, Tuple


class test:
    pass

class MazeGenerator:
    """
    A reusable class for generating mazes.
    Set PERFECT=True for a perfect maze (single path between any two points).
    Set PERFECT=False for an imperfect maze (multiple paths / loops).
    """

    # 1. Bitmask Constants (Power of 2)
    N = 1
    E = 2
    S = 4
    W = 8
    ALL_WALLS = 15  # Binary 1111: all four walls are closed.

    # GPS Dictionary: (dx, dy, opposite_wall)
    DIRECTIONS = {
        N: (0, -1, S),
        E: (1, 0, W),
        S: (0, 1, N),
        W: (-1, 0, E)
    }

    # ── Config ──────────────────────────────────────────────────────────────
    LOOP_FACTOR = 0.15   # % of extra walls removed when PERFECT=False

    def __init__(self, width: int, height: int, perfect: bool = True, seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.perfect = perfect    # ← stores it so generate() can read self.perfect
        self.seed = seed
        self.grid = [[self.ALL_WALLS for _ in range(width)] for _ in range(height)]
        self.patern_cells = self._get_42_pattern_cells()

    def _get_42_pattern_cells(self) -> Set[Tuple[int, int]]:
        """
        Calculates the coordinates of the '42' pattern to be placed in the center.

        Returns:
            set[tuple[int, int]]: A set of (x, y) coordinates representing the pattern.
        """
        pattern_cells: Set[Tuple[int, int]] = set()

        if self.width < 9 or self.height < 7:
            print("Error: Maze too small for '42' pattern", file=sys.stderr)
            return pattern_cells

        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        pattern_offsets = [
            (0,0), (2,0), (0,1), (2,1), (0,2), (1,2), (2,2), (2,3), (2,4),
            (4,0), (5,0), (6,0), (6,1), (4,2), (5,2), (6,2), (4,3), (4,4), (5,4), (6,4)
        ]

        for dx, dy in pattern_offsets:
            x, y = start_x + dx, start_y + dy
            pattern_cells.add((x, y))

        return pattern_cells

    def generate(self) -> List[List[int]]:
        """
        Carve a maze using the iterative Recursive Backtracker.
        If PERFECT=False, extra walls are removed after generation to create loops.

        Returns:
            list[list[int]]: The generated 2D grid containing wall bitmasks.
        """
        if self.seed is not None:
            random.seed(self.seed)

        visited: Set[Tuple[int, int]] = set(self.patern_cells)
        stack: List[Tuple[int, int]] = []

        # Find the first non-pattern cell to start from
        start_x, start_y = 0, 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in visited:
                    start_x, start_y = x, y
                    break
            else:
                continue
            break

        start = (start_x, start_y)
        visited.add(start)
        stack.append(start)

        while stack:
            cx, cy = stack[-1]
            unvisited = []

            for wall, (dx, dy, opp) in self.DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        unvisited.append((wall, nx, ny, opp))

            if unvisited:
                wall, nx, ny, opp = random.choice(unvisited)
                # Remove wall between current cell and chosen neighbor
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # ── If PERFECT=False, punch extra holes to create loops ──────────
        if not self.perfect:
            self._add_loops()

        return self.grid

    # ────────────────────────────────────────────────────────────────────────
    # HELPER: Check if two adjacent cells already have an open passage
    # Uses the bitmask grid that your class already maintains
    # ────────────────────────────────────────────────────────────────────────
    def _are_connected(self, x: int, y: int, nx: int, ny: int) -> bool:
        """
        Returns True if the wall between (x,y) and (nx,ny) is already removed.
        Works by checking the bitmask of the current cell.

        How it works:
          - dx/dy tells us which direction the neighbor is in
          - We find the matching wall bitmask (N/E/S/W)
          - If that bit is 0 in self.grid[y][x], the wall is gone -> connected
        """
        dx, dy = nx - x, ny - y
        # Find which wall constant matches this direction
        for wall, (ddx, ddy, _) in self.DIRECTIONS.items():
            if ddx == dx and ddy == dy:
                # Bit is 0 means wall was removed (passage exists)
                return (self.grid[y][x] & wall) == 0
        return False

    # ────────────────────────────────────────────────────────────────────────
    # HELPER: Remove the wall between two adjacent cells (both sides)
    # ────────────────────────────────────────────────────────────────────────
    def _remove_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        """
        Opens the passage between (x,y) and (nx,ny) by clearing
        the wall bit on BOTH sides (your bitmask grid requires this).

        How it works:
          - Find which wall bitmask matches the direction to the neighbor
          - &= ~wall clears that bit in the current cell
          - Do the same for the opposite wall in the neighbor cell
        """
        dx, dy = nx - x, ny - y
        for wall, (ddx, ddy, opp) in self.DIRECTIONS.items():
            if ddx == dx and ddy == dy:
                self.grid[y][x] &= ~wall   # Remove wall on current cell side
                self.grid[ny][nx] &= ~opp  # Remove opposite wall on neighbor side
                return

    # ────────────────────────────────────────────────────────────────────────
    # MAIN: Add loops to make the maze imperfect (PERFECT=False)
    # ────────────────────────────────────────────────────────────────────────
    def _add_loops(self) -> None:
        """
        Randomly removes extra walls to create multiple paths (loops).
        Only runs when PERFECT=False.

        How it works:
          1. Calculate how many extra passages to add (LOOP_FACTOR % of all cells)
          2. Pick a random cell and a random neighbor direction
          3. If they are NOT already connected -> remove the wall between them
          4. Skip pattern cells (the '42' logo) so we don't break it
          5. Repeat until we've added enough extra passages
        """
        extra_passages = int(self.width * self.height * self.LOOP_FACTOR)
    # extra_passages = 90
        attempts = 0
        added = 0

        while added < extra_passages and attempts < extra_passages * 10:
            attempts += 1

            # Pick a random cell
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            # Skip cells that are part of the '42' pattern
            if (x, y) in self.patern_cells:
                continue

            # Pick a random neighbor direction
            wall, (dx, dy, opp) = random.choice(list(self.DIRECTIONS.items()))
            nx, ny = x + dx, y + dy

            # Check bounds
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            # Skip if neighbor is part of the '42' pattern
            if (nx, ny) in self.patern_cells:
                continue

            # Only remove wall if it's still standing (avoid doing nothing)
            if not self._are_connected(x, y, nx, ny):
                self._remove_wall(x, y, nx, ny)
                added += 1
