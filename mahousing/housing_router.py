from typing import Any, AsyncGenerator
from operator import ge, le
from geoalchemy2.functions import ST_DWithin, ST_Point, ST_Transform
from pydantic import BaseModel
from sqlalchemy import and_, distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from mahousing.database import async_housing_session_maker
from mahousing.models import HousingListing, SRID, MbtaLine, MbtaStation
from mahousing.schemas import (
    HousingAttribValSchema,
    ListingSchema,
    MbtaLineSchema,
    MbtaStationSchema
)


MAHOUSING_TAG = "ma_housing"
MAHOUSING_PREFIX = "/" + MAHOUSING_TAG

DIV_MI_TO_METER = 0.0006213712

MA_SRID = 26986

PRICE_FIELD_PREFIX = "price_"
SQFEET_FIELD_PREFIX = "sqfeet_"
SPLIT_ON_CHAR = "_"


router = APIRouter(
    prefix=MAHOUSING_PREFIX,
    tags=[MAHOUSING_TAG]
)


class HousingQuery(BaseModel):
    region:                     str | None = None
    price_min:                  int | None = None
    price_max:                  int | None = None
    type:                       str | None = None
    sqfeet_min:                 int | None = None
    sqfeet_max:                 int | None = None
    beds:                       int | None = None
    baths:                      float | None = None

    cats_allowed:               int | None = None
    dogs_allowed:               int | None = None
    smoking_allowed:            int | None = None
    wheelchair_access:          int | None = None
    electric_vehicle_charge:    int | None = None
    comes_furnished:            int | None = None

    laundry_options:            str | None = None
    parking_options:            str | None = None


class MbtaStationQuery(BaseModel):
    name:       str
    dist_mi:    float


class PointDistQuery(BaseModel):
    x:          float
    y:          float
    dist_mi:    float


class CombinedOptionsQuery(BaseModel):
    housing_query:          HousingQuery | None = None
    mbta_station_query:     MbtaStationQuery | None = None
    point_dist_query:       PointDistQuery | None = None


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


@router.get("/housing_attrib_vals", response_model=HousingAttribValSchema)
async def get_housing_attrib_vals(
    db_session: AsyncSession = Depends(get_async_housing_session)
) -> Any:

    val_schema_dict = {}

    for field in HousingAttribValSchema.model_fields.keys():

        if field.startswith((PRICE_FIELD_PREFIX, SQFEET_FIELD_PREFIX)):
            # Create query for max col value:
            field_prefix = field.split(SPLIT_ON_CHAR)[0]
            attrib = getattr(HousingListing, field_prefix)

            val_query = select(attrib).order_by(
                attrib.desc()
            ).fetch(1)

            result = await db_session.execute(val_query)
            val_schema_dict[field] = result.scalars().one()

        else:
            # Create query for distinct col values:
            attrib = getattr(HousingListing, field)
            val_query = select(
                distinct(attrib)
            ).where(
                attrib.isnot(None)
            ).order_by(attrib)

            result = await db_session.execute(val_query)
            val_schema_dict[field] = result.scalars().all()

    return HousingAttribValSchema(**val_schema_dict)


@router.post("/get_housing_listings", response_model=list[ListingSchema])
async def get_listings_by_query(
    query: CombinedOptionsQuery,
    db_session: AsyncSession = Depends(get_async_housing_session)
) -> Any:

    if not any(
        (query.dict()[field] for field in query.model_fields.keys())
    ):
        listings_query = select(HousingListing)

    # initialize query and potential filter list:
    listings_query = select(HousingListing)

    filter_list = []

    if query.mbta_station_query:
        filter_list.append(
            (
                ST_DWithin(
                    ST_Transform(HousingListing.geom, MA_SRID),
                    select(ST_Transform(MbtaStation.geom, MA_SRID)).where(
                        MbtaStation.name == query.mbta_station_query.name
                    ).fetch(1).scalar_subquery(),
                    query.mbta_station_query.dist_mi / DIV_MI_TO_METER
                )
            )
        )

    if query.point_dist_query:
        filter_list.append(
            (
                ST_DWithin(
                    ST_Transform(HousingListing.geom, MA_SRID),
                    ST_Transform(
                        ST_Point(
                            query.point_dist_query.x,
                            query.point_dist_query.y,
                            SRID
                        ),
                        MA_SRID
                    ),
                    query.point_dist_query.dist_mi / DIV_MI_TO_METER
                )
            )
        )

    if query.housing_query:
        housing_dict = query.housing_query.dict()

        for field in housing_dict.keys():
            if housing_dict[field]:

                if field.startswith((PRICE_FIELD_PREFIX, SQFEET_FIELD_PREFIX)):
                    field_prefix, field_suffix = field.split(SPLIT_ON_CHAR)

                    comparison_op = le if field_suffix == "max" else ge
                    filter_list.append(
                        comparison_op(
                            getattr(HousingListing, field_prefix),
                            housing_dict[field]
                        )
                    )

                else:
                    filter_list.append(
                        getattr(HousingListing, field) == housing_dict[field]
                    )

    # If multiple where statements, use 'and_', else just use 'where'
    if len(filter_list) > 1:
        listings_query = listings_query.where(and_(*filter_list))
    elif len(filter_list) == 1:
        listings_query = listings_query.where(filter_list[0])
    else:
        listings_query = select(HousingListing)

    result = await db_session.execute(listings_query)
    listings = result.scalars().all()

    return listings
