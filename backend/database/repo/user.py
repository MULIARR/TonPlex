from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.classes.encryption_manager import encryption_manager
from backend.database.db import database
from backend.database.models.user import User


class UserRepo:
    def __init__(self):
        self.session: AsyncSession = database.session

    async def get_user(self, user_id: int):
        result = await self.session.execute(select(User).filter_by(user_id=user_id))
        user = result.scalars().first()

        # decrypt wallet mnemonic
        user.mnemonic = encryption_manager.decrypt(user.mnemonic)
        return user

    async def create_user(self, user_id: int, mnemonic: str):
        # encrypt wallet mnemonic
        mnemonic = '_'.join(mnemonic)
        encrypted_mnemonic = encryption_manager.encrypt(mnemonic)

        new_user = User(user_id=user_id, mnemonic=encrypted_mnemonic)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()


user_repo = UserRepo()
