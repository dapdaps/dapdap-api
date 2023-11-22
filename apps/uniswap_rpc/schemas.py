# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : schemas.py
import uuid
from typing import Optional

from pydantic import BaseModel, validator

class BaseProperties(BaseModel):
    @validator("hashed_id", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()

    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={"id", "is_superuser", "is_active"},
        )

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class ChainTokenIn(BaseModel):
    token_in: Optional[str]
    token_out: Optional[str]
    chain_id: Optional[str]
    amount: Optional[int]

class Router(BaseModel):
    token_in: str | None = None
    token_out: str | None = None
    chain_id: int | None = None
    amount: str | None = None


class SwapRecordIn(BaseModel):
    address: str | None = None

class AddSwapRecordIn(BaseModel):
    sender: str
    tx_hash: str
    token_in_address: str
    token_in_volume: str
    token_in_usd_amount: str
    token_out_address: str
    token_out_volume: str
    token_out_usd_amount: str