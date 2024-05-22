from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
import textwrap
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

from database import get_async_session
from models import TaxiLocation
from schemas import TaxiIdSchema, TaxiLocationSchema


TAXIMOVEMENT_TAG = "taxi_movement"

DOCS_DESCRIPTION = """
    ## Notes:
    - Dataset used for taxi_movement API: [Kaggle: Rome Taxi Data (subset)](https://www.kaggle.com/datasets/asjad99/rome-taxi-data-subset).\
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


@app.get(
    "/api/v1/taxi_movement/taxi_ids",
    response_model=list[TaxiIdSchema],
    tags=[TAXIMOVEMENT_TAG]
)
async def get_driver_ids(
        db_session: AsyncSession = Depends(get_async_session)
    ):

    taxi_id_query = select(
        distinct(TaxiLocation.driver_id)
    ).order_by(TaxiLocation.driver_id)

    result = await db_session.execute(taxi_id_query)
    taxi_ids = [
        {"driver_id": driver_id}
        for driver_id in result.scalars().all()
    ]
 
    return taxi_ids


@app.get(
    "/api/v1/taxi_movement/taxi_locations/{driver_id}",
    response_model=list[TaxiLocationSchema],
    tags=[TAXIMOVEMENT_TAG]
)
async def get_locations_for_driver(
        driver_id: Annotated[
            int,
            Path(
                title="The ID of the Taxi Driver to get",
                gt=0,
                lt=500
            )
        ],
        db_session: AsyncSession = Depends(get_async_session)
    ):

    taxi_loc_query = select(TaxiLocation).where(
        TaxiLocation.driver_id == driver_id
    ).order_by(TaxiLocation.time)

    result = await db_session.execute(taxi_loc_query)

    taxi_locs = []
    for row in result.scalars().all():
        taxi_locs.append(
            {
                "driver_id": row.driver_id,
                "time": row.time,
                "geom": row.geom
            }
        )

    if not taxi_locs:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return taxi_locs
