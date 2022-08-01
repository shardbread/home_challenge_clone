from functools import lru_cache
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import settings


@lru_cache
def get_master_engine() -> AsyncEngine:
    return create_async_engine(
        settings.async_database_url,
        echo=settings.DB_ECHO_LOG,
        pool_size=settings.DB_POOL_SIZE,
        pool_recycle=settings.DB_POOL_RECYCLE,
    )


class DbSessionContext:

    def __init__(
            self,
            session
    ):
        self.session = session

    async def __aenter__(
            self
    ) -> AsyncSession:
        async with self.session:
            async with self.session.begin():
                return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        elif self.session.is_active:
            await self.session.commit()


class DbSessionProvider:
    """
        DB session manager
    """
    master_engine: AsyncEngine = None

    @classmethod
    def setup(cls) -> None:
        cls.master_engine = get_master_engine()

    @classmethod
    def make_new_sessionmaker(cls) -> sessionmaker:
        if not cls.master_engine:
            cls.setup()
        return sessionmaker(
            cls.master_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @classmethod
    async def teardown(cls) -> None:
        """
            Dispose session
        """
        if cls.master_engine:
            await cls.master_engine.dispose()
            cls.master_engine = None

    @classmethod
    def get_session(cls) -> AsyncContextManager[AsyncEngine]:
        """
            Create new session
        """
        return DbSessionContext(cls.make_new_sessionmaker()())
