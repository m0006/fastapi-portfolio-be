import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


load_dotenv(os.environ["DOTENV_PATH"])
TAXI_DB_URL = os.environ["TAXI_DB_URL"]

async_taxi_session_maker = async_sessionmaker(
    create_async_engine(TAXI_DB_URL),
    expire_on_commit=False
)
