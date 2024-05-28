import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from load_common import commit_record_list, csv_loader, is_table_empty
from taximovement.database import async_taxi_session_maker
from taximovement.models import TaxiLocation


def create_taxi_location(row: list) -> TaxiLocation:
    return TaxiLocation(
        driver_id=int(row[0]),
        time=row[1],
        geom=f"POINT({row[2]} {row[3]})",
    )


async def load_taxi_data(
    async_session: async_sessionmaker[AsyncSession]
) -> None:

    taxi_locations = csv_loader(
        "taximovement/data/taxi_data_subset_cleaned.csv",
        create_taxi_location
    )

    await commit_record_list(async_session, taxi_locations, "location")


async def async_main() -> None:
    if await is_table_empty(async_taxi_session_maker, TaxiLocation):
        await load_taxi_data(async_taxi_session_maker)


if __name__ == "__main__":
    asyncio.run(async_main())
