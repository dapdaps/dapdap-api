from datetime import datetime

from apps.quest.models import UserQuest
from apps.user.models import UserReward
from core.base.db_provider import start_transaction


async def claimReward(userId: int, userQuestId: int):
    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId}")
        userQuest = await UserQuest.filter(id=userQuestId).first().select_related('quest')
        if userQuest.is_claimed:
            raise Exception("Already claimed,Cannot be claimed multiple times")
        userReward = await UserReward.filter(account_id=userId).first()
        await connection.execute_query('update user_quest set is_claimed=$1,claimed_at=$2 where id=$3', (True, datetime.now(), userQuestId))
        await connection.execute_query(f'update user_reward set claimed_reward={userReward.claimed_reward+userQuest.quest.reward} where account_id={userId}')
    await start_transaction(local_function)