from tortoise.fields import CASCADE

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
    total_action = fields.IntField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest'


class QuestAction(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=50, null=False)
    quest_campaign_id = fields.IntField(null=False)
    quest_id = fields.IntField(null=False)
    category_id = fields.IntField(null=False)
    description = fields.CharField(max_length=200, null=True)
    difficulty = fields.IntField(null=False)
    times = fields.IntField(null=False)
    source = fields.CharField(max_length=50, null=True)
    dapps = fields.CharField(max_length=200, null=True)
    networks = fields.CharField(max_length=100, null=True)
    to_networks = fields.CharField(max_length=200, null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_action'


class QuestCategory(BaseDBModel, BaseCreatedAtModel):
    name = fields.CharField(max_length=50, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_category'


class UserQuest(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False)
    quest_campaign_id = fields.IntField(null=False)
    action_completed = fields.IntField(null=False)
    status = fields.CharField(max_length=20, null=False)
    is_claimed = fields.BooleanField()
    claimed_at = fields.DatetimeField(null=True)
    quest = fields.ForeignKeyField(
        'models.Quest', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="quest",
    )

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_quest'


class UserRequestAction(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False)
    quest_id = fields.IntField(null=False)
    quest_action_id = fields.IntField(null=False)
    quest_campaign_id = fields.IntField(null=False)
    times = fields.IntField(null=False)
    status = fields.CharField(max_length=20, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_action'


class QuestCampaignReward(BaseDBModel, BaseCreatedAtModel):
    quest_campaign_id = fields.IntField(null=False)
    reward = fields.IntField(null=False)
    rank = fields.IntField(null=False)
    account = fields.ForeignKeyField(
        'models.UserInfo', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="user",
    )

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_campaign_reward'