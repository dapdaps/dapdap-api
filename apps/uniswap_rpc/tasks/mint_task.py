import asyncio
import time
from typing import List

import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from apps.uniswap_rpc.constant import GraphApi
from apps.uniswap_rpc.models import Mint
from tortoise import Tortoise
from core.init_app import TORTOISE_ORM

logger = logging.getLogger(__name__)


async def update_mints(graphApi: str, chainId: int):
    await Tortoise.init(config=TORTOISE_ORM)
    pageSize = 100
    if not graphApi:
        logger.error("not find graph api url")
        return {"done": "fail"}
    # Configure the GraphQL client
    transport = RequestsHTTPTransport(url=graphApi)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    fromTimestamp = await getLastTimestamp(chainId)
    if not fromTimestamp:
        fromTimestamp = 0
    logger.info(f"update_mints chainId:{chainId} fromTimestamp:{fromTimestamp}")
    while True:
        mints = getMints(client, fromTimestamp, pageSize, chainId)
        if not mints or len(mints) == 0:
            break
        await saveMints(mints)
        fromTimestamp = mints[len(mints)-1].timestamp
        if len(mints) < pageSize:
            break
    return {"done": "ok"}


async def getLastTimestamp(chainId: int):
    query = f'SELECT max(timestamp) FROM mint where chain_id={chainId}'
    results = await Tortoise.get_connection(connection_name='default').execute_query(query)
    if len(results) > 0:
        return results[1][0]['max']
    return 0


def getMints(client, fromTimestamp, pageSize, chainId: int) -> List[Mint]:
    # Define your GraphQL query
    query = gql('''
        query getMints($timestamp:BigInt!,$pageSize:Int!){
          mints(
            first: $pageSize
            orderBy: timestamp
            where: {
                timestamp_gt:$timestamp
            }
          ){
            id
            timestamp
            token0 {
                id
            }
            token1 {
                id
            }
            pool {
                id
                feeTier
            }
          }
        }
        ''')

    params = {
        "timestamp": fromTimestamp,
        "pageSize": pageSize,
    }

    # Execute the query
    start_time = time.time()
    response = client.execute(query, variable_values=params)
    end_time = time.time()
    logger.info(f"getMints time: {end_time - start_time}")
    if not response or len(response['mints']) == 0:
        logger.info("no more mints")
        return []
    mints = list()
    for mintEvent in response['mints']:
        mint = Mint()
        mintId:str = mintEvent['id']
        mint.tx_hash = mintId[0:mintId.index("#")].lower()
        mint.token0 = mintEvent['token0']['id'].lower()
        mint.token1 = mintEvent['token1']['id'].lower()
        mint.pool_address = mintEvent['pool']['id'].lower()
        mint.pool_fee = mintEvent['pool']['feeTier']
        mint.timestamp = mintEvent['timestamp']
        mint.chain_id = chainId
        mints.append(mint)
    return mints


async def saveMints(mints: List[Mint]):
    await Mint.bulk_create(mints)


async def testMints():
    await Tortoise.init(config=TORTOISE_ORM)
    await update_mints(GraphApi['scroll_mainnet'], 534352)

if __name__ == "__main__":
    asyncio.run(testMints())