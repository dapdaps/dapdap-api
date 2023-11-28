from pydantic import BaseModel


class DappFavoriteIn(BaseModel):
    dapp_id: int
    favorite: bool