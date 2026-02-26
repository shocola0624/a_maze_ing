from typing import Dict, Optional
from config_utils.keys import keys as CK


def validate_config(config_data: Optional[Dict[str, str]]) -> Optional[str]:
    """
    [TODO]
    """
    # 1
    if config_data is None:
        return "Error: config_data is None."

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

    for required_key in required_keys:
        if required_key not in config_data:
            return f"Error: Missing required key '{required_key.value}' in configuration."

    for actual_key in config_data.keys():
        if isinstance(actual_key, str):
            return f"Error: Unknown key '{actual_key}' found in config_file."

    try:
        width_val = int(config_data[CK.WIDTH])
        height_val = int(config_data[CK.HEIGHT])
    except ValueError:
        return "Error: WIDTH and HEIGHT must be integer values."

    if width_val <= 0 or height_val <= 0:
        return "Error: WIDTH and HEIGHT must be positive integers."

    config_data[CK.WIDTH] = width_val
    config_data[CK.HEIGHT] = height_val

    def parse_coordinate(coord_str: str) -> Optional[tuple[int, int]]:
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

    config_data[CK.ENTRY] = entry_val
    config_data[CK.EXIT] = exit_val

    perfect_str = str(config_data[CK.PERFECT]).strip().lower()
    if perfect_str == "true":
        config_data[CK.PERFECT] = True
    elif perfect_str == "false":
        config_data[CK.PERFECT] = False
    else:
        return "Error: PERFECT must be either 'True' or 'False'."
    return None


if __name__ == "__main__":
    print("=== test1: good_data ===")
    valid_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt"
    }
    err1 = validate_config(valid_data)
    print(f"Return error: {err1}")
    print(f"Data after conversion: {valid_data}")

    print("=== test2: Missing keys ===")
    missing_data = {
        "WIDTH": "10",
        "HEIGHT": "10"
    }
    err2 = validate_config(missing_data)
    print(f"Return error {err2}")

    print("=== test3: extra_data ===")
    valid_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "PERFECT": "True",
        "OUTPUT_FILE": "maze.txt",
        "Extra_info": "Brue"
    }
    err3 = validate_config(valid_data)
    print(f"Return error: {err3}")

    print("=== test4: excess_data ===")
    out_of_bounds_data = {
        "WIDTH": "5",
        "HEIGHT": "5",
        "ENTRY": "10,10",
        "EXIT": "1,1",
        "PERFECT": "False",
        "OUTPUT_FILE": "maze.txt"
    }
    err4 = validate_config(out_of_bounds_data)
    print(f"Return error: {err4}")
