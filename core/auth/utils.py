# @Time : 10/25/23 6:03 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : utils.py
from datetime import datetime
from typing import Optional
from fastapi import Security, HTTPException
from jose import jwt
from jose.exceptions import JWTError
from starlette.status import HTTP_403_FORBIDDEN

from core.auth.schemas import CredentialsSchema, JWTTokenPayload
from apps.user.models import UserInfo
from apps.invite.models import InviteCodePool
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, HTTPAuthorizationCredentials
from settings.config import settings


async def authenticate(credentials: CredentialsSchema) -> Optional[UserInfo]:
    if credentials.address:
        user = await UserInfo.get_or_none(address=credentials.address)
    else:
        return None

    if user is None:
        return None

    code_obj = await InviteCodePool.get_or_none(used_user__address=credentials.address)
    if not code_obj or not code_obj.is_used:
        return None

    return user


async def update_last_login(user_id: int) -> None:
    user = await UserInfo.get(id=user_id)
    user.last_login = datetime.now()
    await user.save()


reusable_oauth2 = OAuth2AuthorizationCodeBearer(
    tokenUrl="/api/auth/login/access-token",
    authorizationUrl="/api/auth/access-token",
    refreshUrl="/api/auth/refresh-access-token"
)
async def get_current_user(token: str = Security(reusable_oauth2)) -> Optional[UserInfo]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await UserInfo.get_or_none(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user