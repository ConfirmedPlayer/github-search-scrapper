from typing import Self

from asyncpg import create_pool
from database import sql_queries


class Database:
    def __init__(self, db_credentials: dict[str, str]) -> None:
        self.db_credentials = db_credentials

    async def async_init(self) -> Self:
        async with create_pool(**self.db_credentials) as conn:
            await conn.execute(sql_queries.create_table_if_not_exists)
        return self

    async def insert_new_data(self, *args) -> None:
        async with create_pool(**self.db_credentials) as conn:
            await conn.execute(sql_queries.add_new_record, *args)
