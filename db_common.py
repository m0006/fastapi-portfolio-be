from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_session_maker(url: str) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        create_async_engine(url),
        expire_on_commit=False
    )
