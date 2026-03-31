#!/usr/bin/env python3

import sys


def main(config_path: str | None = None) -> None:
    """Run the maze generator from config loading to output and display.

    Reads config, generates the maze, writes the output file, prints
    the maze, and starts the interactive menu.

    Args:
        config_path: Optional path to the config file. If None, the path is
            obtained from command-line input.
    """
    try:
        from maze_utils import (MazeGenerator, convert_maze,
                                output_maze, get_shortest_path,
                                ask_next_process)
        from config_utils import get_config_path, read_config, validate_config
        from config_utils import Keys as CK
    except ImportError as e:
        print(e, file=sys.stderr)
        return

    # read command-line
    if config_path is None:
        config_path = get_config_path()

    # open the config file
    # receive config: Dict[str, str] or None if any errors occured
    config_data_raw = read_config(config_path)

    # validate config
    try:
        config_data = validate_config(config_data_raw)
    except ValueError as err:
        print(err, file=sys.stderr)
        return

    # generate maze
    # receive maze: List[List[int]]
    Gen = MazeGenerator()
    expanded_maze = Gen.generate_expanded_maze(config_data)
    converted_maze = convert_maze(expanded_maze, config_data)

    # write the maze into output file
    output_path = config_data.get(CK.OUTPUT_FILE.name)
    shortest_path = get_shortest_path(expanded_maze, config_data)
    output_maze(converted_maze, output_path, config_data, shortest_path)
    Gen.print_maze(expanded_maze, config_data)
    ask_next_process(expanded_maze, config_data, config_path)


if __name__ == "__main__":
    try:
        main()
    except RecursionError as e:
        print(e)
