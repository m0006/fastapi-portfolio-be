from typing import Annotated, AsyncGenerator
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Path

from taximovement.database import async_taxi_session_maker
from taximovement.models import TaxiLocation
from taximovement.schemas import TaxiIdSchema, TaxiLocationSchema


TAXIMOVEMENT_TAG = "taxi_movement"
TAXIMOVEMENT_PREFIX = "/" + TAXIMOVEMENT_TAG


router = APIRouter(
    prefix=TAXIMOVEMENT_PREFIX,
    tags=[TAXIMOVEMENT_TAG]
)


async def get_async_taxi_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_taxi_session_maker() as session:
        yield session


@router.get("/taxi_ids", response_model=list[TaxiIdSchema])
async def get_driver_ids(
    db_session: AsyncSession = Depends(get_async_taxi_session)
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


@router.get(
    "/taxi_locations/{driver_id}",
    response_model=list[TaxiLocationSchema]
)
async def get_locations_for_driver(
    driver_id: Annotated[
        int,
        Path(
            title="The ID of the Taxi Driver to get",
            gt=0,
            lt=400
        )
    ],
    db_session: AsyncSession = Depends(get_async_taxi_session)
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
