# @Time : 10/20/23 10:29 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : init_data.py
from apps.uniswap_rpc.models import ChainTokenSwap


async def init_chain_token_data():
    CHAIN_META = {

    }
    await ChainTokenSwap.create()


async def eth_token_data():
    pass


async def arb_token_data():
    pass


async def op_token_data():
    pass


async def polygon_token_data():
    pass


async def base_token_data():
    pass


async def bsc_token_data():
    pass

async def celo_token_data():
    pass