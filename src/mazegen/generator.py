import random
import sys
from typing import Optional, List, Set, Tuple

class MazeGenerator:
    """
    A reusable class for generating perfect mazes.
    """
    # 1. Bitmask Constants (Power of 2)
    N, E, S, W = 1, 2, 4, 8
    ALL_WALLS = 15 # Binary 1111: all four walls are closed.
    # GPS Dictionary: (dx, dy, opposite_wall)
    DIRECTIONS = {
        N: (0, -1, S),
        E: (1, 0, W),
        S: (0, 1, N),
        W: (-1, 0, E)
    }

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """Initialize parameters and create the empty grid."""
        self.width = width
        self.height = height
        self.seed = seed
        # Initialize grid with all walls closed for every cell.
        self.grid = [[self.ALL_WALLS for _ in range(width)] for _ in range(height)]
        print(self.grid)

    def _get_42_pattern_cells(self) -> Set[Tuple[int, int]]:
        """Calculates and returns the coordinates of the 42 pattern."""
        pattern_cells: Set[Tuple[int, int]] = set()

        # Subject requirement: Print error if too small
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

    def generate(self) -> List[list[int]]:
        """
        Carve a perfect maze using the iterative Recursive Backtracker.
        """
        # Set the seed for reproducibility
        if self.seed is not None:
            random.seed(self.seed)

        visited: Set[Tuple[int, int]] = set()
        stack: List[Tuple[int, int]] = []

        start = (0, 0)
        # Failsafe: Ensure (0,0) isn't accidentally part of the 42 pattern in tiny mazes
        if start not in visited:
            visited.add(start)
            stack.append(start)
        while stack:
            # First, I look at my current coordinates (cx, cy) by checking the very last step in my GPS memory (stack[-1])
            cx, cy = stack[-1]
            # unvisited to write down any valid rooms I can dig into next
            unvisited = []

            # Check neighbors in all 4 cardinal directions
            for wall, (dx, dy, opp) in self.DIRECTIONS.items():
                nx, ny = cx + dx, cy + dy

                # Verify the neighbor is within bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        unvisited.append((wall, nx, ny, opp))

            if unvisited:
                # Move forward: Pick a random neighbor
                wall, nx, ny, opp = random.choice(unvisited)

                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opp

                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Backtrack: Pop from stack when at a dead end.
                stack.pop()

        return self.grid
