from typing import Any, Dict, List
from config_utils import keys as CK


RESET   = "\x1b[0m"
BLACK   = "\x1b[40m"
RED     = "\x1b[41m"
MAGENTA = "\x1b[45m"
WHITE   = "\x1b[47m"


def clear_screen() -> None:
    """
    [TODO]
    """
    print("\x1b[2J\x1b[H", end="")


def overwrite_maze(expanded_maze: List[List[int]], coord: tuple, n: int) -> None:
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
    overwrite_maze(expanded_maze, entry, 2)
    overwrite_maze(expanded_maze, exit, 3)

    # black floor, white wall, magenta entry, red exit
    colors = {
        0: BLACK,
        1: WHITE,
        2: MAGENTA,
        3: RED
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
    import config_utils.keys as CK
    config_data = {
        CK.WIDTH: 8,
        CK.HEIGHT: 8,
        CK.ENTRY: (0, 0),
        CK.EXIT: (7, 7),
        CK.PERFECT: True
    }
    expanded_maze = generate_expanded_maze(config_data)
    print_maze(expanded_maze, config_data)
