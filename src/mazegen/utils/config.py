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
                # Skip empty line and comments
                if not clean_line or clean_line.startswith('#'):
                    continue

                if '=' not in clean_line:
                    raise ValueError(f"Invalid format (missing '='): {clean_line}")
                # Split by "="
                splitted = clean_line.split("=", 1)
                key = splitted[0].strip()
                value = splitted[1].strip()
                settings[key] = value

        return settings

    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at '{filepath}'")

def validate_config(raw_settings: Dict[str, str]) -> Dict[str, Any]:
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
            raise ValueError(f"Error: Missing mandatory setting '{key}'")

    # 1. Validate Dimensions
    try:
        clean_settings["WIDTH"] = int(raw_settings["WIDTH"])
        clean_settings["HEIGHT"] = int(raw_settings["HEIGHT"])
        w, h = clean_settings["WIDTH"], clean_settings["HEIGHT"]
        # Handle HEIGHT and WIDTH must be 3x3 and more
        if w < 3 or h < 3:
            raise ValueError("Error: WIDH and HEIGHT must be at least 3")  # typo: WIDH
    except ValueError as e:
        raise ValueError("Error: WIDTH and HEIGHT must be valid numbers!")  # swallows the above!

    except ValueError as e:
        raise ValueError("Error: WIDTH and HEIGHT must be valid numbers!")

    # 2. Validate Coordinates
    try:
        # Split coordinates
        entry_part = raw_settings["ENTRY"].split(",")
        exit_part = raw_settings["EXIT"].split(",")


        if len(entry_part) != 2 or len(exit_part) != 2:
            raise ValueError("ENTRY and EXIT must be exactly X,Y format.")

        # Convert to int and put them in tuple
        clean_settings["ENTRY"] = (int(entry_part[0]), int(entry_part[1]))
        clean_settings["EXIT"] = (int(exit_part[0]), int(exit_part[1]))

        entry_x, entry_y = clean_settings["ENTRY"]
        exit_x, exit_y = clean_settings["EXIT"]


        # Bounds checking
        if not (0 <= entry_x < w and 0 <= entry_y < h):
            raise ValueError(f"ENTRY ({entry_x}, {entry_y}) is out of bounds for {w}x{h} maze.")
        if not (0 <= exit_x < w and 0 <= exit_y < h):
            raise ValueError(f"EXIT ({exit_x}, {exit_y}) is out of bounds for {w}x{h} maze.")
        if (entry_x, entry_y) == (exit_x, exit_y):
            raise ValueError("ENTRY and EXIT must be different coordinates.")
    except (ValueError, IndexError):
        raise ValueError("Error: ENTRY and EXIT must be in format X,Y (e.g., 0,0)")

    # 3. Handle PERFECT and OUTPUT_FILE
    perfect_str = raw_settings.get("PERFECT", "True")
    clean_settings["PERFECT"] = (perfect_str.lower() == "true")
    clean_settings["OUTPUT_FILE"] = raw_settings.get("OUTPUT_FILE", "maze.txt")

    return clean_settings
