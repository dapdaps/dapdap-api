# @Time : 10/7/23 2:17 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : main.py
from fastapi import FastAPI
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise

from core.exceptions import SettingNotFound
from core.init_app import configure_logging, init_middlewares, register_db, register_exceptions, register_routers, \
    get_app_list, register_slowapi, get_limiter
import uvicorn

try:
    from settings.config import settings
except ImportError:
    raise SettingNotFound('Can not import settings. Create settings file from template.config.py')

limiter = get_limiter()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.VERSION
)

configure_logging()
init_middlewares(app)

register_db(app)
# db_url = settings.DB_URL
# app_list = get_app_list()
# # app_list.append('aerich.models')
# register_tortoise(
#     app,
#     db_url=db_url,
#     # modules={'models': app_list},
#     modules={'models': ["apps"]},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )
register_exceptions(app)
register_slowapi(app)
register_routers(app)

@app.get("/")
async def root():
    return {"message": "welcome to dapdap"}


@app.get("/health_check")
@limiter.limit('1/second')
async def health_check(request: Request):
    return {"message": "Running!"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=3007, reload=True, log_level="info")
