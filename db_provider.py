import decimal
import time

import pymysql
import json
from datetime import datetime
from config import Cfg
from tool_util import handel_page_number


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


def get_db_connect(network_id: str):
    conn = pymysql.connect(
        host=Cfg.NETWORK[network_id]["DB_HOST"],
        port=int(Cfg.NETWORK[network_id]["DB_PORT"]),
        user=Cfg.NETWORK[network_id]["DB_UID"],
        passwd=Cfg.NETWORK[network_id]["DB_PWD"],
        db=Cfg.NETWORK[network_id]["DB_DSN"])
    return conn


def add_action(network_id, insert_action_data):
    now_time = int(time.time())
    db_conn = get_db_connect(network_id)
    add_action_sql = "insert into t_action(action_title, action_type, `status`, action_tokens, action_amount, " \
                     "account_id, account_info, template, action_network_id, `timestamp`, create_time) " \
                     "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now())"
    add_action_record_sql = "insert into t_action_record(action_id, action_title, action_type, action_tokens, " \
                            "action_amount, account_id, account_info, template, tx_id, action_status, " \
                            "action_network_id, `timestamp`, create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                            "%s,%s,%s, now())"
    action_status = ""
    if "action_status" in insert_action_data:
        action_status = insert_action_data["action_status"]
    tx_id = ""
    if "tx_id" in insert_action_data:
        tx_id = insert_action_data["tx_id"]
    account_id = ""
    if "account_id" in insert_action_data:
        account_id = insert_action_data["account_id"]
    account_info = ""
    if "account_info" in insert_action_data:
        account_info = insert_action_data["account_info"]
    action_data_status = "0"
    if "action_switch" in insert_action_data and (insert_action_data["action_switch"] == "1" or insert_action_data["action_switch"] == 1):
        action_data_status = "1"
    action_network_id = ""
    if "action_network_id" in insert_action_data:
        action_network_id = insert_action_data["action_network_id"]
    par_action = (insert_action_data["action_title"], insert_action_data["action_type"], action_data_status,
                  str(insert_action_data["action_tokens"]), insert_action_data["action_amount"],
                  account_id, account_info, insert_action_data["template"], action_network_id, now_time)
    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        if tx_id != "" and tx_id is not None:
            query_action_record_sql = "select action_id from t_action_record where tx_id = '%s'" % tx_id
            cursor.execute(query_action_record_sql)
            action_record_data = cursor.fetchone()
            if action_record_data is not None:
                action_id = action_record_data["action_id"]
                return action_id

        action_where_sql = handle_action_where_sql(account_id, account_info)
        action_amount_where_sql = ""
        if "action_amount" in insert_action_data and insert_action_data["action_amount"] is not None:
            action_amount_where_sql = "and action_amount = '" + str(insert_action_data["action_amount"]) + "' "
        query_action_sql = "select action_id, `status` from t_action where action_type = '%s' and action_tokens = " \
                           "'%s' %s and template = '%s' and action_network_id = '%s' " \
                           "%s" % (insert_action_data["action_type"], insert_action_data["action_tokens"],
                                   action_amount_where_sql, insert_action_data["template"], action_network_id,
                                   action_where_sql)
        cursor.execute(query_action_sql)
        query_action_data = cursor.fetchone()
        if query_action_data is None:
            cursor.execute(add_action_sql, par_action)
            action_id = cursor.lastrowid
            db_conn.commit()
        else:
            action_id = query_action_data["action_id"]
            update_action_sql = "update t_action set count_number = count_number + 1 where action_id = %s" % action_id
            if action_data_status == "1" and query_action_data["status"] == "0":
                update_action_sql = "update t_action set `status` = '1', count_number = count_number + 1 " \
                                           "where action_id = %s" % action_id
            cursor.execute(update_action_sql)
            db_conn.commit()
        par_action_record = (action_id, insert_action_data["action_title"], insert_action_data["action_type"],
                             str(insert_action_data["action_tokens"]), insert_action_data["action_amount"],
                             account_id, account_info, insert_action_data["template"], tx_id, action_status,
                             action_network_id, now_time)
        cursor.execute(add_action_record_sql, par_action_record)
        db_conn.commit()
        return action_id
    except Exception as e:
        db_conn.rollback()
        print("insert t_action to db error:", e)
        raise e
    finally:
        cursor.close()


