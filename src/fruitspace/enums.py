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

class LevelDifficulty(Enum):
    NA = -1
    AUTO = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5
    EASY_DEMON = 6
    MEDIUM_DEMON = 7
    HARD_DEMON = 8
    INSANE_DEMON = 9
    EXTREME_DEMON = 10

class SearchDifficulty(Enum):
    """
    Values are tuple, containing demonFilter request argument as [0] and diff value as [1]
    """
    NONE = (0, 0)
    NA = (0, -1)
    EASY = (0, 1)
    NORMAL = (0, 2)
    HARD = (0, 3)
    HARDER = (0, 4)
    INSANE = (0, 5)
    EASY_DEMON = (-2, 1)
    MEDIUM_DEMON = (-2, 2)
    HARD_DEMON = (-2, 3)
    INSANE_DEMON = (-2, 4)
    EXTREME_DEMON = (-2, 5)
    DEMON = (-2, 0)

class LevelListSearchFilter(Enum):
    QUERY = 0
    DOWNLOADS = 1
    LIKES = 2
    TRENDING = 3
    RECENT = 4
    USERS = 5
    DEFAULT = 6
    MAGIC = 7
    AWARDED = 11
    FOLLOWED = 12
    FRIENDS = 13
    SENT = 27

class DemonDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    INSANE = 4
    EXTREME = 5
    DEFAULT = 3