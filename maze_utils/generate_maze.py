import sys
from typing import Dict, List, Tuple, Iterator, Optional
from config_utils import Keys as CK, ConfigData
from random import seed, randint, choice
from time import sleep


RESET = "\x1b[0m"
BLACK = "\x1b[40m"
RED = "\x1b[41m"
BLUE = "\x1b[44m"
MAGENTA = "\x1b[45m"
GRAY = "\x1b[47m"
WHITE = "\x1b[107m"


class MazeGenerator:
    """
    Generate, solve, and render an expanded maze grid.

    This class builds a maze on an "expanded" representation of the original
    logical grid. If the logical maze size is `(width, height)`, the expanded
    maze size becomes `(width * 2 + 1, height * 2 + 1)`, allowing walls and
    passages to be represented explicitly as separate cells.

    Main responsibilities:
        - Initialize the expanded grid with outer borders, entry, and exit.
        - Place a central "42" pattern when the maze is large enough.
        - Grow walls from lattice points to form the maze layout.
        - Find and mark the shortest path from entry to exit.
        - Render the maze in the terminal using ANSI colors.

    Cell values used in the expanded maze:
        0: floor / open path
        1: wall
        2: cell belonging to the inside of the "42" pattern
        3: reserved area surrounding the "42" pattern
        4: entry
        5: exit
        6: shortest path
    """

    @staticmethod
    def print_maze(
            expanded_maze: List[List[int]],
            config_data: ConfigData,
            color_scheme: List[str] | None = None,
            show_path: bool | None = False
    ) -> None:
        """
        Render an expanded maze to the terminal using ANSI colors.

        Args:
            expanded_maze: Expanded maze grid.
            config_data: Config data obtained from the specific file.
            color_scheme: Optional list of ANSI color strings.
                If None, defaults are used.
            show_path: If True, render shortest path.
        """
        def clear_screen() -> None:
            """
            Clear the terminal screen and move the cursor to the top-left
            corner. Uses ANSI escape sequences to reset the display.
            """
            print("\x1b[2J\x1b[H", end="")
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
        print("seed:", config_data[CK.SEED.name])

    @staticmethod
    def overwrite_maze(
        expanded_maze: List[List[int]], coord: Tuple[int, int], n: int
    ) -> None:
        """
        Write a value into the expanded maze grid at (x, y).

        Args:
            expanded_maze: Expanded maze grid.
            coord: Target coordinate as (x, y).
            n: Value to write into the grid.
        """
        try:
            x, y = coord
            expanded_maze[y][x] = n
        except (TypeError, IndexError):
            pass

    def initialize_maze(
        self,
        expanded_maze: List[List[int]],
        config_data: ConfigData,
        exp_wd: int,
        exp_h: int
    ) -> None:
        """
        Initialize the expanded maze with borders, entry/exit,
        and an optional "42" pattern.

        Args:
            expanded_maze: Expanded maze grid.
            config_data: Config data obtained from the specific file.
            exp_wd: Width of the expanded maze grid.
            exp_h: Height of the expanded maze grid.
        """
        def build_wall_around(
            expanded_maze: List[List[int]], x: int, y: int
        ) -> None:
            """Mark the 8 neighboring cells around (x, y)."""
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i != 0 or j != 0:
                        expanded_maze[y+i][x+j] = 3

        # entry and exit
        x, y = config_data[CK.ENTRY.name]
        start = x * 2 + 1, y * 2 + 1
        x, y = config_data[CK.EXIT.name]
        goal = x * 2 + 1, y * 2 + 1
        self.overwrite_maze(expanded_maze, start, 4)
        self.overwrite_maze(expanded_maze, goal, 5)

        # wall
        for w in range(exp_wd):
            for h in range(exp_h):
                expanded_maze[0][w] = 1
                expanded_maze[h][0] = 1
                expanded_maze[exp_h-1][w] = 1
                expanded_maze[h][exp_wd-1] = 1

        # 42 pattern
        if exp_wd >= 19 and exp_h >= 15:
            width = exp_wd // 2
            height = exp_h // 2
            center = (width + (width % 2 == 0), height + (height % 2 == 0))
            c_x, c_y = center
            coord_on_42 = [
                (-6, -4), (-6, -2), (-6, 0), (-4, 0), (-2, 0), (-2, 2),
                (-2, 4), (2, -4), (4, -4), (6, -4), (6, -2), (6, 0), (4, 0),
                (2, 0), (2, 2), (2, 4), (4, 4), (6, 4)
            ]
            for x, y in coord_on_42:
                build_wall_around(expanded_maze, c_x + x, c_y + y)
                expanded_maze[c_y+y][c_x+x] = 2
        else:
            print("Error: It's too small to draw 42", file=sys.stderr)

    def grow_wall_from(
            self,
            expanded_maze: List[List[int]],
            config_data: ConfigData,
            coord: Tuple[int, int],
            taken_coords: List[Tuple[int, int]] | None = None,
            mode: str | None = None
    ) -> None:
        """
        Grow maze walls starting from a given cell on the expanded grid.

        Args:
            expanded_maze: Expanded maze grid.
            config_data: Config data obtained from the specific file.
            coord: Starting (x, y) coordinate on the expanded grid.
            taken_coords: List of coordinates already passed.
            mode: Mode string to switch between wall-growth strategies.
        """
        def lay_wall_toward(
            expanded_maze: List[List[int]],
            coord: Tuple[int, int],
            dir: str
        ) -> Optional[Tuple[int, int]]:
            """Lay a 2-cell wall segment from `coord` toward `dir`.

            Writes wall tiles (value 1) into the intermediate cell and the cell
            two steps ahead, if they are currently floor (0). If the
            destination cell (two steps ahead) is already non-zero,
            returns None to signal that the wall hit an existing structure.

            Args:
                dir: Direction to extend ("N", "E", "S", "W").

            Returns:
                The new (x, y) coordinate two steps ahead if extension
                succeeded, otherwise None.
            """
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
                if expanded_maze[y][x] == 0:
                    expanded_maze[y][x] = 1
            if is_wall:
                return None
            return coord_to_overwrite[dir][1]

        def get_open_adjacent_dirs(coord: Tuple[int, int]) -> List[str]:
            """
            Return directions whose adjacent cell is open (floor = 0).

            Args:
                coord: Current (x, y) position on the expanded grid.

            Returns:
                A list of direction letters ("N", "E", "S", "W") for which the
                immediately adjacent cell is within bounds and equals 0.
            """
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
            """Filter open directions to those that can be extended safely.

            In normal mode, a direction is extendable only if the cell two
            steps ahead is also floor (0). In "to_wall" mode, any open adjacent
            direction is considered extendable. Directions whose
            two-steps-ahead coordinate is in `taken_coords` are removed.

            Args:
                coord: Current (x, y) position on the expanded grid.
                open_adjacent_dirs: Directions with an open adjacent cell.
                taken_coords: Coordinates already used as wall-growth points.

            Returns:
                A list of direction letters that are extendable.
            """
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
            self.grow_wall_from(
                expanded_maze, config_data, choice(taken_coords),
                taken_coords, mode
            )

        if extendable_dirs:
            dir = choice(extendable_dirs)
            new_coord = lay_wall_toward(expanded_maze, coord, dir)
            wait_sec = config_data[CK.WAIT_SEC.name]
            if wait_sec > 0:
                sleep(wait_sec)
                self.print_maze(expanded_maze, config_data)
            if new_coord:
                self.grow_wall_from(
                    expanded_maze, config_data, new_coord, taken_coords, mode
                )

    def set_walls(
            self,
            expanded_maze: List[List[int]],
            config_data: ConfigData,
            exp_wd: int,
            exp_h: int
    ) -> None:
        """Seed wall starters and grow walls to generate the maze layout.

        If `CK.PERFECT` is enabled and the grid is large enough, this first
        grows walls starting from predefined points around the central
        "42" pattern. Then it iterates over even-even lattice points as
        candidate wall seeds: for each chosen seed, it places an initial wall
        tile and calls `grow_wall_from()` to extend walls from that seed.

        Args:
            expanded_maze: Expanded maze grid.
            config_data: Config data obtained from the specific file.
            exp_wd: Width of the expanded maze grid.
            exp_h: Height of the expanded maze grid.
        """
        # extend walls on 42 pattern
        is_perfect = config_data[CK.PERFECT.name]
        if is_perfect:
            if exp_wd >= 19 and exp_h >= 15:
                width = config_data[CK.WIDTH.name]
                height = config_data[CK.HEIGHT.name]
                x, y = width + (width % 2 == 0), height + (height % 2 == 0)
                on_4 = [
                    (x-7, y-5), (x-7, y-3), (x-7, y-1), (x-7, y+1), (x-5, y+1),
                    (x-3, y+3), (x-3, y+5), (x-1, y+5), (x-1, y-1), (x-3, y-1),
                    (x-5, y-3), (x-5, y-5)
                ]
                on_2 = [
                    (x+1, y-5), (x+3, y-5), (x+5, y-5), (x+7, y-5), (x+7, y-3),
                    (x+7, y-1), (x+7, y+1), (x+7, y+3), (x+7, y+5), (x+5, y+5),
                    (x+3, y+5), (x+1, y+5), (x+1, y+3), (x+1, y+1), (x+1, y-1),
                    (x+1, y-3)
                ]
                self.overwrite_maze(expanded_maze, (x, y+5), 1)
                self.grow_wall_from(
                    expanded_maze, config_data, choice(on_4),
                    on_4.copy() + on_2.copy(), "to_wall"
                )

        lattice_points = []
        for x in range(exp_wd):
            for y in range(exp_h):
                if x % 2 == 0 and y % 2 == 0:
                    lattice_points.append((x, y))

        while lattice_points:
            coord = lattice_points.pop(randint(0, len(lattice_points)-1))
            x, y = coord
            if expanded_maze[y][x] == 0:
                expanded_maze[y][x] = 1
            self.grow_wall_from(expanded_maze, config_data, coord)

    def find_shortest_path(
            self,
            expanded_maze: List[List[int]],
            config_data: ConfigData
    ) -> None:
        """Find the shortest path from entry to exit and mark it on the maze.

        Args:
            expanded_maze: Expanded maze grid.
            config_data: Config data obtained from the specific file.
        """

        def adjacent_coord(
                coord: Tuple[int, int]
        ) -> Iterator[Tuple[int, int]]:
            """Yield adjacent coordinates that can be moved to from `coord`.

            Args:
                coord: Current (x, y) position in the expanded maze.

            Yields:
                An iterator of neighboring coordinates whose tile is open.
            """
            x, y = coord
            around = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

            for i_x, i_y in around:
                try:
                    if expanded_maze[i_y][i_x] in (0, 5):  # 0:floor, 5:exit
                        yield (i_x, i_y)
                except IndexError:
                    pass

        x, y = config_data[CK.ENTRY.name]
        start = x * 2 + 1, y * 2 + 1
        x, y = config_data[CK.EXIT.name]
        goal = x * 2 + 1, y * 2 + 1
        prev: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}
        coords = [start]
        cur: Tuple[int, int] | None
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
                self.overwrite_maze(expanded_maze, cur, 6)
            cur = prev[cur]

    def generate_expanded_maze(
            self,
            config_data: ConfigData
    ) -> List[List[int]]:
        """Generate an expanded maze grid from validated configuration data.

        Args:
            config_data: Config data obtained from the specific file.

        Returns:
            A 2D expanded maze grid with walls initialized, generated, and the
            shortest path marked.
        """
        width = config_data[CK.WIDTH.name]
        height = config_data[CK.HEIGHT.name]
        exp_wd = width * 2 + 1
        exp_h = height * 2 + 1
        expanded_maze = [[0 for _ in range(exp_wd)] for _ in range(exp_h)]
        self.initialize_maze(expanded_maze, config_data, exp_wd, exp_h)

        # set seed
        try:
            seed_value = config_data[CK.SEED.name]
        except KeyError:
            seed_value = randint(0, 2147483647)
            config_data[CK.SEED.name] = seed_value
        seed(seed_value)

        self.set_walls(expanded_maze, config_data, exp_wd, exp_h)

        self.find_shortest_path(expanded_maze, config_data)

        return expanded_maze
