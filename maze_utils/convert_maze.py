from typing import Any, Dict, List
from config_utils import keys as CK


N, E, S, W = 1, 2, 4, 8


def func(
        converted_maze: List[List[int]],
        expanded_maze: List[List[int]],
        exp_x: int,
        exp_y: int
) -> None:
    """
    [TODO] 関数名も変えること。
    """
    con_x = exp_x // 2
    con_y = exp_y // 2
    if expanded_maze[exp_y-1][exp_x] == 1:
        converted_maze[con_y][con_x] += N
    if expanded_maze[exp_y][exp_x+1] == 1:
        converted_maze[con_y][con_x] += E
    if expanded_maze[exp_y+1][exp_x] == 1:
        converted_maze[con_y][con_x] += S
    if expanded_maze[exp_y][exp_x-1] == 1:
        converted_maze[con_y][con_x] += W


def convert_maze(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any]
) -> List[List[int]]:
    """
    [TODO]
    """
    width = config_data[CK.WIDTH]
    height = config_data[CK.HEIGHT]
    converted_maze = [[0 for _ in range(width)] for _ in range(height)]
    exp_wd = width * 2 + 1
    exp_h = height * 2 + 1
    for exp_x in range(exp_wd):
        for exp_y in range(exp_h):
            if exp_x % 2 and exp_y % 2:
                func(converted_maze, expanded_maze, exp_x, exp_y)
    return converted_maze


if __name__ == "__main__":
    from maze_utils import generate_expanded_maze, print_maze
    config_data = {
        CK.WIDTH: 8,
        CK.HEIGHT: 8,
        CK.ENTRY: (0, 0),
        CK.EXIT: (7, 7),
        CK.PERFECT: True,
        CK.SEED: 42,
        CK.WAIT_SEC: 0.1
    }
    expanded_maze = generate_expanded_maze(config_data)
    cells = convert_maze(expanded_maze, config_data)
    print(cells)

    h = len(cells)
    w = len(cells[0]) if h else 0
    H, Wd = 2 * h + 1, 2 * w + 1
    g = [[0 for _ in range(Wd)] for _ in range(H)]
    for y in range(h):
        for x in range(w):
            cy, cx = 2 * y + 1, 2 * x + 1
            mask = cells[y][x]
            if mask & N:
                g[cy-1][cx] = 1
            if mask & S:
                g[cy+1][cx] = 1
            if mask & W:
                g[cy][cx-1] = 1
            if mask & E:
                g[cy][cx+1] = 1

    for r in range(0, H, 2):
        for c in range(0, Wd, 2):
            if ((r > 0 and g[r-1][c] == 1) or (r < H - 1 and g[r+1][c] == 1) or
               (c > 0 and g[r][c-1] == 1) or (c < Wd - 1 and g[r][c+1] == 1)):
                g[r][c] = 1
    print_maze(g, config_data)
