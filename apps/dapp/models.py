from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
from tortoise import fields


class Network(BaseDBModel, BaseCreatedUpdatedAtModel):
    chain_id = fields.IntField(null=False, unique=True)
    name = fields.CharField(max_length=128, null=False)
    technology = fields.CharField(max_length=100, null=False)
    description = fields.CharField(max_length=1000, null=True)
    native_currency = fields.CharField(max_length=200, null=False)
    tbd_token = fields.CharField(max_length=10, null=False)
    logo = fields.CharField(max_length=100, null=True)
    rpc = fields.CharField(max_length=500, null=True)
    block_explorer = fields.CharField(max_length=100, null=True)
    milestones = fields.TextField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'network'


class Dapp(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=128, null=False)
    description = fields.CharField(max_length=1000, null=True)
    route = fields.CharField(max_length=200, null=True)
    logo = fields.CharField(max_length=100, null=True)
    favorite = fields.IntField()
    default_chain_id = fields.IntField()
    priority = fields.IntField()
    tbd_token = fields.CharField(max_length=10, null=True)
    recommend = fields.BooleanField(null=False, default=False)
    recommend_icon = fields.CharField(max_length=100, null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp'


class DappNetwork(BaseDBModel, BaseCreatedAtModel):
    dapp_id = fields.IntField(null=False)
    network_id = fields.IntField(null=False)
    dapp_src = fields.CharField(max_length=200)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp_network'
