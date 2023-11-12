import asyncio
import logging
import threading
import time
from web3 import Web3, AsyncWeb3

import settings.config
from apps.uniswap_rpc.constant import ChainEnum, CHAIN_RPC
from settings.config import settings

logger = logging.getLogger(__name__)
gasPrice = 0
gasPriceTime = 0

def startSmartRouterTask():
    job_thread = threading.Thread(target=lambda: run_coroutine_every_interval(fetchGasPriceTask, 5))
    job_thread.start()

def getGasPrice():
    if int(time.time()) > gasPriceTime+15:
        return 0
    else:
        return gasPrice

def run_coroutine_every_interval(coroutine, interval):
    """Run the given coroutine function at a set interval."""
    async def run_coroutine():
        while True:
            await coroutine()  # Run the coroutine function
            await asyncio.sleep(interval)  # Wait for specified interval

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_coroutine())
    loop.close()

async def fetchGasPriceTask():
    provider = CHAIN_RPC.get(ChainEnum.Linea) if settings.ENV != "test" else CHAIN_RPC.get(ChainEnum.LineaTestnet)
    w3 = AsyncWeb3(Web3.AsyncHTTPProvider(provider))
    global gasPrice
    global gasPriceTime
    try:
        gasPrice = await w3.eth.gas_price
        gasPriceTime = int(time.time())
        #print(f'{gasPrice} {gasPriceTime}')
        #logger.info(f"fetchGasPriceTask {gasPrice} {gasPriceTime}")
    except Exception as e:
        logger.error(f"fetchGasPriceTask Exception: {e}")

# if __name__ == "__main__":
#     startSmartRouterTask()
#     while True:
#         time.sleep(1000)
