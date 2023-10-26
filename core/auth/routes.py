"""

"""
from datetime import timedelta

from fastapi import APIRouter, HTTPException

from core.auth.jwt import create_access_token
from core.auth.schemas import JWTToken, CredentialsSchema
from core.auth.utils import authenticate, update_last_login
from core.utils.base_util import get_limiter
import logging

from settings.config import settings

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/auth")



@router.post("/access-token", response_model=JWTToken, tags=["login"])
async def login_access_token(credentials: CredentialsSchema):
    user = await authenticate(credentials)
    if user:
        await update_last_login(user.id)
    elif not user:
        raise HTTPException(status_code=400, detail="Incorrect address")
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }