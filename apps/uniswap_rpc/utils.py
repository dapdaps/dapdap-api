# @Time : 10/20/23 10:02 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
import asyncio
import json
from web3 import Web3, AsyncWeb3
from web3.exceptions import TooManyRequests, Web3Exception
from settings.config import settings

with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoter.abi") as f:
    QUOTER_ABI: str = json.load(f)

with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoterv2.abi") as f:
    QUOTER_V2_ABI: str = json.load(f)

async def fetch_quote(contract, token_in, token_out, fee, amount, sqrtPriceLimitX96):
    price = None
    try:
        price = await contract.functions.quoteExactInputSingle(
            token_in, token_out, fee, amount, sqrtPriceLimitX96
        ).call()
    except TooManyRequests:
        print("Too many Requests Need change RPC!")
    except Web3Exception:
        pass
    except Exception as e:
        print(e)
    return {"price": price, "fee": fee}

async def quoter_check(provider, quoter_contract_address, token_in, token_out, amount):
    # w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
    w3 = AsyncWeb3(Web3.AsyncHTTPProvider(provider))
    sqrtPriceLimitX96 = 0
    contract = w3.eth.contract(address=quoter_contract_address, abi=QUOTER_ABI)

    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)
    fee_list = [100, 500, 3000, 10000]
    tasks = [fetch_quote(contract, token_in, token_out, fee, amount, sqrtPriceLimitX96) for fee in fee_list]
    result = await asyncio.gather(*tasks)
    result = [item for item in result if item["price"]]
    # lambda x: x
    if not result:
        result = {"noPair": True}
    else:
        result = sorted(result, key=lambda t: t['price'], reverse=True)
        result = {
            "max_fee": result[0]["fee"],
            "max_price": result[0]["price"],
            "noPair": False,
            "all_price": result
        }
        # result.append(price)
    return result

async def fetch_quote_v2(contract_v2, token_in, token_out, fee, amount, sqrtPriceLimitX96):
    price = None
    gas_estimate = None
    try:
        price = await contract_v2.functions.quoteExactInputSingle(
            {
                "tokenIn": token_in,
                "tokenOut": token_out,
                "amountIn": amount,
                "fee": fee,
                "sqrtPriceLimitX96": sqrtPriceLimitX96
            }
        ).call()
        gas_estimate = price[3]
        price = price[0]
    except TooManyRequests:
        print("Too many Requests Need change RPC!")
    except Web3Exception:
        pass
    except Exception as e:
        print(e)

    return {"price": price, "gasEstimate": gas_estimate, "fee": fee}

async def quoter_v2_check(provider, quoter_v2_contract_address, token_in, token_out, amount):
    w3 = AsyncWeb3(Web3.AsyncHTTPProvider(provider))
    sqrtPriceLimitX96 = 0
    contract_v2 = w3.eth.contract(address=quoter_v2_contract_address, abi=QUOTER_V2_ABI)

    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)
    fee_list = [100, 500, 3000, 10000]
    tasks = [fetch_quote_v2(contract_v2, token_in, token_out, fee, amount, sqrtPriceLimitX96) for fee in fee_list]
    result = await asyncio.gather(*tasks)
    result = [item for item in result if item["price"]]

    if not result:
        result = {"noPair": True}
    else:
        result = sorted(result, key=lambda t: t['price'], reverse=True)
        result = {
            "max_fee": result[0]["fee"],
            "max_price": result[0]["price"],
            "max_gasEstimate": result[0]["gasEstimate"],
            "noPair": False,
            "all_price": result
        }
    return result