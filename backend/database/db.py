from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import config


class Database:
    Base = declarative_base()

    def __init__(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            echo=True,
            pool_size=10,
            max_overflow=20,
            pool_recycle=1800,
            pool_pre_ping=True
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)


database = Database(config.db.database_url)

# import all models (native import)
import backend.database.models
