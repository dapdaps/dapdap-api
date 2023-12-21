# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : models.py
from enum import IntEnum

from tortoise import fields
from tortoise.fields.base import CASCADE
from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel

# class UserAddress(BaseDBModel, BaseCreatedAtModel):
#     class ChainTypeEnum(str, Enum):
#         ETH = 'eth'
#         OTHER = 'other'
#     address = fields.CharField(max_length=25, unique=True, description="user's evm address")
#     chain_type = fields.CharEnumField(ChainTypeEnum, default=ChainTypeEnum.ETH)
#
#     def __str__(self):
#         return self.address
#
#     class Meta:
#         table = 'user_address'


class InviteCodePool(BaseDBModel, BaseCreatedUpdatedAtModel):
    class CreatorTypeEnum(IntEnum):
        SYSTEM = 1
        USER = 2

    code = fields.CharField(max_length=25, unique=True)
    creator_user = fields.ForeignKeyField(
        'models.UserInfo', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True,
        related_name="relate_creator_user",
        description="address create invite code"
    )
    used_user = fields.ForeignKeyField(
        'models.UserInfo', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True,
        related_name="relate_used_user",
        description="address used invite code"
    )
    creator_type = fields.IntEnumField(CreatorTypeEnum, description="user type", default=CreatorTypeEnum.SYSTEM)
    is_used = fields.BooleanField(default=False, description="code is used")
    is_claimed = fields.BooleanField(default=False)
    status = fields.CharField(max_length=20, null=True)
    reward = fields.IntField(null=True)

    def __str__(self):
        return self.code

    class Meta:
        table = 'invite_code_pool'
