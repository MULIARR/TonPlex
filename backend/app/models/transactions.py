from typing import Union, Optional

from pydantic import BaseModel


class TransactionModel(BaseModel):
    tonviewer_link: str
    type: str
    value: str
    image: str


class TransactionsModel(BaseModel):
    transactions: list[TransactionModel]


class TransactionToSendModel(BaseModel):
    user_id: int
    amount: Union[int, float]
    to_address: str
    memo: Optional[str] = None
