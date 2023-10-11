import pytest
from repositories.errors import RepositoryError


def test_repository_error_message():
    error_message = "Test error message"
    with pytest.raises(RepositoryError, match=error_message) as exc_info:
        raise RepositoryError(error_message)

    assert str(exc_info.value) == error_message
