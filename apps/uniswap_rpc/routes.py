# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
import json

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from apps.uniswap_rpc.constant import CHAIN_RPC, QUOTER_V2_CONTRACT_ADDRESS, USE_QUOTER_V2, QUOTER_CONTRACT_ADDRESS
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.utils import quoter_v2_check, quoter_check
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
import logging
from web3 import Web3

from core.utils.tool_util import success

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