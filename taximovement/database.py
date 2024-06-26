import os
from dotenv import load_dotenv

from db_common import get_session_maker


load_dotenv(os.environ["DOTENV_PATH"])
TAXI_DB_URL = os.environ["TAXI_DB_URL"]

async_taxi_session_maker = get_session_maker(TAXI_DB_URL)
