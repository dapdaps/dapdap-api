# @Time : 10/8/23 9:51 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : api.py
import logging
from fastapi import APIRouter
from starlette.requests import Request
from core.utils.base_util import get_limiter
from core.utils.redis_provider import list_base_token_price
from core.utils.tool_util import success, error

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


@router.get('/get-token-price-by-dapdap', tags=['get_token_price_by_dapdap'])
async def get_token_price_by_dapdap():
    result_data = list_base_token_price()
    return success(result_data)

@router.get('/debank', tags=['quote-local'])
async def debank(token_in: str, token_out:str, chain_id: int):
    # result = await ChainTokenSwap.filter(chain_id=chain_id, token_in=token_in, token_out=token_out).values(
    #     "quote_price", "quote_fee", "updated_timestamp",
    # )
    pass
    return {}
