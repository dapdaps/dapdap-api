from datetime import datetime
import json
import logging

import math
from tortoise.functions import Sum, Count
from starlette.requests import Request

from apps.dapp.models import Network, Dapp, DappNetwork
from apps.quest.dao import claimReward
from apps.quest.models import QuestCampaign, Quest, UserQuest, QuestCategory, QuestAction, QuestCampaignReward, UserDailyCheckIn, QuestLong
from apps.quest.schemas import ClaimIn
from apps.user.models import UserInfo, UserFavorite
from core.common.constants import STATUS_COMPLETED
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user
from core.utils.time_util import getUtcSecond
from core.utils.tool_util import success, error


logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/quest")


@router.get('/campaign_list', tags=['quest'])
@limiter.limit('60/minute')
async def campaign_list(request: Request):
    campaigns = await QuestCampaign.all().values()
    if len(campaigns) == 0:
        return success()
    for campaign in campaigns:
        totalReward = await Quest.filter(quest_campaign_id=campaign['id']).annotate(total_reward=Sum("reward")).first().values("total_reward")
        campaign['reward'] = totalReward['total_reward']
    return success(campaigns)


@router.get('/list', tags=['quest'])
@limiter.limit('60/minute')
async def quest_list(request: Request, campaign_id: int, user: UserInfo = Depends(get_current_user)):
    quests = await Quest.filter(quest_campaign_id=campaign_id).order_by("-id").all().values()
    if len(quests) == 0:
        return success()
    questCategorys = await QuestCategory.all().values("id", "name")
    userQuests = await UserQuest.filter(account_id=user.id, quest_campaign_id=campaign_id).order_by("created_at").all().values("quest_id","action_completed")
    for quest in quests:
        for questCategory in questCategorys:
            if quest['quest_category_id'] == questCategory['id']:
                quest['quest_category_name'] = questCategory['name']
        if len(userQuests) == 0:
            quest['action_completed'] = 0
            continue
        for userQuest in userQuests:
            if quest['id'] == userQuest['quest_id']:
                quest['action_completed'] = userQuest['action_completed']
                break
    return success(quests)


@router.get('/recommend_list', tags=['quest'])
@limiter.limit('60/minute')
async def recommend_list(request: Request, campaign_id: int, page: int = 1, page_size: int = 4, user: UserInfo = Depends(get_current_user)):
    logger.info(f"page:{page} page_size:{page_size}")
    totalQuests = await Quest.filter(quest_campaign_id=campaign_id, priority__gte=1).annotate(count=Count('id')).first().values('count')
    total = totalQuests['count']
    total_page = math.ceil(total/page_size)
    if total == 0:
        return success({
            'data': [],
            'total_page': total_page,
        })

    quests = await Quest.filter(quest_campaign_id=campaign_id, priority__gte=1).order_by('-priority').limit(page_size).offset((page-1)*page_size).values()
    if len(quests) == 0:
        return success({
            'data': [],
            'total_page': total_page,
        })

    questIds = list()
    for quest in quests:
        questIds.append(quest['id'])
    userQuests = await UserQuest.filter(account_id=user.id, quest_id__in=questIds).all().values('quest_id', 'action_completed')
    for quest in quests:
        quest['action_completed'] = 0
        if len(userQuests) == 0:
            continue
        for userQuest in userQuests:
            if quest['id'] == userQuest['quest_id']:
                quest['action_completed'] = userQuest['action_completed']
                break
    return success({
        'data': quests,
        'total_page': total_page,
    })


@router.get('/participation_list', tags=['quest'])
@limiter.limit('60/minute')
async def participation_list(request: Request, user: UserInfo = Depends(get_current_user)):
    userQuests = await UserQuest.filter(account_id=user.id).select_related("quest")
    if len(userQuests) == 0:
        return success([])
    userQuests.sort(key=lambda x: x.quest.created_at, reverse=True)
    data = list()
    for userQuest in userQuests:
        data.append({
            'id': userQuest.quest_id,
            'name': userQuest.quest.name,
            'description': userQuest.quest.description,
            'logo': userQuest.quest.logo,
            'total_action': userQuest.quest.total_action,
            'reward': userQuest.quest.reward,
            'is_period': userQuest.quest.is_period,
            'action_completed': userQuest.action_completed,
            'quest_status': userQuest.quest.status,
            'participation_status': userQuest.status,
            'start_time': userQuest.quest.start_time,
            'end_time': userQuest.quest.end_time,
            'created_at': userQuest.quest.created_at,
        })
    return success(data)


