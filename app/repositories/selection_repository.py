import asyncpg
from schemas import SelectionOutcome

class SelectionRepository:

    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def get_all(self) -> list:
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM selections")
            return [dict(row) for row in rows]

    async def create(self, selection: dict) -> dict:
        outcome_value = selection["outcome"].value if isinstance(selection["outcome"], SelectionOutcome) else selection["outcome"]
        
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO selections(name, event_id, price, active, outcome) 
                VALUES($1, $2, $3, $4, $5) 
                RETURNING *
                """,
                selection["name"], selection["event_id"], selection["price"], selection["active"], outcome_value
            )
            return dict(row)

