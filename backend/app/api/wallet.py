from fastapi import APIRouter, Request

from backend.app.models.transactions import TransactionToSendModel
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.database.repo.user import user_repo

wallet_router = APIRouter(
    prefix="/wallet"
)


@wallet_router.post("/send_transaction")
async def send_transaction(request: Request, transaction_model: TransactionToSendModel):
    # get user
    user_model = await user_repo.get_user(transaction_model.user_id)

    # get user's wallet
    wallet_model = ton_wallet_manager.get_wallet(user_model.mnemonic)

    result = await ton_wallet_manager.transfer(
        wallet=wallet_model.wallet,
        to_address=transaction_model.to_address,
        amount=transaction_model.amount,
        payload=transaction_model.memo
    )

    if result:
        return {"success": True}
    else:
        return {"success": False}
