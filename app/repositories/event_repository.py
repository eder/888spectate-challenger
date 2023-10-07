from datetime import datetime
from schemas import EventType, EventStatus, SearchFilter
import asyncpg
from db.database import get_db_pool 

from utils.query_builder import QueryBuilder 

class EventRepository:

    def __init__(self, db_pool: get_db_pool):
        self.db_pool = db_pool
        self.query_builder = QueryBuilder('events')

    async def get_all(self) -> list:
            """
            Fetch all events from the database.

            Returns:
                list: List of dictionary representations of events.
                      Returns an empty list if there's an error.

            Raises:
                Prints an error message in case of database or unexpected error//s.
            """
            try:
                query = self.query_builder.build_query()
                async with self.db_pool.acquire() as connection:
                    rows = await connection.fetch(query)
                    return [dict(row) for row in rows]

            except (asyncpg.QueryCanceledError, asyncpg.PostgresError):
                print("Database error.")
                return []

            except Exception as e:
                print(f"Unexpected error: {e}")
                return []

    async def create(self, event: dict) -> dict:
        self.query_builder.add_insert_data(event_data)
        insert_query = self.query_builder.build_insert_query()
        
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(insert_query)
            return dict(row)
    

    async def update(self, event_id: int, event: dict) -> dict:

        self.query_builder.add_condition("id", event_id) 
        self.query_builder.add_update_data(event)
        update_query = self.query_builder.build_update_query()
        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(update_query)
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


    async def get_events_with_min_active_selections(self, min_selections: int):
            query = """
                SELECT e.*
                FROM events e
                JOIN selections s ON e.id = s.event_id
                WHERE s.active = true
                GROUP BY e.id
                HAVING COUNT(s.id) >= $1
            """
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, min_selections)
                return [dict(row) for row in rows]
      
