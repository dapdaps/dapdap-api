from tortoise import fields
from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel


class ChainTokenSwap(BaseDBModel, BaseCreatedUpdatedAtModel):
    chain_id = fields.BigIntField()
    token_in = fields.CharField(max_length=100)
    token_in_decimal = fields.IntField()
    token_in_name = fields.CharField(max_length=100)
    token_out = fields.CharField(max_length=100)
    token_out_decimal = fields.IntField()
    token_out_name = fields.CharField(max_length=100)
    quote_price = fields.CharField(max_length=255, null=True)
    quote_fee = fields.IntField(null=True)
    updated_timestamp = fields.IntField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'chain_token_swap'

class Mint(BaseDBModel, BaseCreatedAtModel):
    tx_hash = fields.CharField(max_length=66, unique=True)
    token0 = fields.CharField(max_length=66)
    token1 = fields.CharField(max_length=66)
    pool_address = fields.CharField(max_length=66)
    pool_fee = fields.IntField()
    timestamp = fields.BigIntField(index=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'mint'
        indexes = ("token0", "token1")