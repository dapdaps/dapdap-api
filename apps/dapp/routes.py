import logging
import time

import math
from starlette.requests import Request
from tortoise.functions import Count

from apps.dapp.models import DappNetwork, DappCategory, Dapp, DappRelate, Category
from apps.dapp.service import filterDapps
from apps.user.models import UserInfo, UserFavorite
from core.auth.utils import get_current_user, get_current_user_optional
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.utils.tool_util import success, error

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/dapp")


@router.get('/category_list', tags=['dapp'])
@limiter.limit('60/minute')
async def category_list(request: Request):
    data = await Category.all().order_by('-id')
    return success(data)


@router.get('/list', tags=['dapp'])
@limiter.limit('60/minute')
async def dapp_list(request: Request, page: int = 0, page_size: int = 20):
    offset = (page - 1) * page_size
    total = await Dapp.all().annotate(count=Count('id')).first().values('count')
    data = await Dapp.all().order_by('-created_at').offset(offset).limit(page_size).values()
    if len(data) > 0:
        dappIds = list()
        for dapp in data:
            dappIds.append(dapp['id'])
        dappNetworks = await DappNetwork.filter(dapp_id__in=dappIds).all()
        for dapp in data:
            if len(dapp['category_ids']) > 0:
                dappCategoryList = list()
                categoryIds = dapp['category_ids'].split(",")
                for id in categoryIds:
                        dappCategoryList.append({
                            'dapp_id': dapp['id'],
                            'category_id': int(id),
                        })
                dapp['dapp_category'] = dappCategoryList
            if len(dapp['network_ids']) > 0:
                dappNetworkList = list()
                networkIds = dapp['network_ids'].split(",")
                for id in networkIds:
                    dappSrc = ""
                    for dappNetwork in dappNetworks:
                        if dappNetwork.dapp_id == dapp['id'] and dappNetwork.network_id == int(id):
                            dappSrc = dappNetwork.dapp_src
                            break
                    dappNetworkList.append({
                        'dapp_id': dapp['id'],
                        'network_id': int(id),
                        'dapp_src': dappSrc,
                    })
                dapp['dapp_network'] = dappNetworkList
            del dapp['category_ids']
            del dapp['network_ids']
    return success({
        'data': data,
        'total': total['count'],
        'total_page':  math.ceil(total['count']/page_size)
    })


@router.get('', tags=['dapp'])
@limiter.limit('60/minute')
async def get_one(request: Request, id: int):
    dapp = await Dapp.filter(id=id).first().values()
    if not dapp:
        return error("not find")

    dappNetworks = await DappNetwork.filter(dapp_id=dapp['id']).all()
    if len(dapp['category_ids']) > 0:
        dappCategoryList = list()
        categoryIds = dapp['category_ids'].split(",")
        for id in categoryIds:
            dappCategoryList.append({
                'dapp_id': dapp['id'],
                'category_id': int(id),
            })
        dapp['dapp_category'] = dappCategoryList
    if len(dapp['network_ids']) > 0:
        dappNetworkList = list()
        networkIds = dapp['network_ids'].split(",")
        for id in networkIds:
            dappSrc = ""
            for dappNetwork in dappNetworks:
                if dappNetwork.network_id == int(id):
                    dappSrc = dappNetwork.dapp_src
                    break
            dappNetworkList.append({
                'dapp_id': dapp['id'],
                'network_id': int(id),
                'dapp_src': dappSrc,
            })
        dapp['dapp_network'] = dappNetworkList
    del dapp['category_ids']
    del dapp['network_ids']
    return success(dapp)


@router.get('/hot_list', tags=['dapp'])
@limiter.limit('60/minute')
async def hot_list(request: Request, network_id: int):
    dappNetworks = await DappNetwork.filter(network_id=network_id).select_related("dapp")
    for index, dappNetwork in enumerate(dappNetworks):
        if dappNetwork.dapp.priority <= 0:
            del dappNetworks[index]

    dapps = list()
    if len(dappNetworks) == 0:
        return success(dapps)

    dappNetworks.sort(key=lambda x: x.dapp.priority, reverse=True)
    dappIds = list()
    for dappNetwork in dappNetworks:
        dappIds.append(dappNetwork.dapp.id)
    dappCategorys = await DappCategory.filter(dapp_id__in=dappIds)
    for dappNetwork in dappNetworks:
        dapp = {
            'id':   dappNetwork.dapp.id,
            'name': dappNetwork.dapp.name,
            'description': dappNetwork.dapp.description,
            'logo': dappNetwork.dapp.logo,
            'src': dappNetwork.dapp_src,
        }
        dappCategoryIds = set()
        for dappCategory in dappCategorys:
            if dappNetwork.dapp.id == dappCategory.dapp_id:
                dappCategoryIds.add(dappCategory.category_id)
        dapp['category_ids'] = dappCategoryIds
        dapps.append(dapp)
    return success(dapps)


@router.get('/relate_list', tags=['dapp'])
@limiter.limit('60/minute')
async def relate_list(request: Request, dapp_id: int):
    dappRelates = await DappRelate.filter(dapp_id=dapp_id).order_by("-created_at").values("dapp_id_relate")
    if len(dappRelates) == 0:
        return success([])

    dappIds = set()
    for dappRelate in dappRelates:
        dappIds.add(dappRelate['dapp_id_relate'])
    dapps = await Dapp.filter(id__in=dappIds)
    dappCategorys = await DappCategory.filter(dapp_id__in=dappIds)
    for dapp in dapps:
        dappCategoryIds = set()
        for dappCategory in dappCategorys:
            if dappCategory.dapp_id == dapp.id:
                dappCategoryIds.add(dappCategory.category_id)
        dapp.category_ids = dappCategoryIds
    return success(dapps)


@router.get('/filter_list', tags=['dapp'])
@limiter.limit('60/minute')
async def filter_list(request: Request, tbd_token: bool = False, is_favorite: bool = False, network_ids: str = None, category_ids: str = None, quest: int = 0, page: int = 0, page_size: int = 100, user: UserInfo = Depends(get_current_user_optional)):
    data = await filterDapps(user.id if user else 0, tbd_token, is_favorite, network_ids, category_ids, quest, page, page_size)
    return success(data)


@router.get('/favorite_list', tags=['dapp'])
@limiter.limit('60/minute')
async def favorite_list(request: Request, user: UserInfo = Depends(get_current_user)):
    userFavorites = await UserFavorite.filter(account_id=user.id, category="dapp", is_favorite=True)
    if len(userFavorites) == 0:
        return success([])
    dappIds = list()
    for userFavorite in userFavorites:
        dappIds.append(userFavorite.relate_id)
    favoriteDapps = await Dapp.filter(id__in=dappIds).all().values()
    if len(favoriteDapps) == 0:
        return success([])
    for favoriteDapp in favoriteDapps:
        if len(favoriteDapp['category_ids']) > 0:
            dappIds = favoriteDapp['category_ids'].split(",")
            favoriteDapp['category_ids'] = [int(item) for item in dappIds]
        if len(favoriteDapp['network_ids']) > 0:
            networkIds = favoriteDapp['network_ids'].split(",")
            favoriteDapp['network_ids'] = [int(item) for item in networkIds]
    return success(favoriteDapps)