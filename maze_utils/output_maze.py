from typing import List


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


def output_maze(maze: List[List[int]], output_path: str) -> None:
    """
    Writes a 2D maze to a text file in hexadecimal format.
    Args:
        maze: A 2D list of integers representing the maze.
        output_path: The file path where the maze will be saved.
    """
    with open(output_path, "w") as f:
        for row in maze:
            line_str = ""
            for cell in row:
                line_str += int_to_hex(cell)
            f.write(line_str + "\n")


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
