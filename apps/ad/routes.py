import logging

from starlette.requests import Request

from apps.ad.models import Ad
from core.utils.base_util import get_limiter
from fastapi import APIRouter
from core.utils.tool_util import success

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/ad")


@router.get('', tags=['ad'])
@limiter.limit('60/minute')
async def get_one(request: Request, category: str, category_id: int = 0):
    if category_id > 0:
        ad = await Ad.filter(category=category, category_id=category_id).all()
    else:
        ad = await Ad.filter(category=category).order_by('-updated_at').all()
    return success(ad)


