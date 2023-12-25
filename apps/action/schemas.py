# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : schemas.py
import uuid
from typing import Optional

from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from apps.action.models import ActionRecord

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


class TokenCurrency(BaseModel):
    address: Optional[str] = ""
    symbol: Optional[str] = ""
    decimals: Optional[int] = 0

    def to_dict(self):
        return {
            "address": self.address,
            "symbol": self.symbol,
            "decimals": self.decimals,
        }

class ActionIn(BaseModel):
   action_status: Optional[str] = ""
   tx_id: Optional[str] = ""
   account_id: Optional[str] = ""
   account_info: Optional[str] = ""
   action_switch: Optional[int] = 0
   action_network_id: Optional[str] = ""
   action_title: Optional[str] = ""
   action_type: Optional[str] = ""
   action_tokens: Optional[str] = ""
   action_amount: Optional[str] = ""
   template: Optional[str] = ""
   source: Optional[str] = ""
   chain_id: Optional[int] = 0
   to_chain_id: Optional[int] = 0
   token_in_currency: Optional[TokenCurrency]
   token_out_currency: Optional[TokenCurrency]

   
class DeleteActionIn(BaseModel):
    action_id: Optional[int] = 0
    action_id_list: Optional[list] = []


class UpdateActionRecordIn(BaseModel):
    action_record_id: Optional[int] = 0
    tx_id: Optional[str] = ""
    action_status: Optional[str] = ""


ActionRecordResultOut = pydantic_model_creator(ActionRecord)

