from typing import Tuple, TypedDict
from enum import Enum


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
