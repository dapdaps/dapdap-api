from tortoise.fields import CASCADE

from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
from tortoise import fields


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
    native_currency = fields.CharField(max_length=200, null=False)
    theme = fields.CharField(max_length=300, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp'


class DappNetwork(BaseDBModel, BaseCreatedAtModel):
    dapp_src = fields.CharField(max_length=200)
    dapp = fields.ForeignKeyField(
        'models.Dapp', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="dapp",
    )
    network = fields.ForeignKeyField(
        'models.Network', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="network",
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


class Category(BaseDBModel, BaseCreatedAtModel):
    name = fields.CharField(max_length=50, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'category'