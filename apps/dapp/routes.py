import logging

from starlette.requests import Request

from apps.dapp.models import DappNetwork, DappCategory, Dapp, DappRelate
from apps.dapp.service import filterDapps
from apps.user.models import UserInfo
from core.auth.utils import get_current_user
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.utils.tool_util import success

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/dapp")


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
async def filter_list(request: Request, tad_token: bool = False, is_favorite: bool = False, network_ids: str = None, category_ids: str = None, quest: int = 0, page: int = 0, page_size: int = 100, user: UserInfo = Depends(get_current_user)):
    data = await filterDapps(user.id, tad_token, is_favorite, network_ids, category_ids, quest, page, page_size)
    return success(data)

