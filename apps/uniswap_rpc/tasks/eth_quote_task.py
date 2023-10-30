# @Time : 10/23/23 3:03 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : eth_quote_task.py
import asyncio
import time

from web3 import Web3

from apps.uniswap_rpc.constant import ChainEnum, QUOTER_CONTRACT_ADDRESS, CHAIN_RPC
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.utils import quoter_check
from tortoise import run_async, Tortoise

from core.init_app import TORTOISE_ORM


async def get_all_token_quoter(provider, contract_address, token_in, token_out, amount):
    check_res = await quoter_check(provider, contract_address, token_in, token_out, amount)
    if check_res["noPair"]:
        return {}
    return {
        "max_fee": check_res["max_fee"],
        "max_price": check_res["max_price"],
        "token_in": token_in,
        "token_out": token_out
    }

async def update_swap():
    await Tortoise.init(config=TORTOISE_ORM)
    start_time = time.time()

    token_objs = await ChainTokenSwap.filter(chain_id=ChainEnum.Ethereum).all()
    provider = CHAIN_RPC.get(ChainEnum.Ethereum)
    all_tasks = []
    for token_o in token_objs:
        token_in = token_o.token_in
        token_in_decimal = token_o.token_in_decimal
        token_out = token_o.token_out
        # token_out_decimal = token_o.token_out_decimal

        contract_address = QUOTER_CONTRACT_ADDRESS.get(ChainEnum.Ethereum)
        contract_address = Web3.to_checksum_address(contract_address)
        # result = await quoter_check(provider, contract_address, token_in, token_out, amount=10**token_in_decimal)
        all_tasks.append(get_all_token_quoter(provider, contract_address, token_in, token_out, amount=10**token_in_decimal))
    print(f"all_tasks number {len(all_tasks)}")
    all_result = await asyncio.gather(*all_tasks)
    rpc_end_time = time.time()
    print(f"RPC request sec {rpc_end_time-start_time}")

    update_db_tasks = []
    for item in all_result:
        if not item:
            continue
        update_db_tasks.append(ChainTokenSwap.filter(
            chain_id=ChainEnum.Ethereum, token_in=item['token_in'], token_out=item['token_out']
        ).update(
            quote_price=str(item['max_price']),
            quote_fee=item['max_fee'],
            updated_timestamp=time.time(),
        ))
    await asyncio.gather(*update_db_tasks)
    print(f"Write databse time sec {time.time()-rpc_end_time}")
    return {"result": "task Done"}

if __name__ == "__main__":
    run_async(update_swap())