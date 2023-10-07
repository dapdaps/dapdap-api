# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
import secrets

def generate_invite_code():
    return secrets.token_hex(4)