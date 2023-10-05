from datetime import datetime
from schemas import EventType, EventStatus, SearchFilter
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
    

    async def update(self, event_id: int, event: dict) -> dict:
        
        def process_field(field, value):
            if (field in ["scheduled_start", "actual_start"]) and isinstance(value, str):
                return datetime.fromisoformat(value)
            if field == "type" and isinstance(value, EventType):
                return value.value
            if field == "status" and isinstance(value, EventStatus):
                return value.value
            return value

        processed_event = {key: process_field(key, value) for key, value in event.items() if value is not None}

        set_clause = ", ".join([f"{key}=${i}" for i, (key, value) in enumerate(processed_event.items(), start=1)])
        values = list(processed_event.values()) + [event_id]

        query = f"""
        UPDATE events
        SET {set_clause}
        WHERE id=${len(values)}
        RETURNING *;
        """

        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(query, *values)
                if row:
                    return dict(row)
                return None
        except asyncpg.exceptions.PostgresError as e:
            raise Exception(f"Error updating event with ID {event_id}. Error: {str(e)}")

    async def search_events_by_criteria(self, criteria: SearchFilter) -> list:
            conditions = []
            values = []

            if criteria.name_regex:
                conditions.append("name ~ $1")
                values.append(criteria.name_regex)

            if criteria.start_time_from and criteria.start_time_to:
                conditions.append("scheduled_start BETWEEN $2 AND $3")
                
                start_time_from = criteria.start_time_from
                start_time_to = criteria.start_time_to
                
                if isinstance(criteria.start_time_from, str):
                    start_time_from = datetime.fromisoformat(criteria.start_time_from)
                
                if isinstance(criteria.start_time_to, str):
                    start_time_to = datetime.fromisoformat(criteria.start_time_to)

                values.append(start_time_from)
                values.append(start_time_to)

            where_clause = " AND ".join(conditions) if conditions else "TRUE"

            query = f"SELECT * FROM events WHERE {where_clause}"

            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, *values)
                return [dict(row) for row in rows]
