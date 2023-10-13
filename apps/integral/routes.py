# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : routes.py
from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from apps.invite.schemas import ActivateCodeIn, GenerateCodeIn, GenerateCodeOut, InviteCodePoolDetailOut
from apps.invite.utils import generate_invite_code
from core.utils.base_util import get_limiter
from settings.config import settings
import logging

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/integral")