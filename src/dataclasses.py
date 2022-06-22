from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


@dataclass
class AudioSetData:
    title: str
    dir: str
    files: Optional[list]


@dataclass
class AudioFileData:
    channel: int
    title: str
    file: str


@dataclass
class PlayerStatus(Enum):
    """Player status"""
    PLAYING = auto()
    STOPPED = auto()
    PAUSED = auto()
    IDDLE = auto()


@dataclass
class WindowProp:
    """GUI props """
    TITLE = 'Noise Generator'
    TOP = 100
    LEFT = 100
    WIDTH = 480
    HEIGHT = 300
