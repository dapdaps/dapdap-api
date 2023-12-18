# @Time : 10/8/23 9:51 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : api.py
import logging

import boto3
from fastapi import APIRouter, Depends, Response, UploadFile, File
from starlette.requests import Request

from apps.network.models import Network
from apps.dapp.models import Dapp
from apps.quest.dao import actionCompleted
from apps.quest.models import Quest, QuestAction, UserQuestAction
from apps.user.models import UserInfo
from core.auth.utils import get_current_user, get_current_user_optional
from core.common.constants import STATUS_ONGOING
from core.utils.base_util import get_limiter
from core.utils.redis_provider import list_base_token_price
from core.utils.tool_util import success, error
from apps.uniswap_rpc.constant import UNISWAP_API
from pydantic.types import Json
from urllib.parse import urljoin
import requests
from typing import Annotated, List

from settings.config import settings

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter()


@router.get('/health_check', tags=['base'])
@limiter.limit('5/second')
async def health_check(request: Request):
    logger.info(request)
    return {"message": "Running!"}


# @router.get('/get-token-price-by-dapdap', tags=['other'], dependencies=[Depends(get_current_user)])
@router.get('/get-token-price-by-dapdap', tags=['other'])
async def get_token_price_by_dapdap():
    result_data = list_base_token_price()
    return success(result_data)


@router.get('/debank', tags=['other'], dependencies=[Depends(get_current_user)])
@limiter.limit('10/second')
def debank_api(request: Request, url: str, params: Json):
    prefix_url = "https://pro-openapi.debank.com/"
    headers = {
        "AccessKey": "280c587032858a5df53764007c8a9fceea75d3bd"
    }
    full_url = urljoin(prefix_url , url)
    rep = requests.get(full_url, params=params, headers=headers, verify=False)
    result = rep.json()
    if rep.status_code == 200:
        return success(result)
    return error(result)


@router.get('/api/monitor/uniswap', tags=['base'], status_code=200)
@limiter.limit('5/second')
async def uniswap_api_check(request: Request, response: Response):
    logger.info(request)
    full_url = UNISWAP_API+"/monitor"
    rep = requests.get(full_url)
    response.status_code = rep.status_code


@router.get('/api/search', tags=['base'])
@limiter.limit('100/minute')
async def search(request: Request, content: str, user: UserInfo = Depends(get_current_user_optional)):
    if len(content) == 0:
        return success()

    if user:
        questActions = await QuestAction.filter(source='search', category__not='dapp').all()
        if len(questActions) > 0:
            for questAction in questActions:
                userQuestAction = await UserQuestAction.filter(account_id=user.id, quest_action_id=questAction.id).first()
                if userQuestAction:
                    continue
                quest = await Quest.filter(id=questAction.quest_id).first()
                if quest.status != STATUS_ONGOING:
                    continue
                await actionCompleted(user.id, questAction, quest)

    networks = await Network.filter(tag__contains=content).order_by("-created_at").all()
    dapps = await Dapp.filter(tag__contains=content).order_by("-created_at").all()
    quests = await Quest.filter(tag__contains=content).order_by("-created_at").all()

    dappDatas = list()
    if len(dapps) > 0:
        for dapp in dapps:
            dappData = {
                'id': dapp.id,
                'name': dapp.name,
                'description': dapp.description,
                'logo': dapp.logo,
            }
            if len(dapp.category_ids) > 0:
                dappIds = dapp.category_ids.split(",")
                dappData['category_ids'] = [int(item) for item in dappIds]
            if len(dapp.network_ids) > 0:
                networkIds = dapp.network_ids.split(",")
                dappData['network_ids'] = [int(item) for item in networkIds]
            dappDatas.append(dappData)

    return success({
        'networks': networks,
        'dapps': dappDatas,
        'quests': quests,
    })


@router.get('/config', tags=['base'])
@limiter.limit('100/minute')
async def config(request: Request):
    return success({
        'twitter_client_id': settings.TWITTER_CLIENT_ID,
        'twitter_redirect_url': settings.TWITTER_REDIRECT_URL,
        'telegram_bot_id': settings.TELEGRAM_BOT_ID,
        'telegram_bot_domain': settings.TELEGRAM_BOT_DOMAIN,
        'discord_client_id': settings.DISCORD_CLIENT_ID,
        'discord_redirect_url': settings.DISCORD_REDIRECT_URL,
    })


@router.post('/s3/upload', tags=['base'])
@limiter.limit('100/minute')
async def upload(request: Request, file: Annotated[UploadFile, File()] = None, files: List[Annotated[UploadFile, File()]] = None):
    def uploadFile(f):
        fileName = f.filename.lower()
        contentType = f.content_type.lower()
        s3 = boto3.client('s3', region_name=settings.AWS_REGION_NAME, aws_access_key_id=settings.AWS_S3_AKI,
                          aws_secret_access_key=settings.AWS_S3_SAK)
        s3.upload_fileobj(file.file, settings.AWS_BUCKET_NAME, "images/" + fileName,
                          ExtraArgs={'ACL': 'public-read', 'ContentType': contentType})

    if file:
        try:
            uploadFile(file)
        except Exception as e:
            logger.error(f'upload error: {e}')
            return error("error upload")
        return success({"url": settings.AWS_PATH + "/" + file.filename.lower()})
    if files:
        data = list()
        for file in files:
            try:
                uploadFile(file)
                data.append({
                    "url": settings.AWS_PATH + "/" + file.filename.lower(),
                })
            except Exception as e:
                logger.error(f'upload error: {e}')
                return error("error upload")

        return success(data)
