from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Role:
    role_name: str
    comment_color: str
    mod_level: int

@dataclass
class Stats:
    stars: int
    diamonds: int
    coins: int
    ucoins: int
    demons: int
    cpoints: int
    orbs: int
    moons: int
    special: int
    lvls_completed: int

@dataclass
class Technical:
    reg_date: str
    access_date: str
    last_ip: str
    game_ver: str

@dataclass
class Social:
    blacklist_ids: Any # needs testing
    friends_count: int
    friendship_ids: Any

@dataclass
class Vessels:
    shown_icon: int
    icon_type: int
    color_primary: int
    color_secondary: int
    color_glow: int
    cube: int
    ship: int
    ball: int
    ufo: int
    wave: int
    robot: int
    spider: int
    swing: int
    jetpack: int
    trace: int
    death: int

@dataclass
class Chests:
    chest_small_count: int
    chest_small_time_left: int
    chest_big_count: int
    chest_big_time_left: int

@dataclass
class Settings:
    allow_friend_requests: int
    allow_view_comments: str
    allow_messages: str
    youtube: str
    twitch: str
    twitter: str

@dataclass
class User:
    uid: int
    uname: str
    role: Role
    is_banned: int
    stats: Stats
    technical: Technical
    social: Social
    vessels: Vessels
    chests: Chests
    settings: Settings
    leaderboard_rank: int = -1

@dataclass
class Comment:
    id: int
    uid: int
    likes: int
    posted_time: datetime
    comment: str
    lvl_id: int
    percent: int
    is_spam: bool


@dataclass
class Level:
    id: int
    name: str
    description: str
    uid: int
    password: str
    version: int
    length: int
    difficulty: int
    demon_difficulty: int
    track_id: int
    song_id: int
    version_game: int
    version_binary: int
    string_extra: str
    string_settings: str
    string_level: str
    string_level_info: str
    original_id: int
    objects: int
    stars_requested: int
    stars_got: int
    ucoins: int
    coins: int
    downloads: int
    likes: int
    reports: int
    is_2p: int
    is_verified: int
    is_featured: int
    is_hall: int
    is_epic: int
    is_unlisted: int
    is_ldm: int
    upload_date: str
    update_date: str

@dataclass
class FriendRequest:
    clr_primary: str
    clr_secondary: str
    comment: str
    date: datetime
    iconId: int
    iconType: int
    id: int
    isNew: int
    special: str
    uid: int
    uname: str

@dataclass
class Song:
    status: str
    id: int
    name: str
    artist: str
    size: float
    url: str
    is_banned: bool
    downloads: int

@dataclass
class Message:
    id: int
    message: str
    subject: str
    uname: str
    is_old: int = None
    is_new: int = None
    uid: int = None
    uid_src: int = None
    uid_dest: int = None
    date: datetime = None
    posted_time: datetime = None

@dataclass
class Gauntlet:
    pack_name: str
    levels: list[int]

@dataclass
class MapPack:
    id: int
    pack_name: str
    levels: str
    pack_stars: int
    pack_coins: int
    pack_difficulty: int
    pack_color: str