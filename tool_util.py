import gzip
from flask import make_response
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def success(data=None):
    ret = {
        "code": "0",
        "msg": "success",
        "data": data
    }
    return compress_response_content(ret)


def error(code, msg, data=None):
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return compress_response_content(ret)


def compress_response_content(data):
    content = gzip.compress(json.dumps(data, cls=DecimalEncoder, ensure_ascii=False).encode('utf8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    return response


def handel_page_number(page_number, size):
    if page_number <= 1:
        start_number = 0
    else:
        start_number = (page_number - 1) * size
    return start_number


if __name__ == '__main__':
    print("#############TOOL_UTILS#############")
    aa = compress_response_content("123")
    print(aa)