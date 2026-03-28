from typing import Tuple, Optional, cast, Any
from config_utils.keys import Keys as CK, ConfigData


def validate_config(config_data: Optional[dict[str, str]]) -> ConfigData:
    """Validate and normalize maze configuration data in place.

    Args:
        config_data: Raw config mapping read from the config file.

    Returns:
        An error message string if validation fails, otherwise None.
    """
    if config_data is None:
        exit()

    new_config_data: dict[str, Any] = config_data.copy()

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
        if required_key.name not in config_data:
            raise ValueError(
                f"Error: Missing required key '{required_key.value}' "
                "in configuration."
            )

    if not config_data[CK.OUTPUT_FILE.name]:
        raise ValueError("Error: Not specified output file")

    # WIDTH, HEIGHT
    try:
        width_val = int(config_data[CK.WIDTH.name])
        height_val = int(config_data[CK.HEIGHT.name])
    except ValueError:
        raise ValueError("Error: WIDTH and HEIGHT must be integer values.")

    if width_val <= 0 or height_val <= 0:
        raise ValueError("Error: WIDTH and HEIGHT must be positive integers.")

    new_config_data[CK.WIDTH.name] = width_val
    new_config_data[CK.HEIGHT.name] = height_val

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

    entry_val = parse_coordinate(config_data[CK.ENTRY.name])

    if entry_val is None:
        raise ValueError("Error: ENTRY must be formatted as integer 'x,y'.")

    exit_val = parse_coordinate(config_data[CK.EXIT.name])

    if exit_val is None:
        raise ValueError("Error: EXIT must be formatted as integer 'x,y'.")
    if not (0 <= entry_val[0] < width_val and 0 <= entry_val[1] < height_val):
        raise ValueError(f"Error: ENTRY {entry_val} is outside boundaries.")
    if not (0 <= exit_val[0] < width_val and 0 <= exit_val[1] < height_val):
        raise ValueError(f"Error: EXIT {exit_val} is outside boundaries.")
    if entry_val == exit_val:
        raise ValueError(
            "Error: ENTRY and EXIT must be at different positions."
        )

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
                raise ValueError(
                    "Error: ENTRY and EXIT must not be on 42 pattern."
                )

    new_config_data[CK.ENTRY.name] = entry_val
    new_config_data[CK.EXIT.name] = exit_val

    # PERFECT
    perfect_str = str(config_data[CK.PERFECT.name]).strip().lower()
    if perfect_str == "true":
        new_config_data[CK.PERFECT.name] = True
    elif perfect_str == "false":
        new_config_data[CK.PERFECT.name] = False
    else:
        raise ValueError("Error: PERFECT must be either 'True' or 'False'.")

    # SEED, WAIT_SEC
    try:
        seed_value = int(config_data[CK.SEED.name])
        new_config_data[CK.SEED.name] = seed_value
    except ValueError:
        raise ValueError("Error: SEED must be integer values.")
    except KeyError:
        pass
    try:
        wait_sec = float(config_data[CK.WAIT_SEC.name])
        new_config_data[CK.WAIT_SEC.name] = wait_sec
    except ValueError:
        raise ValueError("Error: WAIT_SEC must be float values.")
    except KeyError:
        new_config_data[CK.WAIT_SEC.name] = 0.0

    return cast(ConfigData, new_config_data)
