import logging

from core.utils.base_util import get_limiter
from fastapi import APIRouter

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/quest")

