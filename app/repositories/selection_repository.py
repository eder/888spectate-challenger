from typing import List
import logging

from db.database import get_db_pool, CustomPostgresError
from schemas import SelectionOutcome
from utils.query_builder import QueryBuilder


class SelectionRepository:
    """
    A repository class responsible for managing CRUD operations on selections.
    """

    def __init__(self, db_pool: get_db_pool, logger: logging.Logger):
        """
        Initialize the SelectionRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
            logger (logging.Logger): An instance of the logging logger.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("selections")
        self.logger = logger

    async def get_all(self) -> list:
        """
        Fetch all selections from the database.

        Returns:
            list: List of dictionary representations of selections.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        try:
            query = self.query_builder.build_query()
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except Exception as e:
            self.logger.error(f"Error fetching selections: {e}")
            raise RepositoryError(f"Error: {str(e)}")

    async def create(self, selection: dict) -> dict:
        """
        Create a new selection in the database.

        Args:
            selection (dict): Dictionary representing the selection data.

        Returns:
            dict: Dictionary representing the newly created selection.

        Raises:
            CustomPostgresError: If there's a specific database error during the creation.
        """
        try:
            self.query_builder.add_insert_data(selection)
            insert_query = self.query_builder.build_insert_query()
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(insert_query)
                if row:
                    return dict(row)
                else:
                    raise CustomPostgresError("Record not found after insertion")
        except CustomPostgresError as e:
            self.logger.error(f"Error creating selection: {e}")
            raise CustomPostgresError(f"Error creating selection: {str(e)}")

    async def update(self, selection_id: int, selection: dict) -> dict:
        """
        Update an existing selection in the database.

        Args:
            selection_id (int): The ID of the selection to update.
            selection (dict): Dictionary containing updated selection data.

        Returns:
            dict: Dictionary representing the updated selection.

        Raises:
            UpdateError, ForeignKeyError: If there's an error during the update.
        """
        try:
            self.query_builder.add_condition("id", selection_id)
            self.query_builder.add_update_data(selection)
            update_query = self.query_builder.build_update_query()
            self.logger.info(f"Updating selection with ID {selection_id}...")
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(update_query)
                if row:
                    return dict(row)
                raise UpdateError(f"Selection with ID {selection_id} not found.")
        except CustomPostgresError as e:
            self.logger.error(f"Error updating selection with ID {selection_id}: {e}")
            if "selections_event_id_fkey" in str(e):
                raise ForeignKeyError("Invalid Selection ID provided.") from e
            raise UpdateError(
                f"Error updating selection with ID {selection_id}. Error: {str(e)}"
            )

    async def get_active_selections_count(self, event_id: int):
        """
        Get the count of active selections for a given event.

        Args:
            event_id (int): The ID of the event.

        Returns:
            int: The count of active selections.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        count_query = (
            "SELECT COUNT(*) FROM selections WHERE event_id=$1 AND active=TRUE"
        )
        try:
            async with self.db_pool.acquire() as connection:
                return await connection.fetchval(count_query, event_id)
        except Exception as e:
            self.logger.error(
                f"Error fetching active selections count for event ID {event_id}: {e}"
            )
            raise RepositoryError(f"Error: {str(e)}")

    async def get_event_id(self, selection_id: int):
        """
        Fetch the event ID for a given selection ID.

        Args:
            selection_id (int): The ID of the selection.

        Returns:
            int: The event ID associated with the selection.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        event_id_query = "SELECT event_id FROM selections WHERE id = $1"
        try:
            async with self.db_pool.acquire() as connection:
                return await connection.fetchval(event_id_query, selection_id)
        except Exception as e:
            self.logger.error(
                f"Error fetching event ID for selection ID {selection_id}: {e}"
            )
            raise RepositoryError(f"Error: {str(e)}")

    async def filter_selections(self, query, params) -> List[dict]:
        """
        Search selections based on a regex pattern.

        Args:
            regex (str): The regex pattern to search for.

        Returns:
            List[dict]: List of dictionary representations of matched selections.

        Raises:
            Exception: If there's an error during the search.
        """
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, *params)
                return [dict(row) for row in rows]
        except CustomPostgresError as e:
            self.logger.error(f"Error searching selections with regex: {e}")
            raise Exception(f"Error searching selections: {str(e)}")



    async  def get_selections_by_event_id(self, event_id: int) -> List[dict]:
        query = f"SELECT * FROM selections WHERE event_id = {event_id};"
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except CustomPostgresError as e:
            self.logger.error(f"Error getting selections with event ID: {e}")
            raise Exception(f"Error getting selections: {str(e)}")

    
    async  def get_selections_by_sport_id(self, sport_id: int) -> List[dict]:
        query = f"SELECT s.* FROM selections s JOIN events e ON s.event_id = e.id WHERE e.sport_id= {sport_id};"
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except CustomPostgresError as e:
            self.logger.error(f"Error getting selections with sport ID: {e}")
            raise Exception(f"Error getting selections: {str(e)}")

