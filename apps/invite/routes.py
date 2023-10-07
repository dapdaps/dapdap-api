# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException

from apps.invite.schemas import ActivateCodeIn, GenerateCodeIn, GenerateCodeOut, InviteCodePoolDetailOut
from apps.invite.utils import generate_invite_code
from settings.config import settings
import logging
from apps.invite.models import InviteCodePool, UserAddress

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/invite")

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
async def activate(active_in: ActivateCodeIn):
    pre_address_obj = await UserAddress.get_or_create(address=active_in.address)
    code_obj = await InviteCodePool.filter(code=active_in.code).first()
    if not code_obj:
        raise {
            "is_success": False,
            "error": "The code not exist!"
        }
    code_obj.used_user = pre_address_obj
    code_obj.is_used = True
    await code_obj.save()
    return {
        "is_success": True
    }


@router.post('/generate', tags=['invite generate'], response_model=GenerateCodeOut)
async def generate_code(generate_in: GenerateCodeIn):
    create_address_obj = None
    if generate_in.address:
        create_address_obj = await UserAddress.get_or_create(address=generate_in.address)
    code_list = generate_invite_code(generate_in.code_number)
    create_list = [
        InviteCodePool(
            code=code,
            creator_user=create_address_obj,
            creator_type=generate_in.creator_type
        )
        for code in code_list
    ]

    return await InviteCodePool.bulk_create(create_list)


@router.post('/get_address_code/{address}', tags=['invite get_address_code'])
async def get_address_code(address: str):
    return await InviteCodePool.filter(
        creator_user__address=address, is_used=False
    ).values_list("code", flat=True)


@router.post('/get_code_detail/{code}', tags=['invite code'], response_model=InviteCodePoolDetailOut)
async def get_code_detail(code: str):
    return await InviteCodePool.filter(code=code).first()