@router.get('/favorite_list', tags=['quest'])
@limiter.limit('60/minute')
async def favorite_list(request: Request, user: UserInfo = Depends(get_current_user)):
    userFavorites = await UserFavorite.filter(account_id=user.id, category="quest", is_favorite=True)
    if len(userFavorites) == 0:
        return success([])
    questIds = list()
    for userFavorite in userFavorites:
        questIds.append(userFavorite.relate_id)
    favoriteQuests = await Quest.filter(id__in=questIds).all().values()
    if len(favoriteQuests) == 0:
        return success([])
    userQuests = await UserQuest.filter(account_id=user.id, quest_id__in=questIds)
    favoriteQuests.sort(key=lambda x: x['created_at'], reverse=True)
    for favoriteQuest in favoriteQuests:
        if len(userQuests) == 0:
            favoriteQuest['action_completed'] = 0
            favoriteQuest['participation_status'] = ''
            continue
        for userQuest in userQuests:
            if favoriteQuest['id'] == userQuest.quest_id:
                favoriteQuest['action_completed'] = userQuest.action_completed
                favoriteQuest['participation_status'] = userQuest.status
                break
    return success(favoriteQuests)


@router.get('/claimed_list', tags=['quest'])
@limiter.limit('60/minute')
async def claimed_list(request: Request, user: UserInfo = Depends(get_current_user)):
    claimedQuests = await UserQuest.filter(account_id=user.id, is_claimed=True).order_by("-claimed_at").select_related("quest")
    if len(claimedQuests) == 0:
        return success([])
    data = list()
    for claimedQuest in claimedQuests:
        data.append({
            'id': claimedQuest.quest_id,
            'name': claimedQuest.quest.name,
            'description': claimedQuest.quest.description,
            'logo': claimedQuest.quest.logo,
            'total_action': claimedQuest.quest.total_action,
            'reward': claimedQuest.quest.reward,
            'claimed_at': claimedQuest.claimed_at,
        })
    return success(data)


@router.get('', tags=['quest'])
@limiter.limit('60/minute')
async def quest(request: Request, id: int, user: UserInfo = Depends(get_current_user)):
    quest = await Quest.filter(id=id).first().values()
    if not quest:
        return error("quest not find")
    quest['total_user'] = 0
    quest['action_completed'] = 0

    total_user = await UserQuest.filter(quest_id=id).all().annotate(total_user=Count("id")).first().values("total_user")
    if total_user and total_user['total_user']:
        quest['total_user'] = total_user['total_user']

    userQuest = await UserQuest.filter(account_id=user.id, quest_id=id).first().values()
    if userQuest:
        quest['action_completed'] = userQuest['action_completed']

    actions = await QuestAction.filter(quest_id=id).order_by("id").all().values()
    networks = []
    dapps = []
    if actions:
        for action in actions:
            if action['category'] != "dapp":
                continue
            if not networks or len(networks) == 0:
                networks = await Network.all().values()
            if not dapps or len(dapps) == 0:
                dapps = await Dapp.all().values()
            operators = list()
            action['operators'] = operators
            if len(action['dapps']) == 0 or len(action['networks']) == 0:
                continue
            actionDappIds = action['dapps'].split(',')
            actionNetworkIds = action['networks'].split(',')
            dappNetworks = await DappNetwork.filter(dapp_id__in=actionDappIds, network_id__in=actionNetworkIds).all().values()
            if len(dappNetworks) == 0:
                continue
            for dappNetwork in dappNetworks:
                dappName = ""
                dappLogo = ""
                networkName = ""
                for dapp in dapps:
                    if dapp['id'] == dappNetwork['dapp_id']:
                        dappName = dapp['name']
                        dappLogo = dapp['logo']
                        break
                for network in networks:
                    if network['id'] == dappNetwork['network_id']:
                        networkName = network['name']
                        break
                operators.append({
                    'dapp_id': dappNetwork['dapp_id'],
                    'network_id': dappNetwork['network_id'],
                    'dapp_name': dappName,
                    'dapp_src': dappNetwork['dapp_src'],
                    'network_name': networkName,
                    'dapp_logo': dappLogo,
                })

        for action in actions:
            del action['dapps']
            del action['networks']
            del action['to_networks']

    return success({
        'quest': quest,
        'actions': actions,
    })


