import os
import asyncpg

DATABASE_URL = os.getenv('DATABASE_URL')

pool: asyncpg.pool.Pool = None

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
async def connect_to_db():
    global pool

    if pool is not None:
        raise AlreadyConnectedError("The connection pool is already initialized.")
    
    if DATABASE_URL is None:
        raise DatabaseError("DATABASE_URL is not set.")

    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        raise DatabaseError(f"Error connecting to the database: {e}")

async def close_db_connection():
    global pool
    
    if pool is None:
        raise NotConnectedError("The connection pool is not initialized.")

    try:
        await pool.close()
        pool = None
    except Exception as e:
        raise DatabaseError(f"Error closing the database connection: {e}")

def get_db_pool():
    if pool is None:
        raise NotConnectedError("The connection pool is not initialized.")
    return pool

