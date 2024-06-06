from sqlalchemy import Column, Integer, LargeBinary
from backend.database.db import Database


class User(Database.Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    mnemonic = Column(LargeBinary, nullable=False)
