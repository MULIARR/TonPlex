from pydantic import BaseModel


class MnemonicsModel(BaseModel):
    user_id: int
    mnemonics: list[str]
