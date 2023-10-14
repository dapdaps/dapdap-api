# @Time : 10/14/23 5:06 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : test.py
import random
from datetime import datetime
from apps.integral.models import TaskConfig, ChainTypeEnum, ActionTypeEnum, ActivityConfig, ActivityReport, \
    UserTaskResult
from tortoise import Tortoise, connections, run_async

from apps.user.models import UserInfo, GroupInfo
from core.init_app import get_app_list
from settings.config import settings


async def init_project_data():
    db_url = settings.DB_URL
    app_list = get_app_list()
    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )
    # Tortoise.get_connection(connections.get("default"), safe=False)
    # create daily task
    task_list = [
        TaskConfig(
            task_name="Swap on Arbitrum",
            network=ChainTypeEnum.Arbitrum,
            action_type=ActionTypeEnum.Swap,
            position=0,
            task_type=TaskConfig.TaskTypeEnum.DAYLY,
        ),
        TaskConfig(
            task_name="Bridge on Arbitrum",
            network=ChainTypeEnum.Arbitrum,
            action_type=ActionTypeEnum.Bridge,
            position=1,
            task_type=TaskConfig.TaskTypeEnum.DAYLY,
        ),
        TaskConfig(
            task_name="Liquidity on Arbitrum",
            network=ChainTypeEnum.Arbitrum,
            action_type=ActionTypeEnum.Liquidity,
            position=2,
            task_type=TaskConfig.TaskTypeEnum.DAYLY,
        )
    ]
    await TaskConfig.bulk_create(task_list)

    # create activity
    await ActivityConfig.create(
        name = "hackathon_001",
        title = "Win Rare Whale NFT!",
        status = ActivityConfig.ActivityStatusEnum.IN_PROGRESS,
        start_date = datetime(year=2023, month=10, day=12),
        end_date = datetime(year=2023, month=10, day=31),
        description = "For hackathon",
    )
    await Tortoise.close_connections()

async def init_user_fake_data():
    db_url = settings.DB_URL
    app_list = get_app_list()
    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )

    # address_list = [
    #     "0x6608cCF9Eb860dC7Cd92e8b689193C692c9629B7",
    #     "0x6Cd07A52F7129212c4039fb7a8EB46166218B660",
    #     "0xB3385f4AeA990eeE257B22F8e6229F77a03d0c1c",
    #     "0xE0B2026E3DB1606ef0Beb764cCdf7b3CEE30Db4A",
    #     "0x2f46a6764B3Fd7dA627d4F3c901e7f4BA4675d5D",
    #     "0xb0C966782a7298F74BC7CC42d6c3ff811E0C6D3c",
    #     "0xBf94F0AC752C739F623C463b5210a7fb2cbb420B",
    #     "0x4e008A165bC5D96167DccB9de7f6c3E852d4D111",
    #     "0x1dFeDC82B41447D3FA5E587164322B270B6CF995",
    #     "0x8216874887415e2650D12D53Ff53516F04a74FD7"
    # ]
    # await UserInfo.bulk_create([
    #     UserInfo(address=address) for address in address_list
    # ])

    # user_info_objs = await UserInfo.all().limit(3)
    # group_info_obj = await GroupInfo.get_or_create(
    #     name="winwin_group",
    #     title="WinWin Group",
    # )
    # group_info_obj = group_info_obj[0]
    # for user_obj in user_info_objs:
    #     await group_info_obj.users.add(user_obj)
    # await group_info_obj.save()

    all_user_obj = await UserInfo.all()
    group_info_obj = await GroupInfo.all().first()
    activity_config_obj = await ActivityConfig.all().first()
    arb_report_list = [ActivityReport(
        activity=activity_config_obj,
        user=user_obj,
        # group=,
        chain_id=ChainTypeEnum.Arbitrum,
        report_type=ActivityReport.ReportTypeEnum.USER,
        tx_count=random.randint(1,400)
    ) for user_obj in all_user_obj]

    arb_report_list.append(
        ActivityReport(
            activity=activity_config_obj,
            # user=user_obj,
            group=group_info_obj,
            chain_id=ChainTypeEnum.Arbitrum,
            report_type=ActivityReport.ReportTypeEnum.GROUP,
            tx_count=random.randint(1, 400)
        )
    )

    mts_report_list = [ActivityReport(
        activity=activity_config_obj,
        user=user_obj,
        # group=,
        chain_id=ChainTypeEnum.Metis,
        report_type=ActivityReport.ReportTypeEnum.USER,
        tx_count=random.randint(1, 400)
    ) for user_obj in all_user_obj]

    mts_report_list.append(
        ActivityReport(
            activity=activity_config_obj,
            # user=user_obj,
            group=group_info_obj,
            chain_id=ChainTypeEnum.Metis,
            report_type=ActivityReport.ReportTypeEnum.GROUP,
            tx_count=random.randint(1, 400)
        )
    )

    pol_report_list = [ActivityReport(
        activity=activity_config_obj,
        user=user_obj,
        # group=,
        chain_id=ChainTypeEnum.Polygon,
        report_type=ActivityReport.ReportTypeEnum.USER,
        tx_count=random.randint(1, 400)
    ) for user_obj in all_user_obj]

    pol_report_list.append(
        ActivityReport(
            activity=activity_config_obj,
            # user=user_obj,
            group=group_info_obj,
            chain_id=ChainTypeEnum.Polygon,
            report_type=ActivityReport.ReportTypeEnum.GROUP,
            tx_count=random.randint(1, 400)
        )
    )
    all_report_list = arb_report_list + mts_report_list + pol_report_list
    await ActivityReport.bulk_create(all_report_list)

async def init_task_info():
    db_url = settings.DB_URL
    app_list = get_app_list()
    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )
    task_objs = await TaskConfig.all()

    user_obj = await UserInfo.first()
    result = [UserTaskResult(
        user=user_obj,
        task=task,
        status=random.choice(list(UserTaskResult.TaskStatusEnum)),
        record_date=datetime(year=2023, month=10, day=i),
    ) for task in task_objs for i in range(1, 14)]
    await UserTaskResult.bulk_create(result)


if __name__ == "__main__":
    # run_async(init_project_data())
    # run_async(init_user_fake_data())
    run_async(init_task_info())
