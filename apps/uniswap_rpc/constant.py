# @Time : 10/20/23 4:02 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : constant.py
from enum import IntEnum
from web3 import Web3


class ChainEnum(IntEnum):
    Ethereum = 1
    Arbitrum = 42161
    Optimisim = 10
    Polygon = 137
    Base = 8453
    BSC = 56
    Celo = 42220
    Avalanche = 43114


CHAIN_RPC = {
    ChainEnum.Ethereum: "https://rpc.ankr.com/eth/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.Arbitrum: "https://rpc.ankr.com/arbitrum/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.Optimisim: "https://rpc.ankr.com/optimism/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    # ChainEnum.Polygon: "https://rpc.ankr.com/optimism/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.Polygon: "https://polygon-mainnet.infura.io/v3/a13269733d7b4670b050ca945ef1daaa",
    ChainEnum.Base: "https://rpc.ankr.com/base/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.BSC: "https://rpc.ankr.com/bsc/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    ChainEnum.Celo: "https://rpc.ankr.com/celo/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef",
    # ChainEnum.Celo: "https://celo-mainnet.infura.io/v3/a13269733d7b4670b050ca945ef1daaa",
    ChainEnum.Avalanche: "https://rpc.ankr.com/avalanche/fa8cecf2398fe6a2d19fea8b78b641c35edb7bdf60e5bf7a3883565532ba07ef"
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
]