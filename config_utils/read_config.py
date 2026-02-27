from typing import Dict, Optional


def read_config(config_path: str | None) -> Optional[Dict[str, str]]:
    """
    Reads and parses a configuration file into a dictionary.
    Ignores empty lines and lines starting with '#'.

    Args:
        config_path: The path to the configuration file.
            If None, the function returns None.

    Returns:
        Optional: A dictionary containing the configuration
            key-value pairs, or None if the file is not found
            or formatting is invalid.
    """
    if config_path is None:
        return None
    config_data: Dict[str, str] = dict()
    try:
        with open(config_path, "r") as f:
            raw_config_data = f.read()
        config_lines = raw_config_data.splitlines()
        for line_num, line in enumerate(config_lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print(f"Error: Line {line_num} is invalid. "
                      f"Expected 'KEY=VALUE'.")
                return None
            key, value = line.split("=")
            config_data[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'.")
        return None
    except ValueError:
        print(f'Error: The conbination in "{config_path}" '
              "is not match format")
        return None
    return config_data


if __name__ == "__main__":
    test_file = "test_config.txt"
    with open(test_file, "w") as f:
        f.write("WIDTH=20\n")
        f.write("HEIGHT=15\n")
        f.write("# This have to ignore\n")
        f.write("\n")
        f.write("ENTRY=0,0\n")
        f.write("EXIT=19,14\n")
        f.write("PERFECT=True\n")
        f.write("OUTPUT_FILE=maze.txt\n")
    print("=== test1: works good  ===")
    result = read_config(test_file)
    print(f"get_data:\n{result}\n")
    print("=== test2: works bad  ===")
    result_none = read_config("not_exist.txt")
    print(f"return: {result_none}\n")
    bad_filename = "bad_config.txt"
    with open(bad_filename, "w") as f:
        f.write("Height=2=1\n")
    print("=== test3: format errror ===")
    result_bad = read_config(bad_filename)
    print(f"return: {result_bad}\n")
