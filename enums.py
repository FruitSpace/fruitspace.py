from enum import Enum


class TopType(Enum):
    top = 'top'
    relative = 'relative'
    friend = 'friend'
    creators = 'creators'

class LevelLength(Enum):
    TINY = 0,
    SHORT = 1,
    MEDIUM = 2,
    LONG = 3,
    XL = 4,
    PLATFORMER = 5