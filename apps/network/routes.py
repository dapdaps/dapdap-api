import logging

from starlette.requests import Request

from apps.network.models import Network
from core.utils.base_util import get_limiter
from fastapi import APIRouter
from core.utils.tool_util import success

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/network")


@router.get('/list', tags=['network'])
@limiter.limit('60/minute')
async def list(request: Request):
    networks = await Network.all().order_by('-priority')
    return success(networks)


@router.get('', tags=['network'])
@limiter.limit('60/minute')
async def get_network(request: Request, id: int):
    network = await Network.filter(id=id).first()
    return success(network)


@router.get('/getByChainId', tags=['network'])
@limiter.limit('60/minute')
async def get_network(request: Request, chain_id: int):
    network = await Network.filter(chain_id=chain_id).first()
    return success(network)


