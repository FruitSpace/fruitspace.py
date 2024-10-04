import json
from typing import Any
from functools import singledispatch

import requests

import urls
from enums import TopType, LevelLength, LevelDifficulty, SearchDifficulty
from models import User, Comment, Level, FriendRequest, Song, Message, Gauntlet, MapPack, Likeable, LevelList
from urls import GD
from utils import gjp2, gjp, base64

_base_url: str = 'https://rugd.gofruit.space/{gdps}' # %s is GDPS index

_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


def __send(gdps_id: str, url: str, data: dict, use_json: bool = True) -> str | dict:
    r = requests.post(_base_url.format(gdps=gdps_id)+url+'?json', data=data, headers=_headers).text
    if use_json:
        return json.loads(r)
    return r

def _send(gdps_id: str, url: urls.GD | str, data: dict, use_json: bool = True) -> str | dict:
    return __send(gdps_id, url.value if type(url)==GD else url, data, use_json)

class GhostClient:
    username: str = None
    password: str = None
    user_id: int = None


    def __init__(self, gdps_id: str, username: str = None, password: str = None):
        self.gdps_id = gdps_id
        if username and password:
            self.username = username
            self.password = password
            user_id = self._login()
            if user_id < 0:
                raise Exception(f'Incorrect username or password. Error code: {user_id}')
            else:
                self.user_id = user_id


    def _use_session(self, data: dict[str, Any]):
        if self.user_id:
            data['accountID'] = self.user_id
            data['gjp'] = gjp(self.password)
            data['gjp2'] = gjp2(self.password)

    
    def _login(self) -> int:
        r = _send(self.gdps_id, GD.account_login, {'userName': self.username, 'password': self.password})

        if 'code' in r and r['code'] == '-1':
            self._register()
            self._login()
        return int(r['uid'])

    def _register(self):
        data = {'userName': self.username, 'password': self.password, 'email': f'{self.username}@mail.ru'}
        print(_send(self.gdps_id, GD.account_register, data))

    def get_users(self, name: str) -> list[User]:
        data = {
            'str': name
        }

        return [User(**u) for u in _send(self.gdps_id, GD.get_users, data)['users']]

    def get_user(self, _id: int) -> User:
        data = {'targetAccountID': _id}

        self._use_session(data)

        s = _send(self.gdps_id, GD.get_user_info, data)

        return User(**s['user'])

    
    def get_user_posts(self, user: int | User) -> list[Comment]:
        data = {'accountID': user if isinstance(user, int) else User.uid}

        self._use_session(data)

        return [Comment(**comm) for comm in _send(self.gdps_id, GD.account_comment_get, data)['comments']]

    def post(self, plain_text: str):
        data = {
            'comment': base64(plain_text),
            'cType': 1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.account_comment_upload, data)

    def delete_post(self, comment: int | Comment):
        data = {
            'commentID': comment if isinstance(comment, int) else comment.id,
            'cType': 1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.account_comment_delete, data)
    
    def get_level(self, _id: int):
        data = {'levelID': _id}

        self._use_session(data)

        return _send(self.gdps_id, GD.level_download, data)

    
    def get_levels(self,
                   gauntlet: int | None = None,
                   followed: str | None = None,
                   diff: SearchDifficulty = SearchDifficulty.NONE,
                   _len: int | None = None,
                   song: int | None = None,
                   customSong: int | None = None,
                   page: int = 0,
                   count: int = 10,
                   _type: int = 0,
                   _str: str = "",
                   uncomlpeted: int | bool = False,
                   onlyCompleted: int | bool = False,
                   featured: int | bool = False,
                   original: int | bool = False,
                   twoPlayer: int | bool = False,
                   coins: int | bool = False,
                   epic: int | bool = False,
                   noStar: int | bool = False,
                   star: int | bool = False,
                   completedLevels: int | bool = False,
                   ) -> list[Level]:
        d: dict = {}
        if gauntlet:
            d['gauntlet'] = gauntlet
        if followed:
            d['followed'] = followed

        d['demonFilter'] = diff.value[0]
        d['diff'] = diff.value[1]

        if _len:
            d['len'] = _len
        if song:
            d['song'] = song
        if customSong:
            d['customSong'] = customSong

        d['page'] = page
        d['count'] = count
        d['type'] = _type
        d['str'] = _str
        d['uncomlpeted'] = int(uncomlpeted)
        d['onlyCompleted'] = int(onlyCompleted)
        d['featured'] = int(featured)
        d['original'] = int(original)
        d['twoPlayer'] = int(twoPlayer)
        d['coins'] = int(coins)
        d['epic'] = int(epic)
        d['noStar'] = int(noStar)
        d['star'] = int(star)
        d['completedLevels'] = int(completedLevels)

        self._use_session(d)

        return [Level(**l) for l in _send(self.gdps_id, GD.get_levels, d)['levels']]


    def get_leaderboard(self, _type: TopType = TopType.top, count: int = 100) -> list[User]:
        data = {'type': _type.value, 'count': count}

        self._use_session(data)

        return [User(**u) for u in _send(self.gdps_id, GD.get_scores, data)['leaderboard']]

    def get_friend_requests(self, getSent: bool = False, total: int = 10) -> list[FriendRequest]:
        data = {
            'getSent': 1 if getSent else 0,
            'total': total
        }

        self._use_session(data)

        return [FriendRequest(**r) for r in _send(self.gdps_id, GD.friend_get_requests, data)['requests']]

    def read_friend_request(self, request: int | FriendRequest):
        data = {
            'requestID': request if isinstance(request, int) else request.id
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.friend_read_request, data)

    def accept_friend_request(self, request: int | FriendRequest):
        data = {
            'requestID': request if isinstance(request, int) else request.id
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.friend_accept_request, data)


    def reject_friend_request(self, accounts: int | FriendRequest | list[int | User | FriendRequest]):
        data = {
            'targetAccountID': accounts if isinstance(accounts, int) else accounts.uid if isinstance(accounts, FriendRequest) else None
        }
        _accounts: str = ''
        if isinstance(accounts, list):
            _accounts.join([str(_id) if isinstance(_id, int) else _id.uid for _id in accounts])

        data['accounts'] = _accounts

        self._use_session(data)

        return _send(self.gdps_id, GD.friend_accept_request, data)

    def remove_friend(self, targetAccount: int | User):
        data = {
            'targetAccountID': targetAccount if isinstance(targetAccount, int) else targetAccount.uid
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.friend_remove, data)

    def block_user(self, target: int | User):
        data = {
            'targetAccountID': target if isinstance(target, int) else target.uid
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.block_user, data)

    def unblock_user(self, target: int | User):
        data = {
            'targetAccountID': target if isinstance(target, int) else target.uid
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.unblock_user, data)

    def send_friend_request(self, toAccount: int | User, comment: str = ''):
        data = {
            'toAccountID': toAccount if isinstance(toAccount, int) else toAccount.uid,
            'comment': base64(comment)
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.friend_request, data)

    def get_comment_history(self, user: int | User, mode: int = 0, page: int = 0, total: int = 0) -> list[Comment]:
        data = {
            'userID': user if isinstance(user, int) else user.uid,
            'mode': mode,
            'page': page,
            'total': total
        }

        ret = [Comment(**comm) for comm in _send(self.gdps_id, GD.comment_get_history, data)['comments']]

        return ret


    def get_level_comments(self, level: int | Level, page: int = 0, mode: int = 0, total: int = 10) -> list[Comment]:
        data = {
            'levelID': level if isinstance(level, int) else level.id,
            'page': page,
            'mode': mode,
            'total': total
        }

        ret = [Comment(**comm) for comm in _send(self.gdps_id, GD.comments_get, data)['comments']]

        return ret


    def get_challenges(self):
        data: dict[str, Any] = {
            'udid': '228-1337-swag-trolling-trollface',
            'chk': 'abcdE'
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.get_challenges, data)

    # if there was a way to get actual lvl id...
    def get_daily(self) -> int:
        data = {
            'weekly': 0
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_get_daily, data)['id']

    def get_weekly(self) -> int:
        data = {
            'weekly': 1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_get_daily, data)['id']

    def get_creators(self) -> list[User]:
        return [User(**u) for u in _send(self.gdps_id, GD.get_creators, {})['leaderboards']]

    def get_user_list(self, _type: int = 0):
        data = {
            'type': _type
        }

        self._use_session(data)

        return [User(**u) for u in _send(self.gdps_id, GD.get_user_list, data)['users']]

    # я не знаю как выглядят левелскоры потому что их сука нету
    def get_level_scores(self, level: int | Level, _type: int = 1, mode: int = 0, is_platformer: bool = False):
        data = {
            'levelID': level if level is int else level.id,
            'type': _type,
            'mode': mode
        }
        self._use_session(data)
        if not is_platformer:
            return _send(self.gdps_id, GD.get_level_scores, data)
        else:
            return _send(self.gdps_id, GD.get_level_plat_scores, data)


    def get_song_info(self, songID: int) -> Song:
        data = {
            'songID': songID
        }

        return Song(**_send(self.gdps_id, GD.get_song_info, data)['music'])

    def get_top_artists(self, page: int = 0) -> list[str]:
        data = {
            'page': page
        }

        return [artist for artist in _send(self.gdps_id, GD.get_top_artists, data)['artists'].values() if artist]

    def get_messages(self, page: int = 0, getSent: bool = False):
        data = {
            'page': page,
            'getSent': 1 if getSent else 0
        }

        self._use_session(data)

        return [Message(**m) for m in _send(self.gdps_id, GD.message_get, data)['messages']]

    def get_message(self, messageID: int):
        data = {
            'messageID': messageID
        }

        self._use_session(data)

        return Message(**_send(self.gdps_id, GD.message_get, data)['content'])

    def get_gauntlets(self, special: bool = True):
        data = {
            'special': 1 if special else 0
        }

        return [Gauntlet(**g) for g in _send(self.gdps_id, GD.get_gauntlets, data)['gauntlets']]

    def get_map_packs(self, page: int = 0):
        data = {
            'page': page
        }

        return [MapPack(**p) for p in _send(self.gdps_id, GD.get_map_packs, data)['packs']]

    def delete_message(self, message: int | Message, isSender: bool | None):
        data = {
            'messageID': message if isinstance(message, int) else message.id,
            'isSender': 1 if isSender else 1 if isinstance(message, Message) and message.uid == self.user_id else 0
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.message_delete, data)

    def delete_comment(self, comment: int | Comment, level: int | Level | None = None):
        data = {
            'commentID': comment if isinstance(comment, int) else comment.id,
            'levelID': level if isinstance(level, int) else level.id if isinstance(level, Level) else comment.lvl_id \
                if isinstance(comment, Comment) else -1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.comment_delete, data)

    def upload_level(self, levelName: str, levelLength: LevelLength, objects: int, coins: int, levelString: str,
                    gameVersion: int = 22, levelID: int = 0, levelDesc: str = 'None', levelVersion: int = 1,
                    audioTrack: int = 0, songID: int = 0, twoPlayer: bool = 0, requestedStars: int = 0,
                    unlisted: int = 0, ldm: bool = False):
        data = {
            'levelName': levelName,
            'levelLength': levelLength.value,
            'objects': objects,
            'coins': coins,
            'levelString': levelString,
            'gameVersion': gameVersion,
            'levelID': levelID,
            'levelDesc': levelDesc,
            'levelVersion': levelVersion,
            'audioTrack': audioTrack,
            'songID': songID,
            'twoPlayer': twoPlayer,
            'requestedStars': requestedStars,
            'unlisted': unlisted,
            'ldm': 1 if ldm else 0
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_upload, data)

    def delete_level(self, level: int | Level):
        data = {
            'levelID': level if isinstance(level, int) else level.id
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_delete, data)

    def update_level_description(self, level: int | Level, plain_desc: str):
        data = {
            'levelID': level if isinstance(level, int) else level.id,
            'levelDesc': base64(plain_desc)
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_update_description, data)

    def report_level(self, level: int | Level):
        data = {
            'levelID': level if isinstance(level, int) else level.id
        }

        return _send(self.gdps_id, GD.level_report, data)

    @singledispatch
    def like_item(self, item: Likeable):
        data = {
            'itemID': item.id,
            'type': item.type,
            'like': 1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.like_item, data)

    @like_item.register
    def like_item(self, itemID: int, item_type: int):
        data = {
            'itemID': itemID,
            'type': item_type,
            'like': 1
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.like_item, data)

    @singledispatch
    def dislike_item(self, item: Likeable):
        data = {
            'itemID': item.id,
            'type': item.type,
            'like': 0
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.like_item, data)

    @dislike_item.register
    def dislike_item(self, itemID: int, item_type: int):
        data = {
            'itemID': itemID,
            'type': item_type,
            'like': 0
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.like_item, data)

    def upload_level_list(self, listName: str, listDesc: str, difficulty: LevelDifficulty, levels: list[Level] | LevelList, listID: int = 0, unlisted: int = 0):
        data = {
            'listName': listName,
            'listDesc': listDesc,
            'difficulty': difficulty.value,
            'listLevels': ','.join([str(lvl.id) for lvl in levels]) if isinstance(levels, list) else levels.levels,
            'listID': levels.id if not listID and isinstance(levels, LevelList) else 0,
            'unlisted': unlisted
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_list_upload, data)

    def get_level_lists(self, type: int = 2, _str: str = '',
                        page: int = 0, diff: SearchDifficulty = SearchDifficulty.NONE,
                        rated: bool = False, followed: str | list[User] = '') -> list[LevelList]:
        data = {
            'type': type,
            'page': page,
            'str': _str,
            'diff': diff.value[1],
            'demonFilter': diff.value[0],
            'star': 1 if rated else 0,
            'followed': followed if isinstance(followed, str) else ','.join([str(u.uid) for u in followed])
        }

        self._use_session(data)

        return [LevelList(**l) for l in _send(self.gdps_id, GD.level_list_search, data)['lists']]

    def delele_level_list(self, list: int | LevelList):
        data = {
            'listID': list if isinstance(list, int) else list.id
        }

        self._use_session(data)

        return _send(self.gdps_id, GD.level_list_delete, data)