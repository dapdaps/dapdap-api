# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : models.py
from enum import Enum, IntEnum
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.fields.base import CASCADE
from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel



class UserIntegral(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField(db_constraint=False, model_name="models.UserInfo")
    integral = fields.IntField(default=0, description="user‘s integral")

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_integral'