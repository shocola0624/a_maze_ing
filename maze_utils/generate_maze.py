from typing import Any, Dict, List, Tuple, Iterator
from config_utils import keys as CK
from random import seed, randint, choice
from time import sleep
from .print_maze import print_maze


def overwrite_maze(
    expanded_maze: List[List[int]], coord: Tuple[int], n: int
) -> None:
    """
    [TODO]
    """
    try:
        x, y = coord
        expanded_maze[y][x] = n
    except (TypeError, IndexError):
        pass


def initialize_maze(
    expanded_maze: List[List[int]],
    config_data: Dict[str, Any],
    exp_wd: int,
    exp_h: int
) -> None:
    """
    [TODO]
    """
    def build_wall_around(
        expanded_maze: List[List[int]], x: int, y: int
    ) -> None:
        """
        [TODO]
        """
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    expanded_maze[y+i][x+j] = 3

    # entry and exit
    start = (i * 2 + 1 for i in config_data[CK.ENTRY])
    goal = (i * 2 + 1 for i in config_data[CK.EXIT])
    overwrite_maze(expanded_maze, start, 4)
    overwrite_maze(expanded_maze, goal, 5)

    # wall
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
        coord_on_42 = [
            (-6, -4), (-6, -2), (-6, 0), (-4, 0), (-2, 0), (-2, 2), (-2, 4),
            (2, -4), (4, -4), (6, -4), (6, -2), (6, 0), (4, 0), (2, 0), (2, 2),
            (2, 4), (4, 4), (6, 4)
        ]
        c_x, c_y = center
        for x, y in coord_on_42:
            build_wall_around(expanded_maze, c_x + x, c_y + y)
            expanded_maze[c_y+y][c_x+x] = 2
    else:
        print("Error: It's too small to draw 42")


def grow_wall_from(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any],
        coord: Tuple[int, int],
        taken_coords: List[Tuple[int, int]] | None = None,
        mode: str | None = None
) -> None:
    """
    [TODO]
    """
    def lay_wall_toward(
        expanded_maze: List[List[int]],
        coord: Tuple[int, int],
        dir: str
    ) -> Tuple[int, int]:
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

    def get_open_adjacent_dirs(coord: Tuple[int, int]) -> List[str]:
        """[TODO]"""
        x, y = coord
        open_adjacent_dirs = []
        around = {
            "N": (x, y-1),
            "E": (x+1, y),
            "S": (x, y+1),
            "W": (x-1, y)
        }

        for dir, (i_x, i_y) in around.items():
            try:
                if expanded_maze[i_y][i_x] == 0:
                    open_adjacent_dirs.append(dir)
            except IndexError:
                pass
        return open_adjacent_dirs

    def get_extendable_dirs(
        coord: Tuple[int, int],
        open_adjacent_dirs: List[str],
        taken_coords: List[Tuple[int, int]]
    ) -> List[str]:
        """[TODO]"""
        x, y = coord
        coord_ahead = {
            "N": (x, y-2),
            "E": (x+2, y),
            "S": (x, y+2),
            "W": (x-2, y)
        }

        if mode == "to_wall":
            extendable_dirs = open_adjacent_dirs
        else:
            extendable_dirs = []
            for dir in open_adjacent_dirs:
                i_x, i_y = coord_ahead[dir]
                if expanded_maze[i_y][i_x] == 0:
                    extendable_dirs.append(dir)

        # delete taken_coords from extendable_dirs
        for dir in extendable_dirs.copy():
            if coord_ahead[dir] in taken_coords:
                extendable_dirs.remove(dir)
        return extendable_dirs

    # ---------------
    # grow_wall_from
    x, y = coord
    if taken_coords is None:
        taken_coords = []

    open_adjacent_dirs = get_open_adjacent_dirs(coord)

    if len(open_adjacent_dirs) == 4:
        mode = "to_wall"

    extendable_dirs = get_extendable_dirs(
        coord, open_adjacent_dirs, taken_coords
    )

    taken_coords.append(coord)

    if not extendable_dirs and mode == "to_wall":
        grow_wall_from(
            expanded_maze, config_data, choice(taken_coords),
            taken_coords, mode
        )

    if extendable_dirs:
        dir = choice(extendable_dirs)
        new_coord = lay_wall_toward(expanded_maze, coord, dir)
        wait_sec = config_data[CK.WAIT_SEC]
        if wait_sec > 0:
            sleep(wait_sec)
            print_maze(expanded_maze, config_data)
        if new_coord:
            grow_wall_from(
                expanded_maze, config_data, new_coord, taken_coords, mode
            )


