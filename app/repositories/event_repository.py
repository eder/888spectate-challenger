import logging

from datetime import datetime
from db.database import get_db_pool, CustomPostgresError
from utils.query_builder import QueryBuilder
from .errors import RepositoryError


class EventRepository:
    def __init__(self, db_pool: get_db_pool, logger: logging.Logger):
        """
        Initialize the EventRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
            logger (logging.Logger): An instance of the logging logger.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("events")
        self.logger = logger

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
            self.logger.info("Fetching all events...")
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error fetching events: {e}")
            raise RepositoryError(f"Error fetching events: {e}")

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

        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(insert_query)
                return dict(row)

        except Exception as e:
            self.logger.error(f"Error creating event: {e}")
            raise RepositoryError(f"Error creating event: {e}")

    async def update(self, event_id: int, event: dict) -> dict:
        """
        Update an event in the database.

        Args:
            event_id (int): The ID of the event to be updated.
            event (dict): Dictionary representing the updated event data.

        Returns:
            dict: Dictionary representing the updated event, or None if not found.

        Raises:
            RepositoryError: If there's an error during database access.
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
            self.logger.error(f"Error updating event with ID {event_id}: {e}")
            raise RepositoryError(f"Error updating event with ID {event_id}: {e}")

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
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, min_selections)
                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error fetching events with min active selections: {e}")
            raise RepositoryError(
                f"Error fetching events with min active selections: {e}"
            )

    async def filter_events(self, query, params):
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, *params)
                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error searching events with regex: {e}")
            raise Exception(f"Error searching events with regex: {e}")

    async def get_active_events_count(self, sport_id: int):
        query = "SELECT COUNT(*) FROM events WHERE sport_id=$1 AND active=TRUE"
        try:
            async with self.db_pool.acquire() as connection:
                return await connection.fetchval(query, sport_id)

        except Exception as e:
            self.logger.error(f"Error fetching active events count: {e}")
            raise RepositoryError(f"Error fetching active events count: {e}")

    async def set_event_as_inactive(self, event_id: int):
        event = {"active": False}
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
            self.logger.error(f"Error setting event as inactive: {e}")
            raise RepositoryError(f"Error setting event as inactive: {e}")

    async def get_events_selections(self):
        select_query = """
        SELECT events.id, events.name, COUNT(selections.id) as active_selection_count 
        FROM events 
        JOIN selections ON events.id = selections.event_id 
        WHERE selections.active = TRUE 
        GROUP BY events.id 
        """
        try:
            async with self.db_pool.acquire() as connection:
                result = await connection.fetch(select_query)
                return result

        except Exception as e:
            self.logger.error(f"Error fetching events' selections: {e}")
            raise RepositoryError(f"Error fetching events' selections: {e}")
