import time
from datetime import datetime

from apps.invite.models import InviteCodePool
from apps.user.models import UserReward
from core.base.db_provider import start_transaction


async def claimInviteReward(userId: int):
    now = datetime.now()
    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId} for update")
        invites = await InviteCodePool.filter(creator_user_id=userId, status='Active', is_claimed=False)
        if not invites or len(invites) == 0:
            return
        totalReward = 0
        for invite in invites:
            if invite.reward <= 0:
                continue
            totalReward += invite.reward
            await connection.execute_query(
                'update invite_code_pool set is_claimed=$1 where id=$2',
                (True, invite.id)
            )
        if totalReward <= 0:
            return
        await connection.execute_query(
            'insert into user_reward_claim(reward, account_id, category, name, description, claim_time) VALUES($1, $2, $3, $4, $5, $6)',
            (totalReward, userId, 'invite', 'invite', '', int(time.mktime(now.timetuple())))
        )
        userReward = await UserReward.filter(account_id=userId).first()
        if userReward:
            totalReward += userReward.claimed_reward
        await connection.execute_query(
            'update user_reward set claimed_reward=$1, updated_at=$2 where account_id=$3',
            (totalReward, now, userId)
        )
    await start_transaction(local_function)