import logging
import math

from tortoise.functions import Count

from apps.dapp.models import Dapp
from apps.invite.models import InviteCodePool
from apps.quest.models import QuestCampaign, Quest, QuestCampaignReward, UserQuest
from apps.user.dao import updateUserFavorite
from apps.user.models import UserInfo, UserFavorite
from apps.user.schemas import FavoriteIn
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user
from starlette.requests import Request
from core.utils.tool_util import success, error

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/user")


@router.get('', tags=['user'])
@limiter.limit('60/minute')
async def user(request: Request, campaign_id: int, user: UserInfo = Depends(get_current_user)):
    userInfo = await UserInfo.filter(id=user.id).first()
    inviteTotal = await InviteCodePool.filter(creator_user_id=user.id, is_used=True).all().annotate(count=Count('id')).first().values("count")
    rewardRank = await QuestCampaignReward.filter(quest_campaign_id=campaign_id, account_id=user.id).first()

    achieved = 0
    completedQuest = await UserQuest.filter(quest_campaign_id=campaign_id, account_id=user.id, status='completed').annotate(count=Count('id')).first().values("count")
    if completedQuest['count'] > 0:
        totalQuest = await Quest.filter(quest_campaign_id=campaign_id).annotate(count=Count('id')).first().values("count")
        achieved = math.ceil(completedQuest['count']/totalQuest['count']*100)

    return success({
        'id': userInfo.id,
        'address': userInfo.address,
        'avatar': userInfo.avatar,
        'reward': rewardRank.reward,
        'rank': rewardRank.rank,
        'total_invited': inviteTotal['count'],
        'achieved': achieved
    })


@router.post('/favorite', tags=['user'])
@limiter.limit('60/minute')
async def favorite(request: Request, param: FavoriteIn, user: UserInfo = Depends(get_current_user)):
    if param.category == "dapp":
        dapp = await Dapp.filter(id=param.id).first()
        if not dapp:
            return error(msg="dapp not find")
    elif param.category == "quest_campaign":
        campaign = await QuestCampaign.filter(id=param.id).first()
        if not campaign:
            return error(msg="quest campaign not find")
    elif param.category == "quest":
        quest = await Quest.filter(id=param.id).first()
        if not quest:
            return error(msg="quest not find")
    else:
        return error(msg="illegal category")

    userFavorite = await UserFavorite.filter(account_id=user.id, relate_id=param.id, category=param.category).first().values("is_favorite")
    if param.favorite and userFavorite and userFavorite["is_favorite"]:
        return success(msg="Already favorited, cannot favorite again")
    if not param.favorite and (not userFavorite or not userFavorite["is_favorite"]):
        return success()

    await updateUserFavorite(user.id, param.id, param.category, param.favorite)
    # await UserFavorite.update_or_create(
    #     defaults={
    #         "is_favorite": param.favorite,
    #     },
    #     account_id=user.id,
    #     relate_id=param.id,
    #     category=param.category,
    # )
    return success()


@router.get('/favorite', tags=['user'])
@limiter.limit('60/minute')
async def is_favorite(request: Request, id: int, category: str, user: UserInfo = Depends(get_current_user)):
    userFavorite = await UserFavorite.filter(account_id=user.id, relate_id=id, category=category).first().values("is_favorite")
    return success({
        "favorite": True if userFavorite and userFavorite["is_favorite"] else False
    })
