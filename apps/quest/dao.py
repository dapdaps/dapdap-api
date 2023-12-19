from datetime import datetime

from apps.quest.models import UserQuest, UserDailyCheckIn, QuestAction, Quest, UserQuestAction
from apps.user.models import UserReward
from core.base.db_provider import start_transaction
from core.common.constants import STATUS_COMPLETED, STATUS_INPROCESS


async def claimReward(userId: int, userQuestId: int):
    now = datetime.now()
    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId} for update")
        userQuest = await UserQuest.filter(id=userQuestId).first().select_related('quest')
        if userQuest.is_claimed:
            raise Exception("Already claimed,Cannot be claimed multiple times")
        userReward = await UserReward.filter(account_id=userId).first()
        claimReward = userQuest.quest.reward
        if userReward:
            claimReward += userReward.claimed_reward
        await connection.execute_query(
            'update user_quest set is_claimed=$1,claimed_at=$2 where id=$3',
            (True, now, userQuestId))
        await connection.execute_query(
            'update user_reward set claimed_reward=$1, set updated_at=$2 where account_id=$3',
            (claimReward, now, userId))
    await start_transaction(local_function)


async def claimDailyCheckIn(userId: int, data: UserDailyCheckIn, consecutiveDays: int):
    now = datetime.now()
    questActions = await QuestAction.filter(category__in=['daily_check_in_day_1', 'daily_check_in_day_3']).all()
    userNotCompletedQuestActions = list()
    if questActions:
        questActionIds = list()
        for questAction in questActions:
            questActionIds.append(questAction.id)
        userQuestActions = await UserQuestAction.filter(account_id=userId, quest_action_id__in=questActionIds).all()
        for questAction in questActions:
            hasCompleted = False
            if userQuestActions:
                for userQuestAction in userQuestActions:
                    if questAction.id == userQuestAction.quest_action_id:
                        hasCompleted = True
            if not hasCompleted:
                userNotCompletedQuestActions.append(questAction)

    async def local_function(connection):
        await connection.execute_query(f"select * from user_info where id={userId} for update")
        await connection.execute_query(
            'insert into user_daily_check_in(account_id,quest_long_id,reward,check_in_time) VALUES($1,$2,$3,$4)',
            (userId, data.quest_long_id, data.reward, data.check_in_time))
        userReward = await UserReward.filter(account_id=userId).first()
        reward = data.reward
        claimReward = data.reward
        if userReward:
            reward += userReward.reward
            claimReward += userReward.claimed_reward
        if len(userNotCompletedQuestActions) > 0:
            for questAction in userNotCompletedQuestActions:
                if questAction.category == "daily_check_in_day_1" or (questAction.category == "daily_check_in_day_3" and consecutiveDays >= 3):
                    completedAction = 0
                    userQuestStatus = ""
                    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
                    if not quest:
                        continue
                    userQuest = await UserQuest.filter(account_id=userId, quest_id=questAction.quest_id).first()
                    if userQuest:
                        completedAction = userQuest.action_completed
                    completedAction += 1
                    if completedAction < quest.total_action:
                        userQuestStatus = STATUS_INPROCESS
                    else:
                        userQuestStatus = STATUS_COMPLETED
                        reward += quest.reward
                    await connection.execute_query(
                        "insert into user_quest_action(account_id,quest_action_id,quest_id,quest_campaign_id,times,status) VALUES($1,$2,$3,$4,$5,$6)",
                        (userId, questAction.id, quest.id, quest.quest_campaign_id, 1, STATUS_COMPLETED))
                    await connection.execute_query(
                        "insert into user_quest(account_id,quest_id,quest_campaign_id,action_completed,status,updated_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT (account_id,quest_id) DO UPDATE SET action_completed=EXCLUDED.action_completed,status=EXCLUDED.status,updated_at=EXCLUDED.updated_at",
                        (userId, quest.id, quest.quest_campaign_id, completedAction, userQuestStatus, now))
        await connection.execute_query(
            'insert into user_reward(account_id,reward,claimed_reward,updated_at) VALUES($1,$2,$3,$4) ON CONFLICT (account_id) DO UPDATE SET reward=EXCLUDED.reward,claimed_reward=EXCLUDED.claimed_reward,updated_at=EXCLUDED.updated_at',
            (userId, reward, claimReward, now)
        )
    await start_transaction(local_function)


async def actionCompleted(userId: int, questAction: QuestAction, quest: Quest):
    now = datetime.now()
    completedAction = 0
    userQuestStatus = ""
    userQuest = await UserQuest.filter(account_id=userId, quest_id=quest.id).first()
    if userQuest:
        completedAction = userQuest.action_completed
    completedAction += 1
    if completedAction < quest.total_action:
        userQuestStatus = STATUS_INPROCESS
    else:
        userQuestStatus = STATUS_COMPLETED

    async def local_function(connection):
        if userQuestStatus == STATUS_COMPLETED:
            await connection.execute_query(f"select * from user_info where id={userId} for update")
            userReward = await UserReward.filter(account_id=userId).first()
            reward = quest.reward
            if userReward:
                reward += userReward.reward
            await connection.execute_query(
                'insert into user_reward(account_id,reward,updated_at) VALUES($1,$2,$3) ON CONFLICT (account_id) DO UPDATE SET reward=EXCLUDED.reward,updated_at=EXCLUDED.updated_at',
                (userId, reward, now)
            )
        await connection.execute_query(
            "insert into user_quest_action(account_id,quest_action_id,quest_id,quest_campaign_id,times,status) VALUES($1,$2,$3,$4,$5,$6)",
            (userId, questAction.id, quest.id, quest.quest_campaign_id, 1, STATUS_COMPLETED))
        await connection.execute_query(
            "insert into user_quest(account_id,quest_id,quest_campaign_id,action_completed,status,updated_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT (account_id,quest_id) DO UPDATE SET action_completed=EXCLUDED.action_completed,status=EXCLUDED.status,updated_at=EXCLUDED.updated_at",
            (userId, quest.id, quest.quest_campaign_id, completedAction, userQuestStatus, now))
    await start_transaction(local_function)

