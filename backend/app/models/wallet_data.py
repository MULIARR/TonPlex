from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    symbol: str
    image: str


class WalletDataModel(BaseModel):
    total: float
    wallet_address: str
    shorten_wallet_address: str
    assets: list[Asset]
