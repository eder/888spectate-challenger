from datetime import datetime
from schemas import EventType, EventStatus
import asyncpg

class EventRepository:

    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def get_all(self) -> list:
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM events")
            return [dict(row) for row in rows]

    async def create(self, event: dict) -> dict:
        scheduled_start = datetime.fromisoformat(event["scheduled_start"].isoformat())
        actual_start = datetime.fromisoformat(event["actual_start"].isoformat())
        type_value = event["type"].value if isinstance(event["type"], EventType) else event["type"]
        status_value = event["status"].value if isinstance(event["status"], EventStatus) else event["status"]
        
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO events(name, slug, active, type, sport_id, status, scheduled_start, actual_start)
                VALUES($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING *
                """,
                event["name"], event["slug"], event["active"], type_value, 
                event["sport_id"], status_value, scheduled_start, actual_start
            )
            return dict(row)

