from repositories.sport_repository import SportRepository
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert
from logging import Logger


class SportService:
    def __init__(
        self,
        sport_repository: SportRepository,
        event_repository: EventRepository,
        logger: Logger,
    ):
        """
        Initialize the SportService.

        Args:
            sport_repository (SportRepository): An instance of the SportRepository.
            event_repository (EventRepository): An instance of the EventRepository.
            logger (Logger): An instance of the logging logger.
        """
        self.sport_repository = sport_repository
        self.event_repository = event_repository
        self.logger = logger

    async def get_all(self):
        """
        Fetch all sports.

        Returns:
            List[dict]: List of dictionary representations of sports.
        """
        try:
            self.logger.info("Fetching all sports...")
            return await self.sport_repository.get_all()
        except Exception as e:
            self.logger.error(f"Error fetching sports: {e}")
            raise

    async def create(self, sport):
        """
        Create a new sport.

        Args:
            sport: The sport data.

        Returns:
            dict: Dictionary representing the newly created sport.
        """
        try:
            sport_data = {
                "name": sport.name,
                "slug": sport.slug,
                "active": sport.active,
            }
            self.logger.info("Creating a new sport...")
            return await self.sport_repository.create(sport_data)
        except Exception as e:
            self.logger.error(f"Error creating sport: {e}")
            raise

    async def update(self, sport_id: int, sport_data: dict) -> dict:
        """
        Update a sport.

        Args:
            sport_id (int): The ID of the sport to be updated.
            sport_data (dict): Dictionary representing the updated sport data.

        Returns:
            dict: Dictionary representing the updated sport.
        """
        try:
            res = prepare_data_for_insert(sport_data)
            if sport_data["active"] == False:
                await self.check_and_update_sport_status(sport_id)

            self.logger.info(f"Updating sport with ID {sport_id}")
            return await self.sport_repository.update(sport_id, sport_data)
        except Exception as e:
            self.logger.error(f"Error updating sport {sport_id}: {e}")
            raise

    async def check_and_update_sport_status(self, sport_id: int):
        try:
            active_event_count = await self.event_repository.get_active_events_count(
                sport_id
            )
            if active_event_count == 0:
                await self.sport_repository.set_sport_inactive(sport_id)

            self.logger.info(f"Checked and updated sport status for sport {sport_id}")
        except Exception as e:
            self.logger.error(
                f"Error checking and updating sport status for sport {sport_id}: {e}"
            )
            raise

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
        try:
            # if criteria.name_regex is not None and criteria.name_regex != "":
            return await self.sport_repository.search_sports_with_regex(criteria)
            raise ValueError(
                "The 'name_regex' parameter cannot be None or an empty string"
            )
        except Exception as e:
            self.logger.error(f"Error searching for sports: {e}")
            raise

    async def get_sports_events(self) -> dict:
        try:
            self.logger.info("Fetching sports' events...")
            return await self.sport_repository.get_sports_events()
        except Exception as e:
            self.logger.error(f"Error fetching sports' events: {e}")
            raise
