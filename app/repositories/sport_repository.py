from typing import List

from db.database import get_db_pool 
from schemas import SportBase

class SportRepository:

    def __init__(self, db_pool: get_db_pool):
        self.db_pool = db_pool

    async def get_all(self) -> List[dict]:
        async with self.db_pool.acquire() as connection:
            rows = await connection.fetch("SELECT * FROM sports")
            return [dict(row) for row in rows]

    async def create(self, sport: SportBase) -> dict:
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                "INSERT INTO sports(name, slug, active, type) VALUES($1, $2, $3, $4) RETURNING *",
                sport.name, sport.slug, sport.active, sport.type.value
            )
            return dict(row)
    
    async def update(self, sport_id: int, sport_data: dict) -> dict:
        set_clause = ", ".join(f"{key}=${i+1}" for i, key in enumerate(sport_data.keys()))
        query = f"""
        UPDATE sports
        SET {set_clause}
        WHERE id=${len(sport_data) + 1}
        RETURNING *;
        """
        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(query, *sport_data.values(), sport_id)
                if row:
                    return dict(row)
                return None
        except asyncpg.exceptions.PostgresError as e:
            raise Exception(f"Error updating sport with ID {sport_id}. Error: {str(e)}")
        
