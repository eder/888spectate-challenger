from repositories.sport_repository import SportRepository
from utils.prepare_data_for_insert import prepare_data_for_insert


class SportService:
    def __init__(self, sport_repository: SportRepository):
        """
        Initialize the SportService.

        Args:
            sport_repository (SportRepository): An instance of the SportRepository.
        """
        self.sport_repository = sport_repository

    async def get_all(self):
        """
        Fetch all sports.

        Returns:
            List[dict]: List of dictionary representations of sports.
        """
        return await self.sport_repository.get_all()

    async def create(self, sport):
        """
        Create a new sport.

        Args:
            sport: The sport data.

        Returns:
            dict: Dictionary representing the newly created sport.
        """
        sport_data = {"name": sport.name, "slug": sport.slug, "active": sport.active}
        return await self.sport_repository.create(sport_data)

    async def update(self, sport_id: int, sport_data: dict) -> dict:
        """
        Update a sport.

        Args:
            sport_id (int): The ID of the sport to be updated.
            sport_data (dict): Dictionary representing the updated sport data.

        Returns:
            dict: Dictionary representing the updated sport.
        """
        res = prepare_data_for_insert(sport_data)
        return await self.sport_repository.update(sport_id, sport_data)

    async def search_sports(self, criteria: dict) -> dict:
        """
        Performs a sports search based on the provided criteria.

        Args:
            criteria (dict): A dictionary containing search criteria.
                - name_regex (str): An optional regular expression to filter sports by name.

        Returns:
            dict: A dictionary containing the results of the sports search.

        Raises:
            ValueError: If the 'name_regex' parameter is None or an empty string.
        """
        if criteria.name_regex is not None and criteria.name_regex != "":
            return await self.sport_repository.search_sports_with_regex(
                criteria.name_regex
            )
        raise ValueError("The 'name_regex' parameter cannot be None or an empty string")
