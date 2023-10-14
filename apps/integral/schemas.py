# @Time : 10/7/23 1:56 PM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : schemas.py
import uuid
from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel, EmailStr, UUID4, field_validator, validator
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from apps.integral.models import ActivityConfig
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
