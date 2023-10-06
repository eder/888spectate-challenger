from db.database import get_db_pool 
from schemas import SelectionOutcome

class SelectionRepository:

    def __init__(self, db_pool:get_db_pool):
        self.db_pool = db_pool

    async def get_all(self) -> list:
            try:
                async with self.db_pool.acquire() as connection:
                    rows = await connection.fetch("SELECT * FROM selections")
                    return [dict(row) for row in rows]
            except Exception as e:
                raise RepositoryError(f"Erro ao buscar seleções: {str(e)}")



    async def create(self, selection: dict) -> dict:
        outcome_value = selection["outcome"].value if isinstance(selection["outcome"], SelectionOutcome) else selection["outcome"]
        
        async with self.db_pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                INSERT INTO selections(name, event_id, price, active, outcome) 
                VALUES($1, $2, $3, $4, $5) 
                RETURNING *
                """,
                selection["name"], selection["event_id"], selection["price"], selection["active"], outcome_value
            )
            return dict(row)
    
    
    async def update(self, selection_id: int, selection_data: dict) -> dict:
        selection_data["outcome"] = selection_data["outcome"].value if isinstance(selection_data["outcome"], SelectionOutcome) else selection_data["outcome"]
        set_clause = ", ".join(f"{key}=${i+1}" for i, key in enumerate(selection_data.keys()))
        values = list(selection_data.values()) + [selection_id]

        query = f"""
        UPDATE selections
        SET {set_clause}
        WHERE id=${len(values)}
        RETURNING *;
        """
        try:
            async with self.db_pool.acquire() as connection:
                row = await connection.fetchrow(query, *values)
                if row:
                    return dict(row)
                raise UpdateError(f"Selection with ID {selection_id} not found.")

        except asyncpg.ForeignKeyViolationError as e:
            if "selections_event_id_fkey" in str(e):
                raise ForeignKeyError("Invalid event ID provided.") from e
            raise UpdateError(f"Error updating selection with ID {selection_id}. Error: {str(e)}")

            