def query_action_by_account(network_id, account_id, account_info, action_network_id):
    where_sql = handle_action_where_sql(account_id, account_info)
    network_sql = ""
    if action_network_id is not None and action_network_id != "":
        network_sql = " and action_network_id = '%s'" % action_network_id
    db_conn = get_db_connect(network_id)
    sql = "select action_id, account_id,action_title,`timestamp`,template, account_info, sum(count_number) as " \
          "count_number from t_action where `status` = '1' %s %s group by action_title order by " \
          "count_number desc" % (network_sql, where_sql)

    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        action_data_list = cursor.fetchall()
        return action_data_list
    except Exception as e:
        print("query account t_action to db error:", e)
    finally:
        cursor.close()


def query_hot_action(network_id, hot_number, action_title, action_network_id):
    network_sql = ""
    if action_network_id is not None and action_network_id != "":
        network_sql = " and action_network_id = '%s'" % action_network_id
    db_conn = get_db_connect(network_id)
    sql = "select account_id,action_title,action_type,action_tokens,action_amount,account_info,`timestamp`,template," \
          "sum(count_number) as count_number from t_action where action_title like '%%%s%%' %s group by action_title " \
          "order by count_number desc limit %s" % (action_title, network_sql, hot_number)

    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        action_data_list = cursor.fetchall()
        return action_data_list
    except Exception as e:
        print("query hot t_action to db error:", e)
    finally:
        cursor.close()


def delete_action_by_id(network_id, action_id):
    conn = get_db_connect(network_id)
    query_sql = "select action_title, account_id, action_network_id from t_action where action_id = %s" % action_id
    sql = "update t_action set `status` = '0' where action_title = %s and account_id = %s " \
          "and action_network_id = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query_sql)
        action_data = cursor.fetchone()
        par = (action_data[0], action_data[1], action_data[2])
        cursor.execute(sql, par)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update t_action to db error:", e)
    finally:
        cursor.close()


def batch_delete_action_by_id(network_id, action_ids):
    conn = get_db_connect(network_id)
    query_sql = "select action_title, account_id, action_network_id from t_action where action_id in %s"
    sql = "update t_action set `status` = '0' where action_title in %s and account_id in %s " \
          "and action_network_id in %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query_sql, (action_ids, ))
        action_data_list = cursor.fetchall()
        action_title_list = []
        account_id_list = []
        action_network_id_list = []
        for action_data in action_data_list:
            action_title_list.append(action_data[0])
            account_id_list.append(action_data[1])
            action_network_id_list.append(action_data[2])
        par = (action_title_list, account_id_list, action_network_id_list)
        cursor.execute(sql, par)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update t_action to db error:", e)
    finally:
        cursor.close()


def update_action_by_id(network_id, action_record_id, tx_id, action_status):
    conn = get_db_connect(network_id)
    sql = "update t_action_record set tx_id = '%s', action_status = '%s' where id = %s" % (tx_id, action_status, action_record_id)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update t_action to db error:", e)
    finally:
        cursor.close()


