from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
from tortoise import fields


class Network(BaseDBModel, BaseCreatedUpdatedAtModel):
    chain_id = fields.IntField(null=False, unique=True)
    priority = fields.IntField(null=True)
    name = fields.CharField(max_length=128, null=False)
    technology = fields.CharField(max_length=100, null=False)
    description = fields.CharField(max_length=1000, null=True)
    native_currency = fields.CharField(max_length=200, null=False)
    tbd_token = fields.CharField(max_length=10, null=False)
    logo = fields.CharField(max_length=100, null=True)
    rpc = fields.CharField(max_length=500, null=True)
    block_explorer = fields.CharField(max_length=100, null=True)
    milestones = fields.TextField(null=True)
    tag = fields.CharField(max_length=200, null=True)
    deepdive = fields.BooleanField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'network'