# @Time : 10/8/23 9:51 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : api.py
import logging
from fastapi import APIRouter, Depends, Response
from starlette.requests import Request

from apps.dapp.models import Network, Dapp
from apps.quest.models import Quest
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
from core.utils.redis_provider import list_base_token_price
from core.utils.tool_util import success, error
from apps.uniswap_rpc.constant import UNISWAP_API
from pydantic.types import Json
from urllib.parse import urljoin
import requests
logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter()


# @router.get('/', tags=['invite check code'])
# async def root():
#     return {"message": "welcome to dapdap"}


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
async def uniswap_api_check(request: Request, content: str):
    if len(content) == 0:
        return success()
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

