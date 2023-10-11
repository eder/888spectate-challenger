from repositories.selection_repository import SelectionRepository
from repositories.event_repository import EventRepository
from schemas import SelectionBase, SelectionOutcome, SelectionUpdate
from utils.prepare_data_for_insert import prepare_data_for_insert
from logging import Logger


class SelectionService:
    def __init__(
        self,
        selection_repository: SelectionRepository,
        event_repository: EventRepository,
        logger: Logger,
    ):
        """
        Initialize the SelectionService.

        Args:
            selection_repository (SelectionRepository): An instance of the SelectionRepository.
            event_repository (EventRepository): An instance of the EventRepository.
            logger (Logger): An instance of the logging logger.
        """
        self.selection_repository = selection_repository
        self.event_repository = event_repository
        self.logger = logger

    async def get_all(self):
        """
        Fetch all selections.

        Returns:
            List[dict]: List of dictionary representations of selections.
        """
        return await self.selection_repository.get_all()

    async def create(self, selection):
        """
        Create a new selection.

        Args:
            selection: The selection data.

        Returns:
            dict: Dictionary representing the newly created selection.
        """
        try:
            outcome_value = (
                selection["outcome"].value
                if isinstance(selection["outcome"], SelectionOutcome)
                else selection["outcome"]
            )

            selection_data = {
                "name": selection["name"],
                "event_id": selection["event_id"],
                "price": selection["price"],
                "active": selection["active"],
                "outcome": outcome_value,
            }

            self.logger.info("Creating a new selection...")

            return await self.selection_repository.create(selection_data)
        except Exception as e:
            self.logger.error(f"Error creating selection: {e}")
            raise

    async def update(self, selection_id: int, selection_data: dict) -> dict:
        """
        Update a selection.

        Args:
            selection_id (int): The ID of the selection to be updated.
            selection_data (dict): Dictionary representing the updated selection data.

        Returns:
            dict: Dictionary representing the updated selection.
        """
        try:
            selection_data["outcome"] = (
                selection_data["outcome"].value
                if isinstance(selection_data["outcome"], SelectionOutcome)
                else selection_data["outcome"]
            )
            res = prepare_data_for_insert(selection_data)
            await self.selection_repository.update(selection_id, res)

            # TO DO this I would do this validation in a queue to check everyone canceling and send a direct message to update the event data
            if selection_data["active"] == False:
                await self.check_and_update_event_status(selection_id)

            self.logger.info(f"Updated selection with ID {selection_id}")

            return await self.selection_repository.update(selection_id, res)
        except Exception as e:
            self.logger.error(f"Error updating selection {selection_id}: {e}")
            raise

    async def check_and_update_event_status(self, selection_id: int):
        try:
            event_id = await self.selection_repository.get_event_id(selection_id)
            active_selection_count = (
                await self.selection_repository.get_active_selections_count(event_id)
            )

            if active_selection_count == 0:
                await self.event_repository.set_event_as_inactive(event_id)

            self.logger.info(
                f"Checked and updated event status for selection {selection_id}"
            )
        except Exception as e:
            self.logger.error(
                f"Error checking and updating event status for selection {selection_id}: {e}"
            )
            raise

    async def filter_selections(self, criteria: dict) -> dict:
        """
        Performs a selections search based on the provided criteria.

        Args:
            criteria (dict): A dictionary containing search criteria.
                - name_regex (str): An optional regular expression to filter sports by name.

        Returns:
            dict: A dictionary containing the results of the selections search.

        Raises:
            ValueError: If the 'name_regex' parameter is None or an empty string.
        """
        try:
            query_parts = [
                "SELECT * FROM selections WHERE 1=1"
            ]
            params = []
            
            if "name_regex" in criteria and criteria["name_regex"]:
                query_parts.append(" AND name ~ $" + str(len(params) + 1))
                params.append(criteria["name_regex"])
            
            if "active" in criteria and isinstance(criteria["active"], bool):
                query_parts.append(" AND active = $" + str(len(params) + 1))
                params.append(criteria["active"])
            
            query = " ".join(query_parts)

            return await self.selection_repository.filter_selections(query, params)
        except Exception as e:
            self.logger.error(f"Error filter for selections: {e}")
            raise
    
    async def get_selections_by_event_id(self, event_id):
        try:
            return await self.selection_repository.get_selections_by_event_id(event_id)
        except Exception as e:
            self.logger.error(f"Error get selections by event ID: {e}")
            raise
    
    async def get_selections_by_sport_id(self, sport_id):
        try:
            return await self.selection_repository.get_selections_by_sport_id(sport_id)
        except Exception as e:
            self.logger.error(f"Error get selections sport ID: {e}")
            raise
