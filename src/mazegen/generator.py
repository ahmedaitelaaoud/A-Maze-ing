import random
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

    def _42_pattern(self, visited_set):
        pass
