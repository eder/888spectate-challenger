from repositories.selection_repository import SelectionRepository
from schemas import SelectionBase, SelectionOutcome, SelectionUpdate
from utils.prepare_data_for_insert import prepare_data_for_insert


class SelectionService:
    def __init__(self, selection_repository: SelectionRepository):
        """
        Initialize the SelectionService.

        Args:
            selection_repository (SelectionRepository): An instance of the SelectionRepository.
        """
        self.selection_repository = selection_repository

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
        return await self.selection_repository.create(selection_data)

    async def update(self, selection_id: int, selection_data: dict) -> dict:
        """
        Update a selection.

        Args:
            selection_id (int): The ID of the selection to be updated.
            selection_data (dict): Dictionary representing the updated selection data.

        Returns:
            dict: Dictionary representing the updated selection.
        """
        selection_data["outcome"] = (
            selection_data["outcome"].value
            if isinstance(selection_data["outcome"], SelectionOutcome)
            else selection_data["outcome"]
        )
        res = prepare_data_for_insert(selection_data)
        await self.selection_repository.update(selection_id, res)
        # Todo eu faria essa validação em um fila para vericar todos cancelando e mandar uma mensagem direta para atualizar os dados de evento
        if selection_data["active"] == False:
            await self.selection_repository.check_and_update_event_status()

        return self.selection_repository.update(selection_id, res)

    async def search_selections(self, criteria: dict) -> dict:
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

        if criteria.name_regex is not None and criteria.name_regex != "":
            return await self.selection_repository.search_selections(
                criteria.name_regex
            )
        raise ValueError("The 'name_regex' parameter cannot be None or an empty string")
