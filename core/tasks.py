# @Time : 10/18/23 2:30 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : tasks.py
import time
from celery.utils.log import get_logger

from apps.uniswap_rpc.constant import GraphApi
from core.celery_app import celery_app
from tortoise import run_async

logger = get_logger(__name__)


# @celery_app.task(acks_late=True)
# def test_data_celery(word: str) -> str:
#     for i in range(1, 11):
#         sleep(1)
#         current_task.update_state(state='PROGRESS',
#                                   meta={'process_percent': i * 10})
#     return f"test task return {word}"


@celery_app.task(name="uniswap_quote_task")
def uniswap_quote_task(chian_id):
    from apps.uniswap_rpc.tasks.quote_task import update_swap
    # print("*********** uniswap_eth_task **********")
    logger.info("*********** START uniswap_quote_task **********")
    start_time = time.time()
    # asyncio.run(update_eth_swap())
    run_async(update_swap(chian_id))
    # await update_eth_swap()
    end_time = time.time()
    logger.info(f"TOTAL RUN TIME sec {end_time - start_time}")
    logger.info("*********** END uniswap_quote_task **********")
    return {"done": "ok"}

@celery_app.task(name="uniswap_mint_task")
def uniswap_mint_task():
    from apps.uniswap_rpc.tasks.mint_task import update_mints
    # print("*********** uniswap_eth_task **********")
    logger.info("*********** START uniswap_mint_task **********")
    start_time = time.time()
    run_async(update_mints(GraphApi['linea_mainnet'], 59144))
    run_async(update_mints(GraphApi['scroll_mainnet'], 534352))
    end_time = time.time()
    logger.info(f"TOTAL RUN TIME sec {end_time - start_time}")
    logger.info("*********** END uniswap_mint_task **********")
    return {"done": "ok"}