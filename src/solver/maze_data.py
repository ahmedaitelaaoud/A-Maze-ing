from dataclasses import dataclass
from typing import List, Tuple




@dataclass(frozen=True)
class MazeData:

    grid_result: List[List[int]]
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]

    def get_walls(self, x: int, y: int) -> int:
        """
        Safely gets the walls at (x, y).
        Returns 15 (solid block) if outside the map.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid_result[y][x]
        return 15

grid = [
    [10, 20],
    [88, 90],
    [19, 67],
]

entry = (0, 0)
exit = (19, 19)


a = MazeData(grid, 20, 10, entry, exit)

# a.entry = 1000
print(a.entry)
