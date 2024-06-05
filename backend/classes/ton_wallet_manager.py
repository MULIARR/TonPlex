import asyncio
import logging
from typing import Optional

import requests
from pydantic import BaseModel
from pytonlib import TonlibClient, BlockNotFound, ExternalMessageNotAccepted, TonlibNoResponse
from tonsdk.contract.wallet import Wallets, WalletVersionEnum, WalletContract
from tonsdk.utils import to_nano

from pathlib import Path

logger = logging.getLogger(__name__)


class TonWallet(BaseModel):
    mnemonics: list[str]
    public_key: bytes
    private_key: bytes
    wallet: WalletContract

    class Config:
        arbitrary_types_allowed = True


class TONWalletManager:
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

    async def deploy_wallet(self, wallet: WalletContract):
        query = wallet.create_init_external_message()

        deploy_message = query['message'].to_boc(False)

        try:
            await self.client.raw_send_message(deploy_message)
        except ExternalMessageNotAccepted:
            wallet_address = wallet.address.to_string(True, True, True)
            logger.error(f'Initial contract call failed (probably insufficient balance): {wallet_address}')

            return False

    async def get_seqno(
            self,
            wallet: WalletContract
    ):
        try:
            data = await self.client.raw_run_method(
                method='seqno',
                stack_data=[],
                address=wallet.address.to_string(True, True, True)
            )
        except BlockNotFound:
            return False
        except TonlibNoResponse:
            return 1
        except Exception as e:
            logger.error(f'Unknown error when trying to call a get_seqno request from a wallet: {e}')
            return False

        seqno = int(data['stack'][0][1], 16)
        return seqno

    async def transfer(
            self,
            wallet: WalletContract,
            to_address: str,
            amount: float,
            payload: Optional[str] = None
    ):
        seqno = await self.get_seqno(wallet)

        # means that wallet not deployed
        if not seqno:
            # deploy wallet
            await self.deploy_wallet(wallet)

            # send txn again
            await self.transfer(
                wallet=wallet,
                to_address=to_address,
                amount=amount,
                payload=payload
            )
            return

        transfer_query = wallet.create_transfer_message(
            to_addr=to_address,
            amount=to_nano(amount, 'ton'),
            seqno=seqno,
            payload=payload
        )

        transfer_message = transfer_query['message'].to_boc(False)

        await self.client.raw_send_message(transfer_message)
        return True


# lazy init
ton_manager = TONWalletManager()


# mnemonics = ['mirror', 'shoot', 'mercy', 'share', 'step', 'picture', 'grant', 'promote', 'stock', 'absent', 'picnic', 'vacuum', 'apple', 'else', 'promote', 'income', 'slot', 'behave', 'shock', 'champion', 'mystery', 'father', 'stone', 'media']

mnemonics = ['loyal', 'tiny', 'furnace', 'hip', 'such', 'curtain', 'ensure', 'fresh', 'rely', 'budget', 'rocket', 'system', 'suspect', 'confirm', 'hedgehog', 'okay', 'fuel', 'topic', 'force', 'spoon', 'stool', 'sunset', 'display', 'review']


async def main():
    wallet_model = ton_manager.get_wallet(mnemonics=mnemonics)
    print(wallet_model.wallet.address.to_string(True, True, True))
    print(await ton_manager.transfer(wallet_model.wallet,
                                     'UQB1wRfCgskWK_vyb--_oVnynDa9QLV5x6aNxNqtTfXxuaJK',
                                     0.1
                                     ))
    # print(await ton_manager.get_seqno(wallet_model.wallet))
    # print(await ton_manager.deploy_wallet(wallet_model.wallet))

    # await ton_manager.deploy_wallet(wallet_model.wallet)ddd


# asyncio.get_event_loop().run_until_complete(main())


# mnemonics = ['loyal', 'tiny', 'furnace', 'hip', 'such', 'curtain', 'ensure', 'fresh', 'rely', 'budget', 'rocket', 'system', 'suspect', 'confirm', 'hedgehog', 'okay', 'fuel', 'topic', 'force', 'spoon', 'stool', 'sunset', 'display', 'review']
# public_key = b',\xe2\xc1*;\xa99\xe5\x83,\xf7S\xcf\xcb\x7fl\xb9\xfaa\xb6\xa50Qe\xac\xacnf0\x0bFa'
# private_key = b'\x907^\xe50\xa2\xa0\x7f*\x1fG.\xee\xaf\xde\xbb\xe2*\x93\xc1\xcd\xb4\xfc\xab\xff\x8c<\x7fe\xc1P\xe1,\xe2\xc1*;\xa99\xe5\x83,\xf7S\xcf\xcb\x7fl\xb9\xfaa\xb6\xa50Qe\xac\xacnf0\x0bFa'


