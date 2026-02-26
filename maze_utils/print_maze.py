from typing import Any, Dict, List, Tuple
from config_utils import keys as CK


RESET = "\x1b[0m"
BLACK = "\x1b[40m"
RED = "\x1b[41m"
MAGENTA = "\x1b[45m"
GRAY = "\x1b[47m"
WHITE = "\x1b[107m"


def clear_screen() -> None:
    """
    [TODO]
    """
    print("\x1b[2J\x1b[H", end="")


def overwrite_maze(
    expanded_maze: List[List[int]], coord: Tuple[int], n: int
) -> None:
    """
    [TODO]
    """
    try:
        x, y = coord
        expanded_maze[y*2+1][x*2+1] = n
    except (TypeError, IndexError):
        pass


def print_maze(
        expanded_maze: List[List[int]], config_data: Dict[str, Any]
) -> None:
    """
    [TODO]
    """
    entry = config_data[CK.ENTRY]
    exit = config_data[CK.EXIT]
    overwrite_maze(expanded_maze, entry, 3)
    overwrite_maze(expanded_maze, exit, 4)

    # black floor, white wall, magenta entry, red exit
    colors = {
        0: BLACK,
        1: WHITE,
        2: GRAY,
        3: MAGENTA,
        4: RED
    }
    str_maze = ""

    clear_screen()
    for i in expanded_maze:
        for j in i:
            try:
                str_maze += colors[j] + "  " + RESET
            except KeyError:
                str_maze += "  "
        str_maze += "\n"
    print(str_maze)


if __name__ == "__main__":
    from maze_utils import generate_expanded_maze
    config_data = {
        CK.WIDTH: 30,
        CK.HEIGHT: 30,
        CK.ENTRY: (0, 0),
        CK.EXIT: (29, 29),
        CK.PERFECT: True,
        CK.WAIT_SEC: 0.01
    }
    expanded_maze = generate_expanded_maze(config_data)
    print_maze(expanded_maze, config_data)
