# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from web3 import Web3
from apps.invite.schemas import ActivateCodeIn, GenerateCodeIn, GenerateCodeOut, InviteCodePoolDetailOut
from apps.invite.utils import generate_invite_code, is_w3_address
from core.utils.base_util import get_limiter
from settings.config import settings
import logging
from apps.invite.models import InviteCodePool
from apps.user.models import UserInfo
from core.utils.tool_util import success,  error

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/invite")

@router.get('/check-code/{code}', tags=['invite check code'])
@limiter.limit('100/minute')
async def check_code(request: Request, code: str):
    can_use = await InviteCodePool.filter(code=code, is_used=False).exists()
    return success({
        "can_use": can_use
    })

@router.get('/check-address/{address}', tags=['invite check address'])
@limiter.limit('100/minute')
async def check_address(request: Request, address: str):
    if not is_w3_address(address):
        return error("address is not web3")
    w3_address = Web3.to_checksum_address(address)
    current_user = await InviteCodePool.filter(used_user__address=w3_address).first().values("is_used")
    return success({
        "is_activated": current_user['is_used'] if current_user and current_user['is_used'] else False
    })

@router.post('/activate', tags=['invite activate'])
@limiter.limit('100/minute')
async def activate(request: Request, active_in: ActivateCodeIn):
    if not is_w3_address(active_in.address):
        return error("address is not web3")
    w3_address = Web3.to_checksum_address(active_in.address)
    pre_address_obj = await UserInfo.get_or_create(address=w3_address)
    pre_address_obj = pre_address_obj[0]
    code_obj = await InviteCodePool.filter(code=active_in.code).select_related("creator_user").first()
    if not code_obj:
        return error("The code not exist!")
    creator_w3_address = Web3.to_checksum_address(code_obj.creator_user.address)
    if creator_w3_address == w3_address:
        return error("creator user cannot invite self!")
    code_obj.used_user = pre_address_obj
    code_obj.is_used = True
    await code_obj.save()

    code_list = generate_invite_code(3)
    create_list = [
        InviteCodePool(
            code=code,
            creator_user=pre_address_obj,
            creator_type=InviteCodePool.CreatorTypeEnum.SYSTEM
        )
        for code in code_list
    ]

    result = await InviteCodePool.bulk_create(create_list)

    return success({
        "is_success": True,
        "invite_code_list": result
    })


@router.post('/generate', tags=['invite generate'], response_model=list[GenerateCodeOut])
@limiter.limit('100/minute')
async def generate_code(request: Request, generate_in: GenerateCodeIn):
    create_address_obj = None
    if generate_in.address:
        create_address_obj = await UserInfo.get_or_create(address=generate_in.address)
        create_address_obj = create_address_obj[0]
        # create_address_obj = await UserAddress.get(address=generate_in.address)
    code_list = generate_invite_code(generate_in.code_number)
    create_list = [
        InviteCodePool(
            code=code,
            creator_user=create_address_obj,
            creator_type=generate_in.creator_type
        )
        for code in code_list
    ]

    result =  await InviteCodePool.bulk_create(create_list)
    return [
        {
            "address": item.creator_user.address,
            "code": item.code,
            "creator_type": item.creator_type,
            "is_used": item.is_used
        }
        for item in result
    ]


@router.get('/get-address-code/{address}', tags=['invite get_address_code'])
@limiter.limit('100/minute')
async def get_address_code(request: Request, address: str):
    if not is_w3_address(address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(address)
    result = await InviteCodePool.filter(creator_user__address=web3_address).all()
    return success(result)


@router.get('/get-code-detail/{code}', tags=['invite code'], response_model=InviteCodePoolDetailOut)
@limiter.limit('100/minute')
async def get_code_detail(request: Request, code: str):
    result = await InviteCodePool.filter(code=code).first()
    return success(result)


@router.get('/get-invited-info/{address}', tags=['get some user invited info'])
@limiter.limit('100/minute')
async def get_invited_info(request: Request, address: str):
    if not Web3.is_address(address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(address)
    result = await InviteCodePool.filter(creator_user__address=web3_address, is_used=True).values(
        "code","created_at", "updated_at", used_user_address="used_user__address",
    )
    return success(result)
