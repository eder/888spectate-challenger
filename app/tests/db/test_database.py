
import pytest
import asyncio
from  db.database import (
    DatabaseConnection,
    connect_to_db,
    close_db_connection,
    get_db_pool,
    AlreadyConnectedError,
    NotConnectedError,
    DatabaseError
)

pytestmark = pytest.mark.asyncio


class TestDatabaseConnection:

    @pytest.fixture(autouse=True)
    async def cleanup(self):
        yield
        try:
            await close_db_connection()
        except NotConnectedError:
            pass

    async def test_connect_to_db(self):
        with pytest.raises(NotConnectedError):
            get_db_pool()

        await connect_to_db()

        assert get_db_pool() is not None

    async def test_double_connect_to_db(self):
        with pytest.raises(AlreadyConnectedError, match="The connection pool is already initialized."):
            await connect_to_db()
            await connect_to_db()
       
