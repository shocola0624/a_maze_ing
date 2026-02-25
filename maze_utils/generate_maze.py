from typing import Any, Dict, List, Tuple
from config_utils import keys as CK
from random import seed, randint, choice
from time import sleep
from .print_maze import print_maze


def build_wall_around(
    expanded_maze: List[List[int]], x: int, y: int
) -> None:
    """
    [TODO]
    """
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i != 0 or j != 0:
                expanded_maze[y+i][x+j] = 1


def initialize_maze(
    expanded_maze: List[List[int]], exp_wd: int, exp_h: int
) -> None:
    """
    [TODO]
    """
    for w in range(exp_wd):
        for h in range(exp_h):
            expanded_maze[0][w] = 1
            expanded_maze[h][0] = 1
            expanded_maze[exp_h-1][w] = 1
            expanded_maze[h][exp_wd-1] = 1

    # 42 pattern
    if exp_wd >= 15 and exp_h >= 11:
        width = exp_wd // 2
        height = exp_h // 2
        center = (width + (width % 2 == 0), height + (height % 2 == 0))
        cood_on_42 = [
            (-6, -4), (-6, -2), (-6, 0), (-4, 0), (-2, 0), (-2, 2), (-2, 4),
            (2, -4), (4, -4), (6, -4), (6, -2), (6, 0), (4, 0), (2, 0), (2, 2),
            (2, 4), (4, 4), (6, 4)
        ]
        c_x, c_y = center
        for x, y in cood_on_42:
            build_wall_around(expanded_maze, c_x + x, c_y + y)
            expanded_maze[c_y+y][c_x+x] = 2
    else:
        print("Error: It's too small to draw 42")


def extend_wall(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any],
        coord: Tuple[int],
        taken_coords: List[Tuple[int]] | None = [],
        mode: str | None = None
) -> None:
    """
    [TODO]
    """
    def extend_wall_to(expanded_maze: List[List[int]], coord: Tuple[int], dir: str) -> Tuple[int]:
        """[TODO]"""
        x, y = coord
        coord_to_overwrite = {
            "N": [(x, y-1), (x, y-2)],
            "E": [(x+1, y), (x+2, y)],
            "S": [(x, y+1), (x, y+2)],
            "W": [(x-1, y), (x-2, y)]
        }
        x, y = coord_to_overwrite[dir][1]
        is_wall = bool(expanded_maze[y][x])
        for x, y in coord_to_overwrite[dir]:
            expanded_maze[y][x] = 1
        if is_wall:
            return None
        return coord_to_overwrite[dir][1]
    # taken_coordがないかつ、周囲が壁でない->壁にくっつくまで動く
    # taken_coordがないかつ、周囲に壁がある->進めるとこまで進む
    x, y = coord
    coords_around_point = {
        "N": (x, y-1),
        "E": (x+1, y),
        "S": (x, y+1),
        "W": (x-1, y)
    }
    blanks = []

    for dir, (i_x, i_y) in coords_around_point.items():
        try:
            if expanded_maze[i_y][i_x] == 0:
                blanks.append(dir)
        except IndexError:
            pass

    if len(blanks) == 4:
        mode = "to_wall"

    can_move_toward = []
    coord_ahead = {
        "N": (x, y-2),
        "E": (x+2, y),
        "S": (x, y+2),
        "W": (x-2, y)
    }
    if mode == "to_wall":
        can_move_toward = blanks
    else:
        for dir in blanks:
            i_x, i_y = coord_ahead[dir]
            if expanded_maze[i_y][i_x] == 0:
                can_move_toward.append(dir)

    # delete taken_coords from can_move_toward
    for dir in can_move_toward.copy():
        if coord_ahead[dir] in taken_coords:
            can_move_toward.remove(dir)
    taken_coords.append(coord)

    if can_move_toward:
        dir = choice(can_move_toward)
        new_coord = extend_wall_to(expanded_maze, coord, dir)
        wait_sec = config_data[CK.WAIT_SEC]
        sleep(wait_sec)
        print_maze(expanded_maze, config_data)
        if new_coord:
            extend_wall(expanded_maze, config_data, new_coord, taken_coords, mode)
    taken_coords.clear()

def set_walls(
        expanded_maze: List[List[int]], config_data: Dict[str, Any], exp_wd: int, exp_h: int
) -> None:
    """
    [TODO]壁の種をランダムな場所に植え付ける。別の関数で壁を成長させる。
    """
    lattice_points = []
    for x in range(exp_wd):
        for y in range(exp_h):
            if x % 2 == 0 and y % 2 == 0:
                lattice_points.append((x, y))
    while lattice_points:
        coord = lattice_points.pop(randint(0, len(lattice_points)-1))
        x, y = coord
        expanded_maze[y][x] = 1
        extend_wall(expanded_maze, config_data, coord)


def generate_expanded_maze(config_data: Dict[str, Any]) -> List[List[int]]:
    """
    [TODO]
    """
    width = config_data[CK.WIDTH]
    height = config_data[CK.HEIGHT]
    exp_wd = width * 2 + 1
    exp_h = height * 2 + 1
    expanded_maze = [[0 for _ in range(exp_wd)] for _ in range(exp_h)]
    initialize_maze(expanded_maze, exp_wd, exp_h)

    # set seed
    try:
        seed_value = config_data[CK.SEED]
    except KeyError:
        seed_value = randint(0, 10000)
    seed(seed_value)

    set_walls(expanded_maze, config_data, exp_wd, exp_h)
    print(seed_value) # debug

    return expanded_maze


if __name__ == "__main__":
    config_data = {
        CK.WIDTH: 8,
        CK.HEIGHT: 8,
        CK.ENTRY: (0, 0),
        CK.EXIT: (10, 15),
        CK.PERFECT: True,
        CK.SEED: 42
    }
    m = generate_expanded_maze(config_data)
    print(m)
