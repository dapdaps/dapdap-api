# @Time : 10/20/23 4:02 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : constant.py
from enum import IntEnum


class ChainEnum(IntEnum):
    Ethereum = 1
    Arbitrum = 42161
    Optimisim = 10
    Polygon = 137
    Base = 8453
    BSC = 56
    Celo = 42220
    Avalanche = 43114
    LineaTestnet = 59140


CHAIN_RPC = {
    ChainEnum.Ethereum: "https://ethereum.blockpi.network/v1/rpc/c43cf5556a42c2e8689613010b287dbed77b8d4e",
    ChainEnum.Arbitrum: "https://arbitrum.blockpi.network/v1/rpc/3d394eeb24fbafa0a02feebdb0ae1e57efac0b92",
    ChainEnum.Optimisim: "https://optimism.blockpi.network/v1/rpc/65df1b8055a8721d2c4fa12326731065cd713ab1",
    ChainEnum.Polygon: "https://polygon.blockpi.network/v1/rpc/ea85a35602e377c6c7531ca4572dfacf5dece0c8",
    ChainEnum.Base: "https://base.blockpi.network/v1/rpc/cfda722ee7fc992bae25aae68db68718f24e4823",
    ChainEnum.BSC: "https://bsc.blockpi.network/v1/rpc/de0f17bc8d626ecdfabea1ef6bb029d5a2746c21",
    ChainEnum.Avalanche: "https://avalanche.blockpi.network/v1/rpc/0d6b707292fe05e1c18bbfee82bc73246f032315",
    # https://linea.blockpi.network/v1/rpc/29868ca3524cde823e3b1cdad905aad8df71e31c

    # celo free RPC
    ChainEnum.Celo: "https://rpc.ankr.com/celo/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.LineaTestnet: "https://rpc.goerli.linea.build",
}


QUOTER_V2_CONTRACT_ADDRESS = {
    ChainEnum.Ethereum: "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    ChainEnum.Arbitrum: "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    ChainEnum.Optimisim: "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    ChainEnum.Polygon: "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    ChainEnum.Base: "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
    ChainEnum.BSC: "0x78D78E420Da98ad378D7799bE8f4AF69033EB077",
    ChainEnum.Celo: "0x82825d0554fA07f7FC52Ab63c961F330fdEFa8E8",
    ChainEnum.Avalanche: "0xbe0F5544EC67e9B3b2D979aaA43f18Fd87E6257F",
    ChainEnum.LineaTestnet: "0x2Dd5C9E53d6467E13d77037d4a9E9b84571eAE2e",
}

QUOTER_CONTRACT_ADDRESS = {
    ChainEnum.Ethereum: "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
    ChainEnum.Arbitrum: "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
    ChainEnum.Optimisim: "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6",
    ChainEnum.Polygon: "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
}

# router = [56, 8453, 42220, 43114]
USE_QUOTER_V2 = [
    ChainEnum.Base,
    ChainEnum.BSC,
    ChainEnum.Celo,
    ChainEnum.Avalanche,
    ChainEnum.LineaTestnet
]

GraphApi = {
    "testnet": "https://graph-query.goerli.linea.build/subgraphs/name/dapdap/uniswap-v3-test",
    "prd": "https://graph-query.linea.build/subgraphs/name/dapdap/uniswap-v3-prd",
}