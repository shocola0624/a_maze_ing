from typing import Any, Dict, List, Optional
from config_utils.keys import keys as CK


def get_shortest_path(
    expanded_maze: List[List[int]],
    config_data: Dict[str, Any]
) -> Optional[str]:
    """
    Find a path from ENTRY to EXIT as a string of N/E/S/W moves.

    Args:
        expanded_maze: Expanded maze grid.
        config_data: Config data obtained from the specific file.

    Returns:
        A direction string (e.g., "NNEESW"), or None if no path is found.
    """
    start = config_data[CK.ENTRY]
    start = tuple(i * 2 + 1 for i in start)
    goal = config_data[CK.EXIT]
    goal = tuple(i * 2 + 1 for i in goal)
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
        print(new_path)
        if new_path:
            path += new_path
        else:
            return None

    return path
