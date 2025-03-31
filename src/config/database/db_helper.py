from typing import AsyncGenerator
from asyncio import current_task
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session

from . import settings_db

class DatabaseHelper:
    #Инициализация бд с использованием параметров из файла конфигурации и Фабрики сессий
    def __init__(self):
        self.engine = create_async_engine(
            url=settings_db.database_url,
            echo=settings_db.DB_ECHO_LOG,
            connect_args={"check_same_thread": False}
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    #Возвращает ссесию привязанную к текущей задаче
    def get_scoped_session(self):
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )

    #Асинхронный менеджер для взаимодействия с БД
    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

db_helper1 = DatabaseHelper()