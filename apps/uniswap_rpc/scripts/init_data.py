# @Time : 10/20/23 10:29 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : init_data.py
import logging
from itertools import permutations
from tortoise import run_async, Tortoise
from apps.uniswap_rpc.models import ChainTokenSwap
from apps.uniswap_rpc.constant import ChainEnum
from core.init_app import get_app_list
from settings.config import settings

logger = logging.getLogger(__name__)


async def eth_token_data():
    token_dict = {
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": {
            "name": "USDC",
            "decimals": 6
        },
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": {
            "name": "WETH",
            "decimals": 18
        },
        "0xdAC17F958D2ee523a2206206994597C13D831ec7": {
            "name": "USDT",
            "decimals": 6
        },
        "0x6B175474E89094C44Da98b954EedeAC495271d0F": {
            "name": "DAI",
            "decimals": 18
        },
        "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": {
            "name": "WBTC",
            "decimals": 8
        },
        "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8": {
            "name": "agEUR",
            "decimals": 18
        },
        "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd": {
            "name": "GUSD",
            "decimals": 2
        },
        "0x5f98805a4e8be255a32880fdec7f6728c6568ba0": {
            "name": "LUSD",
            "decimals": 18
        },
        "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c": {
            "name": "EUROC",
            "decimals": 6
        },
        "0x70e8dE73cE538DA2bEEd35d14187F6959a8ecA96": {
            "name": "XSGD",
            "decimals": 6
        }
    }

    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
                # "chain_id": ChainEnum.Ethereum.value,
                # "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
                # "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Ethereum.value,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def arb_token_data():
    token_dict = {
        "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": {
            "name": "WETH",
            "decimals": "18"
        },
        "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": {
            "name": "USDT",
            "decimals": "6"
        },
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1": {
            "name": "DAI",
            "decimals": "18"
        },
        "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": {
            "name": "WBTC",
            "decimals": "8"
        },
        "0xFA5Ed56A203466CbBC2430a43c66b9D8723528E7": {
            "name": "agEUR",
            "decimals": "18"
        },
        "0x93b346b6BC2548dA6A1E7d98E9a421B42541425b": {
            "name": "LUSD",
            "decimals": "18"
        }
    }

    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Arbitrum,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Arbitrum,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def op_token_data():
    token_dict = {
        "0x0b2c639c533813f4aa9d7837caf62653d097ff85": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x4200000000000000000000000000000000000006": {
            "name": "WETH",
            "decimals": "18"
        },
        "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58": {
            "name": "USDT",
            "decimals": "6"
        },
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1": {
            "name": "DAI",
            "decimals": "18"
        },
        "0x68f180fcCe6836688e9084f035309E29Bf0A2095": {
            "name": "WBTC",
            "decimals": "8"
        },
        "0x9485aca5bbBE1667AD97c7fE7C4531a624C8b1ED": {
            "name": "agEUR",
            "decimals": "18"
        },
        "0xc40F949F8a4e094D1b49a23ea9241D289B7b2819": {
            "name": "LUSD",
            "decimals": "18"
        }
    }
    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Optimisim,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Optimisim,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def polygon_token_data():
    token_dict = {
        "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619": {
            "name": "WETH",
            "decimals": "18"
        },
        "0xc2132D05D31c914a87C6611C10748AEb04B58e8F": {
            "name": "USDT",
            "decimals": "6"
        },
        "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063": {
            "name": "DAI",
            "decimals": "18"
        },
        "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6": {
            "name": "WBTC",
            "decimals": "8"
        },
        "0xE0B52e49357Fd4DAf2c15e02058DCE6BC0057db4": {
            "name": "agEUR",
            "decimals": "18"
        },
        "0x23001f892c0C82b79303EDC9B9033cD190BB21c7": {
            "name": "LUSD",
            "decimals": "18"
        },
        "0xDC3326e71D45186F113a2F448984CA0e8D201995": {
            "name": "XSGD",
            "decimals": "6"
        },
        "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270": {
            "name": "WMATIC",
            "decimals": 18
        }
    }

    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Polygon,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Polygon,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def base_token_data():
    token_dict = {
        "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x4200000000000000000000000000000000000006": {
            "name": "WETH",
            "decimals": 18
        },
        "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb": {
            "name": "DAI",
            "decimals": 18
        },
        "0xA61BeB4A3d02decb01039e378237032B351125B4": {
            "name": "agEUR",
            "decimals": 18
        }
    }
    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Base,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Base,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def bsc_token_data():
    token_dict = {
        "0x2170Ed0880ac9A755fd29B2688956BD959F933F8": {
            "name": "ETH",
            "decimals": 18
        },
        "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d": {
            "name": "USDC",
            "decimals": 18
        },
        "0x4DB5a66E937A9F4473fA95b1cAF1d1E1D62E29EA": {
            "name": "WETH",
            "decimals": 18
        },
        "0x55d398326f99059fF775485246999027B3197955": {
            "name": "USDT",
            "decimals": 18
        },
        "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3": {
            "name": "DAI",
            "decimals": 18
        },
        "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c": {
            "name": "BTCB",
            "decimals": 18
        },
        "0x12f31B73D812C6Bb0d735a218c086d44D5fe5f89": {
            "name": "agEUR",
            "decimals": 18
        },
        "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c": {
            "name": "WBNB",
            "decimals": 18
        }
    }

    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.BSC,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.BSC,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def celo_token_data():
    token_dict = {
        "0x66803FB87aBd4aaC3cbB3fAd7C3aa01f6F3FB207": {
            "name": "WETH",
            "decimals": 18
        },
        "0x37f750B7cC259A2f741AF45294f6a16572CF5cAd": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x2DEf4285787d58a2f811AF24755A8150622f4361": {
            "name": "WETH",
            "decimals": 18
        },
        "0xd71Ffd0940c920786eC4DbB5A12306669b5b81EF": {
            "name": "WBTC",
            "decimals": 8
        },
        "0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73": {
            "name": "CEUR",
            "decimals": 18
        }
    }
    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Celo,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Celo,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def ava_token_data():
    token_dict = {
        "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E": {
            "name": "USDC",
            "decimals": "6"
        },
        "0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB": {
            "name": "WETH",
            "decimals": "18"
        },
        "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7": {
            "name": "USDT",
            "decimals": "6"
        },
        "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70": {
            "name": "DAI",
            "decimals": "18"
        },
        "0x50b7545627a5162f82a992c33b87adc75187b218": {
            "name": "WBTC",
            "decimals": "8"
        },
        "0xAEC8318a9a59bAEb39861d10ff6C7f7bf1F96C57": {
            "name": "agEUR",
            "decimals": "18"
        },
        "0xC891EB4cbdEFf6e073e859e987815Ed1505c2ACD": {
            "name": "EUROC",
            "decimals": 6
        },
        "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7": {
            "name": "WAVAX",
            "decimals": 18
        }
    }
    for p in permutations(token_dict.keys(), 2):
        token_in_key = p[0]
        token_out_key = p[1]

        await ChainTokenSwap.update_or_create(
            defaults={
#                 "chain_id": ChainEnum.Avalanche,
#                 "token_in": token_in_key,
                "token_in_decimal": token_dict[token_in_key]['decimals'],
                "token_in_name": token_dict[token_in_key]['name'],
#                 "token_out": token_out_key,
                "token_out_decimal": token_dict[token_out_key]['decimals'],
                "token_out_name": token_dict[token_out_key]['name'],
            },
            chain_id=ChainEnum.Avalanche,
            token_in=token_in_key,
            token_out=token_out_key,
        )


async def init_all_data():
    db_url = settings.DB_URL
    app_list = get_app_list()
    await Tortoise.init(
        db_url=db_url,
        modules={'models': app_list}
    )
    # print("Start ETH data")
    # await eth_token_data()
    # print("Start ARB data")
    # await arb_token_data()
    # print("Start OP data")
    # await op_token_data()
    print("Start Polygon data")
    await polygon_token_data()
    # print("Start Base data")
    # await base_token_data()
    print("Start BSC data")
    await bsc_token_data()
    # print("Start Celo data")
    # await celo_token_data()
    print("Start Ava data")
    await ava_token_data()


if __name__ == '__main__':
    print("Start init Chain Token data")
    run_async(init_all_data())
    print("End init data")