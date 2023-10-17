# @Time : 10/8/23 9:51 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : api.py
import logging
from fastapi import APIRouter
from starlette.requests import Request
import requests
from core.utils.base_util import get_limiter

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter()

# @router.get('/', tags=['invite check code'])
# async def root():
#     return {"message": "welcome to dapdap"}


@router.get('/health_check', tags=['base health_check'])
@limiter.limit('5/second')
async def health_check(request: Request):
    logger.info(request)
    return {"message": "Running!"}


@router.get('/get_quote', tags=['base quote'])
@limiter.limit('5/second')
async def get_quote(request: Request):
    res = requests.post("https://api.uniswap.org/v2/quote", data={
        "tokenInChainId": 1,
        "tokenIn": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "tokenOutChainId": 1,
        "tokenOut": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "amount": "995000000000000000",
        "sendPortionEnabled": False,
        "type": "EXACT_INPUT",
        "configs": [
            {
                "protocols": [
                    "V3"
                ],
                "enableUniversalRouter": False,
                "routingType": "CLASSIC",
                "recipient": "0xc25d79fc4970479b88068ce8891ed9be5799210d"
            }
        ]
    })
    res = res.json()
    return res
