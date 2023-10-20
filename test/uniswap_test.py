# @Time : 10/18/23 8:29 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : uniswap_test.py
import json

from uniswap import Uniswap, _str_to_addr
from web3 import Web3
from settings.config import settings

def test():
    address = None  # or None if you're not going to make transactions
    private_key = None  # or None if you're not going to make transactions
    version = 2  # specify which version of Uniswap to use
    provider = "https://mainnet.infura.io/v3/a13269733d7b4670b050ca945ef1daaa"  # can also be set through the environment variable `PROVIDER`
    uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)
    # Some token addresses we'll be using later in this guide
    eth = "0x0000000000000000000000000000000000000000"
    bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
    dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    usdt = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    usdc = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

    print(uniswap.get_price_input(Web3.to_checksum_address(usdt), Web3.to_checksum_address(usdc), 10**6))

    w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
    # quoter_abi = open("./uniswap-v3/quoter.abi")

    with open(f"{settings.PROJECT_ROOT}/test/uniswap-v3/quoter.abi") as f:
        quoter_abi: str = json.load(f)
    # address = Web3.to_checksum_address(address)
    quoter_addr = _str_to_addr("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")
    quoter_addr = Web3.to_checksum_address(quoter_addr)
    quoter_contract = w3.eth.contract(address=quoter_addr, abi=quoter_abi)
    sqrtPriceLimitX96 = 0

    token0 = eth
    token1 = bat
    token0 = Web3.to_checksum_address(usdt)
    token1 = Web3.to_checksum_address(usdc)
    fee=3000
    qty=10**6
    price = quoter_contract.functions.quoteExactInputSingle(
        token0, token1, fee, qty, sqrtPriceLimitX96
    ).call()
    print(price)


    # 8570781297292584595020

if __name__ == '__main__':
    test()