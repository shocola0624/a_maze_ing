#!/usr/bin/env python3

def main() -> None:
    """
    docs
    """
    try:
        from maze_utils import generate_maze
        from config_utils import get_config_path, read_config
        import config_utils.keys as CK
    except ImportError as e:
        print(e)
        return

    # 以下実装の流れメモ

    # read command-line with sys module
    config_path = get_config_path()

    # open config.txt file
    # process keys + error handling
    # receive config: Dict[str, Any] or None if any errors occured
    config_data = read_config(config_path)

    # generate maze
    # receive maze: List[List[int]]
    maze = generate_maze(config_data)

    # write the maze into output file
    output_path = config_data.get(CK.OUTPUT_FILE)


if __name__ == "__main__":
    main()
