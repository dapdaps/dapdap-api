import logging

from apps.dapp.dao import updateFavorite
from apps.dapp.models import DappFavorite, Dapp
from apps.dapp.schemas import DappFavoriteIn
from apps.user.models import UserInfo
from core.utils.base_util import get_limiter
from fastapi import APIRouter, Depends
from core.auth.utils import get_current_user
from starlette.requests import Request
from core.utils.tool_util import success, error

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/dapp")


@router.post('/favorite', tags=['dapp'])
@limiter.limit('60/minute')
async def favorite(request: Request, param: DappFavoriteIn, user: UserInfo = Depends(get_current_user)):
    dapp = await Dapp.filter(id=param.dapp_id).first()
    if not dapp:
        return error(msg="dapp not find")

    dappFavorite = await DappFavorite.filter(dapp_id=param.dapp_id, account_id=user.id).first().values("is_favorite")
    if param.favorite and dappFavorite and dappFavorite["is_favorite"]:
        return success(msg="Already favorited, cannot favorite again")
    if not param.favorite and (not dappFavorite or not dappFavorite["is_favorite"]):
        return success()

    await updateFavorite(param.dapp_id, user.id, param.favorite)
    # await DappFavorite.update_or_create(
    #     defaults={
    #         "is_favorite": param.favorite,
    #     },
    #     dapp_id=param.dapp_id,
    #     account_id=user.id,
    # )
    return success()
