# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException
from settings.config import settings
import logging
from models import InviteCodePool
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invite")

@router.get('/check_code/{code}', tags=['invite check code'])
async def check_code(code: str):
    can_use = await InviteCodePool.filter(code=code, is_used=False).exists()
    return {
        "can_use": can_use
    }

@router.get('/check_address/{address}', tags=['invite check address'])
async def check_address(address: str):
    current_user = await InviteCodePool.filter(used_user__address=address).first().values("is_used")
    return {
        "is_activated": current_user['is_used'] if current_user['is_used'] else False
    }

@router.post('/activate', tags=['invite activate'])
async def activate():
    pass

@router.post('/generate', tags=['invite generate'])
async def generate_code():
    pass