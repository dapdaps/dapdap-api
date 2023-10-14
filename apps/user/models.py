# @Time : 10/13/23 1:15 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : models.py
from enum import Enum, IntEnum

from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.fields.base import CASCADE, NO_ACTION

from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel


class UserInfo(BaseDBModel, BaseCreatedAtModel):
    class ChainTypeEnum(str, Enum):
        ETH = 'eth'
        OTHER = 'other'
    address = fields.CharField(max_length=50, unique=True, description="user's evm address")
    account_info = fields.CharField(max_length=25, null=True)
    chain_type = fields.CharEnumField(ChainTypeEnum, default=ChainTypeEnum.ETH)

    def __str__(self):
        return self.address

    class Meta:
        table = 'user_info'

class GroupInfo(BaseDBModel, BaseCreatedAtModel):
    name = fields.CharField(max_length=100)
    users = fields.ManyToManyField("models.UserInfo", on_delete=CASCADE)
