# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
import json
import time
from typing import Type, List, Optional
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect
from apps.integral.models import ActivityReport
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

@router.get("/leaderboard/{activity_name}/{chain_id}")
async def leaderboard_top_realtime(activity_name: str, chain_id: str):
    report_data = await ActivityReport.filter(
        activity__name=activity_name, chain_id=chain_id
    ).order_by('-tx_count').limit(10).values(
        "tx_count", address="user__address", group_name="group__name"
    )
    return report_data
