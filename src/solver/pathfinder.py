"""
Pathfinder module using Breadth-First Search (BFS).
Guarantees the shortest path from entry to exit.
"""

from collections import deque
from typing import Set, Tuple, Deque
from src.solver.maze_data import MazeData


class Pathfinder:
    """
    Solves the maze using a BFS algorithm.
    """

    def __init__(self, maze: MazeData):
        """
        Initializes the Pathfinder with the read-only MazeData.
        """
        self.maze = maze

    def solve(self) -> str:
        """
        Finds the shortest path from entry to exit using BFS.

        Returns:
            str: A string of directions (N, E, S, W) representing the path.
                 Returns an empty string if no path exists.
        """
        # EDGE CASE: If entry and exit are the same room
        if self.maze.entry == self.maze.exit:
            return ""

        # 1. THE QUEUE: Stores tuples of ((x, y), "path_taken_so_far")
        queue: Deque[Tuple[Tuple[int, int], str]] = deque([(self.maze.entry, "")])

        # 2. THE NOTEBOOK: Stores coordinates we have already visited
        visited: Set[Tuple[int, int]] = {self.maze.entry}

        # 3. THE COMPASS: (change_in_x, change_in_y, binary_wall_bit, letter)
        # 1=North, 2=East, 4=South, 8=West
        directions = [
            (0, -1, 1, "N"),
            (1, 0, 2, "E"),
            (0, 1, 4, "S"),
            (-1, 0, 8, "W")
        ]

        # 4. THE BFS LOOP
        while queue:
            # Get the next person in line
            (cx, cy), current_path = queue.popleft()

#0100
#1000

# queue =  0, 0 ""|0,-1"N"|1,-1"NE"|1,0"NES"|0,0"NESW"
# current_walls = 4
#cx, cy = 0, 0
# nx, ny = 0,0
#new_path = N
            # Ask the map for the walls in this specific room
            current_walls = self.maze.get_walls(cx, cy)

            # Check all 4 walls
            for dx, dy, wall_bit, letter in directions:

                # BITWISE MATH: If the result is 0, the door is OPEN
                if (current_walls & wall_bit) != 0:

                    # Calculate the coordinate of the next room
                    nx, ny = cx + dx, cy + dy

                    # If we haven't visited this room yet
                    if (nx, ny) not in visited:
                        new_path = current_path + letter

                        # WIN CONDITION: Did we just step on the exit?
                        if (nx, ny) == self.maze.exit:
                            return new_path

                        # Otherwise, write it in the notebook and get in line
                        visited.add((nx, ny))
                        queue.append(((nx, ny), new_path))

        # 5. NO PATH FOUND
        return ""