def set_walls(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any],
        exp_wd: int,
        exp_h: int
) -> None:
    """
    [TODO]壁の種をランダムな場所に植え付ける。別の関数で壁を成長させる。
    """
    # extend walls on 42 pattern
    is_perfect = config_data[CK.PERFECT]
    if is_perfect:
        if exp_wd >= 15 and exp_h >= 11:
            width = config_data[CK.WIDTH]
            height = config_data[CK.HEIGHT]
            x, y = width + (width % 2 == 0), height + (height % 2 == 0)
            on_4 = [
                (x-7, y-5), (x-7, y-3), (x-7, y-1), (x-7, y+1), (x-5, y+1),
                (x-3, y+3), (x-3, y+5), (x-1, y+5), (x-1, y+3), (x-1, y+1),
                (x-1, y-1), (x-3, y-1), (x-5, y-3), (x-5, y-5)
            ]
            on_2 = [
                (x+1, y-5), (x+3, y-5), (x+5, y-5), (x+7, y-5), (x+7, y-3),
                (x+7, y-1), (x+7, y+1), (x+7, y+3), (x+7, y+5), (x+5, y+5),
                (x+3, y+5), (x+1, y+5), (x+1, y+3), (x+1, y+1), (x+1, y-1),
                (x+1, y-3)
            ]
            grow_wall_from(
                expanded_maze, config_data,
                choice(on_4), on_4.copy(), "to_wall"
            )
            grow_wall_from(
                expanded_maze, config_data, choice(on_2),
                on_2.copy(), "to_wall"
            )

    lattice_points = []
    for x in range(exp_wd):
        for y in range(exp_h):
            if x % 2 == 0 and y % 2 == 0:
                lattice_points.append((x, y))

    while lattice_points:
        coord = lattice_points.pop(randint(0, len(lattice_points)-1))
        x, y = coord
        expanded_maze[y][x] = 1
        grow_wall_from(expanded_maze, config_data, coord)


def find_shortest_path(
        expanded_maze: List[List[int]],
        config_data: Dict[str, Any]
) -> None:
    """[TODO]"""

    def adjacent_coord(coord: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
        """[TODO]"""
        x, y = coord
        around = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

        for i_x, i_y in around:
            try:
                if expanded_maze[i_y][i_x] in (0, 5):
                    yield (i_x, i_y)
            except IndexError:
                pass

    start = tuple(i * 2 + 1 for i in config_data[CK.ENTRY])
    goal = tuple(i * 2 + 1 for i in config_data[CK.EXIT])
    prev: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}
    coords = [start]
    while coords:
        cur = coords.pop(0)
        if cur == goal:
            break
        for adj in adjacent_coord(cur):
            if adj not in prev:
                prev[adj] = cur
                coords.append(adj)

    cur = prev.get(goal)
    while cur:
        x, y = cur
        if expanded_maze[y][x] == 0:
            overwrite_maze(expanded_maze, cur, 6)
        cur = prev[cur]


def generate_expanded_maze(config_data: Dict[str, Any]) -> List[List[int]]:
    """
    [TODO]
    """
    width = config_data[CK.WIDTH]
    height = config_data[CK.HEIGHT]
    exp_wd = width * 2 + 1
    exp_h = height * 2 + 1
    expanded_maze = [[0 for _ in range(exp_wd)] for _ in range(exp_h)]
    initialize_maze(expanded_maze, config_data, exp_wd, exp_h)

    # set seed
    try:
        seed_value = config_data[CK.SEED]
    except KeyError:
        seed_value = randint(0, 2147483647)
        config_data[CK.SEED] = seed_value
    seed(seed_value)

    set_walls(expanded_maze, config_data, exp_wd, exp_h)

    find_shortest_path(expanded_maze, config_data)

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
