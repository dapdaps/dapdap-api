#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'dom'

try:
    from redis_info import REDIS_HOST, REDIS_PORT
except ImportError:
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6379"

try:
    from db_info import DB_DSN, DB_UID, DB_PWD, DB_HOST, DB_PORT
except ImportError:
    DB_DSN = "shanshan"
    DB_UID = "root"
    DB_PWD = "root"
    DB_HOST = "127.0.0.1"
    DB_PORT = "3306"

"""

"""


class Cfg:
    NETWORK_ID = "MAINNET"
    REDIS = {
        "REDIS_HOST": REDIS_HOST,
        "REDIS_PORT": REDIS_PORT,
    }
    NETWORK = {
        "DEVNET": {
            "DB_DSN": DB_DSN,
            "DB_UID": DB_UID,
            "DB_PWD": DB_PWD,
            "DB_HOST": DB_HOST,
            "DB_PORT": DB_PORT,
        },
        "TESTNET": {
            "DB_DSN": DB_DSN,
            "DB_UID": DB_UID,
            "DB_PWD": DB_PWD,
            "DB_HOST": DB_HOST,
            "DB_PORT": DB_PORT,
        },
        "MAINNET": {
            "DB_DSN": DB_DSN,
            "DB_UID": DB_UID,
            "DB_PWD": DB_PWD,
            "DB_HOST": DB_HOST,
            "DB_PORT": DB_PORT,
        }
    }


if __name__ == '__main__':
    print(type(Cfg))
    print(type(Cfg.NETWORK_ID), Cfg.NETWORK_ID)
