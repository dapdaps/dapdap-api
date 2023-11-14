# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py

from fastapi import APIRouter
from starlette.requests import Request
from apps.uniswap_rpc.constant import CHAIN_RPC, QUOTER_V2_CONTRACT_ADDRESS, USE_QUOTER_V2, QUOTER_CONTRACT_ADDRESS, UNISWAP_API
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.utils import quoter_v2_check, quoter_check
from core.utils.base_util import get_limiter
import logging
from web3 import Web3

from core.utils.tool_util import success,error
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

@router.get('/v2/quote', tags=['uniswap'])
@limiter.limit('100/minute')
async def quote_router(request: Request, token_in: str, token_out:str, chain_id: int, amount: int):
    full_url = UNISWAP_API+"/router?chainId="+str(chain_id)+"&tokenIn="+token_in+"&tokenOut="+token_out+"&amount="+str(amount)
    rep = requests.get(full_url)
    result = rep.json()
    if result['code'] == 0:
        return error(result['message'])
    else:
        return success(result['data'])
