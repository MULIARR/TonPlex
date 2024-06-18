from pytonapi import AsyncTonapi
from pytonapi.schema.accounts import Account
from pytonapi.schema.blockchain import Transactions
from pytonapi.schema.jettons import JettonsBalances, JettonBalance
from pytonapi.utils import nano_to_amount

from backend.app.models.transactions import TransactionsModel, TransactionModel
from backend.app.models.wallet import TonWalletAssetsDataModel, TonWalletModel, AssetModel
from backend.config import config
from backend.constants import CryptoLogo, SmartContractAddresses
from backend.utils.shorten_address import get_shorten_address


class AsyncTONApiClient:
    def __init__(self, tonapi_key: str):
        self.tonapi_client = AsyncTonapi(api_key=tonapi_key)

    async def get_wallet_assets_data(self, wallet: TonWalletModel) -> TonWalletAssetsDataModel:
        jettons_list = await self.get_jettons(address=wallet.address)

        account_data = await self.get_account_info(address=wallet.address)
        ton_balance = nano_to_amount(int(account_data.balance))

        # adding TON to the assets
        jettons_list.insert(
            0, AssetModel(
                smart_contract_address=SmartContractAddresses.TON,
                balance=ton_balance,
                name='Toncoin',
                symbol='TON',
                image=CryptoLogo.TON
            )
        )

        jettons_list = await self.get_rates_for_jettons_list(jettons_list)

        total_balance = sum(jetton.balance_in_usd for jetton in jettons_list)
        interface = account_data.interfaces[0] if account_data.interfaces else 'Undefined'

        account_status = account_data.status

        if account_status != 'active':
            # NOTE: non-bounceable address is needed for contracts where it is important that the
            # transaction be completed regardless of whether the recipient can accept it.

            wallet.address = wallet.address_model.to_string(True, True)  # non-bounceable
            wallet.shorten_address = get_shorten_address(wallet.address)  # TODO: maybe validate model instead

        return TonWalletAssetsDataModel(
            wallet=wallet,
            total_balance=total_balance,
            interface=interface,
            status=account_status,
            assets=jettons_list
        )

    async def get_rates_for_jettons_list(self, jettons_list: list[AssetModel]) -> list[AssetModel]:

        jettons_addresses = [jetton.smart_contract_address for jetton in jettons_list]

        rates_response = await self.tonapi_client.rates.get_prices(jettons_addresses, ['USD'])
        rates_dict = rates_response.rates

        for jetton in jettons_list:
            jetton.diff_24h = rates_dict[jetton.smart_contract_address]['diff_24h']['USD']

            jetton_price_in_usd = float(rates_dict[jetton.smart_contract_address]['prices']['USD'])

            jetton.balance_in_usd = jetton_price_in_usd * jetton.balance

        return jettons_list

    async def get_jettons(self, address: str) -> list[AssetModel]:
        jettons_data: JettonsBalances = (
            await self.tonapi_client.accounts.get_jettons_balances(
                account_id=address
            )
        ).balances

        jettons_list = []

        for jetton in jettons_data:
            jetton: JettonBalance

            jetton_user_friendly_address = jetton.jetton.address.to_userfriendly(is_bounceable=True)

            balance = nano_to_amount(int(jetton.balance))

            if balance > 0:
                jettons_list.append(
                    AssetModel(
                        smart_contract_address=jetton_user_friendly_address,
                        balance=balance,
                        name=jetton.jetton.name,
                        symbol=jetton.jetton.symbol,
                        image=jetton.jetton.image
                    )
                )

        return jettons_list

    async def get_account_info(self, address: str) -> Account:
        return await self.tonapi_client.accounts.get_info(account_id=address)

    async def get_transactions(self, account: str) -> TransactionsModel:
        result: Transactions = await self.tonapi_client.blockchain.get_account_transactions(
            account_id=account,
            limit=25
        )

        transactions_list = []

        for transaction in result.transactions:
            tonviewer_link = f'https://tonviewer.com/transaction/{transaction.hash}'
            ton_amount = nano_to_amount(transaction.in_msg.value)

            if ton_amount > 0:
                transaction_model = TransactionModel(
                    tonviewer_link=tonviewer_link,
                    type='Received',
                    value=f'+{ton_amount} TON',
                    image='/static/img/Inbox.png',
                )
                transactions_list.append(transaction_model)
            elif transaction.out_msgs:
                ton_amount = nano_to_amount(transaction.out_msgs[0].value)
                if ton_amount > 0:
                    transaction_model = TransactionModel(
                        tonviewer_link=tonviewer_link,
                        type='Sent',
                        value=f'-{ton_amount} TON',
                        image='/static/img/Outbox.png',
                    )
                    transactions_list.append(transaction_model)

        return TransactionsModel(transactions=transactions_list)


tonapi = AsyncTONApiClient(tonapi_key=config.tonapi.tonapi_key)
