import asyncpg
from typing import List
from schemas import SportBase

class SportRepository:

    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def get_all(self) -> List[dict]:
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM sports")
            return [dict(row) for row in rows]

    async def create(self, sport: SportBase) -> dict:
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                "INSERT INTO sports(name, slug, active, type) VALUES($1, $2, $3, $4) RETURNING *",
                sport.name, sport.slug, sport.active, sport.type.value
            )
            return dict(row)

