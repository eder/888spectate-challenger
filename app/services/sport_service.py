import logging

from repositories.sport_repository import SportRepository
from repositories.event_repository import EventRepository
from utils.prepare_data_for_insert import prepare_data_for_insert
from utils.slugify import to_slug

class SportService:
    def __init__(
        self,
        sport_repository: SportRepository,
        event_repository: EventRepository,
        logger: logging.Logger
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
                "name": sport['name'],
                "slug": to_slug(sport['name']),
                "active": sport['active']
            }
            return await self.sport_repository.create(sport_data)
        except Exception as e:
            self.logger.error(f"Error creating sport: {e}")
            raise

    async def update(self, sport_id: int, sport: dict) -> dict:
        """
        Update a sport.

        Args:
            sport_id (int): The ID of the sport to be updated.
            sport_data (dict): Dictionary representing the updated sport data.

        Returns:
            dict: Dictionary representing the updated sport.
        """
        try:
            sport['slug'] = to_slug(sport['name']) 
            res = prepare_data_for_insert(sport)
            if sport["active"] == False:
                await self.check_and_update_sport_status(sport_id)

            return await self.sport_repository.update(sport_id, sport)
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

        except Exception as e:
            self.logger.error(
                f"Error checking and updating sport status for sport {sport_id}: {e}"
            )
            raise

    async def filter_sports(self, criteria: dict) -> dict:
        """
        Asynchronously performs a sports search based on the provided criteria. The filter
        can be filtered by sport name using a regular expression and further filtered 
        based on the active status of the sport.

        Args:
            criteria (dict): A dictionary containing search criteria with the following optional keys:
                - name_regex (str): A regular expression to filter sports by name.
                - active (bool): Filter sports based on their active status. 
                - threshold (int, optional): The minimum number of events a sport must have to be included in the results.
                                 Default value is 1.

        Returns:
            dict: A dictionary containing the results of the sports search.

        Raises:
            Exception: Any unexpected issues encountered during the search process are logged and re-raised.

        Note:
            The function builds a dynamic SQL query based on the criteria provided.
        """        
        try:
            query_parts = [
                "WITH ActiveEvents AS (",
                "    SELECT s.id, s.name, COUNT(e.id) as threshold",
                "    FROM sports s",
                "    LEFT JOIN events e ON s.id = e.sport_id AND e.active = TRUE",
                "    WHERE 1=1"
            ]

            params = []

            if "name_regex" in criteria and criteria["name_regex"]:
                query_parts.append("    AND s.name ~ $" + str(len(params) + 1))
                params.append(criteria["name_regex"])

            if "active" in criteria and isinstance(criteria["active"], bool):
                query_parts.append("    AND s.active = $" + str(len(params) + 1))
                params.append(criteria["active"])

            threshold_value = criteria.get("threshold", 1)
            if threshold_value:
                query_parts.append("    GROUP BY s.id, s.name")
                query_parts.append("    HAVING COUNT(e.id) > $" + str(len(params) + 1))
                params.append(threshold_value)
            else:
                query_parts.append("    GROUP BY s.id, s.name")

            if criteria.get("start_time") and criteria.get("end_time"):
                query_parts.extend([
                    "),",
                    "TimeRangeEvents AS (",
                    "    SELECT DISTINCT s.id, s.name",
                    "    FROM sports s",
                    "    JOIN events e ON s.id = e.sport_id",
                    f"    WHERE e.actual_start BETWEEN ${str(len(params) + 1)} AND ${str(len(params) + 2)})",
                ])
                params.extend([criteria["start_time_from"], criteria["start_time_to"]])
                query_parts.extend([
                    "SELECT a.id, a.name, COALESCE(a.threshold, 0) as threshold FROM ActiveEvents a",
                    "UNION",
                    "SELECT t.id, t.name, 0 as threshold FROM TimeRangeEvents t",
                    "WHERE NOT EXISTS (SELECT 1 FROM ActiveEvents a WHERE a.id = t.id)"
                ])
            else:
                query_parts.extend([
                    ")",
                    "SELECT a.id, a.name, COALESCE(a.threshold, 0) as threshold FROM ActiveEvents a"
                ])

            query = " ".join(query_parts)
                        

            return await self.sport_repository.filter_sports(query, params)
            raise ValueError(
                "The 'name_regex' parameter cannot be None or an empty string"
            )
        except Exception as e:
            self.logger.error(f"Error searching for sports: {e}")
            raise
