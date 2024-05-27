import asyncio
import csv

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from taximovement.database import async_taxi_session_maker
from taximovement.models import TaxiLocation


async def is_taxi_table_empty(
        async_session: async_sessionmaker[AsyncSession]
    ) -> bool:

    async with async_session() as session:
        query = select(TaxiLocation.id.isnot(None))
        query = select(exists(query))
        result = await session.execute(query)

    table_exists = result.scalars().one()
    return not (table_exists)


async def load_data(
        async_session: async_sessionmaker[AsyncSession]
    ) -> None:

    taxi_locations = []
    with open("taximovement/data/taxi_data_subset_cleaned.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        # Skip the first row (header)
        next(csv_reader)

        for row in csv_reader:
            taxi_location = TaxiLocation(
                driver_id=int(row[0]),
                time=row[1],
                geom=f"POINT({row[2]} {row[3]})",
            )
            taxi_locations.append(taxi_location)

    print(f"Loading {len(taxi_locations)} records into db...")
    async with async_session() as session:
        async with session.begin():
            session.add_all(taxi_locations)
            await session.commit()


async def async_main() -> None:
    if await is_taxi_table_empty(async_taxi_session_maker):
        await load_data(async_taxi_session_maker)


if __name__ == "__main__":
    asyncio.run(async_main())
