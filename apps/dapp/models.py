from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel
from tortoise import fields


class Chain(BaseDBModel, BaseCreatedUpdatedAtModel):
    network_id = fields.CharField(max_length=128, null=False, unique=True)
    technology = fields.CharField(max_length=100, null=False)
    description = fields.CharField(max_length=1000, null=True)
    native_token = fields.CharField(max_length=50, null=True)
    milestones = fields.TextField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'chain'


class Dapp(BaseDBModel, BaseCreatedUpdatedAtModel):
    template = fields.CharField(max_length=255, null=False, index=True)
    description = fields.CharField(max_length=1000, null=True)
    favorite = fields.IntField()
    native_token = fields.CharField(max_length=50, null=True)
    quest = fields.BooleanField(null=True, default=False)
    chains = fields.CharField(max_length=300, null=False)
    functions = fields.CharField(max_length=200, null=False)
    show = fields.BooleanField(null=False, default=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'dapp'



