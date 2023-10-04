import asyncpg

class EventRepository:

    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def get_all(self) -> list:
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM events")
            return [dict(row) for row in rows]

    async def create(self, event: dict) -> dict:
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO events(name, slug, active, type, sport_id, status, scheduled_start, actual_start) 
                VALUES($1, $2, $3, $4, $5, $6, $7, $8) 
                RETURNING *
                """,
                event["name"], event["slug"], event["active"], event["type"], event["sport_id"], 
                event["status"], event["scheduled_start"], event["actual_start"]
            )
            return dict(row)

