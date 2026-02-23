from typing import Optional
import sys


def get_config_path() -> Optional[str]:
    """
    Get configuration file path from command line arguments.

    Returns:
        str: The file path if exactly one argument is given.
        None: If the number arguments is invalid.
    """
    if len(sys.argv) != 2:
        print("Error: Invalid number of argument.", file=sys.stderr)
        return None
    return sys.argv[1]


if __name__ == "__main__":
    result = get_config_path()
    print(f"Test Output: {result}")
