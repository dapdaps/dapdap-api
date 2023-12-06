from apps.user.models import UserReward
from core.base.db_provider import start_transaction


async def claimInviteReward(userId: int, reward: int, invitedIds: list):
    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId} for update")
        for id in invitedIds:
            await connection.execute_query('update invite_code_pool set is_claimed=$1 where id=$2', (True, id))
        userReward = await UserReward.filter(account_id=userId).first()
        await connection.execute_query(f'update user_reward set claimed_reward={userReward.claimed_reward+reward} where account_id={userId}')
    await start_transaction(local_function)