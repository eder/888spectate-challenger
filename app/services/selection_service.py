from repositories.selection_repository import SelectionRepository 

class SelectionService:

    def __init__(self, selection_repository: SelectionRepository):
        self.selection_repository = selection_repository

    async def get_all(self):
        return await self.selection_repository.get_all()

    async def create(self, selection):
        return await self.selection_repository.create(selection)

    async def update(self, selection_id: int, selection_data: dict) -> dict:
        return await self.selection_repository.update(selection_id, selection_data)
