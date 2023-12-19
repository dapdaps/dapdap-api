import json
import logging
from typing import Optional

import math
from tortoise.functions import Count
from starlette.requests import Request

from apps.network.models import Network
from apps.dapp.models import Dapp, DappNetwork
from apps.quest.dao import claimReward, claimDailyCheckIn, actionCompleted
from apps.quest.models import QuestCampaign, Quest, UserQuest, QuestCategory, QuestAction, \
    UserDailyCheckIn, QuestLong, QuestCampaignInfo, UserRewardRank, UserQuestAction
from apps.quest.schemas import ClaimIn, SourceIn
from apps.user.models import UserInfo, UserFavorite
from core.common.constants import STATUS_COMPLETED, STATUS_ENDED, STATUS_ONGOING
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user, get_current_user_optional
from core.utils.time_util import getUtcSecond
from core.utils.tool_util import success, error


logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/quest")


@router.get('/campaign_list', tags=['quest'])
@limiter.limit('60/minute')
async def campaign_list(request: Request):
    campaigns = await QuestCampaign.all().order_by('-created_at').values()
    if len(campaigns) == 0:
        return success()
    for campaign in campaigns:
        allQuest = await Quest.filter(quest_campaign_id=campaign['id']).all()
        if len(allQuest) == 0:
            campaign['reward'] = 0
            campaign['quests'] = {
                'total': 0,
                'total_category': [],
            }
            continue
        totalReward = 0
        allQuestCategory = list()
        for quest in allQuest:
            totalReward += quest.reward
            qc = None
            for questCategory in allQuestCategory:
                if questCategory['quest_category_id'] == quest.quest_category_id:
                    qc = questCategory
                    break
            if not qc:
                qc = {
                    'quest_category_id': quest.quest_category_id,
                    'total': 1,
                }
                allQuestCategory.append(qc)
            else:
                qc['total'] += 1
        campaign['reward'] = totalReward
        campaign['quests'] = {
            'total': len(allQuest),
            'total_category': allQuestCategory,
        }
    return success(campaigns)


@router.get('/category_list', tags=['quest'])
@limiter.limit('60/minute')
async def category_list(request: Request):
    data = await QuestCategory.all().order_by('-created_at')
    return success(data)


@router.get('/list', tags=['quest'])
@limiter.limit('60/minute')
async def quest_list(request: Request, campaign_id: int, user: Optional[UserInfo] = Depends(get_current_user_optional)):
    quests = await Quest.filter(quest_campaign_id=campaign_id).order_by("-id").all().values()
    if len(quests) == 0:
        return success()
    questCategorys = await QuestCategory.all().values("id", "name")

    userQuests = list()
    if user:
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
async def recommend_list(request: Request, campaign_id: int, page: int = 1, page_size: int = 4, user: UserInfo = Depends(get_current_user_optional)):
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

    userQuests = list()
    if user:
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
            'is_claimed': True if userQuest.is_claimed == True else False,
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
        favoriteQuest['is_claimed'] = False
        if len(userQuests) == 0:
            favoriteQuest['action_completed'] = 0
            favoriteQuest['participation_status'] = ''
            continue
        for userQuest in userQuests:
            if favoriteQuest['id'] == userQuest.quest_id:
                favoriteQuest['action_completed'] = userQuest.action_completed
                favoriteQuest['participation_status'] = userQuest.status
                favoriteQuest['is_claimed'] = True if userQuest.is_claimed == True else False
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


@router.get('/list_by_dapp', tags=['quest'])
@limiter.limit('60/minute')
async def dapp_list(request: Request, dapp_id: int, user: UserInfo = Depends(get_current_user_optional)):
    if dapp_id <= 0:
        return success()
    questActions = await QuestAction.filter(dapps__contains=str(dapp_id)).all()
    if len(questActions) == 0:
        return success()

    questIds = list()
    questIdsDic = dict()
    for questAction in questActions:
        if questAction.quest_id in questIdsDic:
            continue
        dappIds = questAction.dapps.split(',')
        for dappId in dappIds:
            if dappId == str(dapp_id):
                questIds.append(questAction.quest_id)
                questIdsDic[questAction.quest_id] = questAction.quest_id
                break
    quests = await Quest.filter(id__in=questIds, status__not=STATUS_ENDED).order_by("-created_at").limit(3).values()

    userQuests = list()
    if user:
        questIds = list()
        for quest in quests:
            questIds.append(quest['id'])
        userQuests = await UserQuest.filter(account_id=user.id, quest_id__in=questIds).all().values('quest_id','action_completed')

    for quest in quests:
        quest['action_completed'] = 0
        if len(userQuests) == 0:
            continue
        for userQuest in userQuests:
            if quest['id'] == userQuest['quest_id']:
                quest['action_completed'] = userQuest['action_completed']
                break

    return success(quests)


