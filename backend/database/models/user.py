from sqlalchemy import Column, LargeBinary, BigInteger
from backend.database.db import Database


class User(Database.Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    mnemonic = Column(LargeBinary, nullable=False)
