# @Time : 10/7/23 2:02 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : init_app.py
import logging
import random
import secrets
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise

from apps.integral.utils import init_integral_signal
from core.exceptions import APIException, on_api_exception
from core.utils.base_util import get_limiter
from settings.config import settings
from settings.log import DEFAULT_LOGGING
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from apps.invite.routes import router as invite_router
from core.base.api import router as base_router
from apps.integral.routes import router as integral_router


def configure_logging(log_settings: dict = None):
    log_settings = log_settings or DEFAULT_LOGGING
    logging.config.dictConfig(log_settings)


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

def init_http_middleware(app: FastAPI):
    logger = logging.getLogger(__name__)
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        idem = secrets.token_hex(8)
        logger.info(f"rid={idem} start request path={request.url.path}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

        return response


def init_signal():
    init_integral_signal()


def get_app_list():
    app_list = [f'{settings.APPLICATIONS_MODULE}.{app}.models' for app in settings.APPLICATIONS]
    return app_list


def get_tortoise_config() -> dict:
    app_list = get_app_list()
    # app_list.append('aerich.models')
    config = {
        'connections': settings.DB_CONNECTIONS,
        'apps': {
            'models': {
                'models': app_list,
                'default_connection': 'default',
            }
        }
    }
    return config


TORTOISE_ORM = get_tortoise_config()


def register_db(app: FastAPI, db_url: str = None):
    db_url = db_url or settings.DB_URL
    app_list = get_app_list()
    # app_list.append('aerich.models')
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': app_list},
        generate_schemas=False,
        add_exception_handlers=True,
    )

def register_exceptions(app: FastAPI):
    app.add_exception_handler(APIException, on_api_exception)

def register_slowapi(app: FastAPI):
    limiter = get_limiter()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



def register_routers(app: FastAPI):
    app.include_router(base_router)
    app.include_router(invite_router)
    app.include_router(integral_router)