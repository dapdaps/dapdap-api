# @Time : 10/20/23 10:02 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
import json
from web3 import Web3
from settings.config import settings


async def quoter_check(provider, quoter_contract_address, token_in, token_out, amount):
    w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
    with open(f"{settings.PROJECT_ROOT}/apps/uniswap_rpc/uniswap-v3/quoter.abi") as f:
        quoter_abi: str = json.load(f)
    sqrtPriceLimitX96 = 0
    contract = w3.eth.contract(address=quoter_contract_address, abi=quoter_abi)

    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)
    fee_list = [100, 500, 3000, 10000]
    max_fee = 0
    max_price = 0
    for fee in fee_list:
        price = None
        try:
            price = contract.functions.quoteExactInputSingle(
                token_in, token_out, fee, amount,sqrtPriceLimitX96
            ).call()
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

async def quoter_v2_check(provider, quoter_v2_contract_address, token_in, token_out, amount):
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