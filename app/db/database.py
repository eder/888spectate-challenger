import os
import asyncpg

class DatabaseError(Exception):
    pass

class AlreadyConnectedError(DatabaseError):
    """Exception raised when a connection attempt is made while already connected."""
    pass

class NotConnectedError(DatabaseError):
    """Exception raised when an operation requires a connection that isn't present."""
    pass

class CustomPostgresError(asyncpg.PostgresError):
    """Custom exception to wrap asyncpg.PostgresError."""
    pass

class DatabaseConnection:
    def __init__(self):
        self._pool: asyncpg.pool.Pool = None
        self._database_url = os.getenv("DATABASE_URL")

    async def connect_to_db(self):
        if self._database_url is None:
            raise DatabaseError("DATABASE_URL is not set.")

        if self._pool is not None:
            raise AlreadyConnectedError("The connection pool is already initialized.")

        try:
            self._pool = await asyncpg.create_pool(self._database_url)
        except Exception as e:
            raise DatabaseError(f"Error connecting to the database: {e}")
   
    async def close_db_connection(self):
        if self._pool is None:
            raise NotConnectedError("The connection pool is not initialized.")

        try:
            await self._pool.close()
            self._pool = None
        except Exception as e:
            raise DatabaseError(f"Error closing the database connection: {e}")

    def get_db_pool(self):
        if self._pool is None:
            raise NotConnectedError("The connection pool is not initialized.")
        return self._pool


_db_instance = DatabaseConnection()

async def connect_to_db():
    await _db_instance.connect_to_db()

async def close_db_connection():
    await _db_instance.close_db_connection()

def get_db_pool():
    return _db_instance.get_db_pool()

