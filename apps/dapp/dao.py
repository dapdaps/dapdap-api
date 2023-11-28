from core.base.db_provider import start_transaction


async def updateFavorite(dapp_id: int, account_id: int, is_favorite: bool):
    async def local_function(connection):
        dapp = await connection.execute_query(f"select * from dapp where id={dapp_id}")
        count = dapp[1][0]['favorite']
        if is_favorite:
            count = count+1
        else:
            count = count-1
        if count < 0:
            count = 0
        await connection.execute_query(f"update dapp set favorite={count} where id={dapp_id}")
        await connection.execute_query(f"insert into dapp_favorite(account_id,dapp_id,is_favorite) VALUES({account_id},{dapp_id},{is_favorite}) ON CONFLICT (account_id,dapp_id) DO UPDATE SET is_favorite=EXCLUDED.is_favorite")

    await start_transaction(local_function)