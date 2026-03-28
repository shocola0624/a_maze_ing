import sys
from typing import Optional, Dict
from config_utils.keys import Keys as CK


def read_config(config_path: str) -> Optional[Dict[str, str]]:
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
    config_data = dict()
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
                      "Expected 'KEY=VALUE'.", file=sys.stderr)
                return None
            key, value = line.split("=")
            config_data[CK[key.strip()].name] = value.strip()
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return None
    except ValueError:
        print(f'Error: The conbination in "{config_path}" '
              "is not match format", file=sys.stderr)
        return None
    except KeyError:
        print("Error: Invalid key", file=sys.stderr)
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
