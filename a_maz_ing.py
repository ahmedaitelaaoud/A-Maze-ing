import sys
from src.utils.config import parse_config, validate_config
from src.mazegen import MazeGenerator

def main() -> None:
    # 1. Subject requirement: Check arguments
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>", file=sys.stderr)
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # 2. Parse and validate the configuration
        raw_config = parse_config(config_file)
        config = validate_config(raw_config)

        # 3. Instantiate the Maze Generator
        generator = MazeGenerator(width=config["WIDTH"], height=config["HEIGHT"])

        # 4. Generate the grid
        grid = generator.generate()

        # --- HANDOFF TO STUDENT 2 ---
        print("Maze generated successfully! (Passing to display...)")
        # display.render(grid, config["ENTRY"], config["EXIT"])

    except (FileNotFoundError, ValueError) as e:
        # Subject requirement: Graceful error handling, no ugly crashes
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
