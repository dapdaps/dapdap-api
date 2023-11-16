# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py

from fastapi import APIRouter
from starlette.requests import Request
from apps.uniswap_rpc.constant import CHAIN_RPC, QUOTER_V2_CONTRACT_ADDRESS, USE_QUOTER_V2, QUOTER_CONTRACT_ADDRESS, UNISWAP_API
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.utils import quoter_v2_check, quoter_check
from apps.uniswap_rpc.schemas import Router
from core.utils.base_util import get_limiter
import logging
from web3 import Web3

from core.utils.tool_util import success,error,successByInTract,errorByInTract
import requests

logger = logging.getLogger(__name__)
limiter = get_limiter()
# router = APIRouter(prefix="/api/uniswap", dependencies=[Depends(get_current_user)])
router = APIRouter(prefix="/api/uniswap")


@router.get('/quote', tags=['uniswap'])
@limiter.limit('100/minute')
async def quote_check(request: Request, token_in: str, token_out:str, chain_id: int, amount: int):
    provider = CHAIN_RPC.get(chain_id)

    if chain_id in USE_QUOTER_V2:
        quoter_v2_contract_address = QUOTER_V2_CONTRACT_ADDRESS.get(chain_id)
        quoter_v2_contract_address = Web3.to_checksum_address(quoter_v2_contract_address)
        result = await quoter_v2_check(provider, quoter_v2_contract_address, token_in, token_out, amount)
    else:
        contract_address = QUOTER_CONTRACT_ADDRESS.get(chain_id)
        contract_address = Web3.to_checksum_address(contract_address)
        result = await quoter_check(provider, contract_address, token_in, token_out, amount)
    return result

@router.get('/quote-local', tags=['uniswap'])
async def quote_local(token_in: str, token_out:str, chain_id: int):
    result = await ChainTokenSwap.filter(chain_id=chain_id, token_in=token_in, token_out=token_out).values(
        "quote_price", "quote_fee", "updated_timestamp",
    )
    return success(result)

@router.post('/v2/quote', tags=['uniswap'], status_code=200)
@limiter.limit('100/minute')
async def quote_router(request: Request, router: Router=None):
    if not router:
        return errorByInTract("lack params")
    if not router.token_in or len(router.token_in) == 0:
        return errorByInTract("illegal token_in")
    if not router.token_out or len(router.token_out) == 0:
        return errorByInTract("illegal token_out")
    if not router.amount or len(router.amount) == 0:
        return errorByInTract("illegal amount")
    if not router.chain_id or router.chain_id <= 0:
        return errorByInTract("illegal chain_id")

    full_url = UNISWAP_API+"/router?chainId="+str(router.chain_id)+"&tokenIn="+router.token_in+"&tokenOut="+router.token_out+"&amount="+router.amount
    try:
        rep = requests.get(full_url)
        result = rep.json()
    except Exception as e:
        logger.error(f"router exception: {e}")
        return errorByInTract("Internal Server Error")
    if result['code'] == 0:
        return errorByInTract(result['message'])
    else:
        return successByInTract(result['data'])
