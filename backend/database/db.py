from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import config


class Database:
    Base = declarative_base()

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True, pool_size=10, max_overflow=20)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            print("Starting database initialization...")
            await conn.run_sync(self.Base.metadata.create_all)
            print("Database initialization complete.")


database = Database(config.db.database_url)

# import all models
import backend.database.models