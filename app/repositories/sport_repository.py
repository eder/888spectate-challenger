import logging
from typing import List

from db.database import get_db_pool
from schemas import SportBase
from utils.query_builder import QueryBuilder
from .errors import RepositoryError

class SportRepository:
    def __init__(self, db_pool: get_db_pool, logger: logging.Logger):
        """
        Initialize the SportRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
            logger (logging.Logger): An instance of the logging logger.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("sports")
        self.logger = logger

    async def get_all(self) -> List[dict]:
        """
        Fetch all sports from the database.

        Returns:
            List[dict]: List of dictionary representations of sports.
                        Returns an empty list if there's an error.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        try:
            query = self.query_builder.build_query()
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except RepositoryError as e:
            self.logger.error(f"Error fetching all sports: {str(e)}")
            raise RepositoryError(f"Error: {str(e)}")

    async def create(self, sport: dict) -> dict:
        """
        Create a new sport in the database.

        Args:
            sport (dict): Dictionary representing the sport data.

        Returns:
            dict: Dictionary representing the newly created sport.

        Raises:
             If there's an error during database access.
        """
        try:
            self.query_builder.add_insert_data(sport)
            insert_query = self.query_builder.build_insert_query()
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(insert_query)
                if row:
                    return dict(row)
                else:
                    raise RepositoryError("Record not found after insertion")
        except RepositoryError as e:
            self.logger.error(f"Error creating sport: {str(e)}")
            raise RepositoryError(f"Error creating sport: {str(e)}")

    async def update(self, sport_id: int, sport: dict) -> dict:
        """
        Update a sport in the database.

        Args:
            sport_id (int): The ID of the sport to be updated.
            sport (dict): Dictionary representing the updated sport data.

        Returns:
            dict: Dictionary representing the updated sport, or None if not found.

        Raises:
            UpdateError: If the sport with the specified ID is not found.
            ForeignKeyError: If an invalid sport ID is provided.
        """
        try:
            self.query_builder.add_condition("id", sport_id)
            self.query_builder.add_update_data(sport)
            update_query = self.query_builder.build_update_query()
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(update_query)
                if row:
                    return dict(row)
                raise UpdateError(f"Sport with ID {selection_id} not found.")
        except RepositoryError as e:
            if "selections_event_id_fkey" in str(e):
                raise RepositoryError("Invalid sport ID provided.") from e
            raise RepositoryError(f"Error updating sport with ID {sport_id}. Error: {str(e)}")

    async def filter_sports(self, query, params) -> List[dict]:
        try:
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, *params)
                return [dict(row) for row in rows]

        except RepositoryError as e:
            self.logger.error(f"Error searching sports: {str(e)}")
            raise RepositoryError(f"Error searching sports: {str(e)}")

    async def set_sport_inactive(self, sport_id: int):
        """
        Set a sport as inactive in the database.

        Args:
            sport_id (int): The ID of the sport to be marked as inactive.
        """
        update_query = "UPDATE sports SET active=FALSE WHERE id=$1"
        async with self.db_pool.acquire() as connection:
            await connection.execute(update_query, sport_id)
