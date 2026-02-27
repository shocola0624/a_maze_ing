from typing import Any, List, Dict
from .print_maze import print_maze
from a_maze_ing import main


BLACK = "\x1b[40m"
RED = "\x1b[41m"
BLUE = "\x1b[44m"
MAGENTA = "\x1b[45m"
GRAY = "\x1b[47m"
WHITE = "\x1b[107m"


def ask_next_process(
    expanded_maze: List[List[int]],
    config_data: Dict[str, Any],
    config_path: str,
    scheme_index: int | None = 0,
    show_path: bool | None = False
) -> None:
    """[TODO]"""
    color_schemes = [
        [BLACK, WHITE, GRAY, WHITE, MAGENTA, RED, BLUE]
    ]
    color_scheme = color_schemes[scheme_index % len(color_schemes)]

    print("=== A-Maze-ing ===")
    print("1: Re-generate a new maze")
    print("2: Show/Hide path from entry to exit")
    print("3: Rotate maze colors")
    print("4: Quit")
    choice = input("Choice? (1-4): ").strip()
    try:
        choice = int(choice)
    except ValueError:
        return

    if choice == 1:
        main(config_path)
    if choice == 2:
        show_path = not show_path
        print_maze(expanded_maze, config_data, color_scheme, show_path)
        ask_next_process(
            expanded_maze, config_data, config_path, scheme_index, show_path
        )
    if choice == 3:
        scheme_index += 1
        color_scheme = color_schemes[scheme_index % len(color_schemes)]
        print_maze(expanded_maze, config_data, color_scheme)
        ask_next_process(
            expanded_maze, config_data, config_path, scheme_index, show_path
        )
    return
