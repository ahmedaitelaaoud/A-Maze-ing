from src.solver.maze_data import MazeData


class HexWriter:

    def __init__(self, maze: MazeData, path: str, output_path: str):
        self.maze = maze
        self.path = path
        self.output_path = output_path

    def __get_cell_hex(self, x: int, y: int) -> str:
        value = self.maze.get_walls(x, y)
        hex_value = hex(value).upper()
        return hex_value[2:]

    def write(self) -> None:

        with open(self.output_path, "w") as f:

            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    f.write(self.__get_cell_hex(x, y))
                f.write("\n")

            f.write("\n")
            f.write(f"{self.maze.entry[0]},{self.maze.entry[1]}\n")
            f.write(f"{self.maze.exit[0]},{self.maze.exit[1]}\n")
            f.write(f"{self.path}\n")
