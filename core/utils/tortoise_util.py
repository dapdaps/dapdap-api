# @Time : 10/7/23 9:05 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : tortoise_util.py
from tortoise import Tortoise, connections, run_async
from tortoise.utils import get_schema_sql
from core.init_app import get_app_list
from settings.config import settings


async def get_db_sql(db_url: str = None, app_name: str = None):
    db_url = db_url or settings.DB_URL
    if app_name:
        app_list = [f'{settings.APPLICATIONS_MODULE}.{app_name}.models']
    else:
        app_list = get_app_list()
        # app_list.append('aerich.models')

    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )
    sql = get_schema_sql(connections.get("default"), safe=False)
    print(sql)


if __name__ == '__main__':
    # run_async(get_db_sql('invite'))
    run_async(get_db_sql())

