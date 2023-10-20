# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : models.py
from enum import Enum, IntEnum
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.fields.base import CASCADE
from apps.integral.models import ChainTypeEnum
from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel


class ChainTokenSwap(BaseDBModel, BaseCreatedUpdatedAtModel):
    chain_id = fields.CharEnumField(ChainTypeEnum, max_length=100)
    token_in = fields.CharField(max_length=100)
    token_in_decimal = fields.IntField()
    token_in_name = fields.CharField(max_length=100)
    token_out = fields.CharField(max_length=100)
    token_out_decimal = fields.IntField()
    token_out_name = fields.CharField(max_length=100)
    quote_result = fields.FloatField()

    def __str__(self):
        return self.id

    class Meta:
        table = 'chain_token_swap'