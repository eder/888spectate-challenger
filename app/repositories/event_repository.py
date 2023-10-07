from datetime import datetime
from schemas import EventType, EventStatus, SearchFilter
from db.database import get_db_pool, CustomPostgresError
from utils.query_builder import QueryBuilder


class EventRepository:

    def __init__(self, db_pool: get_db_pool):
        """
        Initialize the EventRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder('events')

    async def get_all(self) -> list:
        """
        Fetch all events from the database.

        Returns:
            list: List of dictionary representations of events.
                  Returns an empty list if there's an error.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        query = self.query_builder.build_query()

        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]

        except Exception as e:
            raise RepositoryError(f"Error: {str(e)}")

    async def create(self, event: dict) -> dict:
        """
        Create a new event in the database.

        Args:
            event (dict): Dictionary representing the event data.

        Returns:
            dict: Dictionary representing the newly created event.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        self.query_builder.add_insert_data(event)
        insert_query = self.query_builder.build_insert_query()
        
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(insert_query)
            return dict(row)

    async def update(self, event_id: int, event: dict) -> dict:
        """
        Update an event in the database.

        Args:
            event_id (int): The ID of the event to be updated.
            event (dict): Dictionary representing the updated event data.

        Returns:
            dict: Dictionary representing the updated event, or None if not found.

        Raises:
            Exception: If there's an error during database access.
        """
        self.query_builder.add_condition("id", event_id) 
        self.query_builder.add_update_data(event)
        update_query = self.query_builder.build_update_query()
        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(update_query)
                if row:
                    return dict(row)
                return None
        except CustomPostgresError as e:
            raise Exception(f"Error updating event with ID {event_id}. Error: {str(e)}")

    async def search_events_by_criteria(self, criteria: SearchFilter) -> list:
        """
        Search for events based on the given criteria.

        Args:
            criteria (SearchFilter): The search criteria.

        Returns:
            list: List of dictionary representations of events that match the criteria.
        """
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
        """
        Get events with a minimum number of active selections.

        Args:
            min_selections (int): The minimum number of active selections.

        Returns:
            list: List of dictionary representations of events that meet the criteria.
        """
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

