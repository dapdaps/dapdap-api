# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : models.py
from tortoise.models import Model
from tortoise import fields
from core.base.base_models import BaseDBModel


class Action(Model):
    action_id = fields.BigIntField(pk=True, index=True)
    action_title =  fields.CharField(max_length=255, null=True, index=True)
    action_type =  fields.CharField(max_length=255, null=True, index=True)
    action_tokens =  fields.CharField(max_length=255, null=True, index=True)
    action_amount =  fields.CharField(max_length=255, null=True, index=True)
    account_id =  fields.CharField(max_length=255, null=True, index=True)
    account_info =  fields.CharField(max_length=255, null=True, index=True)
    template =  fields.CharField(max_length=255, null=True, index=True)
    status =  fields.CharField(max_length=1, null=True, index=True)
    count_number =  fields.BigIntField(index=True)
    action_network_id = fields.CharField(max_length=255, null=True, index=True)
    timestamp = fields.BigIntField(index=True)
    create_time = fields.DatetimeField()
    token_in_currency = fields.CharField(max_length=255, null=True)
    token_out_currency = fields.CharField(max_length=255, null=True)
    chain_id = fields.IntField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 't_action'


class ActionRecord(BaseDBModel):
    action_id = fields.BigIntField(index=True)
    action_title =  fields.CharField(max_length=255, null=True, index=True)
    action_type =  fields.CharField(max_length=255, null=True, index=True)
    action_tokens =  fields.CharField(max_length=255, null=True, index=True)
    action_amount =  fields.CharField(max_length=255, null=True, index=True)
    account_id =  fields.CharField(max_length=255, null=True, index=True)
    account_info =  fields.CharField(max_length=255, null=True, index=True)
    template =  fields.CharField(max_length=255, null=True, index=True)
    status =  fields.CharField(max_length=1, null=True, index=True)
    action_status =  fields.CharField(max_length=255, null=True, index=True)
    tx_id =  fields.CharField(max_length=255, null=True, index=True)
    action_network_id = fields.CharField(max_length=255, null=True, index=True)
    gas = fields.CharField(max_length=255, null=True)
    timestamp = fields.BigIntField(index=True)
    create_time = fields.DatetimeField()
    source = fields.CharField(max_length=20, null=True)
    dapp_id = fields.IntField(null=True)
    chain_id = fields.IntField(null=True)
    to_chain_id = fields.IntField(null=True)
    token_in_currency = fields.CharField(max_length=255, null=True)
    token_out_currency = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.action_id

    class Meta:
        table = 't_action_record'


class ActionChain(BaseDBModel):
    count =  fields.IntField()
    network_id = fields.IntField()
    action_title =  fields.CharField(max_length=512, null=False)
    dapp_id =  fields.IntField()

    def __str__(self):
        return self.id

    class Meta:
        table = 't_action_chain'
        indexes = ("action_network_id", "count")
        unique_together = ("action_title", "template", "action_network_id")