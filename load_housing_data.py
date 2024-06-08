import asyncio

from shapely import MultiLineString
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Callable, TypeVar

from db_common import Base
from load_common import (
    commit_record_list,
    csv_loader,
    geojson_loader,
    is_table_empty
)
from mahousing.database import async_housing_session_maker
from mahousing.models import HousingListing, MbtaLine, MbtaStation


DATA_PATH_PREFIX = "mahousing/data/"
GEOJSON_EXT = ".geojson"

FUNC_MODEL_REGISTRY = []

C = TypeVar('C', bound=Callable)


def run_with_model(param: Base) -> C:
    """ Adds decorated funcs to registry to be looped over """
    def register(fn: Callable[async_sessionmaker[AsyncSession], None]) -> C:
        FUNC_MODEL_REGISTRY.append((fn, param))
        return fn
    return register


def create_housing_listing(row: list) -> HousingListing:
    return HousingListing(
        region=row[0],
        price=int(row[1]),
        type=row[2],
        sqfeet=int(row[3]),
        beds=int(row[4]),
        baths=float(row[5]),
        cats_allowed=int(row[6]),
        dogs_allowed=int(row[7]),
        smoking_allowed=int(row[8]),
        wheelchair_access=int(row[9]),
        electric_vehicle_charge=int(row[10]),
        comes_furnished=int(row[11]),
        laundry_options=row[12] if row[12] else None,
        parking_options=row[13] if row[13] else None,
        geom=f"POINT({row[14]} {row[15]})"
    )


def create_lines_record(feature: dict) -> MbtaLine:
    return MbtaLine(
        name=feature["properties"]["LINE"],
        type=feature["properties"]["TYPE"],
        geom=MultiLineString(
            lines=feature["geometry"]["coordinates"]
        ).wkt
    )


def create_station_record(feature: dict) -> MbtaStation:
    coords = feature["geometry"]["coordinates"]
    return MbtaStation(
        name=feature["properties"]["STATION"],
        line=feature["properties"]["LINE"],
        type=feature["properties"]["TYPE"],
        geom=f"POINT({coords[0]} {coords[-1]})"
    )


@run_with_model(HousingListing)
async def load_housing_listings(
    async_session: async_sessionmaker[AsyncSession]
) -> None:

    housing_listings = csv_loader(
        f"{DATA_PATH_PREFIX}housing_cleaned_clipped_4326.csv",
        create_housing_listing
    )
    await commit_record_list(async_session, housing_listings, "listing")


@run_with_model(MbtaLine)
async def load_mbta_lines(
    async_session: async_sessionmaker[AsyncSession]
) -> None:

    for filename in ("commrail_line_4326", "transit_line_4326"):
        mbta_lines = geojson_loader(
            f"{DATA_PATH_PREFIX}{filename}{GEOJSON_EXT}",
            create_lines_record
        )
        await commit_record_list(async_session, mbta_lines, "line")


@run_with_model(MbtaStation)
async def load_mbta_stations(
    async_session: async_sessionmaker[AsyncSession]
) -> None:

    for filename in ("commrail_point_4326", "transit_point_4326"):
        mbta_stations = geojson_loader(
            f"{DATA_PATH_PREFIX}{filename}{GEOJSON_EXT}",
            create_station_record
        )
        await commit_record_list(async_session, mbta_stations, "station")


async def async_main() -> None:
    for func, model in FUNC_MODEL_REGISTRY:
        if await is_table_empty(async_housing_session_maker, model):
            await func(async_housing_session_maker)


if __name__ == "__main__":
    asyncio.run(async_main())
