from tortoise import fields

from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel

class Token(BaseDBModel, BaseCreatedUpdatedAtModel):
    chain_id = fields.IntField(null=False, default=0)
    address = fields.CharField(max_length=50, unique=True, null=False)
    symbol = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=50, null=True)
    icon = fields.CharField(max_length=100, null=True)
    decimal = fields.IntField(null=False, default=0)

    def __str__(self):
        return self.address

    class Meta:
        table = 'token'