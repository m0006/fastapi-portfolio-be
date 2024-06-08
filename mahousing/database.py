import os
from dotenv import load_dotenv

from db_common import get_session_maker


load_dotenv(os.environ["DOTENV_PATH"])
HOUSING_DB_URL = os.environ["HOUSING_DB_URL"]

async_housing_session_maker = get_session_maker(HOUSING_DB_URL)
