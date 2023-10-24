# @Time : 10/24/23 3:09 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : quote_task.py
import asyncio
import time

from web3 import Web3

from apps.uniswap_rpc.constant import ChainEnum, QUOTER_CONTRACT_ADDRESS, CHAIN_RPC, USE_QUOTER_V2, QUOTER_V2_CONTRACT_ADDRESS
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.utils import quoter_check, quoter_v2_check
from tortoise import run_async, Tortoise

from core.init_app import TORTOISE_ORM


async def get_all_token_quoter(provider, contract_address, token_in, token_out, amount, is_v2=False):
    if is_v2:
        check_res = await quoter_v2_check(provider, contract_address, token_in, token_out, amount)
    else:
        check_res = await quoter_check(provider, contract_address, token_in, token_out, amount)
    if check_res["noPair"]:
        return {}
    return {
        "max_fee": check_res["max_fee"],
        "max_price": check_res["max_price"],
        "token_in": token_in,
        "token_out": token_out
    }


async def update_swap(chain_id: ChainEnum):
    await Tortoise.init(config=TORTOISE_ORM)
    start_time = time.time()

    token_objs = await ChainTokenSwap.filter(chain_id=chain_id).all()
    provider = CHAIN_RPC.get(chain_id)
    all_tasks = []
    is_v2 = chain_id in USE_QUOTER_V2
    contract_address = QUOTER_V2_CONTRACT_ADDRESS.get(chain_id) if is_v2 else QUOTER_CONTRACT_ADDRESS.get(chain_id)
    contract_address = Web3.to_checksum_address(contract_address)
    for token_o in token_objs:
        token_in = token_o.token_in
        token_in_decimal = token_o.token_in_decimal
        token_out = token_o.token_out
        # token_out_decimal = token_o.token_out_decimal

        # result = await quoter_check(provider, contract_address, token_in, token_out, amount=10**token_in_decimal)
        all_tasks.append(
            get_all_token_quoter(provider, contract_address, token_in, token_out,
                                 amount=10 ** token_in_decimal, is_v2=is_v2)
        )
    print(f"all_tasks number {len(all_tasks)}")
    all_result = await asyncio.gather(*all_tasks)
    rpc_end_time = time.time()
    print(f"RPC request sec {rpc_end_time - start_time}")

    update_db_tasks = []
    for item in all_result:
        if not item:
            continue
        update_db_tasks.append(ChainTokenSwap.filter(
            chain_id=chain_id, token_in=item['token_in'], token_out=item['token_out']
        ).update(
            quote_price=str(item['max_price']),
            quote_fee=item['max_fee'],
            updated_timestamp=time.time(),
        ))
    await asyncio.gather(*update_db_tasks)
    print(f"Write databse time sec {time.time() - rpc_end_time}")
    return {"result": "task Done"}
