from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    symbol: str
    image: str


class UserBalance(BaseModel):
    total: float
    wallet_address: str
    assets: dict[Asset]
