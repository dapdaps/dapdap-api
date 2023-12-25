# @Time : 10/18/23 11:36 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : celery_app.py
from celery import Celery
from settings.config import settings
from apps.uniswap_rpc.constant import ChainEnum
broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'
backend_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1'

celery_app = Celery("celery_worker", backend=backend_url, broker=broker_url)
celery_app.config_from_object('settings.celery_config')
celery_app.autodiscover_tasks(['core'])


celery_app.conf.beat_schedule = {
    # 'eth_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Ethereum, )
    # },
    # 'arb_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Arbitrum, )
    # },
    # 'op_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Optimisim, )
    # },
    # 'polygon_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Polygon, )
    # },
    # 'base_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Base, )
    # },
    # 'bsc_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.BSC, )
    # },
    # 'ava_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Avalanche, )
    # },
    # 'celo_beat_quote': {
    #     'task': 'uniswap_quote_task',
    #     'schedule': 20,
    #     'args': (ChainEnum.Celo, )
    # },
    'uniswap_beat_mint': {
        'task': 'uniswap_mint_task',
        'schedule': 20,
    },
    'uniswap_pair_task': {
        'task': 'uniswap_pair_task',
        'schedule': 20,
    }
}