from sqlalchemy.future import select
from backend.classes.encryption_manager import encryption_manager
from backend.database.db import database
from backend.database.models.user import User


class UserRepo:
    def __init__(self):
        self.SessionLocal = database.SessionLocal

    async def get_user(self, user_id: int):
        async with self.SessionLocal() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            user = result.scalars().first()

            # decrypt wallet mnemonic
            if user:
                user.mnemonic = encryption_manager.decrypt(user.mnemonic)
            return user

    async def create_user(self, user_id: int, mnemonic: str):
        # encrypt wallet mnemonic
        mnemonic = '_'.join(mnemonic)
        encrypted_mnemonic = encryption_manager.encrypt(mnemonic)

        async with self.SessionLocal() as session:
            new_user = User(user_id=user_id, mnemonic=encrypted_mnemonic)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def delete_user(self, user_id: int):
        async with self.SessionLocal() as session:
            user = await self.get_user(user_id)
            if user:
                await session.delete(user)
                await session.commit()


user_repo = UserRepo()
