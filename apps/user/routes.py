import asyncio
import base64
import json
import logging
import time

import math
import requests
from tortoise import Tortoise

from tortoise.functions import Count

from apps.dapp.models import Dapp
from apps.invite.models import InviteCodePool
from apps.quest.models import QuestCampaign, Quest, UserQuest, UserRewardRank
from apps.user.dao import updateUserFavorite
from apps.user.models import UserInfo, UserFavorite, UserInfoExt
from apps.user.schemas import FavoriteIn, BindTwitterIn
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user
from starlette.requests import Request
from core.utils.tool_util import success, error
from settings.config import Settings

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/user")


@router.get('', tags=['user'])
@limiter.limit('60/minute')
async def user(request: Request, campaign_id: int = None, user: UserInfo = Depends(get_current_user)):
    userInfo = await UserInfo.filter(id=user.id).first()
    inviteTotal = await InviteCodePool.filter(creator_user_id=user.id, is_used=True).all().annotate(count=Count('id')).first().values("count")
    rewardRank = await UserRewardRank.filter(account_id=user.id).first()

    achieved = 0
    if campaign_id and campaign_id > 0:
        completedQuest = await UserQuest.filter(quest_campaign_id=campaign_id, account_id=user.id, status='completed').annotate(count=Count('id')).first().values("count")
        if completedQuest and completedQuest['count'] > 0:
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


@router.post('/bind/twitter', tags=['user'])
@limiter.limit('60/minute')
async def bind_twitter(request: Request, param: BindTwitterIn, user: UserInfo = Depends(get_current_user)):
    userInfo = await UserInfo.filter(id=user.id).first()
    if not userInfo:
        return error("user not exist")
    headers = {
        "Authorization": "Basic "+base64.b64encode((Settings.TWITTER_CLIENT_ID+":"+Settings.TWITTER_CLIENT_SECRET).encode()).decode(),
    }
    data = {
        'code': param.code,
        'grant_type': "authorization_code",
        'redirect_uri': Settings.TWITTER_REDIRECT_URL,
        'code_verifier': "challenge",
    }
    rep = requests.post("https://api.twitter.com/2/oauth2/token", params=data, headers=headers, verify=False)
    if rep.status_code != 200:
        logger.error(f"bind_twitter failed getToken status_code:{rep.status_code} text:{rep.text}")
        return error('bind failed')
    response = json.loads(rep.text)
    accessToken = response['access_token']
    refreshToken = response['refresh_token']
    tokenType = response['token_type']
    expiresIn = response['expires_in']
    if len(accessToken) <= 0 or len(tokenType) <= 0 or expiresIn <= 0:
        logger.error(f"bind_twitter failed accessToken:{accessToken} tokenType:{tokenType} expiresIn:{expiresIn}")
        return error('bind failed')

    headers = {
        "Authorization": f"{tokenType} {accessToken}",
    }
    rep = requests.get("https://api.twitter.com/2/users/me?user.fields=id,name,username,profile_image_url", headers=headers, verify=False)
    if rep.status_code != 200:
        logger.error(f"bind_twitter failed getUserInfo status_code:{rep.status_code} text:{rep.text}")
        return error('bind failed')
    response = json.loads(rep.text)
    avatar = response['data']['profile_image_url']
    username = response['data']['username']
    id = response['data']['id']
    if len(id) == 0:
        logger.error(f"bind_twitter failed getUserInfo id is empty")
        return error('bind failed')

    userInfo.avatar = avatar
    userInfo.username = username
    await userInfo.save()
    await UserInfoExt.update_or_create(defaults={
        'twitter_user_id': id,
        'twitter_access_token': accessToken,
        'twitter_refresh_token': refreshToken,
        'twitter_access_token_type': tokenType,
        'twitter_access_token_expires': int(time.time())+expiresIn,
    }, account_id=user.id)
    return success()