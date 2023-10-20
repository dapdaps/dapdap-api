# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
import json

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from apps.uniswap_rpc.constant import CHAIN_RPC, QUOTER_V2_CONTRACT_ADDRESS
from apps.uniswap_rpc.schemas import ChainTokenIn
from core.utils.base_util import get_limiter
from settings.config import settings
import logging
import datetime
from tortoise.expressions import Q
from apps.integral.models import ChainTypeEnum
from web3 import Web3
logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/uniswap")

@router.get('/get_token', tags=['get_token'])
@limiter.limit('100/minute')
async def get_token(request: Request, token_in: str, token_out:str, chain_id: int, amount: int):
    provider = CHAIN_RPC.get(chain_id)
    quoter_v2_contract_address = QUOTER_V2_CONTRACT_ADDRESS.get(chain_id)
    quoter_v2_contract_address = Web3.to_checksum_address(quoter_v2_contract_address)
    w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
    # with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoter.abi") as f:
    #     quoter_abi: str = json.load(f)
    with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoterv2.abi") as f:
        quoter_v2_abi: str = json.load(f)
    sqrtPriceLimitX96 = 0
    contract_v2 = w3.eth.contract(address=quoter_v2_contract_address, abi=quoter_v2_abi)
    # contract = w3.eth.contract(address=quoter_contract_address, abi=quoter_abi)

    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)
    fee_list = [100, 500, 3000, 10000]
    max_fee = 0
    max_price = 0
    for fee in fee_list:
        price = None
        try:
            price = contract_v2.functions.quoteExactInputSingle(
                {
                    "tokenIn": token_in,
                    "tokenOut": token_out,
                    "amountIn": amount,
                    "fee": fee,
                    "sqrtPriceLimitX96": sqrtPriceLimitX96
                }
            ).call()[0]
        except Exception as e:
            print(e)
        if price and price > max_price:
            max_fee = fee
            max_price = price

    if max_fee == 0:
        result = {"noPair": True}
    else:
        result = {
            "max_fee": max_fee,
            "max_price": max_price,
            "noPair": False
        }
            # result.append(price)
    return result