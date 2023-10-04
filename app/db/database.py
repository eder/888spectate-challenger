import os
import asyncpg

#DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgresql://sportsbook_user:12345@db:5432/sportsbook_db"

pool: asyncpg.pool.Pool = None

async def connect_to_db():
    global pool 
    pool = await asyncpg.create_pool(DATABASE_URL)

async def close_db_connection():
    await pool.close()

def get_db_pool():
    return pool

