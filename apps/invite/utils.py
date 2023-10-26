# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
import secrets
from web3 import Web3
def generate_invite_code(number: int):
    return [secrets.token_hex(4) for x in range(0, number)]

def is_w3_address(address):
    try:
        Web3.is_checksum_address(address)
    except:
        return False
    return True