def query_action_records_by_account(network_id, account_id, action_type, template, action_status, page_number,
                                    page_size, action_network_id):
    start_number = handel_page_number(page_number, page_size)
    network_sql = ""
    if action_network_id is not None and action_network_id != "":
        network_sql = " and action_network_id = '%s'" % action_network_id
    where_sql = ""
    if action_type is not None and "" != action_type:
        if action_type == "Lending":
            where_sql = where_sql + "and (action_type = '" + action_type + "' or action_type = 'Supply' or " \
                        "action_type = 'Repay' or action_type = 'Borrow')"
        else:
            where_sql = where_sql + "and action_type = '" + action_type + "' "
    if template is not None and "" != template:
        where_sql = where_sql + "and template = '" + template + "' "
    if action_status is not None and "" != action_status:
        where_sql = where_sql + "and action_status = '" + action_status + "' "
    db_conn = get_db_connect(network_id)
    sql = "select action_id,action_title,action_type,template,action_status,`timestamp`,tx_id,gas from t_action_record " \
          "where account_id = '" + account_id + "' " + network_sql + where_sql + " order by id desc " \
          "limit %s, %s" % (start_number, page_size)

    sql_count = "select count(action_id) as total_number from t_action_record where account_id = '" + account_id + "'" \
                + network_sql + where_sql
    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        action_data_list = cursor.fetchall()
        cursor.execute(sql_count)
        action_data_count = cursor.fetchone()
        return action_data_list, action_data_count["total_number"]
    except Exception as e:
        print("query account t_action to db error:", e)
    finally:
        cursor.close()


def handle_action_where_sql(account_id, account_info):
    where_sql = ""
    if account_id is not None and account_id != "" and account_info is not None and account_info != "":
        where_sql = "and (account_id = '" + account_id + "'" + "or account_info = '" + account_info + "')"
    if (account_id is None or account_id == "") and (account_info is not None and account_info != ""):
        where_sql = "and account_info = '" + account_info + "'"
    if (account_id is not None or account_id != "") and (account_info is None or account_info == ""):
        where_sql = "and account_id = '" + account_id + "'"
    return where_sql


def query_special_action(network_id):
    db_conn = get_db_connect(network_id)
    sql = "select * from (select account_id,action_title,action_type,action_tokens,action_amount,account_info," \
          "`timestamp`,template, sum(count_number) as count_number from t_action where action_network_id = 'zkEVM' " \
          "and template = 'native bridge' group by action_title order by count_number desc limit 1) t1 union all " \
          "select * from (select account_id,action_title,action_type,action_tokens,action_amount,account_info," \
          "`timestamp`,template, sum(count_number) as count_number from t_action where action_network_id = 'zkEVM' " \
          "and template in ('Balancer', 'QuickSwap', 'Pancake Swap') group by action_title order by count_number " \
          "desc limit 1) t2 union all select * from (select account_id,action_title,action_type,action_tokens," \
          "action_amount,account_info,`timestamp`,template, sum(count_number) as count_number from t_action " \
          "where action_network_id = 'zkEVM' and template = '0vix' and action_type = 'Supply' group by " \
          "action_title order by count_number desc limit 1) t3 union all select * from (select account_id," \
          "action_title,action_type,action_tokens,action_amount,account_info,`timestamp`,template, " \
          "sum(count_number) as count_number from t_action where action_network_id = 'zkEVM' and " \
          "template = 'Gamma' and action_type = 'Deposit' group by action_title order by count_number desc limit 1) t4"

    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        action_data_list = cursor.fetchall()
        return action_data_list
    except Exception as e:
        print("query hot t_action to db error:", e)
    finally:
        cursor.close()


def query_action_records_gas_is_null(network_id):
    db_conn = get_db_connect(network_id)
    sql = "select tx_id, action_network_id from t_action_record where `status` = '1' and action_network_id = 'zkEVM' and gas is null order by id desc"

    cursor = db_conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        action_records_data_list = cursor.fetchall()
        return action_records_data_list
    except Exception as e:
        print("query hot t_action to db error:", e)
    finally:
        cursor.close()


def update_gas_by_tx(network_id, tx_id, gas):
    conn = get_db_connect(network_id)
    sql = "update t_action_record set gas = '%s' where tx_id = '%s'" % (gas, tx_id)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update gas to db error:", e)
    finally:
        cursor.close()


def update_status_by_tx(network_id, tx_id):
    conn = get_db_connect(network_id)
    sql = "update t_action_record set `status` = '2' where tx_id = '%s'" % tx_id
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

