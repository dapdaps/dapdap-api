# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : schemas.py
import uuid
from typing import Optional
from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator
from apps.invite.models import InviteCodePool

class BaseProperties(BaseModel):
    @validator("hashed_id", pre=True, always=True, check_fields=False)
    def default_hashed_id(cls, v):
        return v or uuid.uuid4()

    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={"id", "is_superuser", "is_active"},
        )

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class ActivateCodeIn(BaseModel):
    address: Optional[str]
    code: Optional[str]


class GenerateCodeIn(BaseModel):
    address: Optional[str] = None
    code_number: Optional[int] = 3
    creator_type: Optional[int] = 1


class GenerateCodeOut(BaseModel):
    address: Optional[str] = None
    code: Optional[str]
    creator_type: Optional[int]
    is_used: Optional[bool]
    class Config:
        from_attributes = True

InviteCodePoolDetailOut = pydantic_model_creator(InviteCodePool)


# class BaseUser(BaseProperties):
#     first_name: Optional[str]
#     last_name: Optional[str]
#     hashed_id: Optional[UUID4] = None
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
#     is_active: Optional[bool] = True
#     is_superuser: Optional[bool] = False
#     created_at: Optional[datetime]
#
#
# class BaseUserCreate(BaseProperties):
#     first_name: Optional[str]
#     last_name: Optional[str]
#     hashed_id: Optional[UUID4] = None
#     email: EmailStr
#     username: Optional[str]
#     password: str
#
#
# class BaseUserUpdate(BaseProperties):
#     first_name: Optional[str]
#     last_name: Optional[str]
#     password: Optional[str]
#     email: Optional[EmailStr]
#     username: Optional[str]
#
#
# class BaseUserDB(BaseUser):
#     id: int
#     hashed_id: UUID4
#     password_hash: str
#     updated_at: datetime
#     last_login: Optional[datetime]
#
#     class Config:
#         orm_mode = True
#
#
# class BaseUserOut(BaseUser):
#     id: int
#
#     class Config:
#         orm_mode = True
