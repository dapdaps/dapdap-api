# @Time : 10/13/23 1:15 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : models.py
from enum import Enum

from tortoise import fields
from tortoise.fields.base import CASCADE

from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel


class UserInfo(BaseDBModel, BaseCreatedAtModel):
    class ChainTypeEnum(str, Enum):
        ETH = 'eth'
        OTHER = 'other'
    address = fields.CharField(max_length=50, unique=True, description="user's evm address")
    account_info = fields.CharField(max_length=25, null=True)
    chain_type = fields.CharEnumField(ChainTypeEnum, default=ChainTypeEnum.ETH)
    last_login = fields.DatetimeField(null=True)
    avatar = fields.CharField(max_length=200, null=True)
    username = fields.CharField(max_length=50, null=True)

    def __str__(self):
        return self.address

    class Meta:
        table = 'user_info'


class GroupInfo(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=100, unique=True, description="group name")
    title = fields.CharField(max_length=255, description="group title")
    users = fields.ManyToManyField("models.UserInfo", db_constraint=False, on_delete=CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        table = 'group_info'


class UserFavorite(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False)
    relate_id = fields.IntField(null=False)
    category = fields.CharField(max_length=20, null=False)
    is_favorite = fields.BooleanField()

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_favorite'


class UserReward(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False)
    reward = fields.IntField(null=False)
    claimed_reward = fields.IntField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_reward'


class UserInfoExt(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False, unique=True)
    twitter_user_id = fields.CharField(max_length=20, null=True)
    twitter_username = fields.CharField(max_length=100, null=True)
    twitter_access_token_expires = fields.BigIntField(null=True)
    twitter_access_token_type = fields.CharField(max_length=50, null=True)
    twitter_access_token = fields.CharField(max_length=200, null=True)
    twitter_refresh_token = fields.CharField(max_length=200, null=True)
    telegram_user_id = fields.CharField(max_length=20, null=True)
    discord_user_id = fields.CharField(max_length=30, null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_info_ext'