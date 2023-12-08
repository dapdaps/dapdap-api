from datetime import datetime

from apps.invite.models import InviteCodePool
from apps.user.models import UserReward
from core.base.db_provider import start_transaction


async def claimInviteReward(userId: int):
    now = datetime.now()
    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId} for update")
        invites = await InviteCodePool.filter(creator_user_id=userId, status='Active', is_claimed=False)
        if len(invites) == 0:
            return
        totalReward = 0
        for invite in invites:
            totalReward += 10
            await connection.execute_query(
                'update invite_code_pool set is_claimed=$1 where id=$2',
                (True, invite.id)
            )
        userReward = await UserReward.filter(account_id=userId).first()
        if userReward:
            totalReward += userReward.claimed_reward
        await connection.execute_query(
            'update user_reward set claimed_reward=$1,updated_at=$2 where account_id=$3',
            (totalReward, now, userId)
        )
    await start_transaction(local_function)