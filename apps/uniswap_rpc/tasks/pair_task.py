import asyncio

import logging

import requests

from apps.uniswap_rpc.constant import UNISWAP_API
from apps.uniswap_rpc.models import RoutePair
from tortoise import Tortoise
from core.init_app import TORTOISE_ORM

logger = logging.getLogger(__name__)


async def update_pairs():
    await Tortoise.init(config=TORTOISE_ORM)
    data = await RoutePair.filter(status=0).order_by('id').all()
    if not data or len(data) == 0:
        return {"done": "ok"}

    for pair in data:
        full_url = UNISWAP_API + "/router?chainId=" + str(pair.chain_id) + "&tokenIn=" + pair.token0 + "&tokenOut=" + pair.token1 + "&amount=" + str(10 ** pair.token0_decimals)
        try:
            rep = requests.get(full_url)
            result = rep.json()
            if result['code'] != 0 and result['data'] and result['data']['quote']:
                pair.status = 1
                await pair.save()
        except Exception as e:
            logger.error(f"update_pairs router exception: {e}")
            continue
    return {"done": "ok"}

async def testPairs():
    await update_pairs()

if __name__ == "__main__":
    asyncio.run(testPairs())