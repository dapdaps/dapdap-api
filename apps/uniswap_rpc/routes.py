# @Time : 10/7/23 1:56 PM
# @Author : ZQ
# @Email : zq@ref.finance
# @File : routes.py

from fastapi import APIRouter
from starlette.requests import Request
from apps.uniswap_rpc.constant import CHAIN_RPC, QUOTER_V2_CONTRACT_ADDRESS, USE_QUOTER_V2, QUOTER_CONTRACT_ADDRESS, UNISWAP_API
from apps.uniswap_rpc.models import ChainTokenSwap, Mint, SwapRecord
from apps.uniswap_rpc.utils import quoter_v2_check, quoter_check
from apps.uniswap_rpc.schemas import Router, SwapRecordIn, AddSwapRecordIn
from core.utils.base_util import get_limiter
import logging
from web3 import Web3
import time

from core.utils.tool_util import success, successByInTract, errorByInTract
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

@router.get('/mint', tags=['uniswap'])
async def mint_info(token0: str, token1: str):
    mints = await Mint.filter(token0=token0.lower(), token1=token1.lower()).values("pool_fee")
    if not mints or len(mints) == 0:
        return success({"100": "0", "500": "0", "3000": "0", "10000": "0"})
    print(f"total: {len(mints)} {mints}")
    fee100: int = 0
    fee500: int = 0
    fee3000: int = 0
    fee10000: int = 0
    for mint in mints:
        if mint['pool_fee'] == 100:
            fee100 += 1
        elif mint['pool_fee'] == 500:
            fee500 += 1
        elif mint['pool_fee'] == 3000:
            fee3000 += 1
        elif mint['pool_fee'] == 10000:
            fee10000 += 1
    print(f"{fee100} {fee500} {fee3000} {fee10000}")
    data = {"100": str(round(fee100 * 100 / len(mints))), "500": str(round(fee500 * 100 / len(mints))),
            "3000": str(round(fee3000 * 100 / len(mints))), "10000": str(round(fee10000 * 100 / len(mints)))}
    return success(data)


@router.post('/records/add', tags=['uniswap'])
async def add_records(request: Request, swapRecordIn: AddSwapRecordIn):
    sender = swapRecordIn.sender.lower()
    txHash = swapRecordIn.tx_hash.lower()
    tokenIn = swapRecordIn.token_in_address.lower()
    tokenOut = swapRecordIn.token_out_address.lower()
    await SwapRecord(
        tx_hash=txHash,
        sender=sender,
        token_in_address = tokenIn,
        token_in_volume = swapRecordIn.token_in_volume,
        token_in_usd_amount = swapRecordIn.token_in_usd_amount,
        token_out_address = tokenOut,
        token_out_volume = swapRecordIn.token_out_volume,
        token_out_usd_amount = swapRecordIn.token_out_usd_amount,
        timestamp = int(time.time() * 1000)
    ).save()
    return success()


@router.post('/records', tags=['uniswap'], status_code=200)
@limiter.limit('200/minute')
async def query_records(request: Request, swapRecordIn: SwapRecordIn = None):
    if not swapRecordIn or not swapRecordIn.address or len(swapRecordIn.address) == 0:
        return errorByInTract("lack address/illegal address")
    address = swapRecordIn.address.lower()
    result = await SwapRecord.filter(sender=address).order_by('-timestamp').all().values(
        "timestamp", txHash = "tx_hash", tokenInAddress = "token_in_address", tokenInVolume = "token_in_volume", tokenInUsdAmount = "token_in_usd_amount",
        tokenOutAddress = "token_out_address", tokenOutVolume = "token_out_volume", tokenOutUsdAmount = "token_out_usd_amount",
    )
    return successByInTract(result)