@router.get('', tags=['quest'])
@limiter.limit('60/minute')
async def quest(request: Request, id: int = None, source: str = None, user: UserInfo = Depends(get_current_user_optional)):
    quest = None
    if id and id > 0:
        quest = await Quest.filter(id=id).first().values()
        if not quest:
            return error("quest not find")
    elif len(source) > 0:
        questAction = await QuestAction.filter(source=source).order_by("-id").first()
        if not questAction:
            return error("quest not find")
        quest = await Quest.filter(id=questAction.quest_id).first().values()
        if not quest:
            return error("quest not find")
    quest['total_user'] = 0
    quest['action_completed'] = 0

    total_user = await UserQuest.filter(quest_id=quest['id']).all().annotate(total_user=Count("id")).first().values("total_user")
    if total_user and total_user['total_user']:
        quest['total_user'] = total_user['total_user']
    quest['action_completed'] = 0

    userQuestActions = list()
    if user:
        userQuest = await UserQuest.filter(account_id=user.id, quest_id=quest['id']).first().values()
        if userQuest:
            quest['action_completed'] = userQuest['action_completed']
        userQuestActions = await UserQuestAction.filter(account_id=user.id, quest_id=quest['id']).all()

    actions = await QuestAction.filter(quest_id=quest['id']).order_by("id").all().values()

    networks = []
    dapps = []
    if actions:
        for action in actions:
            if len(userQuestActions) > 0:
                for userQuestAction in userQuestActions:
                    if userQuestAction.quest_action_id == action['id']:
                        action['status'] = userQuestAction.status
                        break
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
                dappRoute = ""
                dappName = ""
                dappLogo = ""
                networkName = ""
                for dapp in dapps:
                    if dapp['id'] == dappNetwork['dapp_id']:
                        dappRoute = dapp['route']
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
                    'route': dappRoute,
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
async def leaderboard(request: Request, page: int, page_size: int = 10):
    if page <= 0:
        page = 1
    if page_size <= 0:
        page_size = 10
    campaign = await QuestCampaignInfo.first().values("total_reward", "total_users", "total_quest_execution")
    total = await UserRewardRank.annotate(count=Count('id')).first().values("count")
    userRewards = await UserRewardRank.all().order_by("rank").offset((page-1)*page_size).limit(page_size).select_related("account")
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
        'total_reward': campaign['total_reward'] if campaign and campaign['total_reward'] else 0,
        'total_users': campaign['total_users'] if campaign and campaign['total_reward'] else 0,
        'total_quest_execution': campaign['total_quest_execution'] if campaign and campaign['total_reward'] else 0,
        'data': data,
        'total_page': math.ceil(total['count']/page_size),
    })


@router.get('/daily_check_in', tags=['quest'])
@limiter.limit('60/minute')
async def daily_check_in(request: Request, user: UserInfo = Depends(get_current_user)):
    dailyCheckInQuest = await QuestLong.filter(category='daily_check_in', status='ongoing').order_by("-id").first()
    if not dailyCheckInQuest:
        return success()
    rule = json.loads(dailyCheckInQuest.rule)
    reward_single_day = rule['reward_single_day']
    reward_consecutive = rule['reward_consecutive']
    todayChecInTime = getUtcSecond()
    todayHasClaimed = False
    oneDaySecond = 24 * 60 * 60

    userDailyCheckIns = await UserDailyCheckIn.filter(account_id=user.id, quest_long_id=dailyCheckInQuest.id).all().order_by("-check_in_time").values("reward", "check_in_time")
    data = list()
    if len(userDailyCheckIns) > 0 and todayChecInTime - userDailyCheckIns[0]['check_in_time'] <= oneDaySecond:
        todayHasClaimed = todayChecInTime == userDailyCheckIns[0]['check_in_time']
        userDailyCheckIns[0]['status'] = 'claimed'
        data.append(userDailyCheckIns[0])
        index = 1
        while index < len(userDailyCheckIns):
            if userDailyCheckIns[index-1]['check_in_time']-userDailyCheckIns[index]['check_in_time'] <= oneDaySecond:
                userDailyCheckIns[index]['status'] = 'claimed'
                data.insert(0, userDailyCheckIns[index])
            else:
                break
            index += 1

    consecutive_days = len(data)
    beforeDays = 0
    if len(data) > 7:
        beforeDays = len(data) - len(data) % 7
        data = data[-len(data) % 7:]

    nextDays = 7 - len(data)
    nextDay = 1
    while nextDay <= nextDays:
        reward = 0
        rewardConsecutiveIndex = len(reward_consecutive) - 1
        while rewardConsecutiveIndex >= 0:
            if reward_consecutive[rewardConsecutiveIndex]['day'] <= len(data):
                reward = reward_consecutive[rewardConsecutiveIndex]['reward']
                break
            rewardConsecutiveIndex -= 1
        if reward == 0:
            reward = reward_single_day
        dailyCheckIn = {
            'reward': reward,
        }
        if nextDay == 1 and not todayHasClaimed:
            dailyCheckIn['status'] = "claim"
        else:
            dailyCheckIn['status'] = "will_claim"
        data.append(dailyCheckIn)
        nextDay += 1

    for index, dailyCheckIn in enumerate(data):
        dailyCheckIn['day'] = beforeDays+index+1
    return success({
        'consecutive_days': consecutive_days,
        'data': data
    })


