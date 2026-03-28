from typing import Tuple
from enum import Enum
from typing import TypedDict


class Keys(Enum):
    """Enum of supported keys in the maze configuration file."""
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"
    SEED = "SEED"
    WAIT_SEC = "WAIT_SEC"


class ConfigData(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int
    WAIT_SEC: float
