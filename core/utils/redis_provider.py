import redis

pool = redis.ConnectionPool(host="127.0.0.1", port=int(6379), decode_responses=True)


def list_base_token_price():
    r = redis.StrictRedis(connection_pool=pool)
    ret = r.hgetall("BASE_TOKEN_PRICE_MAINNET")
    r.close()
    return ret


if __name__ == '__main__':
    token_price = list_base_token_price()
    print(token_price)

