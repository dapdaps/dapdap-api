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
    banner = fields.CharField(max_length=100, null=True)
    link = fields.CharField(max_length=100, null=True)
    total_users = fields.IntField()

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_campaign'


class QuestCampaignInfo(BaseDBModel, BaseCreatedUpdatedAtModel):
    total_reward = fields.IntField()
    total_users = fields.IntField()
    total_quest_execution = fields.IntField()

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_campaign_info'


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
    tag = fields.CharField(max_length=200, null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest'


class QuestAction(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=50, null=False)
    quest_campaign_id = fields.IntField(null=False)
    quest_id = fields.IntField(null=False)
    description = fields.CharField(max_length=200, null=True)
    times = fields.IntField(null=False)
    category = fields.CharField(max_length=30, null=True)
    category_id = fields.IntField(null=False)
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


class UserQuestAction(BaseDBModel, BaseCreatedUpdatedAtModel):
    account_id = fields.IntField(null=False)
    quest_id = fields.IntField(null=False)
    quest_action_id = fields.IntField(null=False)
    quest_campaign_id = fields.IntField(null=False)
    times = fields.IntField(null=False)
    status = fields.CharField(max_length=20, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_quest_action'


class QuestLong(BaseDBModel, BaseCreatedUpdatedAtModel):
    name = fields.CharField(max_length=50, null=False)
    description = fields.CharField(max_length=200, null=True)
    category = fields.CharField(max_length=50, null=False)
    rule = fields.TextField(null=True)
    status = fields.CharField(max_length=20, null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'quest_long'


class UserDailyCheckIn(BaseDBModel, BaseCreatedAtModel):
    account_id = fields.IntField(null=False)
    quest_long_id = fields.IntField(null=False)
    reward = fields.IntField(null=False)
    check_in_time = fields.BigIntField(null=False)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_daily_check_in'


class UserRewardRank(BaseDBModel, BaseCreatedAtModel):
    reward = fields.IntField(null=False)
    rank = fields.IntField(null=False)
    account = fields.ForeignKeyField(
        'models.UserInfo', db_constraint=False, on_delete=CASCADE.SET_NULL, null=True, related_name="account",
    )

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_reward_rank'



class UserRewardClaim(BaseDBModel, BaseCreatedAtModel):
    account_id = fields.IntField(null=False)
    reward = fields.IntField(null=False)
    claim_time = fields.BigIntField(null=True)
    category = fields.CharField(max_length=20, null=False)
    obj_id = fields.IntField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_reward_claim'
