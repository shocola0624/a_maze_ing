#!/usr/bin/env python3

def main() -> None:
    """
    docs
    """
    try:
        from maze_utils import generate_maze, convert_maze, output_maze
        from config_utils import get_config_path, read_config, validate_config
        import config_utils.keys as CK
    except ImportError as e:
        print(e)
        return

    # 以下実装の流れメモ

    # read command-line with sys module
    config_path = get_config_path()

    # open config.txt file
    # process keys + error handling
    # receive config: Dict[str, str] or None if any errors occured
    config_data = read_config(config_path)

    # validate
    err = validate_config(config_data)
    if err:
        return

    # generate maze
    # receive maze: List[List[int]]
    expanded_maze = generate_expanded_maze(config_data)
    converted_maze = convert_maze(expanded_maze)

    # write the maze into output file
    output_path = config_data.get(CK.OUTPUT_FILE)
    output_maze(maze, output_path)
    # 描画方法がわからないからどこで処理するか不明


if __name__ == "__main__":
    main()
