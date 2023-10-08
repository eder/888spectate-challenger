from datetime import datetime
from schemas import SearchFilter
from repositories.search_repository import SearchRepository


class SearchService:
    """
    Service class for managing searches.
    """

    def __init__(self, search_repository: SearchRepository):
        """
        Initialize the SearchService.

        Args:
            search_repository (SearchRepository): The repository for event data.
        """
        self.search_repository = search_repository

    async def search(self, criteria: dict) -> dict:
        """
        Search  based on specified criteria.

        Args:
        criteria (SearchFilter): The search criteria.

        Returns:
        list: A list  that match the search criteria.
        """
        # if criteria.min_active_selections:
        # return await self.search_repository.search_events_by_criteria(
        # criteria.min_active_selections
        # )
        # return await self.search_repository.search_by_criteria(criteria)
