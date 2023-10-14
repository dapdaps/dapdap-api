# @Time : 10/14/23 5:06 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : test.py
from datetime import datetime
from apps.integral.models import TaskConfig, ChainTypeEnum, ActionTypeEnum, ActivityConfig
from tortoise import Tortoise, connections, run_async

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

if __name__ == "__main__":
    run_async(init_project_data())