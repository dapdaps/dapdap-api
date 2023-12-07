from tortoise.fields import CASCADE

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
    tag = fields.CharField(max_length=200, null=True)

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
    category_ids = fields.CharField(max_length=100, null=True)
    network_ids = fields.CharField(max_length=100, null=True)
    tag = fields.CharField(max_length=200, null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp'


class DappNetwork(BaseDBModel, BaseCreatedAtModel):
    network_id = fields.IntField(null=False)
    dapp_src = fields.CharField(max_length=200)
    dapp = fields.ForeignKeyField(
        'models.Dapp', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="dapp",
    )

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp_network'


class DappCategory(BaseDBModel, BaseCreatedAtModel):
    dapp_id = fields.IntField(null=False)
    category_id = fields.IntField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp_category'


class DappRelate(BaseDBModel, BaseCreatedAtModel):
    dapp_id = fields.IntField(null=False)
    dapp_id_relate = fields.IntField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp_relate'