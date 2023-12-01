import logging

from tortoise.functions import Sum, Count
from starlette.requests import Request

from apps.dapp.models import Network, Dapp, DappNetwork
from apps.quest.models import QuestCampaign, Quest, UserQuest, QuestCategory, QuestAction
from apps.user.models import UserInfo
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user
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
async def recommend_quest(request: Request, campaign_id: int, page: int = 1, page_size: int = 4, user: UserInfo = Depends(get_current_user)):
    quests = await Quest.filter(quest_campaign_id=campaign_id).order_by('-priority').limit(page_size).offset((page-1)*page_size).values()
    if len(quests) == 0:
        return success()
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
    return success(quests)


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
    if actions:
        networks = await Network.all().values()
        dapps = await Dapp.all().values()
        for action in actions:
            operators = list()
            action['operators'] = operators
            if len(action['dapps']) == 0 or len(action['networks']) == 0:
                continue
            actionDappIds = action['dapps'].split(',')
            actionNetworkIds = action['networks'].split(',')
            dappNetworks = await DappNetwork.filter(dapp_id__in = actionDappIds, network_id__in = actionNetworkIds).all().values()
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
            action['dapps'] = operators

    return success({
        'quest': quest,
        'actions': actions,
    })