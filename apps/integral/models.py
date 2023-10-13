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


class UserIntegral(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField(db_constraint=False, model_name="models.UserInfo", on_delete=CASCADE)
    integral = fields.IntField(default=0, description="user‘s integral")

    def __str__(self):
        return self.id

    class Meta:
        table = 'user_integral'


class TaskConfig(BaseDBModel, BaseCreatedAtModel):
    task_name = fields.CharField(max_length=255)
    network =  fields.CharField(max_length=255, null=True)
    action_type = fields.CharField(max_length=255, null=True)
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


class ActivityReportDaily(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField('models.UserInfo', db_constraint=False)
    score = fields.IntField(default=0)
    report_date = fields.DateField()


class ActivityReportMonthly(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField('models.UserInfo', db_constraint=False)
    score = fields.IntField(default=0)
    report_date = fields.DateField()


class ActivityReportHistory(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField('models.UserInfo', db_constraint=False)
    score = fields.IntField(default=0)