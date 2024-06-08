import textwrap

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taximovement import taxi_router
from mahousing import housing_router


API_PREFIX = "/api/v1"

DOCS_DESCRIPTION = """
    ## Notes:
    - Datasets used and modified for API apps:
        - __housing_app__ API:
            - [Kaggle: USA Housing Listings](https://www.kaggle.com/datasets/austinreese/usa-housing-listings)
            - [MassGIS Data: MBTA Rapid Transit (December 2022 edition)](https://www.mass.gov/info-details/massgis-data-mbta-rapid-transit)
            - [MassGIS Data: Trains (November 2023 edition)](https://www.mass.gov/info-details/massgis-data-trains)
        - __taxi_movement__ API:
            - [Kaggle: Rome Taxi Data (subset)](https://www.kaggle.com/datasets/asjad99/rome-taxi-data-subset)
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
    allow_methods=["GET", "POST"]
)

app.include_router(
    housing_router.router,
    prefix=API_PREFIX
)

app.include_router(
    taxi_router.router,
    prefix=API_PREFIX
)
