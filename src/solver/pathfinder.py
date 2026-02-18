from src.solver.maze_data import MazeData




class Pathfinder:
    def __init__(self, maze: MazeData):
        self.maze = maze  # <-- We save the map here!

    def solve(self):
        # ... inside your BFS loop ...

        # YOU USE IT HERE: "Hey map, what are the walls at this coordinate?"
