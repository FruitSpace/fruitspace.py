import json
from typing import Any

import requests

import enums
import urls
from enums import TopType
from models import User, Comment, Level
from urls import GD
from utils import gjp, gjp2

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
    # username: str = None
    # password: str = None
    # user_id: int = None


    def __init__(self, gdps_id: str, username: str = None, password: str = None):
        self.gdps_id = gdps_id
        # if username and password:
        #     self.username = username
        #     self.password = password
        #     user_id = self._login()
        #     if user_id < 0:
        #         raise Exception(f'Incorrect username or password. Error code: {user_id}')
        #     else:
        #         self.user_id = user_id


    # def _use_session(self, data: dict[str, Any]):
    #     if self.user_id:
    #         data['accountID'] = self.user_id
    #         data['gjp'] = gjp(self.password)
    #         data['gjp2'] = gjp2(self.password)

    
    def _login(self) -> int:
        # noinspection PyTypeChecker
        resp = _send(self.gdps_id, GD.account_login, {'username': self.username, 'password': self.password},
                         use_json=True)
        return int(resp['code'])

    
    def get_user(self, id: int) -> User:
        data = {'targetAccountID': id}

        # self._use_session(data)

        s = _send(self.gdps_id, GD.get_user_info, data)

        return User(**s['user'])

    
    def get_user_comments(self, id: int) -> list[Comment]:
        data = {'accountID': id}

        # self._use_session(data)

        comms = _send(self.gdps_id, GD.account_comment_get, data)['comments']

        ret: list[Comment] = []
        for comm in comms:
            ret.append(Comment(**comm))
        return ret

    
    def get_level(self, id: int):
        data = {'levelID': id}

        # self._use_session(data)

        return _send(self.gdps_id, GD.level_download, data)

    
    def get_levels(self,
                   gauntlet: int | None = None,
                   followed: str | None = None,
                   demonFilter: int | None = None,
                   accountID: int | None = None,
                   gjp: str | None = None,
                   diff: int | None = None,
                   len: int | None = None,
                   song: int | None = None,
                   customSong: int | None = None,
                   page: int = 0,
                   count: int = 10,
                   type: int = 0,
                   str: str = "",
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
        if demonFilter:
            d['demonFilter'] = demonFilter
        if accountID:
            d['accountID'] = accountID
        if gjp:
            d['gjp'] = gjp
        if diff:
            d['diff'] = diff
        if len:
            d['len'] = len
        if song:
            d['song'] = song
        if customSong:
            d['customSong'] = customSong

        d['page'] = page
        d['count'] = count
        d['type'] = type
        d['str'] = str
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

        # self._use_session(d)

        levels = _send(self.gdps_id, GD.get_levels, d)['levels']
        ret: list[Level] = []
        for lvl in levels:
            ret.append(Level(**lvl))
        return ret


    def get_leaderboard(self, type: TopType = TopType.top, count: int = 100) -> list[User]:
        data = {'type': type.value, 'count': count}

        # self._use_session(data)

        leaderboard = _send(self.gdps_id, GD.get_scores, data)['leaderboard']

        ret: list[User] = []
        for l in leaderboard:
            ret.append(User(**l))

        return ret

    def get_friend_requests(self, accountID: int = None, gjp2: str = None, getSent: bool = False, total: int = 10):
        data = {
            'accountID': accountID,
            'gjp2': gjp2,
            'getSent': getSent,
            'total': total
        }
        # TODO
        # self._use_session(data)

        return _send(self.gdps_id, GD.friend_get_requests, data)

        pass


    def get_comment_history(self, userID: int, mode: int = 0, page: int = 0, total: int = 0) -> list[Comment]:
        data = {
            'userID': userID,
            'mode': mode,
            'page': page,
            'total': total
        }

        ret = [Comment(**comm) for comm in _send(self.gdps_id, GD.comment_get_history, data)['comments']]

        return ret


    def get_level_comments(self, levelID: int, page: int = 0, mode: int = 0, total: int = 10):
        data = {
            'levelID': levelID,
            'page': page,
            'mode': mode,
            'total': total
        }

        ret = [Comment(**comm) for comm in _send(self.gdps_id, GD.comments_get, data)['comments']]

        return ret


    def get_challenges(self):
        data = {}

        return _send(self.gdps_id, GD.get_challenges, data)