from pydantic import BaseModel


class FavoriteIn(BaseModel):
    id: int
    category: str
    favorite: bool


class BindTwitterIn(BaseModel):
    code: str