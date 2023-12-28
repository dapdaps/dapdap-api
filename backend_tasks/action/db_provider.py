import decimal

import json
from datetime import datetime
import settings.config
import psycopg2
from psycopg2.extras import RealDictCursor


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


def get_pg_db_connect():
    conn = psycopg2.connect(
        database=settings.config.DATABASE_NAME,
        user=settings.config.DATABASE_USERNAME,
        password=settings.config.DATABASE_PASSWORD,
        host=settings.config.DATABASE_HOST,
        port=5432)
    return conn


def query_action_records():
    db_conn = get_pg_db_connect()
    sql = "select tx_id, chain_id from t_action_record where status = '1' order by id asc limit 100"

    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(sql)
        action_records_data_list = cursor.fetchall()
        return action_records_data_list
    except Exception as e:
        print("query hot t_action to db error:", e)
    finally:
        cursor.close()


def update_gas_by_tx(tx_id, gas, status):
    conn = get_pg_db_connect()
    sql = "update t_action_record set gas = '%s', action_status = '%s', status = '3' where tx_id = '%s'" % (gas, status, tx_id)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update gas to db error:", e)
    finally:
        cursor.close()


def update_action_status_by_tx(tx_id, action_status):
    conn = get_pg_db_connect()
    sql = "update t_action_record set action_status = '%s', status = '3' where tx_id = '%s'" % (action_status, tx_id)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update gas to db error:", e)
    finally:
        cursor.close()


def update_status_fail_by_tx(tx_id):
    conn = get_pg_db_connect()
    sql = "update t_action_record set status = '2' where tx_id = '%s'" % tx_id
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update gas to db error:", e)
    finally:
        cursor.close()


if __name__ == '__main__':
    print("#########START MAIN###########")

