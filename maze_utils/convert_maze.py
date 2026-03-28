from typing import List
from config_utils import Keys as CK, ConfigData


N, E, S, W = 1, 2, 4, 8


def encode_cell_walls(
        converted_maze: List[List[int]],
        expanded_maze: List[List[int]],
        exp_x: int,
        exp_y: int
) -> None:
    """Encode walls around one expanded-grid cell into the compact maze.

    Args:
        converted_maze: Compact maze grid to update in place.
        expanded_maze: Expanded maze grid containing wall information.
        exp_x: X coordinate of the target cell in the expanded maze.
        exp_y: Y coordinate of the target cell in the expanded maze.
    """
    con_x = exp_x // 2
    con_y = exp_y // 2
    if 1 <= expanded_maze[exp_y-1][exp_x] <= 3:
        converted_maze[con_y][con_x] += N
    if 1 <= expanded_maze[exp_y][exp_x+1] <= 3:
        converted_maze[con_y][con_x] += E
    if 1 <= expanded_maze[exp_y+1][exp_x] <= 3:
        converted_maze[con_y][con_x] += S
    if 1 <= expanded_maze[exp_y][exp_x-1] <= 3:
        converted_maze[con_y][con_x] += W


def convert_maze(
        expanded_maze: List[List[int]],
        config_data: ConfigData
) -> List[List[int]]:
    """Convert an expanded maze grid into a compact wall-bit maze grid.

    Args:
        expanded_maze: Expanded maze grid.
        config_data: Config data obtained from the specific file.

    Returns:
        A 2D compact maze grid where each cell stores wall flags derived from
        the expanded maze.
    """
    width = config_data[CK.WIDTH.name]
    height = config_data[CK.HEIGHT.name]
    converted_maze = [[0 for _ in range(width)] for _ in range(height)]
    exp_wd = width * 2 + 1
    exp_h = height * 2 + 1
    for exp_x in range(exp_wd):
        for exp_y in range(exp_h):
            if exp_x % 2 and exp_y % 2:
                encode_cell_walls(converted_maze, expanded_maze, exp_x, exp_y)
    return converted_maze
