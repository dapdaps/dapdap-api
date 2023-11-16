
def success(data=None):
    ret = {
        "code": "0",
        "msg": "success",
        "data": data
    }
    return ret


def error(msg, code=None, data=None):
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return ret


def successByInTract(data=None):
    ret = {
        "error": {
            "code": 0,
            "message": "",
        },
        "data": {
            "result": data,
        },
    }
    return ret


def errorByInTract(msg=None, code=1):
    ret = {
        "error": {
            "code": code,
            "message": msg,
        },
        "data": {
            "result": {},
        },
    }
    return ret