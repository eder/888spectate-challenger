import logging
from typing import List

from db.database import get_db_pool
from schemas import SportBase
from utils.query_builder import QueryBuilder

# Adicione a criação do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SportRepository:
    def __init__(self, db_pool: get_db_pool, logger: logging.Logger = logger):
        """
        Initialize the SportRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
            logger (logging.Logger): An instance of the logging logger.
        """
        self.db_pool = db_pool
        self.query_builder = QueryBuilder("sports")
        self.logger = logger  # Adicione o logger aqui

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
        except Exception as e:
            self.logger.error(
                f"Error fetching all sports: {str(e)}"
            )  # Adicione o log aqui
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
                    raise Exception("Record not found after insertion")
        except Exception as e:
            self.logger.error(f"Error creating sport: {str(e)}")
            raise Exception(f"Error creating sport: {str(e)}")

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
        except Exception as e:
            if "selections_event_id_fkey" in str(e):
                raise Exception("Invalid sport ID provided.") from e
            raise Exception(f"Error updating sport with ID {sport_id}. Error: {str(e)}")

    async def search_sports_with_regex(self, criteria) -> List[dict]:
        try:
            query = (
                "SELECT * FROM (SELECT s.id, s.name, s.active, COUNT(e)  threshold FROM sports s "
                "LEFT JOIN events e ON e.sport_id = s.id "
                "WHERE e.active = TRUE OR e IS NULL "
                "GROUP BY s.id) as sports "
                "WHERE 1=1"
            )

            params = []

            # Add criteria conditions
            if "name_regex" in criteria and criteria["name_regex"]:
                query += " AND name ~ $" + str(len(params) + 1)
                params.append(criteria["name_regex"])

            if "active" in criteria and isinstance(criteria["active"], bool):
                query += " AND active = $" + str(len(params) + 1)
                params.append(criteria["active"])

            threshold_value = criteria.get("threshold", 1)
            if threshold_value:
                query += " AND threshold > $" + str(len(params) + 1)
                params.append(threshold_value)

            async with self.db_pool.acquire() as connection:
                rows = await connection.fetch(query, *params)
                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error searching sports: {str(e)}")
            raise Exception(f"Error searching sports: {str(e)}")

    async def set_sport_inactive(self, sport_id: int):
        """
        Set a sport as inactive in the database.

        Args:
            sport_id (int): The ID of the sport to be marked as inactive.
        """
        update_query = "UPDATE sports SET active=FALSE WHERE id=$1"
        async with self.db_pool.acquire() as connection:
            await connection.execute(update_query, sport_id)

    async def filter_sports(self, threshold: int):
        """
        Filter sports based on a threshold value.

        Args:
            threshold (int): The threshold value used for filtering.
        """
        update_query = "UPDATE sports SET active=FALSE WHERE id=$1"
        async with self.db_pool.acquire() as connection:
            await connection.execute(update_query, sport_id)

    async def get_sports_events(self):
        """
        Get sports events from the database.

        Returns:
            List[dict]: List of dictionary representations of sports events.
        """
        select_query = """
        SELECT s.id, s.name
        FROM sports s
        JOIN events e ON s.id = e.sport_id
        WHERE e.active = TRUE
        GROUP BY s.id, s.name
        """

        try:
            async with self.db_pool.acquire() as connection:
                result = await connection.fetch(select_query)
                return result
        except Exception as e:
            self.logger.error(
                f"Error fetching sports events: {str(e)}"
            )  # Adicione o log aqui
            raise Exception(f"An error occurred while fetching the sports: {str(e)}")