@router.get('/leaderboard', tags=['quest'])
@limiter.limit('60/minute')
async def leaderboard(request: Request, campaign_id: int, page: int, page_size: int = 10):
    if page <= 0:
        page = 1
    if page_size <= 0:
        page_size = 10
    campaign = await QuestCampaign.filter(id=campaign_id).first().values("total_reward", "total_users", "total_quest_execution")
    if not campaign:
        return error("not find quest campaign")
    total = await QuestCampaignReward.filter(quest_campaign_id=campaign_id).annotate(count=Count('id')).first().values("count")
    userRewards = await QuestCampaignReward.filter(quest_campaign_id=campaign_id).order_by("rank").offset((page-1)*page_size).limit(page_size).select_related("account")
    data = list()
    for userReward in userRewards:
        data.append({
            'reward': userReward.reward,
            'rank': userReward.rank,
            'account': {
                'id': userReward.account.id,
                'address': userReward.account.address,
                'avatar': userReward.account.avatar,
            }
        })
    return success({
        'total_reward': campaign['total_reward'],
        'total_users': campaign['total_users'],
        'total_quest_execution': campaign['total_quest_execution'],
        'data': data,
        'total_page': math.ceil(total['count']/page_size),
    })


@router.get('/daily_check_in', tags=['quest'])
@limiter.limit('60/minute')
async def daily_check_in(request: Request, user: UserInfo = Depends(get_current_user)):
    dailyCheckInQuest = await QuestLong.filter(category='daily_check_in', status='ongoing').order_by("-id").first()
    if not dailyCheckInQuest:
        return success()

    userDailyCheckIns = await UserDailyCheckIn.filter(account_id=user.id, quest_long_id=dailyCheckInQuest.id).all().order_by("check_in_time")
    rule = json.loads(dailyCheckInQuest.rule)
    reward_single_day = rule['reward_single_day']
    reward_consecutive = rule['reward_consecutive']
    data = list()

    if len(userDailyCheckIns) == 0:
        index = 0
        reward = 0
        while index < 7:
            rewardConsecutiveIndex = len(reward_consecutive)-1
            while rewardConsecutiveIndex >= 0:
                if reward_consecutive[rewardConsecutiveIndex]['day'] < index+1:
                    reward = reward_consecutive['reward']
                    break
                rewardConsecutiveIndex -= 1
            if reward == 0:
                reward = reward_single_day
            data.append({
                'day:': index+1,
                'reward': reward,
                'status': "claim" if index == 0 else "will_claim"
            })
            index += 1
        return success(data)

    checkInTime = getUtcSecond()
    oneDaySecond = 24 * 60 * 60
    delta = datetime.utcfromtimestamp(checkInTime) - datetime.utcfromtimestamp(userDailyCheckIns[0].check_in_time)
    checkInDay = delta.days+1

    for index, userDailyCheckIn in enumerate(userDailyCheckIns):
        if userDailyCheckIn.day > 1 and userDailyCheckIn.day != userDailyCheckIns[index-1].day+1:
            expiredDay = userDailyCheckIns[index-1].day+1
            while expiredDay < userDailyCheckIn.day:
                data.append({
                    'day:': expiredDay,
                    'reward': reward_single_day,
                    'status': "expired"
                })
                expiredDay += 1
        data.append({
            'day:': userDailyCheckIn.day,
            'reward': userDailyCheckIn.reward,
            'status': "claimed"
        })
    if userDailyCheckIns[len(userDailyCheckIns)-1].check_in_time != checkInTime and userDailyCheckIns[len(userDailyCheckIns)-1].check_in_time != checkInTime-oneDaySecond:
        expiredDay = userDailyCheckIns[len(userDailyCheckIns)-1].day+1
        while expiredDay <= delta.days:
            data.append({
                'day:': expiredDay,
                'reward': reward_single_day,
                'status': "expired"
            })
            expiredDay += 1

    daysConsecutive = 1
    if userDailyCheckIns[len(userDailyCheckIns) - 1].check_in_time != checkInTime-oneDaySecond:
        daysConsecutive = 0
    else:
        userDailyChecnInIndex = len(userDailyCheckIns) - 1
        while userDailyChecnInIndex >= 0:
            if userDailyChecnInIndex == len(userDailyCheckIns) - 1:
                daysConsecutive = 1
            elif userDailyCheckIns[userDailyChecnInIndex+1].check_in_time - userDailyCheckIns[userDailyChecnInIndex].check_in_time <= 24*60*60:
                daysConsecutive += 1
            else:
                break
            userDailyChecnInIndex -= 1

    nextDays = 1 if len(data) >= 7 else 7-len(data)
    nextDay = 0
    if userDailyCheckIns[len(userDailyCheckIns) - 1].check_in_time == checkInTime:
        nextDay = userDailyCheckIns[len(userDailyCheckIns) - 1].day + 1
    else:
        nextDay = checkInDay
    nextDayEnd = nextDay+nextDays
    while nextDay < nextDayEnd:
        reward = 0
        rewardConsecutiveIndex = len(reward_consecutive) - 1
        while rewardConsecutiveIndex >= 0:
            if reward_consecutive[rewardConsecutiveIndex]['day'] <= daysConsecutive:
                reward = reward_consecutive[rewardConsecutiveIndex]['reward']
                break
            rewardConsecutiveIndex -= 1
        if reward == 0:
            reward = reward_single_day
        data.append({
            'day': nextDay,
            'reward': reward,
            'status': "claim" if nextDay == checkInDay else "will_claim",
        })
        nextDay += 1
        daysConsecutive += 1

    return success(data)


