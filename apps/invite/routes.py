# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from datetime import timedelta

from fastapi import APIRouter, Depends
from starlette.requests import Request
from web3 import Web3

from apps.invite.dao import claimInviteReward
from apps.invite.schemas import ActivateCodeIn, GenerateCodeIn, GenerateCodeOut, InviteCodePoolDetailOut
from apps.invite.utils import generate_invite_code, is_w3_address
from core.auth.jwt import create_access_token, create_refresh_access_token
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
import logging
from apps.invite.models import InviteCodePool
from apps.user.models import UserInfo, UserReward
from core.utils.tool_util import success,  error
from settings.config import settings

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/invite")

@router.get('/check-code/{code}', tags=['invite'], dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def check_code(request: Request, code: str):
    can_use = await InviteCodePool.filter(code=code, is_used=False).exists()
    return success({
        "can_use": can_use
    })

@router.get('/check-address/{address}', tags=['invite'])
@limiter.limit('100/minute')
async def check_address(request: Request, address: str):
    if not is_w3_address(address):
        return error("address is not web3")
    w3_address = Web3.to_checksum_address(address)
    current_user = await InviteCodePool.filter(used_user__address=w3_address).first().values("is_used")
    return success({
        "is_activated": current_user['is_used'] if current_user and current_user['is_used'] else False
    })

@router.post('/activate', tags=['invite'])
@limiter.limit('100/minute')
async def activate(request: Request, active_in: ActivateCodeIn):
    if not is_w3_address(active_in.address):
        return error("address is not web3")
    w3_address = Web3.to_checksum_address(active_in.address)
    pre_address_obj = await UserInfo.get_or_create(address=w3_address)
    pre_address_obj = pre_address_obj[0]
    code_obj = await InviteCodePool.filter(code=active_in.code, is_used=False).select_related("creator_user").first()
    if not code_obj:
        return error("The code not exist or already used!")

    already_invited = await InviteCodePool.filter(used_user__address=w3_address, is_used=True).exists()
    if already_invited:
        return error("This address already invited!")

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

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_access_token_expires = timedelta(minutes=settings.JWT_REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES)

    return success({
        "is_success": True,
        "invite_code_list": result,
        "access_token": create_access_token(
            data={"user_id": pre_address_obj.id}, expires_delta=access_token_expires
        ),
        "refresh_access_token": create_refresh_access_token(
            data={"user_id": pre_address_obj.id}, expires_delta=refresh_access_token_expires
        ),
    })


@router.post('/generate', tags=['invite'], response_model=list[GenerateCodeOut], dependencies=[Depends(get_current_user)])
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


@router.get('/get-address-code/{address}', tags=['invite'], dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def get_address_code(request: Request, address: str):
    if not is_w3_address(address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(address)
    result = await InviteCodePool.filter(creator_user__address=web3_address).all()
    return success(result)


@router.get('/get-code-detail/{code}', tags=['invite'], response_model=InviteCodePoolDetailOut, dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def get_code_detail(request: Request, code: str):
    result = await InviteCodePool.get_or_none(code=code)
    return success(result)


@router.get('/get-invited-info/{address}', tags=['invite'], dependencies=[Depends(get_current_user)])
@limiter.limit('100/minute')
async def get_invited_info(request: Request, address: str):
    if not Web3.is_address(address):
        return error("address is not web3")
    web3_address = Web3.to_checksum_address(address)
    result = await InviteCodePool.filter(creator_user__address=web3_address, is_used=True).values(
        "code","created_at", "updated_at", used_user_address="used_user__address",
    )
    return success(result)


@router.get('/list', tags=['invite'])
@limiter.limit('100/minute')
async def invite_list(request: Request, user: UserInfo = Depends(get_current_user)):
    invites = await InviteCodePool.filter(creator_user_id=user.id, is_used=True).select_related("used_user").order_by("-updated_at")
    if len(invites) == 0:
        return success([])

    data = list()
    claimeReward = 0
    for invite in invites:
        if invite.status == "Active" and not invite.is_claimed:
            claimeReward += 10
        data.append({
            'code': invite.code,
            'status': invite.status if invite.status else 'Pending',
            'invited_user': {
                'address': invite.used_user.address,
                'avatar': invite.used_user.avatar,
                'username': invite.used_user.username,
            }
        })
    return success({
        'reward': claimeReward,
        'invite_reward': 10,
        'data': data,
    })


@router.post('/claim', tags=['invite'])
@limiter.limit('60/minute')
async def claim_reward(request: Request, user: UserInfo = Depends(get_current_user)):
    invites = await InviteCodePool.filter(creator_user_id=user.id, status='Active', is_claimed=False)
    if len(invites) == 0:
        return error("Cannot be claimed")
    await claimInviteReward(user.id)
    return success()