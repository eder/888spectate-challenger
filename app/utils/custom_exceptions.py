class CreationError(Exception):
    """Raised when there is an error during the creation process."""
    pass

class ForeignKeyError(Exception):
    """Raised when there's a violation of a foreign key constraint."""
    pass

class UpdateError(Exception):
    """Raised when there is an error during the update process."""
    pass

class ValidationError(Exception):
    """Raised when there is an error if data not valid"""
    pass
