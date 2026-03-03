#!/usr/bin/env python3

import sys


def main(config_path: str | None = None) -> None:
    """
    docs
    """
    try:
        from maze_utils import (generate_expanded_maze, convert_maze,
                                output_maze, get_shortest_path,
                                print_maze, ask_next_process)
        from config_utils import get_config_path, read_config, validate_config
        import config_utils.keys as CK
    except ImportError as e:
        print(e, file=sys.stderr)
        return

    # read command-line
    if config_path is None:
        config_path = get_config_path()

    # open the config file
    # receive config: Dict[str, str] or None if any errors occured
    config_data = read_config(config_path)

    # validate config
    err = validate_config(config_data)
    if err:
        print(err, file=sys.stderr)
        return

    # generate maze
    # receive maze: List[List[int]]
    expanded_maze = generate_expanded_maze(config_data)
    converted_maze = convert_maze(expanded_maze, config_data)

    # write the maze into output file
    output_path = config_data.get(CK.OUTPUT_FILE)
    shortest_path = get_shortest_path(expanded_maze, config_data)
    output_maze(converted_maze, output_path, config_data, shortest_path)
    print_maze(expanded_maze, config_data)
    ask_next_process(expanded_maze, config_data, config_path)


if __name__ == "__main__":
    main()
