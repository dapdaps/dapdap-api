# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
import datetime
import json
import time
from typing import Type, List, Optional
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect
from tortoise.functions import Count, Sum

from apps.integral.models import ActivityReport, ActivityConfig, TaskConfig, UserTaskResult, ChainTypeEnum
from core.utils.base_util import get_limiter, ConnectionManager
from settings.config import settings
from tortoise.expressions import F
import logging

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/integral")

manager = ConnectionManager()


@router.websocket("/leaderboard/{activity_name}/ws", name="leaderboard_top")
async def leaderboard_top(websocket: WebSocket, activity_name: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"1231231231")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"left the chat")


@router.websocket("/leaderboard-test/test/ws")
async def leaderboard_test_top(websocket: WebSocket):
    await websocket.accept()
    # report_data = {}
    # pre_count = settings.ACTIVITY_REPORT_CHANGE
    # report_data = await ActivityReport.all().order_by('-tx_count').limit(10).values(
    #     "tx_count", address="user__address"
    # )
    # await websocket.send_json(report_data)
    try:
        while True:
            if settings.ACTIVITY_REPORT_CHANGE > pre_count:
                report_data = await ActivityReport.all().order_by('-tx_count').limit(10).values(
                    "tx_count", address="user__address"
                )
                pre_count = settings.ACTIVITY_REPORT_CHANGE
                await websocket.send_json(report_data)
    except WebSocketDisconnect:
        await websocket.close()


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
async def leaderboard_user(activity_name:str, address: str):
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

@router.get("/user-task-info/{address}", tags=["user task info"])
async def user_task_info(address: str):
    # return await UserTaskResult.filter(user__address=address, ).all()
    return await UserTaskResult.all()
