from typing import AsyncGenerator
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase


from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, create_async_engine, async_sessionmaker

from config import settings

async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    future=True,
    pool_size=50,
    max_overflow=100,
    connect_args={
        'prepared_statement_name_func': lambda:  f'__asyncpg_{uuid4()}__',
    }
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        yield conn


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"