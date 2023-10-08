# @Time : 10/8/23 10:09 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : base_util.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

def get_limiter():
    limiter = Limiter(key_func=get_remote_address)
    return limiter