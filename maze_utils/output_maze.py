from typing import Any, Dict, List, Optional
from config_utils import Keys as CK


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
    config_data: Dict[str, Any],
    shortest_path: Optional[str]
) -> None:
    """
    Writes a 2D maze to a text file in hexadecimal format.

    Args:
        maze: A 2D list of integers representing the maze.
        output_path: The file path where the maze will be saved.
    """
    output_str = ""
    start = config_data[CK.ENTRY]
    goal = config_data[CK.EXIT]
    with open(output_path, "w") as f:
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
        f.write(output_str)


if __name__ == "__main__":
    print(f"10 -> {int_to_hex(10)}")
    print(f"15 -> {int_to_hex(15)}")
    test_maze = [
        [15, 10, 5],
        [0, 1, 2],
        [9, 11, 14]
    ]
    test_file = "test_maze.txt"
    output_maze(test_maze, test_file)
    print(f"Successfully wrote to {test_file}.")
    print("\n--- output_file ---")
    try:
        with open(test_file, 'r') as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("Error not found file")