@router.post('/daily_check_in', tags=['quest'])
@limiter.limit('60/minute')
async def claim_daily_check_in(request: Request, user: UserInfo = Depends(get_current_user)):
    dailyCheckInQuest = await QuestLong.filter(category='daily_check_in', status='ongoing').order_by("-id").first()
    if not dailyCheckInQuest:
        return error("daily check in not exist")

    checkInTime = getUtcSecond()
    oneDaySecond = 24 * 60 * 60

    hasCheckIn = await UserDailyCheckIn.filter(account_id=user.id, quest_long_id=dailyCheckInQuest.id, check_in_time=checkInTime).first()
    if hasCheckIn:
        return error("already check in")

    userDailyCheckIns = await UserDailyCheckIn.filter(account_id=user.id,quest_long_id=dailyCheckInQuest.id).all().order_by("check_in_time")
    rule = json.loads(dailyCheckInQuest.rule)
    reward_single_day = rule['reward_single_day']
    reward_consecutive = rule['reward_consecutive']

    if len(userDailyCheckIns) == 0:
        dailyCheckIn = UserDailyCheckIn()
        dailyCheckIn.account_id = user.id
        dailyCheckIn.quest_long_id = dailyCheckInQuest.id
        dailyCheckIn.reward = reward_single_day
        dailyCheckIn.day = 1
        dailyCheckIn.check_in_time = checkInTime
        await dailyCheckIn.save()
        return success({
            'day': 1,
            'reward': reward_single_day,
        })

    daysConsecutive = 1
    if userDailyCheckIns[len(userDailyCheckIns) - 1].check_in_time != checkInTime-oneDaySecond:
        daysConsecutive = 0
    else:
        userDailyChecnInIndex = len(userDailyCheckIns) - 1
        while userDailyChecnInIndex >= 0:
            if userDailyChecnInIndex == len(userDailyCheckIns) - 1:
                daysConsecutive = 1
            elif userDailyCheckIns[userDailyChecnInIndex + 1].check_in_time - userDailyCheckIns[userDailyChecnInIndex].check_in_time <= oneDaySecond:
                daysConsecutive += 1
            else:
                break
            userDailyChecnInIndex -= 1

    reward = reward_single_day
    rewardConsecutiveIndex = len(reward_consecutive) - 1
    while rewardConsecutiveIndex >= 0:
        if reward_consecutive[rewardConsecutiveIndex]['day'] <= daysConsecutive:
            reward = reward_consecutive[rewardConsecutiveIndex]['reward']
            break
        rewardConsecutiveIndex -= 1

    delta = datetime.utcfromtimestamp(checkInTime) - datetime.utcfromtimestamp(userDailyCheckIns[0].check_in_time)
    dailyCheckIn = UserDailyCheckIn()
    dailyCheckIn.account_id = user.id
    dailyCheckIn.quest_long_id = dailyCheckInQuest.id
    dailyCheckIn.reward = reward
    dailyCheckIn.day = userDailyCheckIns[0].day+delta.days
    dailyCheckIn.check_in_time = checkInTime
    await dailyCheckIn.save()
    return success({
            'day': dailyCheckIn.day,
            'reward': dailyCheckIn.reward,
        })


@router.post('/claim', tags=['quest'])
@limiter.limit('60/minute')
async def claim_reward(request: Request, claimIn: ClaimIn, user: UserInfo = Depends(get_current_user)):
    userQuest = await UserQuest.filter(quest_id=claimIn.id,account_id=user.id).first().select_related('quest')
    if not userQuest:
        return error("not find quest")
    if userQuest.status != STATUS_COMPLETED:
        return error("Cannot be claimed")
    if userQuest.is_claimed:
        return error("Already claimed,Cannot be claimed multiple times")

    await claimReward(user.id, userQuest.id)
    return success({
        'reward': userQuest.quest.reward
    })

