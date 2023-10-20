# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py
import json

from fastapi import APIRouter, HTTPException
from starlette.requests import Request

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
async def get_token(request: Request, token_in: str, token_out:str, chain_id: str, amount: int):
    quoter = {
        ChainTypeEnum.ETH.upper(): "https://rpc.ankr.com/eth/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
        ChainTypeEnum.Arbitrum.upper(): "https://rpc.ankr.com/arbitrum/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
        ChainTypeEnum.Optimism.upper(): "https://rpc.ankr.com/optimism/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
        ChainTypeEnum.Polygon.upper(): "https://rpc.ankr.com/optimism/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    }
    quoter_v2 = {
        ChainTypeEnum.Base.upper(): "https://rpc.ankr.com/base/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
        ChainTypeEnum.BNB_Chain.upper(): "https://rpc.ankr.com/bsc/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
        ChainTypeEnum.Celo.upper(): "https://rpc.ankr.com/celo/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef"
    }
    quoter_contract_address = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
    quoter_v2_contract_address = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
    if chain_id.upper() == ChainTypeEnum.Celo.upper():
        quoter_contract_address = "0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8"
        quoter_v2_contract_address = "0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8"
    if chain_id.upper() == ChainTypeEnum.BNB_Chain.upper():
        quoter_v2_contract_address = "0x78D78E420Da98ad378D7799bE8f4AF69033EB077"
    if chain_id.upper() == ChainTypeEnum.Base.upper():
        quoter_v2_contract_address = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"

    if chain_id.upper() not in quoter.keys() and  chain_id.upper() not in quoter_v2.keys():
        raise HTTPException(400, "chain_id error")

    quoter_v2_flag = True if quoter_v2.get(chain_id.upper()) else False


    if quoter_v2_flag:
        provider = quoter_v2.get(chain_id.upper())
    else:
        provider = quoter.get(chain_id.upper())

    w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))

    # with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoter.abi") as f:
    #     quoter_abi: str = json.load(f)
    with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoterv2.abi") as f:
        quoter_v2_abi: str = json.load(f)
    fee = 500
    sqrtPriceLimitX96 = 0
    quoter_contract = w3.eth.contract(address=quoter_v2_contract_address, abi=quoter_v2_abi)
    price = quoter_contract.functions.quoteExactInputSingle(
        {
            "tokenIn": token_in,
            "tokenOut": token_out,
            "amountIn": amount,
            "fee": fee,
            "sqrtPriceLimitX96": sqrtPriceLimitX96
        }
        # token0, token1, fee, qty, sqrtPriceLimitX96
    ).call()
    return price[-1]
    # ChainTokenIn.chain_id in [ChainTypeEnum.ETH, ChainTypeEnum.Arbitrum, ChainTypeEnum.Optimism, ChainTypeEnum.Polygon]
    # ChainTokenIn.token_in