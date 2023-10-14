# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : models.py
from enum import Enum, IntEnum
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.fields.base import CASCADE
from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
class ChainTypeEnum(str, Enum):
    ALL = "all"

    Mantle = "Mantle"
    Base = "Base"
    zkEVM = "zkEVM"
    MAINNET = "MAINNET"
    ArbitrumOne = "ArbitrumOne"
    Arbitrum = "Arbitrum"
    Other = "Other"

class ActionTypeEnum(str, Enum):
    Deposit = "Deposit"
    Redeem = "Redeem"
    Repay = "Repay"
    Withdraw = "Withdraw"
    Supply = "Supply"
    Mint = "Mint"
    Bridge = "Bridge"
    Swap = "Swap"
    Liquidity = "Liquidity"
    Other = "Other"

class UserIntegral(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField(db_constraint=False, model_name="models.UserInfo", on_delete=CASCADE)
    integral = fields.IntField(default=0, description="user‘s integral")

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_integral'


class TaskConfig(BaseDBModel, BaseCreatedAtModel):
    class TaskTypeEnum(str, Enum):
        DAYLY = 'day'
        MONTHLY = 'month'
        OTHER = 'other'


    task_name = fields.CharField(max_length=255)
    network =  fields.CharEnumField(ChainTypeEnum, default=ChainTypeEnum.ALL)
    action_type = fields.CharEnumField(ActionTypeEnum, max_length=20, default=ActionTypeEnum.Other)
    position = fields.IntField(default=0)
    task_type = fields.CharEnumField(enum_type=TaskTypeEnum, description="like daily task monthly task")
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = 'task_config'


class UserTaskResult(BaseDBModel, BaseCreatedAtModel):
    class TaskStatusEnum(IntEnum):
        INIT = 1
        DONE = 2
        FAIL = 3
    user = fields.ForeignKeyField('models.UserInfo', db_constraint=False, on_delete=CASCADE)
    task = fields.ForeignKeyField('models.TaskConfig', db_constraint=False, on_delete=CASCADE)
    status = fields.IntEnumField(TaskStatusEnum, default=TaskStatusEnum.INIT)

    class Meta:
        table = 'user_task_result'


class ActivityConfig(BaseDBModel, BaseCreatedAtModel):
    class ActivityStatusEnum(IntEnum):
        PRE_START = 1
        IN_PROGRESS = 2
        END = 3
    name = fields.CharField(max_length=255, unique=True)
    title = fields.CharField(max_length=255)
    status = fields.IntEnumField(ActivityStatusEnum, default=ActivityStatusEnum.PRE_START)
    start_date = fields.DateField()
    end_date = fields.DateField()
    description = fields.TextField()

    class Meta:
        table = 'activity_config'

class ActivityReport(BaseDBModel, BaseCreatedAtModel):
    class ReportTypeEnum(str, Enum):
        USER = 'user'
        GROUP = 'group'
        OTHER = 'other'
    activity = fields.ForeignKeyField('models.ActivityConfig', db_constraint=False, on_delete=CASCADE)
    user = fields.ForeignKeyField(db_constraint=False, model_name="models.UserInfo", on_delete=CASCADE)
    group = fields.ForeignKeyField(db_constraint=False, model_name="models.GroupInfo", on_delete=CASCADE)
    chain_id = fields.CharEnumField(ChainTypeEnum, default = ChainTypeEnum.Other)
    report_type = fields.CharEnumField(ReportTypeEnum)
    tx_count = fields.IntField(default=0)

    class Meta:
        table = 'activity_report'

