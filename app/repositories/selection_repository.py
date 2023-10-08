from typing import List

from db.database import get_db_pool, CustomPostgresError
from schemas import SelectionOutcome
from utils.query_builder import QueryBuilder


class SelectionRepository:
    def __init__(self, db_pool: get_db_pool):
        """
        Initialize the SelectionRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("selections")

    async def get_all(self) -> list:
        """
        Fetch all selections from the database.

        Returns:
            list: List of dictionary representations of selections.
                  Returns an empty list if there's an error.

        Raises:
            RepositoryError: If there's an error during database access.
        """
        try:
            query = self.query_builder.build_query()
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query)
                return [dict(row) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Error: {str(e)}")

    async def create(self, selection: dict) -> dict:
        """
        Create a new selection in the database.

        Args:
            selection (dict): Dictionary representing the selection data.

        Returns:
            dict: Dictionary representing the newly created selection.

        Raises:
            CustomPostgresError: If there's an error during database access.
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
            "error: {e}"

    async def update(self, selection_id: int, selection: dict) -> dict:
        """
        Update a selection in the database.

        Args:
            selection_id (int): The ID of the selection to be updated.
            selection (dict): Dictionary representing the updated selection data.

        Returns:
            dict: Dictionary representing the updated selection, or None if not found.

        Raises:
            UpdateError: If the selection with the specified ID is not found.
            ForeignKeyError: If an invalid selection ID is provided.
        """
        try:
            self.query_builder.add_condition("id", selection_id)
            self.query_builder.add_update_data(selection)
            update_query = self.query_builder.build_update_query()
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(update_query)
                if row:
                    return dict(row)
                raise UpdateError(f"Selection with ID {selection_id} not found.")
        except CustomPostgresError as e:
            if "selections_event_id_fkey" in str(e):
                raise ForeignKeyError("Invalid Selection ID provided.") from e
            raise UpdateError(
                f"Error updating selection with ID {selection_id}. Error: {str(e)}"
            )


    async def get_active_selections_count(self, event_id: int):
        # Count the number of active selections for the event
        count_query = (
            "SELECT COUNT(*) FROM selections WHERE event_id=$1 AND active=TRUE"
        )
        async with self.db_pool.acquire() as connection:
            return await connection.fetchval(count_query, event_id)
    
    async def get_event_id(self, selection_id: int):
        # Get event_id value
        event_id_query = ("SELECT event_id FROM selections WHERE id = $1")
        async with self.db_pool.acquire() as connection:
            return await connection.fetchval(event_id_query, selection_id)
    



    async def search_selections(self, regex: str) -> List[dict]:
        try:
            # Build the SQL query to search for sports with matching names
            # Using named parameters like $1 in asyncpg ensures safe handling of parameter values, protecting against SQL injection in dynamic queries.
            query = self.query_builder.build_regex_query("name", regex)
            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, regex)
                return [dict(row) for row in rows]

        except CustomPostgresError as e:
            raise Exception(f"Error updating event with ID {event_id}. Error: {str(e)}")
