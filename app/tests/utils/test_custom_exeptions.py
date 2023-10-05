import pytest
from utils.custom_exceptions import CreationError, ForeignKeyError, UpdateError, ValidationError

def test_creation_error():
    with pytest.raises(CreationError, match="Error during creation"):
        raise CreationError("Error during creation")

def test_foreign_key_error():
    with pytest.raises(ForeignKeyError, match="Foreign key violation"):
        raise ForeignKeyError("Foreign key violation")

def test_update_error():
    with pytest.raises(UpdateError, match="Error during update"):
        raise UpdateError("Error during update")

def function_that_raises_error(data):
    if not data:
        raise ValidationError("Data is not valid.")

def test_validation_error_exception():
    with pytest.raises(ValidationError, match="Data is not valid."):
        function_that_raises_error(None)
