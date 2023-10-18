# @Time : 10/18/23 11:36 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : celery_app.py
from celery import Celery
from settings.config import settings


broker_url = f'{settings.REDIS_URL}/0'
backend_url = f'{settings.REDIS_URL}/1'

celery_app = Celery("celery_worker", backend=backend_url, broker=broker_url)
celery_app.config_from_object('settings.celery_config')
celery_app.autodiscover_tasks(['core'])