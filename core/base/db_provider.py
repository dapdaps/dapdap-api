import decimal
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from settings.config import DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD
from tortoise.transactions import in_transaction


class Encoder(json.JSONEncoder):
    """
    Handle special data types, such as decimal and time types
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        super(Encoder, self).default(o)


def get_db_connect():
    conn = psycopg2.connect(
        database=DATABASE_NAME,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=5432)
    return conn


def query_special_action():
    db_conn = get_db_connect()
    sql = "select * from (select action_title, sum(count_number) as count_number from t_action where " \
          "chain_id = 1101  and template = 'native bridge' group by action_title order by " \
          "count_number desc limit 1) t1 union all  select * from (select action_title, sum(count_number) " \
          "as count_number from t_action where chain_id = 1101  and template in ('Balancer', " \
          "'QuickSwap', 'Pancake Swap') group by action_title order by count_number  desc limit 1) t2 union all " \
          "select * from (select action_title, sum(count_number) as count_number from t_action  where " \
          "chain_id = 1101 and template = '0vix' and action_type = 'Supply' group by " \
          "action_title order by count_number desc limit 1) t3 union all select * from (select action_title, " \
          "sum(count_number) as count_number from t_action where chain_id = 1101 and " \
          "template = 'Gamma' and action_type = 'Deposit' group by action_title order by count_number desc limit 1) t4"

    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(sql)
        action_data_list = cursor.fetchall()
        return action_data_list
    except Exception as e:
        print("query_special_action to db error:", e)
    finally:
        cursor.close()


async def start_transaction(fun):
    async with in_transaction() as connection:
        # await connection.execute_query("YOUR SQL QUERY HERE")
        return await fun(connection)


if __name__ == '__main__':
    print("#########START MAIN###########")

