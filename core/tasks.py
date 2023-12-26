# @Time : 10/18/23 2:30 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : tasks.py
import time

import redis
from celery.utils.log import get_logger
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


# @celery_app.task(name="uniswap_quote_task")
# def uniswap_quote_task(chian_id):
#     from apps.uniswap_rpc.tasks.quote_task import update_swap
#     logger.info("*********** START uniswap_quote_task **********")
#     start_time = time.time()
#     run_async(update_swap(chian_id))
#     end_time = time.time()
#     logger.info(f"TOTAL RUN TIME sec {end_time - start_time}")
#     logger.info("*********** END uniswap_quote_task **********")
#     return {"done": "ok"}


@celery_app.task(name="uniswap_mint_task")
def uniswap_mint_task():
    from apps.uniswap_rpc.tasks.mint_task import update_mints
    from apps.uniswap_rpc.constant import GraphApi
    logger.info("*********** START uniswap_mint_task **********")
    start_time = time.time()
    run_async(update_mints(GraphApi['linea_mainnet'], 59144))
    run_async(update_mints(GraphApi['scroll_mainnet'], 534352))
    end_time = time.time()
    logger.info(f"TOTAL RUN TIME sec {end_time - start_time}")
    logger.info("*********** END uniswap_mint_task **********")
    return {"done": "ok"}


@celery_app.task(name="uniswap_pair_task")
def uniswap_pair_task():
    from apps.uniswap_rpc.tasks.pair_task import update_pairs
    from core.utils.redis_provider import pool
    lock_id = "uniswap_pair_task-lock"
    have_lock = False
    lock_redis = redis.StrictRedis(connection_pool=pool)
    try:
        have_lock = lock_redis.set(lock_id, "true", nx=True, ex=60 * 10)  # lock expires in 5 minutes
        if have_lock:
            logger.info("*********** START uniswap_pair_task **********")
            start_time = time.time()
            run_async(update_pairs())
            end_time = time.time()
            logger.info(f"TOTAL RUN TIME sec {end_time - start_time}")
            logger.info("*********** END uniswap_pair_task **********")
        else:
            logger.info("uniswap_pair_task is already running, skipping")
    finally:
        if have_lock:
            lock_redis.delete(lock_id)
    return {"done": "ok"}