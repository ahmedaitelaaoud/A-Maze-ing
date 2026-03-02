import random
import sys
from typing import Optional, List, Set, Tuple

class MazeGenerator:
    """
    A reusable class for generating mazes.
    Set PERFECT=True for a perfect maze (single path between any two points).
    Set PERFECT=False for an imperfect maze (multiple paths / loops).
    """

    N = 1
    E = 2
    S = 4
    W = 8
    ALL_WALLS = 15

    DIRECTIONS = {
        N: (0, -1, S),
        E: (1, 0, W),
        S: (0, 1, N),
        W: (-1, 0, E)
    }

    LOOP_FACTOR = 0.15

    def __init__(self, width: int, height: int, perfect: bool = True,
                 algorithm: str = "DFS", seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.perfect = perfect
        self.algorithm = algorithm.lower()
        self.seed = seed
        self.grid = [[self.ALL_WALLS for _ in range(width)] for _ in range(height)]
        self.pattern_cells = self._get_42_pattern_cells()

    def _get_42_pattern_cells(self) -> Set[Tuple[int, int]]:
        """Calculates the coordinates of the '42' pattern."""
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
            pattern_cells.add((start_x + dx, start_y + dy))

        return pattern_cells

    def generate(self) -> List[List[int]]:
        """
        Orchestrates maze generation based on the selected algorithm.
        If PERFECT=False, extra walls are removed to create loops.

        Returns:
            list[list[int]]: The generated 2D grid containing wall bitmasks.
        """
        random.seed(self.seed)

        if self.algorithm == "dfs" or self.algorithm == "backtracker":
            self._generate_backtracker()
        elif self.algorithm == "prim":
            self._generate_prim()
        else:
            print(f"Error: Unknown algorithm '{self.algorithm}'. Defaulting to DFS.", file=sys.stderr)
            self._generate_backtracker()

        if not self.perfect:
            self._add_loops()

        return self.grid

    def _generate_backtracker(self) -> None:
        """Carves a maze using the iterative Recursive Backtracker algorithm."""
        visited: Set[Tuple[int, int]] = set(self.pattern_cells)
        stack: List[Tuple[int, int]] = []

        start = (0, 0)
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
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def _generate_prim(self) -> None:
        """
        Carves a maze using randomized Prim's algorithm.
        Creates highly branched mazes with short dead ends.
        """
        visited: Set[Tuple[int, int]] = set(self.pattern_cells)

        frontier: List[Tuple[int, int, int, int, int, int]] = []
        def add_to_frontier(cx: int, cy: int) -> None:
            """Finds unvisited neighbors of a cell and adds the connecting walls to the frontier."""
            for wall, (dx, dy, opp) in self.DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        frontier.append((cx, cy, nx, ny, wall, opp))

        start_x, start_y = 0, 0
        visited.add((start_x, start_y))
        add_to_frontier(start_x, start_y)

        while frontier:
            idx = random.randint(0, len(frontier) - 1)
            cx, cy, nx, ny, wall, opp = frontier.pop(idx)

            if (nx, ny) not in visited:

                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp

                visited.add((nx, ny))
                add_to_frontier(nx, ny)

    def _are_connected(self, x: int, y: int, nx: int, ny: int) -> bool:
        """Returns True if the wall between (x,y) and (nx,ny) is already removed."""
        dx, dy = nx - x, ny - y
        for wall, (ddx, ddy, _) in self.DIRECTIONS.items():
            if ddx == dx and ddy == dy:
                return (self.grid[y][x] & wall) == 0
        return False

    def _remove_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        """Opens the passage between (x,y) and (nx,ny)."""
        dx, dy = nx - x, ny - y
        for wall, (ddx, ddy, opp) in self.DIRECTIONS.items():
            if ddx == dx and ddy == dy:
                self.grid[y][x] &= ~wall
                self.grid[ny][nx] &= ~opp
                return

    def _add_loops(self) -> None:
        """Randomly removes extra walls to create multiple paths (loops)."""
        extra_passages = int(self.width * self.height * self.LOOP_FACTOR)
        attempts = 0
        added = 0

        while added < extra_passages and attempts < extra_passages * 10:
            attempts += 1
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if (x, y) in self.pattern_cells:
                continue

            wall, (dx, dy, opp) = random.choice(list(self.DIRECTIONS.items()))
            nx, ny = x + dx, y + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if (nx, ny) in self.pattern_cells:
                continue

            if not self._are_connected(x, y, nx, ny):
                self._remove_wall(x, y, nx, ny)
                added += 1