@router.post('/daily_check_in', tags=['quest'])
@limiter.limit('60/minute')
async def claim_daily_check_in(request: Request, user: UserInfo = Depends(get_current_user)):
    dailyCheckInQuest = await QuestLong.filter(category='daily_check_in', status='ongoing').order_by("-id").first()
    if not dailyCheckInQuest:
        return error("Cannot check in")
    rule = json.loads(dailyCheckInQuest.rule)
    reward_single_day = rule['reward_single_day']
    reward_consecutive = rule['reward_consecutive']
    todayChecInTime = getUtcSecond()
    oneDaySecond = 24 * 60 * 60

    userDailyCheckIns = await UserDailyCheckIn.filter(account_id=user.id, quest_long_id=dailyCheckInQuest.id).all().order_by("-check_in_time").values("reward", "check_in_time")
    if len(userDailyCheckIns) > 0 and userDailyCheckIns[0]['check_in_time'] == todayChecInTime:
        return error("Already check in,Cannot be check in multiple times")

    days = 0
    if len(userDailyCheckIns) > 0 and todayChecInTime - userDailyCheckIns[0]['check_in_time'] <= oneDaySecond:
        days = 1
        index = 1
        while index < len(userDailyCheckIns):
            if userDailyCheckIns[index-1]['check_in_time']-userDailyCheckIns[index]['check_in_time'] <= oneDaySecond:
               days += 1
            else:
                break
            index += 1

    reward = reward_single_day
    rewardConsecutiveIndex = len(reward_consecutive) - 1
    while rewardConsecutiveIndex >= 0:
        if reward_consecutive[rewardConsecutiveIndex]['day'] <= days:
            reward = reward_consecutive[rewardConsecutiveIndex]['reward']
            break
        rewardConsecutiveIndex -= 1

    dailyCheckIn = UserDailyCheckIn()
    dailyCheckIn.account_id = user.id
    dailyCheckIn.quest_long_id = dailyCheckInQuest.id
    dailyCheckIn.reward = reward
    dailyCheckIn.day = days+1
    dailyCheckIn.check_in_time = todayChecInTime
    await claimDailyCheckIn(user.id, dailyCheckIn, days+1)
    return success({
            'day': dailyCheckIn.day,
            'reward': dailyCheckIn.reward,
        })


@router.post('/claim', tags=['quest'])
@limiter.limit('60/minute')
async def claim_reward(request: Request, claimIn: ClaimIn, user: UserInfo = Depends(get_current_user)):
    userQuest = await UserQuest.filter(quest_id=claimIn.id, account_id=user.id).first().select_related('quest')
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


@router.post('/source', tags=['quest'])
@limiter.limit('60/minute')
async def source(request: Request, sourceIn: SourceIn, user: UserInfo = Depends(get_current_user)):
    if len(sourceIn.source) == 0:
        return error("source is empty")

    questActions = await QuestAction.filter(source=sourceIn.source, category__not='dapp').all()
    if len(questActions) == 0:
        return success("not find quest")

    for questAction in questActions:
        userQuestAction = await UserQuestAction.filter(account_id=user.id, quest_action_id=questAction.id).first()
        if userQuestAction:
            continue
        quest = await Quest.filter(id=questAction.quest_id).first()
        if quest.status != STATUS_ONGOING:
            continue
        await actionCompleted(user.id, questAction, quest)
    return success()
