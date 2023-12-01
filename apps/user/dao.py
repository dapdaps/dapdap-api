from core.base.db_provider import start_transaction


async def updateUserFavorite(account_id: int, id: int, category: str, is_favorite: bool):
    async def local_function(connection):
        if category == "dapp":
            dapp = await connection.execute_query(f"select * from dapp where id={id}")
            count = dapp[1][0]['favorite']
            if is_favorite:
                count = count+1
            else:
                count = count-1
            if count < 0:
                count = 0
            await connection.execute_query(f"update dapp set favorite={count} where id={id}")
        elif category == "quest_campaign":
            campaign = await connection.execute_query(f"select * from quest_campaign where id={id}")
            count = campaign[1][0]['favorite']
            if is_favorite:
                count = count + 1
            else:
                count = count - 1
            if count < 0:
                count = 0
            await connection.execute_query(f"update quest_campaign set favorite={count} where id={id}")
        elif category == "quest":
            quest = await connection.execute_query(f"select * from quest where id={id}")
            count = quest[1][0]['favorite']
            if is_favorite:
                count = count + 1
            else:
                count = count - 1
            if count < 0:
                count = 0
            await connection.execute_query(f"update quest set favorite={count} where id={id}")

        await connection.execute_query(f"insert into user_favorite(account_id,relate_id,category,is_favorite) VALUES({account_id},{id},'{category}',{is_favorite}) ON CONFLICT (account_id,relate_id,category) DO UPDATE SET is_favorite=EXCLUDED.is_favorite")

    await start_transaction(local_function)