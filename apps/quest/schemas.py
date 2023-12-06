from pydantic import BaseModel


class ClaimIn(BaseModel):
    id: int