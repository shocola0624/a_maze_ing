from typing import List, Optional
from config_utils import Keys as CK, ConfigData


def get_shortest_path(
    expanded_maze: List[List[int]],
    config_data: ConfigData
) -> Optional[str]:
    """
    Find a path from ENTRY to EXIT as a string of N/E/S/W moves.

    Args:
        expanded_maze: Expanded maze grid.
        config_data: Config data obtained from the specific file.

    Returns:
        A direction string (e.g., "NNEESW"), or None if no path is found.
    """
    x, y = config_data[CK.ENTRY.name]
    start = x * 2 + 1, y * 2 + 1
    x, y = config_data[CK.EXIT.name]
    goal = x * 2 + 1, y * 2 + 1
    cur_x, cur_y = start
    path = ""
    adj = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0)
    }
    oposite = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }

    while (cur_x, cur_y) != goal:
        new_path = ""
        for key, (x, y) in adj.items():
            if path[-1:] == oposite[key]:
                continue
            if expanded_maze[cur_y+y][cur_x+x] == 6:
                new_path = key
                cur_x += x * 2
                cur_y += y * 2
                break
        if new_path:
            path += new_path
        else:
            return None

    return path
