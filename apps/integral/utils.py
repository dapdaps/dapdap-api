# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
import asyncio
from typing import Type, List, Optional
from apps.integral.models import ActivityReport
from settings.config import Settings
from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient


async def init_integral_signal():
    pass


ActivityReportFlag = asyncio.Event()
@post_save(ActivityReport)
async def signal_post_save(
        sender: "Type[ActivityReport]",
        instance: ActivityReport,
        created: bool,
        using_db: "Optional[BaseDBAsyncClient]",
        update_fields: List[str],
):
    ActivityReportFlag.set()
    return (sender, instance, created, using_db, update_fields)
    # Settings.ACTIVITY_REPORT_CHANGE += 1
