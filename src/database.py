
from typing import Any, AsyncGenerator

from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from src.config import app_settings

class DatabaseHelper:
    def __init__(self, url:str, echo: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory= self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, Any]:
        """ Каждый раз создает новую сессию для работы """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependecy(self) -> AsyncGenerator[async_scoped_session[AsyncSession], Any]:
        """Создаем или получаем текущую сессию"""
        session = self.get_scoped_session()
        yield session
        await session.close()


database = DatabaseHelper(
    url=app_settings.database_url_test,
    echo=True
)
