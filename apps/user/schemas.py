from pydantic import BaseModel


class FavoriteIn(BaseModel):
    id: int
    category: str
    favorite: bool


class BindTwitterIn(BaseModel):
    code: str


class BindTelegramIn(BaseModel):
    id: str
    first_name: str = None
    last_name: str = None
    username: str = None
    photo_url: str = None
    auth_date: int
    hash: str


class BindDiscordIn(BaseModel):
    code: str