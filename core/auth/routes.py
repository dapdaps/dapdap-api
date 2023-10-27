"""

"""
from datetime import timedelta

from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from starlette.status import HTTP_403_FORBIDDEN
from tortoise.exceptions import ValidationError

from core.auth.jwt import create_access_token, create_refresh_access_token
from core.auth.schemas import JWTToken, CredentialsSchema, JWTRefreshToken, CredentialsRefreshSchema, JWTTokenPayload
from core.auth.utils import authenticate, update_last_login
from core.utils.base_util import get_limiter
import logging

from settings.config import settings

logger = logging.getLogger(__name__)
limiter = get_limiter()
router = APIRouter(prefix="/api/auth")



@router.post("/access-token", response_model=JWTToken, tags=["auth"])
async def login_access_token(credentials: CredentialsSchema):
    try:
        user = await authenticate(credentials)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

    if user:
        await update_last_login(user.id)
    elif not user:
        raise HTTPException(status_code=400, detail="Incorrect address")
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_access_token_expires = timedelta(minutes=settings.JWT_REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),

        "refresh_access_token": create_refresh_access_token(
            data={"user_id": user.id}, expires_delta=refresh_access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/refresh-access-token", response_model=JWTRefreshToken, tags=["auth"])
async def refresh_access_token(cred_token: CredentialsRefreshSchema):
    try:
        payload = jwt.decode(cred_token.refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user_id = token_data.user_id
    if user_id:
        await update_last_login(user_id)
    elif not user_id:
        raise HTTPException(status_code=400, detail="Incorrect address")
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }