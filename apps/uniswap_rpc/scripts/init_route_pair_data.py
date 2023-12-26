# @Time : 10/20/23 10:29 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : init_data.py
import itertools
import logging
from tortoise import run_async, Tortoise
from apps.uniswap_rpc.models import RoutePair
from core.init_app import get_app_list
from settings.config import settings

logger = logging.getLogger(__name__)


# AAVE 0x79379C0E09a41d7978f883a56246290eE9a8c4d3,
# BAL 0x6a28e90582c583fcd3347931c544819C31e9D0e0,
# CRV 0xB755039eDc7910C1F1BD985D48322E55A31AC0bF,
# DAI 0xcA77eB3fEFe3725Dc33bccB54eDEFc3D9f764f97,
# KNC 0x608ef9A3BffE206B86c3108218003b3cfBf99c84,
# LUSD 0xeDEAbc3A1e7D21fE835FFA6f83a710c70BB1a051,
# rETH 0x53878B874283351D26d206FA512aEcE1Bef6C0dD,
# UNI 0x434cdA25E8a2CA5D9c1C449a8Cb6bCbF719233E8,
# WBTC 0x3C1BCa5a656e69edCD0D4E36BEbb3FcDAcA60Cf1,
# wstETH 0xf610A9dfB7C89644979b4A0f27063E9e7d7Cda32,
# USDC 0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4,
# USDT 0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df,
# WETH 0x5300000000000000000000000000000000000004
async def route_pair_scroll_data():
    token_dict = {
        "0x79379c0e09a41d7978f883a56246290ee9a8c4d3": {
            "name": "AAVE",
            "decimals": 18
        },
        "0x6a28e90582c583fcd3347931c544819c31e9d0e0": {
            "name": "BAL",
            "decimals": 18
        },
        "0xb755039edc7910c1f1bd985d48322e55a31ac0bf": {
            "name": "CRV",
            "decimals": 18
        },
        "0x608ef9a3bffe206b86c3108218003b3cfbf99c84": {
            "name": "KNC",
            "decimals": 18
        },
        "0x434cda25e8a2ca5d9c1c449a8cb6bcbf719233e8": {
            "name": "UNI",
            "decimals": 18
        },
        "0x3c1bca5a656e69edcd0d4e36bebb3fcdaca60cf1": {
            "name": "WBTC",
            "decimals": 8
        },
        "0xf610a9dfb7c89644979b4a0f27063e9e7d7cda32": {
            "name": "wstETH",
            "decimals": 18
        },
        "0x53878b874283351d26d206fa512aece1bef6c0dd": {
            "name": "rETH",
            "decimals": 18
        },
        "0x5300000000000000000000000000000000000004": {
            "name": "WETH",
            "decimals": 18
        },
        "0xedeabc3a1e7d21fe835ffa6f83a710c70bb1a051": {
            "name": "LUSD",
            "decimals": 18
        },
        "0xca77eb3fefe3725dc33bccb54edefc3d9f764f97": {
            "name": "DAI",
            "decimals": 18
        },
        "0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4": {
            "name": "USDC",
            "decimals": 6
        },
        "0xf55bec9cafdbe8730f096aa55dad6d22d44099df": {
            "name": "USDT",
            "decimals": 6
        },
    }

    for pair in list(itertools.combinations(token_dict.keys(), 2)):
        await RoutePair.update_or_create(
                defaults={
                    "token0_decimals": token_dict[pair[0]]['decimals'],
                    "token1_decimals": token_dict[pair[1]]['decimals'],
                },
                chain_id=534352,
                token0=pair[0].lower(),
                token1=pair[1].lower(),
            )


async def init_route_pair_data():
    db_url = settings.DB_URL
    app_list = get_app_list()
    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )
    print("Start scroll data")
    await route_pair_scroll_data()
    print("Start scroll data")


if __name__ == '__main__':
    print("Start init route pair data")
    run_async(init_route_pair_data())
    print("End init route pair data")