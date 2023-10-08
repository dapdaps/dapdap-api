# @Time : 10/7/23 1:50 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : log.py
import logging.config
from settings.config import settings

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        # 'require_debug_false': {
        #     '()': 'app.settings.log.RequireDebugFalse',
        # },
        # 'require_debug_true': {
        #     '()': 'app.settings.log.RequireDebugTrue',
        # },
    },
    'formatters': {
        'main_formatter': {
            'format': '[%(levelname)s]:[%(name)s]: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'dapdap': {
            'format': '[%(asctime)s][%(levelname)s] [process_id:%(process)s] [%(filename)s:'
                      '%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        # 'api_file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     # 目前设定每天一个日志文件
        #     'filename': f'{settings.LOGS_ROOT}/app_api.log',
        #     'when': 'midnight',
        #     'interval': 1,
        #     'backupCount': 100,
        #     'formatter': 'dapdap'
        # },
        'production_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{settings.LOGS_ROOT}/app_main.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'main_formatter',
            # 'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{settings.LOGS_ROOT}/app_main_debug.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'main_formatter',
            # 'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            # 'level': "DEBUG",
            'level': 'INFO',
            'propagate': True,
        },

    }
}


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG