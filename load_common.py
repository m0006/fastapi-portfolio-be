import csv
import json

from sqlalchemy import select, exists
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db_common import Base


async def commit_record_list(
    async_session: async_sessionmaker[AsyncSession],
    record_list: list[Base],
    record_type: str
) -> None:

    print(f"Loading {len(record_list)} {record_type} records into db...")
    async with async_session() as session:
        async with session.begin():
            session.add_all(record_list)
            await session.commit()


def csv_loader(
    filepath: str,
    create_records_func: Callable[[list], Base]
) -> list[Base]:

    record_list = []

    with open(filepath, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        # Skip the first row (header)
        next(csv_reader)

        for row in csv_reader:
            record = create_records_func(row)
            record_list.append(record)

    return record_list


def geojson_loader(
    filepath: str,
    create_records_func: Callable[[dict], Base]
) -> list[Base]:

    record_list = []
    with open(filepath) as json_file:
        data = json.load(json_file)

    for feature in data["features"]:
        record = create_records_func(feature)
        record_list.append(record)
    
    return record_list


async def is_table_empty(
    async_session: async_sessionmaker[AsyncSession],
    model: Base
) -> bool:

    async with async_session() as session:
        query = select(model.id.isnot(None))
        query = select(exists(query))
        result = await session.execute(query)

    table_exists = result.scalars().one()
    return not (table_exists)
