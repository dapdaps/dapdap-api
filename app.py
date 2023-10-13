#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'dom'

from flask import Flask
from flask import request
from flask import jsonify
import flask_cors
from loguru import logger
import logging
from config import Cfg
from db_provider import add_action, query_action_by_account, query_hot_action, delete_action_by_id, update_action_by_id, query_action_records_by_account, query_special_action, batch_delete_action_by_id
from tool_util import success, error

service_version = "20230905.01"
Welcome = 'Welcome to shanshan datacenter API server, version ' + service_version
# Instantiation, which can be regarded as fixed format
app = Flask(__name__)


# route()Method is used to set the route; Similar to spring routing configuration
@app.route('/')
def hello_world():
    return Welcome


@app.route('/timestamp', methods=['GET'])
@flask_cors.cross_origin()
def handle_timestamp():
    import time
    return jsonify({"ts": int(time.time())})


@app.route('/add-action-data', methods=['POST'])
@flask_cors.cross_origin()
def handle_add_action_data():
    try:
        action_data = request.json
        if (action_data["account_id"] is None or action_data["account_id"] == "") and \
                (action_data["account_info"] is None or action_data["account_info"] == ""):
            return error("-1", "No account information")
        action_id = add_action(Cfg.NETWORK_ID, action_data)
        return success(action_id)
    except Exception as e:
        return error("-1", e.args)


@app.route('/get-action-by-account', methods=['GET'])
@flask_cors.cross_origin()
def handle_action_by_account():
    account_id = request.args.get("account_id")
    account_info = request.args.get("account_info")
    action_network_id = request.args.get("action_network_id")
    if (account_id is None or account_id == "") and (account_info is None or account_info == ""):
        return success()
    res = query_action_by_account(Cfg.NETWORK_ID, account_id, account_info, action_network_id)
    return success(res)


@app.route('/get-hot-action', methods=['GET'])
@flask_cors.cross_origin()
def handle_hot_action():
    action_title = request.args.get("action_title", type=str, default="")
    hot_number = request.args.get("hot_number", type=int, default=4)
    action_network_id = request.args.get("action_network_id")
    res = query_hot_action(Cfg.NETWORK_ID, hot_number, action_title, action_network_id)
    return success(res)


@app.route('/delete-action-by_id', methods=['DELETE'])
@flask_cors.cross_origin()
def handle_delete_action_by_id():
    action_id = request.json["action_id"]
    if action_id is None:
        return success()
    delete_action_by_id(Cfg.NETWORK_ID, action_id)
    return success(action_id)


@app.route('/batch-delete-action', methods=['DELETE'])
@flask_cors.cross_origin()
def handle_batch_delete_action_by_id():
    action_id_list = request.json["action_id_list"]
    if action_id_list is None or len(action_id_list) < 1:
        return success()
    batch_delete_action_by_id(Cfg.NETWORK_ID, action_id_list)
    return success(action_id_list)


@app.route('/update-action-by_id', methods=['PUT'])
@flask_cors.cross_origin()
def handle_update_action_by_id():
    action_record_id = request.form["action_record_id"]
    tx_id = request.form["tx_id"]
    action_status = request.form["action_status"]
    if action_record_id is None:
        return success()
    update_action_by_id(Cfg.NETWORK_ID, action_record_id, tx_id, action_status)
    return success(action_record_id)


@app.route('/get-action-records-by-account', methods=['GET'])
@flask_cors.cross_origin()
def handle_action_records_by_account():
    account_id = request.args.get("account_id")
    account_info = request.args.get("account_info")
    action_type = request.args.get("action_type", type=str, default=None)
    template = request.args.get("template", type=str, default=None)
    action_status = request.args.get("action_status", type=str, default=None)
    page_number = request.args.get("page_number", type=int, default=1)
    page_size = request.args.get("page_size", type=int, default=10)
    action_network_id = request.args.get("action_network_id")
    if (account_id is None) and account_info is None:
        return success()
    action_list, count_number = query_action_records_by_account(Cfg.NETWORK_ID, account_id, action_type, template,
                                                                action_status, page_number, page_size, action_network_id)
    if count_number % page_size == 0:
        total_page = int(count_number / page_size)
    else:
        total_page = int(count_number / page_size) + 1
    res = {
        "action_list": action_list,
        "page_number": page_number,
        "page_size": page_size,
        "total_page": total_page,
        "total_size": count_number,
    }
    return success(res)


@app.route('/get-special-action', methods=['GET'])
@flask_cors.cross_origin()
def handle_special_action():
    res = query_special_action(Cfg.NETWORK_ID)
    return success(res)


logger.add("app.log")
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.info(Welcome)
    app.run(host='0.0.0.0', port=38080, debug=False)

