import base64 as b64
import hashlib
from itertools import cycle

def xor(data: str, key: str) -> str:
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))

def base64(data: str, encode: bool = True) -> str:
    if encode:
        return b64.urlsafe_b64encode(data.encode()).decode()
    return b64.urlsafe_b64decode(data.encode()).decode()

def gjp(password: str, encode: bool = True) -> str:
    if encode:
        return base64(xor(password, "37526"))
    return xor(base64(password, False), "37526")

def gjp2(password: str) -> str:
    return hashlib.sha1((password+"mI29fmAnxgTs").encode()).hexdigest()