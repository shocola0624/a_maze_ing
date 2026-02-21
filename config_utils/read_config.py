from typing import Dict, Optional


def read_config(config_path: str | None) -> Optional[Dict[str, str]]:
    """
    [TODO] docs
    """
    if config_path is None:
        return None

    config_data = dict()
    try:
        with open(config_path, "r") as f:
            raw_config_data = f.read()
            config_lines = raw_config_data.split("\n")

            for line in config_lines:
                key, value = line.split("=")  # TypeError may occur
                # [TODO] make sure TypeError causes
                config_data.update({key: value})
    except FileNotFoundError:
        # [TODO] error message
        return None
    except TypeError:
        # [TODO] error message
        return None

    return config_data
