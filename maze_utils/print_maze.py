from typing import Any, Dict, List
from config_utils import keys as CK


RESET = "\x1b[0m"
BLACK = "\x1b[40m"
RED = "\x1b[41m"
BLUE = "\x1b[44m"
MAGENTA = "\x1b[45m"
GRAY = "\x1b[47m"
WHITE = "\x1b[107m"


def clear_screen() -> None:
    """
    [TODO]
    """
    print("\x1b[2J\x1b[H", end="")


def print_maze(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any],
        color_scheme: List[str] | None = None,
        show_path: bool | None = False
) -> None:
    """
    [TODO]
    """
    # 0 floor, 1 wall, 2 inside 42, 3 outside 42, 4 entry, 5 exit, 6 path
    if color_scheme is None:
        color_scheme = [BLACK, WHITE, GRAY, WHITE, MAGENTA, RED, BLUE]
    colors = {
        0: color_scheme[0],
        1: color_scheme[1],
        2: color_scheme[2],
        3: color_scheme[3],
        4: color_scheme[4],
        5: color_scheme[5]
    }
    if show_path:
        colors.update({6: color_scheme[6]})
    else:
        colors.update({6: color_scheme[0]})
    str_maze = ""

    # print maze
    clear_screen()
    for i in expanded_maze:
        for j in i:
            try:
                str_maze += colors[j] + "  " + RESET
            except KeyError:
                str_maze += "  "
        str_maze += "\n"
    print(str_maze)
    print("seed:", config_data[CK.SEED])


if __name__ == "__main__":
    from maze_utils import generate_expanded_maze, ask_next_process
    config_data = {
        CK.WIDTH: 30,
        CK.HEIGHT: 30,
        CK.ENTRY: (0, 0),
        CK.EXIT: (29, 29),
        CK.PERFECT: True,
        CK.WAIT_SEC: 0.0
    }
    expanded_maze = generate_expanded_maze(config_data)
    print_maze(expanded_maze, config_data)
    ask_next_process(expanded_maze, config_data, "")
