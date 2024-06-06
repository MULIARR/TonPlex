from pydantic import BaseModel


class UserModel(BaseModel):
    allows_write_to_pm: bool
    first_name: str
    id: int
    language_code: str
    last_name: str
    username: str
