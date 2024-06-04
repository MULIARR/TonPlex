import asyncio
from typing import Optional

import requests
from pydantic import BaseModel
from pytonlib import TonlibClient
from tonsdk.contract.wallet import Wallets, WalletVersionEnum, WalletContract
from tonsdk.utils import to_nano

from pathlib import Path


class TonWallet(BaseModel):
    mnemonics: list[str]
    public_key: bytes
    private_key: bytes
    wallet: WalletContract

    class Config:
        arbitrary_types_allowed = True


class TonManager:
    def __init__(self):
        url_config = 'https://ton.org/global-config.json'
        config = requests.get(url_config).json()

        keystore_dir = '/tmp/ton_keystore'
        Path(keystore_dir).mkdir(parents=True, exist_ok=True)

        self.client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir)

    async def init_client(self):
        await self.client.init()

    @staticmethod
    def create_wallet(
            version=WalletVersionEnum.v4r2,
            workchain=0
    ) -> TonWallet:
        mnemonics, public_key, private_key, wallet = Wallets.create(
            version=version,
            workchain=workchain
        )

        return TonWallet(
            mnemonics=mnemonics,
            public_key=public_key,
            private_key=private_key,
            wallet=wallet
        )

    @staticmethod
    def get_wallet(
            mnemonics: list[str],
            version=WalletVersionEnum.v4r2,
            workchain=0
    ) -> TonWallet:
        mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(
            mnemonics=mnemonics,
            version=version,
            workchain=workchain
        )

        return TonWallet(
            mnemonics=mnemonics,
            public_key=public_key,
            private_key=private_key,
            wallet=wallet
        )

    @staticmethod
    def get_seqno(

    ):
        return True

    def transfer(
            self,
            from_address: WalletContract,
            to_address: str,
            amount: float,
            payload: Optional[str]
    ):
        seqno = self.get_seqno()

        from_address.create_transfer_message(
            to_addr=to_address,
            amount=to_nano(amount, 'ton'),
            seqno=seqno,
            payload=payload
        )


ton_manager = TonManager()
# asyncio.get_event_loop().run_until_complete(ton_manager.init_client())
# print(ton_manager.client.__dict__)
