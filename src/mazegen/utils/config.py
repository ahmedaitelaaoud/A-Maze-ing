import sys
from typing import Dict, Any


def parse_config(filepath: str) -> Dict[str, str]:
    """
    Parse a KEY=VALUE configuration safely.

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        Dict[str, str]: A dictionary containing the parsed settings.
    """
    settings = {}
    try:
        # Open the file
        with open(filepath, 'r') as file:
            for line in file:
                # Clean it
                clean_line = line.strip()
                # Skip empty line
                if not clean_line or '=' not in clean_line:
                    continue
                # Split by "="
                splitted = clean_line.split("=", 1)
                key = splitted[0].strip()
                value = splitted[1].strip()
                settings[key] = value

        return settings

    except FileNotFoundError:
        print(f"File not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)

def validate_config(raw_settings: Dict[str, str]) -> Dict[str, any]:
    """
    Validate and convert raw configuration strings into strict Python types.

    Args:
        raw_settings (Dict[str, str]): The raw dictionary of strings.

    Returns:
        Dict[str, Any]: A clean dictionary with proper ints, tuples, and bools.
    """
    clean_settings = {}
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT"]
    # Check if all setting in
    for key in mandatory_keys:
        if key not in raw_settings:
            print(f"Error: Missing mandatory setting '{key}", file=sys.stderr)
            sys.exit(1)

    # Handling Errors
    try:
        clean_settings["WIDTH"] = int(raw_settings["WIDTH"])
        clean_settings["HEIGHT"] = int(raw_settings["HEIGHT"])
        # Handle HEIGHT and WIDTH must be 3x3 and more
        if clean_settings["WIDTH"] < 3 or clean_settings["HEIGHT"] < 3:
            print("Error: WIDH and HEIGHT must be at least 3", file=sys.stderr)
            sys.exit(1)

    except ValueError as e:
        print("Error: WIDTH and HEIGHT must be valid numbers!", file=sys.stderr)
        sys.exit(1)

    # Parse ENTRY and EXIT
    try:
        # Split coordinates
        entry_part = raw_settings["ENTRY"].split(",")
        exit_part = raw_settings["EXIT"].split(",")
        # Convert to int and put them in tuple
        clean_settings["ENTRY"] = (int(entry_part[0]), int(entry_part[1]))
        clean_settings["EXIT"] = (int(exit_part[0]), int(exit_part[1]))

        entry_x, entry_y = clean_settings["ENTRY"]
        exit_x, exit_y = clean_settings["EXIT"]
        w, h = clean_settings["WIDTH"], clean_settings["HEIGHT"]

        # 1. Check if ENTRY is within bounds
        if not (0 <= entry_x < w and 0 <= entry_y < h):
            print(f"Error: ENTRY {entry_x, entry_y} is out of bounds for {w}x{h} maze.", file=sys.stderr)
            sys.exit(1)

        # 2. Check if EXIT is within bounds
        if not (0 <= exit_x < w and 0 <= exit_y < h):
            print(f"Error: ENTRY {exit_x, exit_y} is out of bounds for {w}x{h} maze.", file=sys.stderr)
            sys.exit(1)

        # 3. Check if ENTRY and EXIT are different
        if (entry_x, entry_y) == (exit_x, exit_y):
            print("Error: ENTRY and EXIT must be different coordinates.", file=sys.stderr)
            sys.exit(1)
    except (ValueError, IndexError):
        print("Error: ENTRY and EXIT must be in format X,Y (e.g., 0,0)", file=sys.stderr)
        sys.exit(1)

    # 1. Handle PERFECT
    perfect_str = raw_settings.get("PERFECT", "True")
    clean_settings["PERFECT"] = (perfect_str.lower() == "true")

    # 2. Handle OUTPUT_FILE
    clean_settings["OUTPUT_FILE"] = raw_settings.get("OUTPUT_FILE", "maze.txt")

    return clean_settings

if __name__ == "__main__":
    a = (parse_config("../../../default_config.txt"))
    validate_config(a)
