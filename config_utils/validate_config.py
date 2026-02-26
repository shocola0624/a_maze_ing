from typing import Dict, Optional
from config_utils_keys.keys import keys as CK


def validate_config(config_data: Dict[str, str]) -> Optional[str]:
    """
    [TODO]
    """
    # 1
    if config_data is None:
        return "Error: config_data is None."

    for enum_key in CK
        if enum_key.value in config_data:
            old_value = config_data.pop(enum_key.value)
            config_data[enum_key] = old_value
    # 2
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
            return (
                f"Error: Missing required key '{required_key.value}'
                in configuration."
            )

    for actual_key in config_data.keys():
        if isinstance(actual_key, str):
            return f"Error: Unknown key '{k}' found in config_file."

    try:
        width_val = int(config_data[CK.WIDTH])
        height_val = int(config_data[CK.HEIGHT])
    except ValueError:
        return "Error: WIDTH and HEIGHT must be integer values."
    if width_val <= 0 or height_val <= 0:
        return "Error: WIDTH and HEIGHT must be positive integers."
    config_data[CK.WIDTH] = width_val
    config_data[CK.HEIGHT] = height_val

    def parse_coodinate(coord_str: str, key_name: str) -> tuple[int, int]:
        parts = coord_str.split(",")
        if len(parts) != 2:
            return None
        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except ValueError:
            return None

