# @Time : 10/19/23 2:01 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : base_uniswap.py


import json

from uniswap import Uniswap, _str_to_addr
from web3 import Web3
from settings.config import settings

def test():
    address = None  # or None if you're not going to make transactions
    private_key = None  # or None if you're not going to make transactions
    version = 2  # specify which version of Uniswap to use
    provider = "https://base-mainnet.g.alchemy.com/v2/4TuLNLsQlwAQ98LpI3Ithta8BfQmaRJ7"  # can also be set through the environment variable `PROVIDER`
    provider = "https://muddy-falling-daylight.base-mainnet.quiknode.pro/04beb18973566dc08041008321a7c9feb25c5885/"
    # uniswap = Uniswap(address=address, private_key=private_key, version=version, provider="https://mainnet.infura.io/v3/a13269733d7b4670b050ca945ef1daaa")
    # Some token addresses we'll be using later in this guide


    usdc = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    DAI = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"
    weth = "0x4200000000000000000000000000000000000006"

    # print(uniswap.get_price_input(Web3.to_checksum_address(usdt), Web3.to_checksum_address(usdc), 10**6))

    w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
    # quoter_abi = open("./uniswap-v3/quoter.abi")

    with open(f"{settings.PROJECT_ROOT}/test/uniswap-v3/quoterv2.abi") as f:
        quoter_abi: str = json.load(f)
    # address = Web3.to_checksum_address(address)
    quoter_addr = _str_to_addr("0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a")
    quoter_addr = Web3.to_checksum_address(quoter_addr)
    quoter_contract = w3.eth.contract(address=quoter_addr, abi=quoter_abi)
    sqrtPriceLimitX96 = 0

    # token0 = eth
    # token1 = bat
    token0 = Web3.to_checksum_address(DAI)
    token1 = Web3.to_checksum_address(usdc)
    fee=3000
    qty=10**6
    price = quoter_contract.functions.quoteExactInputSingle(
        {
            "tokenIn" :  token0,
            "tokenOut" :  token1,
            "amountIn" :  qty,
            "fee" :  fee,
            "sqrtPriceLimitX96" : sqrtPriceLimitX96
        }
        # token0, token1, qty, fee, sqrtPriceLimitX96
    ).call()[-1]
    # base_weth = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")
    # route = [token0, base_weth, token1]
    # price = quoter_contract.functions.getAmountsOut(qty, route).call()[-1]
    print(price)

if __name__ == '__main__':
    test()
