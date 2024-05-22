from dotenv import load_dotenv
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv(os.environ["DOTENV_PATH"])
DB_URL = os.environ["DB_URL"]


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DB_URL)

# expire_on_commit - don't expire objects after transaction commit
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
