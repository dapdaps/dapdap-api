# @Time : 10/25/23 6:04 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : schemas.py
from typing import Optional

from pydantic import BaseModel


class CredentialsSchema(BaseModel):
    address: Optional[str]


class JWTToken(BaseModel):
    access_token: str
    token_type: str


# class JWTTokenData(BaseModel):
#     username: str = None


class JWTTokenPayload(BaseModel):
    user_id: int = None


class Msg(BaseModel):
    msg: str