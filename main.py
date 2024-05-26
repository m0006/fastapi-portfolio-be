import textwrap

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taxi_movement import taxi_router


API_PREFIX = "/api/v1"

DOCS_DESCRIPTION = """
    ## Notes:
    - Dataset used and modified for taxi_movement API: [Kaggle: Rome Taxi Data (subset)](https://www.kaggle.com/datasets/asjad99/rome-taxi-data-subset).\
"""


app = FastAPI(
    title="API",
    description=textwrap.dedent(DOCS_DESCRIPTION),
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"]
)

app.include_router(
    taxi_router.router,
    prefix=API_PREFIX
)
