import os
import time
import sys
from typing import List, Optional, Tuple
from src.solver.maze_data import MazeData
import random


class TerminalDisplay:
    def __init__(
        self,
        maze: MazeData,
        path: Optional[str] = "",
        pattern_cells: List[Tuple[int, int]] = None,
    ):
        self.maze = maze
        self.path = path
        self.pattern_cells = pattern_cells

        # ANSI Colors
        self.c_reset = "\033[0m"
        self.bg_42_pass = "\033[104m"

        self.WALL = "██"
        self.EMPTY = "  "
        self.path_char = "\033[33m██\033[0m"
        self.START = "\033[32m██\033[0m"
        self.EXIT = "\033[31m██\033[0m"

        self.path_is_visible = False

    def __random_color(self) -> tuple[str, str]:
        """Generates random ANSI color codes for walls and the 42 pattern."""
        number = random.randint(1, 4)

        if number == 1:
            return "\033[0;31m", "\033[106m"
        elif number == 2:
            return "\033[0;32m", "\033[105m"
        elif number == 3:
            return "\033[0;33m", "\033[103m"
        else:
            return "\033[0;34m", "\033[102m"

    def render(self, color_operation = False) -> None:
        try:
            print("\033[2J\033[H", end="", flush=True)

            if color_operation:
                wall_color, self.bg_42_pass = self.__random_color()
            else:
                wall_color = "\033[37m"
                self.bg_42_pass = "\033[104m"

            self.WALL = f"{wall_color}██{self.c_reset}"

            for y in range(self.maze.height):
                for row_part in range(3):
                    line = ""
                    for x in range(self.maze.width):
                        line += self.WALL * 3
                    print(line)
            if (color_operation == False):
                time.sleep(0.5)

            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    val = self.maze.get_walls(x, y)
                    sx, sy = x * 3, y * 3

                    is_42 = (x, y) in self.pattern_cells
                    p_char = f"{self.bg_42_pass}  {self.c_reset}" if is_42 else self.EMPTY

                    self._draw_at_canvas(sx + 1, sy + 1, p_char)

                    if not (val & 2):
                        self._draw_at_canvas(sx + 2, sy + 1, p_char)
                        self._draw_at_canvas(sx + 3, sy + 1, p_char)

                    if not (val & 4):
                        self._draw_at_canvas(sx + 1, sy + 2, p_char)
                        self._draw_at_canvas(sx + 1, sy + 3, p_char)

                    if (color_operation == False):
                        time.sleep(0.01)

            self._draw_special_points()
            print(f"\033[{(self.maze.height * 3) + 2};1H")
        except BaseException:
            os.system('clear')
            print("Generation Corrupted!")
            exit()

    def _draw_at_canvas(self, cx: int, cy: int, char: str) -> None:
        tx = (cx * 2) + 1
        ty = cy + 1
        print(f"\033[{ty};{tx}H{char}", end="", flush=True)

    def _draw_special_points(self) -> None:
        ex, ey = self.maze.entry
        bg_s = self.bg_42_pass if (ex, ey) in self.pattern_cells else ""
        self._draw_at_canvas(
            ex * 3 + 1, ey * 3 + 1, f"{bg_s}{self.START}{self.c_reset}"
        )

        xx, xy = self.maze.exit
        bg_e = self.bg_42_pass if (xx, xy) in self.pattern_cells else ""
        self._draw_at_canvas(xx * 3 + 1, xy * 3 + 1, f"{bg_e}{self.EXIT}{self.c_reset}")

    def show_path(self):
        if self.path:
            if self.path_is_visible == False:
                char_to_draw = self.path_char
                self.path_is_visible = True
            else:
                char_to_draw = self.EMPTY
                self.path_is_visible = False

            cx, cy = self.maze.entry

            if (cx, cy) != self.maze.entry and (cx, cy) != self.maze.exit:
                self._draw_at_canvas(cx * 3 + 1, cy * 3 + 1, char_to_draw)

            for direction in self.path:
                sx, sy = cx * 3, cy * 3

                if direction == "E":
                    self._draw_at_canvas(sx + 2, sy + 1, char_to_draw)
                    self._draw_at_canvas(sx + 3, sy + 1, char_to_draw)
                    cx += 1
                elif direction == "S":
                    self._draw_at_canvas(sx + 1, sy + 2, char_to_draw)
                    self._draw_at_canvas(sx + 1, sy + 3, char_to_draw)
                    cy += 1
                elif direction == "W":
                    self._draw_at_canvas(sx, sy + 1, char_to_draw)
                    self._draw_at_canvas(sx - 1, sy + 1, char_to_draw)
                    cx -= 1
                elif direction == "N":
                    self._draw_at_canvas(sx + 1, sy, char_to_draw)
                    self._draw_at_canvas(sx + 1, sy - 1, char_to_draw)
                    cy -= 1

                time.sleep(0.01)


                if (cx, cy) != self.maze.entry and (cx, cy) != self.maze.exit:
                    self._draw_at_canvas(cx * 3 + 1, cy * 3 + 1, char_to_draw)

        self._draw_special_points()
        print(f"\033[{(self.maze.height * 3) + 2};1H")
