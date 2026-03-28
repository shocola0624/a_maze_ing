import sys
from typing import List, Optional
from config_utils import Keys as CK, ConfigData


def int_to_hex(num: int) -> str:
    """
    Converts an integer (0-15) to an upper hex_string (0-F).
    Args:
        num: An integer between 0 and 15.
    Returns:
        A string representing the hex value.
    """
    if not (0 <= num <= 15):
        raise ValueError("Number must be between 0 and 15")
    return f"{num:X}"


def output_maze(
    maze: List[List[int]],
    output_path: str,
    config_data: ConfigData,
    shortest_path: Optional[str]
) -> None:
    """
    Writes a 2D maze to a text file in hexadecimal format.

    Args:
        maze: A 2D list of integers representing the maze.
        output_path: The file path where the maze will be saved.
    """
    output_str = ""
    start = config_data[CK.ENTRY.name]
    goal = config_data[CK.EXIT.name]
    for row in maze:
        line_str = ""
        for cell in row:
            line_str += int_to_hex(cell)
        output_str += line_str + "\n"
    output_str += "\n"
    output_str += str(start)[1:-1].replace(" ", "") + "\n"
    output_str += str(goal)[1:-1].replace(" ", "") + "\n"
    if shortest_path:
        output_str += shortest_path + "\n"
    try:
        with open(output_path, "w") as f:
            f.write(output_str)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
