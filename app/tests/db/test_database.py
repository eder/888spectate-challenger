import unittest
from unittest.mock import patch
import asyncpg

from db.database import connect_to_db, close_db_connection, get_db_pool, DatabaseError


class DatabaseTests(unittest.TestCase):
    @patch.object(asyncpg, "create_pool")
    async def test_connect_to_db(self, mock_create_pool):
        await connect_to_db()
        mock_create_pool.assert_called_once()

        with self.assertRaises(AlreadyConnectedError):
            await connect_to_db()

        with self.assertRaises(DatabaseError):
            os.environ.pop("DATABASE_URL")
            await connect_to_db()

    @patch.object(asyncpg, "close_pool")
    async def test_close_db_connection(self, mock_close_pool):
        await close_db_connection()
        mock_close_pool.assert_called_once()

        with self.assertRaises(NotConnectedError):
            await close_db_connection()

    async def test_get_db_pool(self):
        with patch.object(asyncpg, "create_pool") as mock_create_pool:
            await connect_to_db()
            pool = get_db_pool()

        with self.assertRaises(NotConnectedError):
            get_db_pool()


if __name__ == "__main__":
    unittest.main()
