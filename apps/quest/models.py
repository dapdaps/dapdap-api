from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
from tortoise import fields

class QuestCampaign(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    start_time = fields.BigIntField(null=False)
    end_time = fields.BigIntField(null=False)
    status = fields.CharField(max_length=20, null=False)
    favorite = fields.IntField(null=False)
    total_reward = fields.IntField()
    total_users = fields.IntField()
    total_quest_execution = fields.IntField()

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_campaign'


class Quest(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=50, null=False)
    quest_campaign_id = fields.IntField(null=False)
    quest_category_id = fields.IntField(null=False)
    description = fields.CharField(max_length=200, null=True)
    logo = fields.CharField(max_length=100, null=True)
    start_time = fields.BigIntField(null=False)
    end_time = fields.BigIntField(null=False)
    is_period = fields.BooleanField()
    difficulty = fields.IntField(null=False)
    reward = fields.IntField(null=False)
    priority = fields.IntField(null=False)
    favorite = fields.IntField(null=False)
    gas_required = fields.CharField(max_length=20, null=True)
    time_required = fields.CharField(max_length=20, null=True)
    status = fields.CharField(max_length=20, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest'

