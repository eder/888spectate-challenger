from dataclasses import dataclass, asdict

from schemas import SearchFilter, SearchModel
from db.database import get_db_pool, CustomPostgresError
from utils.search_sql_query import search_query


class SearchRepository:
    def __init__(self, db_pool: get_db_pool):
        """
        Initialize the SearchRepository.

        Args:
            db_pool (asyncpg.pool.Pool): The database connection pool.
        """
        self.db_pool = db_pool

    async def search_by_criteria(self, criteria: dict) -> list:
        """
        Search for events based on the given criteria.

        Args:
            criteria (SearchFilter): The search criteria.

        Returns:
            list: List of dictionary representations of events that match the criteria.
        """
        print(criteria)
        query = search_query(criteria)
        print(f"{query} OK OK OK OK ")

        # async with self.db_pool.acquire() as connection:
        # rows = await connection.fetch(query, *values)
        # return [dict(row) for row in rows]
