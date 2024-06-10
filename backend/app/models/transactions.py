from pydantic import BaseModel


class TransactionModel(BaseModel):
    tonviewer_link: str
    type: str
    value: str
    image: str


class TransactionsModel(BaseModel):
    transactions: list[TransactionModel]
