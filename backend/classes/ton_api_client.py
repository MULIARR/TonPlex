from pytonapi import AsyncTonapi
from pytonapi.schema.blockchain import Transactions
from pytonapi.utils import nano_to_amount

from backend.config import config


class AsyncTONApiClient:
    def __init__(self, tonapi_key: str):
        self.tonapi_client = AsyncTonapi(api_key=tonapi_key)

    async def get_account_info(self, account: str):
        return self.tonapi_client.accounts.get_info(account_id=account)

    async def get_transactions(self, account: str):
        result: Transactions = self.tonapi_client.blockchain.get_account_transactions(
            account_id=account,
            limit=35
        )

        for transaction in result.transactions:
            print(f"Value TON: {nano_to_amount(transaction.in_msg.value)}")

            if transaction.in_msg.decoded_op_name == "text_comment":
                print(f"Comment: {transaction.in_msg.decoded_body['text']}")


tonapi = AsyncTONApiClient(tonapi_key=config.tonapi.tonapi_key)


async def main():
    account_id = "EQBAjCF-QDZMdmgJsxsgN_lOPPO7oG1zisme9gnw_o_U1DOA"

    # Retrieve account information asynchronously
    account = await tonapi.tonapi_client.accounts.get_info(account_id=account_id)

    # Print account details
    print(f"Account Address (raw): {account.address.to_raw()}")
    print(f"Account Address (userfriendly): {account.address.to_userfriendly(is_bounceable=True)}")
    print(f"Account Balance (nanoton): {account.balance.to_nano()}")
    print(f"Account Balance (amount): {account.balance.to_amount()}")


# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.get_event_loop().run_until_complete(main())
