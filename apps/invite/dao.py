from datetime import datetime

from apps.user.models import UserReward
from core.base.db_provider import start_transaction


async def claimInviteReward(userId: int, reward: int, invitedIds: list):
    now = datetime.now()
    async def local_function(connection):
        await connection.execute_query("select * from user_info where id=$1 for update", userId)
        for id in invitedIds:
            await connection.execute_query('update invite_code_pool set is_claimed=$1 where id=$2', (True, id))
        userReward = await UserReward.filter(account_id=userId).first()
        await connection.execute_query(
            'update user_reward set claimed_reward=$1,updated_at=$2 where account_id=$3',
            (userReward.claimed_reward+reward, now, userId)
        )
    await start_transaction(local_function)