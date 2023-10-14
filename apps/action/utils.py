# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : utils.py
import secrets

from typing import Type, List, Optional
from apps.action.models import ActionRecord
from apps.integral.models import ActivityConfig, ActivityReport
from apps.user.models import UserInfo, GroupInfo

from settings.config import  Settings
from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient
from tortoise.expressions import Q
import datetime

@post_save(ActionRecord)
async def action_signal_post_save(
    sender: "Type[ActionRecord]",
    instance: ActionRecord,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
):
    # 1. check user info table
    (user_info,_) = await UserInfo.get_or_create(address = instance.account_id, account_info=instance.account_info,chain_type=instance.action_network_id)

    # 2. get activity from ActivityConfig
    now_time = datetime.datetime.utcnow()
    activity_obj = await ActivityConfig.filter(Q(status = ActivityConfig.ActivityStatusEnum.IN_PROGRESS) &
                                               Q(ActivityConfig.start_date <= now_time) & Q(ActivityConfig.end_date >= now_time))
    if activity_obj is None:
        return

    activity_obj = activity_obj[0]
    
    # 3. update 'user' entry to ActivityReport
    user_activity_report_obj = await ActivityReport.get_or_create(activity_id = activity_obj.id, user_id = user_info.id,chain_id=instance.action_network_id,report_type=ActivityReport.ReportTypeEnum.USER)
    user_activity_report_obj.tx_count += 1
    user_activity_report_obj.save()
    
    # 4. update 'group' entry to ActivityReport
    group_infos = GroupInfo.filter(Q(users__id=user_info.id))
    if group_infos:
        for group in group_infos:
            (group_activity_report_obj, _) = await ActivityReport.get_or_create(activity_id = activity_obj.id, group_id = group.id,chain_id=instance.action_network_id,report_type=ActivityReport.ReportTypeEnum.GROUP)
            group_activity_report_obj.tx_count += 1
            group_activity_report_obj.save()
            