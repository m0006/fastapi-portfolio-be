from typing import Annotated, Any, AsyncGenerator
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Path

from mahousing.database import async_housing_session_maker
from mahousing.models import HousingListing, MbtaLine, MbtaStation
from mahousing.schemas import ListingSchema, MbtaLineSchema, MbtaStationSchema


MAHOUSING_TAG = "ma_housing"
MAHOUSING_PREFIX = "/" + MAHOUSING_TAG


router = APIRouter(
    prefix=MAHOUSING_PREFIX,
    tags=[MAHOUSING_TAG]
)


async def get_async_housing_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_housing_session_maker() as session:
        yield session


@router.get("/mbta_lines", response_model=list[MbtaLineSchema])
async def get_all_mbta_lines(
    db_session: AsyncSession = Depends(get_async_housing_session)
) -> Any:
    lines_query = select(
        MbtaLine
    ).order_by(MbtaLine.type, MbtaLine.name)

    result = await db_session.execute(lines_query)
    lines = result.scalars().all()

    return lines


@router.get("/mbta_stations", response_model=list[MbtaStationSchema])
async def get_all_mbta_stations(
    db_session: AsyncSession = Depends(get_async_housing_session)
) -> Any:
    stations_query = select(
        MbtaStation
    ).order_by(MbtaStation.type, MbtaStation.line, MbtaStation.name)

    result = await db_session.execute(stations_query)
    stations = result.scalars().all()

    return stations
