from typing import List
import re

from db.database import get_db_pool, CustomPostgresError
from schemas import SportBase
from utils.query_builder import QueryBuilder


class SportRepository:
    def __init__(self, db_pool: get_db_pool):
        """
        Initialize the SportRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("sports")

    async def get_all(self) -> List[dict]:
        """
        Fetch all sports from the database.

        Returns:
            List[dict]: List of dictionary representations of sports.
                        Returns an empty list if there's an error.

        Raises:
            RepositoryError: If there's an error during database access.
            irint(f'{query}+ {regex}')
        """
        try:
            query = self.query_builder.build_query()
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Error: {str(e)}")

    async def create(self, sport: dict) -> dict:
        """
        Create a new sport in the database.

        Args:
            sport (dict): Dictionary representing the sport data.

        Returns:
            dict: Dictionary representing the newly created sport.

        Raises:
            CustomPostgresError: If there's an error during database access.
        """
        try:
            self.query_builder.add_insert_data(sport)
            insert_query = self.query_builder.build_insert_query()
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(insert_query)
                if row:
                    return dict(row)
                else:
                    raise CustomPostgresError("Record not found after insertion")
        except CustomPostgresError as e:
            "error: {e}"

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
        except CustomPostgresError as e:
            if "selections_event_id_fkey" in str(e):
                raise ForeignKeyError("Invalid sport ID provided.") from e
            raise UpdateError(
                f"Error updating sport with ID {sport_id}. Error: {str(e)}"
            )

    async def search_sports_with_regex(self, regex: str) -> List[dict]:
        try:
            # Build the SQL query to search for sports with matching names
            # Using named parameters like $1 in asyncpg ensures safe handling of parameter values, protecting against SQL injection in dynamic queries.
            query = self.query_builder.build_regex_query("name", regex)
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, regex)
                return [dict(row) for row in rows]

        except CustomPostgresError as e:
            raise Exception(f"Error updating event with ID {event_id}. Error: {str(e)}")

    async def get_active_events_count(self, sport_id: int) -> int:
        query = "SELECT COUNT(*) FROM events WHERE sport_id=$1 AND active=TRUE"
        async with self.db_pool.acquire() as connection:
            return await connection.fetchval(query, sport_id)

    async def set_sport_inactive(self, sport_id: int):
        update_query = "UPDATE sports SET active=FALSE WHERE id=$1"
        async with self.db_pool.acquire() as connection:
            await connection.execute(update_query, sport_id)
