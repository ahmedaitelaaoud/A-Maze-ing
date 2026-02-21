*This project has been created as part of the 42 curriculum by aait-ela, yrabhi.*

## Description
A-Maze-ing is a Python-based maze generation and visualization tool. It reads configuration parameters from a file, safely generates a perfect maze including a hidden "42" pattern, and visually displays the result alongside the shortest path solution.

## Maze Generation Algorithm (aait-ela)

### Algorithm Choice
We chose the **Iterative Recursive Backtracker** algorithm to generate the maze.

### Why this algorithm?
1. **Perfect Mazes:** The backtracker acts as a Depth-First Search (DFS) that visits every cell exactly once without creating loops. This mathematically guarantees a "perfect maze" (a spanning tree) with exactly one valid path between the ENTRY and EXIT.
2. **Strict Corridor Limits:** The subject requires that no corridors are wider than 2 cells. The Recursive Backtracker inherently carves paths exactly 1 cell wide, automatically satisfying this constraint.
3. **Iterative vs. Recursive:** Standard recursion in Python is limited (usually 1000 calls). By using an iterative approach with a manual `stack`, we avoid `RecursionError` crashes on large mazes, ensuring the program handles errors gracefully.

## Reusable `mazegen` Module (aait-ela)

The core maze generation logic has been isolated into a standalone Python package called `mazegen`. It is fully independent of the display and pathfinding logic.

### Installation
You can install the package using the provided build files located at the root of the repository:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
# OR
pip install mazegen-1.0.0.tar.gz
