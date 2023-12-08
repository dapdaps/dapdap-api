from pydantic import BaseModel


class ClaimIn(BaseModel):
    id: int


class SourceIn(BaseModel):
    source: str