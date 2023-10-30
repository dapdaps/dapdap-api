# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
from tortoise.functions import Sum

from apps.integral.models import ActivityReport, ActivityConfig, TaskConfig, UserTaskResult, ChainTypeEnum
from apps.integral.schemas import UserTaskResultOut
from apps.integral.utils import ActivityReportFlag
from core.utils.base_util import get_limiter, ConnectionManager
import logging
from fastapi_pagination import Page

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/integral")

manager = ConnectionManager()


@router.websocket("/leaderboard/{activity_name}/ws", name="leaderboard_top")
async def leaderboard_top(websocket: WebSocket, activity_name: str):
    await manager.connect(websocket)
    report_data = await ActivityReport.filter(activity__name=activity_name).order_by('-tx_count').limit(10).values(
        "tx_count", address="user__address"
    )
    await manager.broadcast_json(report_data)
    try:
        while True:
            await ActivityReportFlag.wait()
            report_data = await ActivityReport.all().order_by('-tx_count').limit(10).values(
                "tx_count", address="user__address"
            )
            await manager.broadcast_json(report_data)
            ActivityReportFlag.clear()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/leaderboard/test", tags=["leaderboard test"])
async def leaderboard_test():
    report_data = await ActivityReport.create(
        activity_id = 1,
        user_id = 2,
        report_type ="user")
    return report_data


@router.get("/leaderboard/{activity_name}/{chain_id}", tags=["leaderboard_top_realtime"])
async def leaderboard_both(activity_name: str, chain_id: str):
    filters = {"activity__name": activity_name}
    if chain_id != ChainTypeEnum.ALL:
        filters.update({"chain_id": chain_id})
    report_data = await ActivityReport.filter(**filters).order_by('-tx_count').limit(10).values(
        "tx_count","report_type", "chain_id", address="user__address", group_name="group__name",
    )
    return report_data

@router.get("/leaderboard-group/{activity_name}/{chain_id}", tags=["leaderboard_top_realtime group"])
async def leaderboard_group(activity_name: str, chain_id: str):
    filters = {"activity__name": activity_name, "report_type": ActivityReport.ReportTypeEnum.GROUP}
    if chain_id != ChainTypeEnum.ALL:
        filters.update({"chain_id": chain_id})
    report_data = await ActivityReport.filter(**filters).order_by('-tx_count').limit(10).values(
        "tx_count","report_type", "chain_id", address="user__address", group_name="group__name",
    )
    return report_data

@router.get("/leaderboard-user/{activity_name}/{chain_id}", tags=["leaderboard_top_realtime user"])
async def leaderboard_user(activity_name: str, chain_id: str):
    filters = {"activity__name": activity_name, "report_type": ActivityReport.ReportTypeEnum.USER}
    if chain_id != ChainTypeEnum.ALL:
        filters.update({"chain_id": chain_id})
    report_data = await ActivityReport.filter(**filters).order_by('-tx_count').limit(10).values(
        "tx_count","report_type", "chain_id", address="user__address", group_name="group__name",
    )
    return report_data

@router.get("/user-rank/{activity_name}/{address}", tags=["user rank"])
async def user_rank(activity_name:str, address: str):
    # address
    filters = {"activity__name": activity_name}
    report_data = await ActivityReport.filter(**filters).annotate(
        sum_count=Sum("tx_count")).group_by("user__address").order_by('-sum_count').values(
        "sum_count", address="user__address"
    )
    result = {
        "rank": 0,
        "total_tx_count": 0
    }

    for index, data in enumerate(report_data):
        if data["address"] == address:
            result["rank"] = index
            result["total_tx_count"] = data["sum_count"]
            break
    return result

@router.get("/activity-info/{status_type}", tags=["activity_info"])
async def activity_info(status_type: ActivityConfig.ActivityStatusEnum):
    now_activaty = await ActivityConfig.filter(status=status_type).all()
    return now_activaty

@router.get("/task-info", tags=["task_info"])
async def task_info():
    return await TaskConfig.filter(is_active=True).order_by("action_type", "position").all()

@router.get("/user-task-info", tags=["user task info"], response_model=Page[UserTaskResultOut])
async def user_task_info():
    from fastapi_pagination.ext.tortoise import paginate
    # return await UserTaskResult.filter(user__address=address, ).all()
    return await paginate(UserTaskResult)
