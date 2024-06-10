from typing import Union, Optional

from pydantic import BaseModel
from tonsdk.contract.wallet import WalletContract


class TonWalletModel(BaseModel):
    address: str
    shorten_address: str
    mnemonics: list[str]
    public_key: bytes
    private_key: bytes
    wallet: WalletContract

    class Config:
        arbitrary_types_allowed = True


class AssetModel(BaseModel):
    smart_contract_address: str
    diff_24h: Optional[str] = None
    balance: Union[int, float]
    balance_in_usd: Optional[Union[int, float]] = None
    name: str
    symbol: str
    image: str

    def validate_and_round(self):
        if isinstance(self.balance, float):
            self.balance = round(self.balance, 2)
        if isinstance(self.balance_in_usd, float):
            self.balance_in_usd = round(self.balance_in_usd, 2)


class TonWalletAssetsDataModel(BaseModel):
    wallet: TonWalletModel
    total_balance: float
    interface: str
    assets: list[AssetModel]

    def __init__(self, **data):
        """
        autovalidate model
        :param data:
        """
        super().__init__(**data)
        self.sort_assets_by_balance_in_usd()
        self.validate_balance()
        self.validate_assets()

    def sort_assets_by_balance_in_usd(self):
        self.assets.sort(
            key=lambda asset: asset.balance_in_usd if asset.balance_in_usd is not None else 0,
            reverse=True
        )

        for i, asset in enumerate(self.assets):
            if asset.symbol == 'TON':
                ton_asset = self.assets.pop(i)
                self.assets.insert(0, ton_asset)
                break

    def validate_balance(self):
        if isinstance(self.total_balance, float):
            self.total_balance = round(self.total_balance, 2)

    def validate_assets(self):
        for asset in self.assets:
            asset.validate_and_round()
