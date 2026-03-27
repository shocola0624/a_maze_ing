from typing import Dict, Tuple, Optional
from config_utils.keys import Keys as CK


def validate_config(config_data: Optional[Dict[str, str]]) -> Optional[str]:
    """Validate and normalize maze configuration data in place.

    Args:
        config_data: Raw config mapping read from the config file.

    Returns:
        An error message string if validation fails, otherwise None.
    """
    if config_data is None:
        exit()

    for enum_key in CK:
        if enum_key.value in config_data:
            old_value = config_data.pop(enum_key.value)
            config_data[enum_key] = old_value

    required_keys = (
        CK.WIDTH,
        CK.HEIGHT,
        CK.ENTRY,
        CK.EXIT,
        CK.PERFECT,
        CK.OUTPUT_FILE
    )

    # required key
    for required_key in required_keys:
        if required_key not in config_data:
            return (
                f"Error: Missing required key '{required_key.value}' "
                "in configuration."
            )

    for actual_key in config_data.keys():
        if isinstance(actual_key, str):
            return (
                f"Error: Unknown key '{actual_key}' "
                "found in config_file."
            )

    # WIDTH, HEIGHT
    try:
        width_val = int(config_data[CK.WIDTH])
        height_val = int(config_data[CK.HEIGHT])
    except ValueError:
        return "Error: WIDTH and HEIGHT must be integer values."

    if width_val <= 0 or height_val <= 0:
        return "Error: WIDTH and HEIGHT must be positive integers."

    config_data[CK.WIDTH] = width_val
    config_data[CK.HEIGHT] = height_val

    # ENTRY, EXIT
    def parse_coordinate(coord_str: str) -> Optional[Tuple[int, int]]:
        """Parse an "x, y" coordinate string into a tuple of two integers.

        Args:
            coord_str: Coordinate string.

        Returns:
            A tuple `(x, y)` if parsing succeeds, otherwise None.
        """
        parts = coord_str.split(",")
        if len(parts) != 2:
            return None
        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            return None

    entry_val = parse_coordinate(config_data[CK.ENTRY])

    if entry_val is None:
        return "Error: ENTRY must be formatted as integer 'x,y'."

    exit_val = parse_coordinate(config_data[CK.EXIT])

    if exit_val is None:
        return "Error: EXIT must be formatted as integer 'x,y'."
    if not (0 <= entry_val[0] < width_val and 0 <= entry_val[1] < height_val):
        return f"Error: ENTRY {entry_val} is outside boundaries."
    if not (0 <= exit_val[0] < width_val and 0 <= exit_val[1] < height_val):
        return f"Error: EXIT {exit_val} is outside boundaries."
    if entry_val == exit_val:
        return "Error: ENTRY and EXIT must be at different positions."

    width, height = width_val, height_val
    if width > 9 and height > 7:
        center = (width + (width % 2 == 0), height + (height % 2 == 0))
        c_x, c_y = center
        coord_on_42 = [
            (-6, -4), (-6, -2), (-6, 0), (-4, 0), (-2, 0), (-2, 2), (-2, 4),
            (2, -4), (4, -4), (6, -4), (6, -2), (6, 0), (4, 0), (2, 0), (2, 2),
            (2, 4), (4, 4), (6, 4)
        ]
        en = tuple(i * 2 + 1 for i in entry_val)
        ex = tuple(i * 2 + 1 for i in exit_val)
        for x, y in coord_on_42:
            if (en == (c_x+x, c_y+y) or ex == (c_x+x, c_y+y)):
                return "Error: ENTRY and EXIT must not be on 42 pattern."

    config_data[CK.ENTRY] = entry_val
    config_data[CK.EXIT] = exit_val

    # PERFECT
    perfect_str = str(config_data[CK.PERFECT]).strip().lower()
    if perfect_str == "true":
        config_data[CK.PERFECT] = True
    elif perfect_str == "false":
        config_data[CK.PERFECT] = False
    else:
        return "Error: PERFECT must be either 'True' or 'False'."

    # SEED, WAIT_SEC
    try:
        seed_value = int(config_data[CK.SEED])
        config_data[CK.SEED] = seed_value
    except ValueError:
        return "Error: SEED must be integer values."
    except KeyError:
        pass
    try:
        wait_sec = float(config_data[CK.WAIT_SEC])
        config_data[CK.WAIT_SEC] = wait_sec
    except ValueError:
        return "Error: WAIT_SEC must be float values."
    except KeyError:
        config_data[CK.WAIT_SEC] = 0.0

    return None


if __name__ == "__main__":
    print("=== test1: valid_data ===")
    valid_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt"
    }
    err1 = validate_config(valid_data.copy())
    print(f"Return error: {err1}")
    print(f"Data after conversion: {valid_data}\n")

    print("=== test2: missing_keys ===")
    missing_data = {
        "WIDTH": "10",
        "HEIGHT": "10"
    }
    err2 = validate_config(missing_data)
    print(f"Return error: {err2}\n")

    print("=== test3: extra_data ===")
    extra_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt",
        "Extra_info": "Brue"
    }
    err3 = validate_config(extra_data)
    print(f"Return error: {err3}\n")

    print("=== test4: out_of_bounds ===")
    out_of_bounds_data = {
        "WIDTH": "5",
        "HEIGHT": "5",
        "ENTRY": "10,10",  # Out of bounds
        "EXIT": "1,1",
        "PERFECT": "False",
        "OUTPUT_FILE": "maze.txt"
    }
    err4 = validate_config(out_of_bounds_data)
    print(f"Return error: {err4}\n")

    print("=== test5: invalid_size ===")
    invalid_size_data = {
        "WIDTH": "-5",     # Negative value
        "HEIGHT": "abc",   # Not an integer
        "ENTRY": "0,0",
        "EXIT": "1,1",
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt"
    }
    err5 = validate_config(invalid_size_data)
    print(f"Return error: {err5}\n")

    print("=== test6: invalid_coord_format ===")
    invalid_coord_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0-0",    # No comma
        "EXIT": "a,b",     # Not integers
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt"
    }
    err6 = validate_config(invalid_coord_data)
    print(f"Return error: {err6}\n")

    print("=== test7: same_entry_exit ===")
    same_pos_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "5,5",
        "EXIT": "5,5",     # Same position
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt"
    }
    err7 = validate_config(same_pos_data)
    print(f"Return error: {err7}\n")

    print("=== test8: invalid_perfect ===")
    invalid_perfect_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "PERFECT": "Yes",  # Not True/False
        "OUTPUT_FILE": "maze.txt"
    }
    err8 = validate_config(invalid_perfect_data)
    print(f"Return error: {err8}\n")

    print("=== test9: none_input ===")
    err9 = validate_config(None)
    print(f"Return error: {err9}\n")
