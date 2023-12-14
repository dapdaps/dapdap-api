from pydantic import BaseModel


class FavoriteIn(BaseModel):
    id: int
    category: str
    favorite: bool


class BindTwitterIn(BaseModel):
    code: str


class BindTelegramIn(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    photo_url: str
    auth_date: str
    hash: str