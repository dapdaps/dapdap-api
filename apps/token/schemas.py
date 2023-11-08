from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.token.models import Token


class AddTokenIn(BaseModel):
    chain_id: Optional[int] = 0
    address: str = None
    name: Optional[str] = ""
    symbol: Optional[str] = ""
    decimal: Optional[int] = 0
    icon: Optional[str] = ""

TokenOut = pydantic_model_creator(Token)