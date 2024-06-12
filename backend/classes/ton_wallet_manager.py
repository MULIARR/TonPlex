import logging
from pathlib import Path
from typing import Optional

import requests
from pytonlib import TonlibClient, BlockNotFound, ExternalMessageNotAccepted, TonlibNoResponse
from tonsdk.contract.wallet import Wallets, WalletVersionEnum, WalletContract
from tonsdk.crypto.exceptions import InvalidMnemonicsError
from tonsdk.utils import to_nano

from backend.app.models.wallet import TonWalletModel
from backend.utils.shorten_address import get_shorten_address

logger = logging.getLogger(__name__)


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
    ) -> TonWalletModel:
        mnemonics, public_key, private_key, wallet = Wallets.create(
            version=version,
            workchain=workchain
        )

        # get user-friendly wallet address
        # Initially, the address must be without a parameter (is_bounceable) so that it can receive tokens
        # but at this point it's not necessary
        user_friendly_address = wallet.address.to_string(True, True)

        return TonWalletModel(
            address=user_friendly_address,
            address_model=wallet.address,
            shorten_address=get_shorten_address(user_friendly_address),
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
    ) -> TonWalletModel:
        try:
            mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(
                mnemonics=mnemonics,
                version=version,
                workchain=workchain
            )
        except InvalidMnemonicsError:
            return False

        # get user friendly wallet address
        user_friendly_address = wallet.address.to_string(True, True, True)  # bounceable

        return TonWalletModel(
            address=user_friendly_address,
            address_model=wallet.address,
            shorten_address=get_shorten_address(user_friendly_address),
            mnemonics=mnemonics,
            public_key=public_key,
            private_key=private_key,
            wallet=wallet
        )

    async def deploy_wallet(self, wallet: WalletContract) -> bool:
        query = wallet.create_init_external_message()
        deploy_message = query['message'].to_boc(False)

        try:
            res = await self.client.raw_send_message(deploy_message)
            if res['@type'] == 'ok':  # Example: {'@type': 'ok', '@extra': '171885.76129:0:0.17586420542'}
                logger.info(f'Successfully deployed wallet at address: {wallet.address}')
                return True
        except ExternalMessageNotAccepted:
            logger.error(f'Initial contract call failed (probably insufficient balance): {wallet.address}')

        logger.warning(f'Deploy wallet failed for address: {wallet.address}')
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

        amount_in_ton = to_nano(amount, 'ton')

        transfer_query = wallet.create_transfer_message(
            to_addr=to_address,
            amount=amount_in_ton,
            seqno=seqno,
            payload=payload
        )

        transfer_message = transfer_query['message'].to_boc(False)

        try:
            res = await self.client.raw_send_message(transfer_message)
            if res['@type'] == 'ok':
                logger.info(f'The transfer ({amount_in_ton} TON) was successfully sent to the network.')
                return True
        except ExternalMessageNotAccepted:
            return False


# lazy init
ton_wallet_manager = TONWalletManager()
